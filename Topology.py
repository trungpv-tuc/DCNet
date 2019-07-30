from MaxiNet.Frontend.container import Docker
from MaxiNet.tools import Tools
from flask import Flask
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from topo import exp  # base topology is imported
app = Flask(__name__)
api = Api(app, prefix="/api/v1")
sendState = 0


switch = ["s1"]
Topology_request_parser = RequestParser(bundle_errors=True)
Topology_request_parser.add_argument("switch_name", type=str, required=False, help="Name has to be valid string")
Topology_request_parser.add_argument("worker_id", type=int, required=False, help="Please enter valid integer as ID")
###
host = ["h1", "h2"]

Topology_request_parser.add_argument("host_name", type=str, required=False, help="Name has to be valid string")
Topology_request_parser.add_argument("class", type=str, required=False, help="Name has to be valid string")
Topology_request_parser.add_argument("ip", type=str, required=False, help="Name has to be valid string")
Topology_request_parser.add_argument("docker_image", type=str, required=False, help="Name has to be valid string")
Topology_request_parser.add_argument("adjacent_switch", type=str, required=False, help="Name has to be valid string")
##
Topology_request_parser.add_argument("node1", type=str, required=False, help="Name has to be valid string")
Topology_request_parser.add_argument("node2", type=str, required=False, help="Name has to be valid string")
Topology_request_parser.add_argument("sender_node", type=str, required=False, help="Name has to be valid string")
Topology_request_parser.add_argument("target_command", type=str, required=False, help="Name has to be valid string")
@app.route('/')
def hello_world():
    return 'Welcome to our Library!'



class Switch(Resource):
    def get(self):
        return switch

    def post(self):
        args = Topology_request_parser.parse_args()
        switch.append(args)
        print args["switch_name"]
        exp.addSwitch(args["switch_name"],dpid =Tools.makeDPID(args["worker_id"]))
        return {"msg": "Switch added", "switch_data": args}

class Host(Resource):
    def get(self):
        return host

    def post(self):
        args = Topology_request_parser.parse_args()
        host.append(args)
        print args["host_name"],args["class"]
        exp.addHost(args["host_name"], cls=Docker, ip=args["ip"], dimage=args["docker_image"], pos=args["adjacent_switch"])
        exp.addLink(args["host_name"], args["adjacent_switch"], autoconf=True)
        return {"msg": "Host added", "host_data": args}

class Link(Resource):
    def get(self):
        return 'does not matter now'

    def post(self):
        args = Topology_request_parser.parse_args()

        print args["node1"],args["node2"]
        exp.addLink(args["node1"], args["node2"], port1=3 , port2=20)
        return {"msg": "Link added", "link_data": args}
class remoteCommand(Resource):
    def get(self):
        return 'does not matter now'
    def post(self):
        args = Topology_request_parser.parse_args()
        exp.get_node(args["sender_node"]).cmd(args["target_command"])


api.add_resource(Switch, '/switch')
api.add_resource(Host, '/host')
api.add_resource(Link, '/link')
api.add_resource(remoteCommand, '/remoteCommand')