#!/usr/bin/env python3

"""httpfuncs: HTTP interface for pure functions.

This file uses python3 and its stdanard library to provide http interface
to number of pure functinos. One can issue GET request to
/<function name>/<arg1>/<argN> to get result of application of desired
function to provided arguments.

Currently provided function:
 /fib/N -> generate N first numbers of fibbonachi sequence (starting from zero)

Usage:
 ./httpfuncs.py 127.0.0.1 8080
 or, to run tests:
 ./httpfuncs.py --test
 or, to display help:
 ./httpfuncs.py --help
"""

import sys
import unittest

from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler

def fib(n):
    if n < 0:
        raise ValueError('Fibbonachi sequence is not defined for negative input')
    if n == 0:
        # not an error, but do not return anything
        return
    a, b = 0, 1
    # seed value
    # there is no pre-condition loop in python, so do it manually
    yield a
    for _ in range(n - 1):
        a, b = b, a + b
        yield a

def fib_handler(n):
    """Converts input to integer and output to space-separated string"""
    return ' '.join(map(str, fib(int(n))))

ROUTES = {
    'fib': fib_handler
}

class FuncHandler(BaseHTTPRequestHandler):
    def process_result(self, result):
        # without \n at the end of the body,
        # curl will not display the body
        body = result.encode('utf-8') + b"\n"
        self.send_header('Content-Type', 'application/text')
        self.send_header('Content-Length', int(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        (_, func, *args) = self.path.split('/', 3)
        try:
            self.process_result(ROUTES[func](*args))
        except KeyError:
            self.send_error(404,
                            explain='Function not found: {}'.format(func))
        except TypeError as exc:
            # missing parameters, etc
            self.send_error(422, 'Invalid number of arguments', str(exc))
            raise
        except ValueError as exc:
            # invalid input, etc
            self.send_error(422, 'Invalid input for function', str(exc))
        except Exception as exc:
            # any other unexpected errors
            self.send_error(500)


class TestFib(unittest.TestCase):
    """Tests core function"""
    def test_seed_values(self):
        specs = {
            0: [],
            1: [0]
        }
        for (spec, answer) in specs.items():
            self.assertEqual(list(fib(spec)), answer)
    def test_normal_values(self):
        specs = {
            2: [0, 1],
            5: [0, 1, 1, 2, 3]
        }
        for (spec, answer) in specs.items():
            self.assertEqual(list(fib(spec)), answer)
    def test_invalid_input(self):
        specs = {
            -1: ValueError,
            'smth': TypeError,
            2.5: TypeError
        }
        for (spec, exc) in specs.items():
            with self.assertRaises(exc):
                # force generator consumption
                list(fib(spec))

class TestFibHandler(unittest.TestCase):
    def test_seed_values(self):
        specs = {
            '0': '',
            1: '0'
        }
        for (spec, answer) in specs.items():
            self.assertEqual(fib_handler(spec), answer)
    def test_normal_values(self):
        specs = {
            '2': '0 1',
            '5': '0 1 1 2 3'
        }
        for (spec, answer) in specs.items():
            self.assertEqual(fib_handler(spec), answer)
    def test_invalid_input(self):
        specs = {
            '-1': ValueError,
            'smth': ValueError,
            '2.5': ValueError
        }
        for (spec, exc) in specs.items():
            with self.assertRaises(exc):
                fib_handler(spec)


def main(host, port):
    FuncHandler.protocol_version = "HTTP/1.0"
    # disable html errors
    FuncHandler.error_message_format = '%(code)s %(message)s\n%(explain)s\n'
    http_server = HTTPServer((host, port), FuncHandler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting")
        http_server.server_close()
        sys.exit(0)

def usage_and_exit(msg=None, error=True):
    out = sys.stderr if error else sys.stdout
    if msg:
        print(msg, file=out)
        print(file=out)
    print(__doc__, file=out)
    sys.exit(int(error))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            usage_and_exit(error=False)
        elif sys.argv[1] == '--test':
            unittest.main(argv=sys.argv[:1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        usage_and_exit('Incorrect number of arguments provided!')
