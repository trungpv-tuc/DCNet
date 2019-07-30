import time
from mininet.topo import Topo
from mininet.node import OVSSwitch
from MaxiNet.Frontend.container import Docker
from MaxiNet.Frontend import maxinet
from MaxiNet.tools import Tools
import threading
from flask import Flask
from  Topology import exp
app = Flask(__name__)
sendState = 0
@app.route('/')
def hello_world():
    topo = Topo()
    topo.addHost("h1", cls=Docker, ip="10.0.0.251", dimage="ubuntu:trusty")
    topo.addHost("h2", cls=Docker, ip="10.0.0.252", dimage="ubuntu:trusty")
    topo.addSwitch("s1", dpid=Tools.makeDPID(1))
    topo.addLink("h1", "s1")
    topo.addLink("h2", "s1")

    # start cluster
    cluster = maxinet.Cluster(minWorkers=1, maxWorkers=2)

    # start experiment with OVSSwitch on cluster
    exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch)
    exp.setup()
    return 'Welcome to our Library!'

class TopologyCreator(threading.Thread):
    global sendState,exp
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

        print "waiting 5 seconds for routing algorithms on the controller to converge"
        time.sleep(5)

        print "pinging h2 from h1 to check network connectivity..."
        print exp.get_node("h1").cmd("ping -c 5 10.0.0.252")

    def run(self):
        global sendState,exp

        while True:
            choice = int(sendState)
            if choice == 1:
                exp.addSwitch("s2")
                print "adding hosts h3  on ..."
                # Enforce placement of h3 on worker of s2.
                # Remember: we cannot have tunnels between hosts and switches
                exp.addHost("h3", cls=Docker, ip="10.0.0.200", dimage="ubuntu:trusty", pos="s2")
                # autoconf parameter configures link-attachment etc for us
                exp.addLink("s1", "s2", autoconf=True)
                exp.addLink("h3", "s2", autoconf=True)

                time.sleep(2)

                print "pinging h4 and h1 from h3 to check connectivity of new host..."
                # show network connectivity of new hosts

                print exp.get("h3").cmd("ping -c5 10.0.0.251")
                choice = 0
                sendState = 0
                print 'newvalue of choice', choice,sendState
                time.sleep(1.0)

            elif choice == 2:
                print "adding hosts h4  on ..."
                exp.addHost("h4", cls=Docker, ip="10.0.0.201", dimage="ubuntu:trusty", pos="s2")
                exp.addLink("h4", "s2", autoconf=True)
                time.sleep(2)
                print exp.get("h3").cmd("ping -c5 10.0.0.201")
                choice = 0
                sendState = 0
                print 'newvalue of choice', choice, sendState
                time.sleep(1.0)
            else:
                 print "Choose something different"
                 choice = 0
                 sendState = 0
                 print 'newvalue of choice', choice, sendState
                 time.sleep(1.0)
            time.sleep(2.0)
        time.sleep(2.0)
    time.sleep(2.0)


class UserInput(threading.Thread):
    global sendState

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global sendState
        while True:
             choice = input("Please Type 1 if you want to add another switch and host and 2 if you want to add additional host")
             choice = int(choice)
             if choice > 0 :
                 sendState = choice
                 print 'updated', sendState
                 choice = 0
             time.sleep(2.0)
        time.sleep(3.0)


#Topo = TopologyCreator("StatsCollector")
#user = UserInput("Q-Learning")

#Topo.start()
#user.start()
