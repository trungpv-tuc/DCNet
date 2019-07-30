import requests


def switchPost():
	response = requests.post('http://127.0.0.1:5000/api/v1/switch', data={"switch_name":"s6","worker_id":"1"})
	print response

def hostPost():
	response = requests.post('http://127.0.0.1:5000/api/v1/host', data={"host_name":"h3","ip":"10.0.0.253","docker_image":"ubuntu:trusty","adjacent_switch":"s5"})
	print response
	remoteCommand()

def linkPost():
	response = requests.post('http://127.0.0.1:5000/api/v1/link', data={"node1":"s6", "node2":"s5"})
	print response

def remoteCommand():
	response = requests.post('http://127.0.0.1:5000/api/v1/remoteCommand', data={"sender_node":"h3", "target_command": "ping -c 1 10.0.0.251"})
	print response
#switchPost()
linkPost()
#hostPost()

