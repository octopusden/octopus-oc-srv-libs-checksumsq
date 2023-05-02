from collections import namedtuple
from oc_cdt_queue2.queue_rpc import QueueRPC
from oc_cdt_queue2.queue_application import QueueApplication
from os import getenv

FileLocation=namedtuple("FileLocation", ["path", "loctype_code", "revision"])

queue_published = ['ping', 'register_file', 'register_checksum']
queue_name = 'cdt.dlartifacts.input'
queue_cnt_name = 'cdt.dlcontents.input'

class ChecksumsQueueClient(QueueRPC):
    default_queue_name = queue_name
    published = queue_published

    def __init__(self, *args, **argv):
        super(ChecksumsQueueClient, self).__init__(*args, **argv)
        self.queue_cnt = None

    def basic_args(self, parser = None):
        parser = super(ChecksumsQueueClient, self).basic_args(parser)
        parser.add_argument('--queue-cnt', help = 'cdtcontents queue name', default = getenv('AMQP_CNT_QUEUE', queue_cnt_name))
        # Overriding default exchange value for message duplication support
        parser.set_defaults(exchange='cdt.dlartifacts.input')
        return parser

    def setup_from_args(self, args = None):
        args = super(ChecksumsQueueClient, self).setup_from_args(args)  # this sets up all parent classes
        self.setup(queue_cnt = args.queue_cnt) # this relates to current class
        return args

    def setup(self, *args, **argv):
        self.queue_cnt = argv.pop('queue_cnt', None)
        if len(args) > 0 or len(argv) > 0: super(ChecksumsQueueClient, self).setup(*args, **argv)

    def send(self, *args, **argv):
        usual = super(ChecksumsQueueClient, self).send(*args, **argv)

        usual_routing_key = self.routing_key         # TODO: THIS IS UGLY AND NOT THREAD-SAFE
        self.routing_key = self.queue_cnt
        super(ChecksumsQueueClient, self).send(*args, **argv)
        self.routing_key = usual_routing_key

        return usual


# 'artifact_deliverable' default value has been changed to 'None' 
#   otherwise we may occasionly enable forbidden distributive

class ChecksumsQueueServer(QueueApplication):
    default_queue_name = queue_name
    published = queue_published

    def register_file(self, location, citype, depth=0, remove=False, version=None, client=None, parent=None, artifact_deliverable=None):
        pass

    def register_checksum(self, location, checksum, citype=None, cs_prov='Regular', mime='Data', cs_alg='MD5', version=None, client=None, parent=None, artifact_deliverable=None):
        pass

    def ping(self):
        pass


