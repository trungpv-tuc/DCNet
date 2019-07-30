from mininet.topo import Topo
from mininet.node import OVSSwitch
from MaxiNet.Frontend.container import Docker
from MaxiNet.Frontend import maxinet
from MaxiNet.tools import Tools
topo = Topo()
topo.addHost("h1", cls=Docker, ip="10.0.0.251", dimage="ubuntu:trusty")
topo.addHost("h2", cls=Docker, ip="10.0.0.252", dimage="ubuntu:trusty")
topo.addSwitch("s5", dpid=Tools.makeDPID(5))  ## set datapath id
topo.addLink("h1", "s5")
topo.addLink("h2", "s5")

cluster = maxinet.Cluster(minWorkers=1, maxWorkers=2)

# start experiment with OVSSwitch on cluster
exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch)
exp.setup()
exp.get_node("h1").cmd("ping -c 1 10.0.0.252")
exp.get_node("h2").cmd("ping -c 1 10.0.0.251")

