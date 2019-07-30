import requests
from requests.auth import HTTPBasicAuth
import json
import threading
#---------------------------------------------------------------------#
class DevicesDelete(threading.Thread):
    global sendState, Switches_Status,  Switches_StatsData
    deviceids = []
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name


        self.postheader= {'Accept':'application/json'}
        deviceresponse=  requests.get('http://127.0.0.1:8181/onos/v1/devices', auth=HTTPBasicAuth('onos', 'rocks')).json()
        for x in deviceresponse:
            for p in deviceresponse[x]:
                self.deviceids.append(str(p['id']))

        for DeviceID in self.deviceids:
            flowdelete = requests.delete('http://127.0.0.1:8181/onos/v1/devices/'+DeviceID,
                                         auth=('onos', 'rocks'), headers=self.postheader)

device= DevicesDelete('del')
device.start()