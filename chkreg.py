#!/usr/bin/python2.7

import argparse
from cdt_checksumsq.checksums_interface import ChecksumsQueueClient
from cdt_checksumsq.checksums_interface import FileLocation
import os
import json

client = ChecksumsQueueClient()
parser = argparse.ArgumentParser(description='Checksums queue commandline client')

parser.add_argument('--ping', help='Send ping message', default=False, action='store_true')
parser.add_argument('--register', help='Send file registration request', metavar='PATH', default=None)
parser.add_argument('--citype', help='CIType code', default=None)
parser.add_argument('--loctype', help='Location type, default: NXS', default='NXS')
parser.add_argument('--revision', help='SVN revision', default=None)
parser.add_argument('--depth', type=int, help='File registration depth, default: 0', default=0)

#A.Knyazev, SII-10060: these two parameters added for possibility to register in Mongo correctly with 
# deploying deny/allow mechanism
parser.add_argument('--parent', help='Parent list: JSON-parsable string', default=None)
parser.add_argument('--artifact-deliverable', help="Delivery enabled", default=None)
parser.add_argument('--version', help='Version', default=None)
parser.add_argument('--client', help="CDT client code", default=None)

client.basic_args(parser)     # add AMQP-specific arguments
args = parser.parse_args()    # parse command-line options

_parent = args.parent

if _parent:
    _parent = json.loads(_parent)

    if not isinstance(_parent, list):
        _parent = [_parent]

if args.queue is None: 
    args.queue = 'cdt.checksums.input'

client.setup_from_args(args)    # setup AMQP-specific parameters
client.connect()                # connect to server

location = FileLocation(args.register, args.loctype, args.revision)

if args.declare == 'only': 
    exit(0)

if args.ping:
    client.ping()

_deliverable = args.artifact_deliverable

if _deliverable is not None:
    if _deliverable.lower() not in ['yes', 'true', 'no', 'false']:
        raise ValueError("--artifact-deliverable value not supported: '%s'" % _deliverable)

    _deliverable =(_deliverable.lower() in ['yes', 'true'])

if args.register:
    client.register_file(
            location=location,
            citype=args.citype,
            depth=args.depth,
            version=args.version,
            client=args.client,
            parent=_parent,
            artifact_deliverable=_deliverable)

