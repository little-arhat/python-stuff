#!/usr/bin/env python
# -*- coding:utf-8 -*-

# This is simple web crawler. It dumps results onto json file.
# Crawler uses common producer/consumer pattern, where producers crawl
# pages and add links to shared queue, and consumer coordinates crawling.
# It does not respect robots.txt so use with caution.
# CSS, Images, JS files, font files and links to some files count as assets,
# iframes are ignored.
# Crawler tries to find resources inside CSS styles as well.
# Crawler does not retry failed requests.
# Onli assets from the same domain are dumpet to report.

# Requirements.txt:
# BeautifulSoup==3.2.1
# eventlet==0.9.16
# eventlet-log==0.0.3
# greenlet==0.3.4
# wsgiref==0.1.2

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import re
import sys
import json
import urlparse

from itertools import ifilter

import eventlet
import eventlet.timeout
from eventlet.green import urllib2, socket, httplib

from eventlet_log import create_logger

from BeautifulSoup import BeautifulSoup

POOL_SIZE = 256
TIMEOUT = 20

(log, log_exc, _) = create_logger('crawler')

def drain_queue(queue):
    try:
        while True:
            yield queue.get_nowait()
    except eventlet.queue.Empty:
        raise StopIteration

def find_css_uris(css):
    '''Catches url, such as background-url or font-url inside
       CSS stylesheets.
    '''
    return re.findall("url\('(.*?)'\)", css)

def normalize_uri(uri, default_scheme='https'):
    '''Tries to normalize uris, so //example.com becomes https://example.com,
       www.example.com -- https://example.com and so on.
    '''
    parsed = urlparse.urlsplit(uri)
    if parsed.netloc:
        netloc = parsed.netloc
        path = parsed.path
    else:
        (netloc, sep, path) = parsed.path.partition('/')
        if not netloc:
            raise ValueError('Cannot normalize relative uri {}'.format(uri))
        path = sep + path
    return urlparse.urlunsplit((parsed.scheme or default_scheme,
                                netloc,
                                path,
                                parsed.query,
                                ''))

def build_uri(uri, base_uri):
    return urlparse.urljoin(base_uri, uri)

def make_uri_checker(netloc):
    '''Creates checker function that limits uri to specified netloc
       and also ignores #anchors.
    '''
    def checker(uri):
        # ignore empty uri and anchors
        if not uri or uri.startswith('#'):
            return False
        else:
            uri = normalize_uri(uri)
            parsed_uri = urlparse.urlsplit(uri)
            return parsed_uri.netloc == netloc
    return checker

def head_uri(uri, timeout=TIMEOUT):
    try:
        req = urllib2.Request(uri)
        req.get_method = lambda : 'HEAD'
        with eventlet.timeout.Timeout(timeout):
            response = urllib2.urlopen(req)
            return response.headers
    except eventlet.timeout.Timeout as exc:
        log('Timeout while requesting `{}`: {}'.format(uri, exc))
    except (socket.error, urllib2.URLError, httplib.HTTPException) as exc:
        return None

def request(uri, timeout=TIMEOUT):
    try:
        with eventlet.timeout.Timeout(timeout):
            return urllib2.urlopen(uri).read()
    except eventlet.timeout.Timeout as exc:
        log('Timeout while requesting `{}`: {}'.format(uri, exc))
    except (socket.error, urllib2.URLError, httplib.HTTPException):
        log_exc('Error, while requesting {}'.format(uri))
        return None

def get_uri_from_element(elem, base_uri, prop):
    return build_uri(elem.get(prop), base_uri)

def extract_uris(elements, type_, base_uri, prop='src'):
    for elem in elements:
        elem_uri = get_uri_from_element(elem, base_uri, prop)
        log('{} has - {}: {}'.format(base_uri, type_, elem_uri))
        yield elem_uri


def crawl_uri(uri, check_uri, css_cache, visited, worklist, result):
    log('Crawling {}'.format(uri))
    body = request(uri)
    if not body:
        return set(), set()
    bs = BeautifulSoup(body)
    # find all assets on this page (even external)
    assets = set()
    # js:
    assets.update(ifilter(check_uri, extract_uris(bs.findAll('script', src=True),
                                                  'JS', uri)))
    # imgs:
    assets.update(ifilter(check_uri, extract_uris(bs.findAll('img', src=True),
                                                  'IMAGE', uri)))
    # css are a bit harder: there could be links to fonts/imgs inside
    # but we will ignore fonts/imgs represented in base64
    css_elems = bs.findAll('link', href=True, rel="stylesheet")
    for css_uri in ifilter(check_uri, extract_uris(css_elems, 'CSS',
                                                   uri, 'href')):
        assets.add(css_uri)
        if css_uri in css_cache:
            full_css_resource_uris = css_cache[css_uri]
        else:
            css_body = request(css_uri)
            if not css_body:
                continue
            css_resource_uris = find_css_uris(css_body)
            full_css_resource_uris = map(lambda u:build_uri(u, uri),
                                         css_resource_uris)
            css_cache[css_uri] = full_css_resource_uris
        for full_css_resource_uri in full_css_resource_uris:
            log('{} has - CSS_RESOURCE {}'.format(uri, full_css_resource_uri))
            assets.add(full_css_resource_uri)
    links_to = set()
    for link in bs.findAll('a', href=True):
        href = link.get('href')
        link_uri = normalize_uri(build_uri(href, uri))
        if not check_uri(link_uri):
            continue
        if link_uri in links_to:
            continue
        headers = head_uri(link_uri)
        if not headers:
            continue
        log('{} has - LINK TO {}'.format(uri, link_uri))
        # do not add pages to some files to worklist
        if headers['Content-Type'].startswith('text/html'):
            links_to.add(link_uri)
            if link_uri not in visited:
                worklist.put(link_uri)
    result.put((uri, assets, links_to))

def main(uri, default_scheme='https'):
    uri = normalize_uri(uri, default_scheme)
    parsed_uri = urlparse.urlsplit(uri)
    netloc = parsed_uri.netloc
    check_uri = make_uri_checker(netloc)

    visited = set()
    css_cache = {}

    worklist = eventlet.Queue()
    result = eventlet.Queue()
    pool = eventlet.GreenPool(POOL_SIZE)
    worklist.put(uri)
    while True:
        log('Queue has {} items to crawl'.format(worklist.qsize()))
        while not worklist.empty():
            to_work = worklist.get()
            if to_work in visited:
                continue
            visited.add(to_work)
            pool.spawn_n(crawl_uri, to_work, check_uri,
                         css_cache, visited, worklist, result)
        pool.waitall()
        log('We have {} results in total'.format(result.qsize()))
        if worklist.empty():
            break
    res = {}
    for (uri, assets, new_uris) in drain_queue(result):
        res[uri] = {
            'assets': list(assets),
            'links_to': list(new_uris)
        }
    return res


if __name__ == '__main__':
    if len(sys.argv) < 3:
        log('Usage {} uri report.json'.format(sys.argv[0]))
        sys.exit(1)
    else:
        report = main(sys.argv[1])
        try:
            with open(sys.argv[2], 'w') as f:
                json.dump(report, f, indent=4)
        except Exception:
            log_exc('Error while writing report to {}'.format(sys.argv[2]))
            sys.exit(1)
