#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# pylint: disable=superfluous-parens
#
# Created by: Pavlos Parissis <pavlos.parissis@gmail.com>
#
"""Dump a collection of information about frontends, backends and servers

Usage:
    haproxytool dump [-fbsh -D DIR ]

Options:
    -h, --help                show this screen
    -f, --frontends           show frontends
    -b, --backends            show backends
    -s, --servers             show servers
    -D DIR, --socket-dir=DIR  directory with HAProxy socket files
    [default: /var/lib/haproxy]

"""
from docopt import docopt
from haproxyadmin import haproxy


def get_backends(hap):
    print("# backend name, status, requests, servers")
    for backend in hap.backends():
        servers = ','.join([x.name for x in backend.servers()])
        print("{},{},{},{}".format(backend.name, backend.status,
                                   backend.requests, servers))


def get_frontends(hap):
    print("# frontend name, status, requests, process_nb")
    for frontend in hap.frontends():
        print("{},{},{},{}".format(frontend.name, frontend.status,
                                   frontend.requests, frontend.process_nb))


def get_servers(hap):
    print("# server name, status, requests, backend")
    for server in hap.servers():
        print("{},{},{},{}".format(server.name, server.status, server.requests,
                                   server.backendname))


def dump(hap):
    get_frontends(hap)
    get_backends(hap)
    get_servers(hap)


def main():
    arguments = docopt(__doc__)
    hap = haproxy.HAProxy(socket_dir=arguments['--socket-dir'])

    if (not arguments['--frontends'] and not arguments['--pools'] and not
            arguments['--servers']):
        dump(hap)

    if arguments['--frontends']:
        get_frontends(hap)

    if arguments['--backends']:
        get_backends(hap)

    if arguments['--servers']:
        get_servers(hap)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
