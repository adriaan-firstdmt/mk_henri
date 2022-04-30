from abc import abstractmethod,ABC
from dataclasses import dataclass, field
import socket
from requests.auth import HTTPBasicAuth
import paramiko
import requests


class Provisioner(ABC):
    @abstractmethod
    def initialize_tr069(self) -> bool:
        pass

class MirkotikProvisioner(Provisioner):
    """ Class for handeling mikrotik provisioning"""
    # TODO use class in API actions to provision device and set status not just set the status
    def __init__(self,ipaddress:str,port:int=22,username:str="admin",password:str="") -> None:
        self.ipaddress = ipaddress 
        self.port = port
        self.username = username
        self.password = password

    def ssh_connect(self,timeout:int=5) -> bool:
        """Create SSH Conection retruns whether conenction could be established"""
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(self.ipaddress, self.port, self.username, self.password,timeout=timeout)
        except TimeoutError:
            return False
        except socket.timeout:
            return False
        return True


    def initialize_tr069(self,soft_fail=True) -> bool:
        tr069_url="http://demo-axtract.firstdmt.com:9675/live/CPEManager/CPEs/genericTR69"
        # command = "/tr069-client set acs-url=\\ \n{tr069_url} \\ \ncheck-certificate=no connection-request-password=Jo68gae2oNhG \\ \nconnection-request-username=ADqV1FkIrAtW enabled=yes \\ \nperiodic-inform-interval=5m"
        command = 'df'
        if not self.ssh_connect():
            return False
        
        _stdin, _stdout,_stderr = self.ssh_client.exec_command(f"{command}")
        error = _stderr.read().decode()

        if error != "": 
            if not soft_fail:
                raise Exception(error)
        return True



@dataclass
class Device:
    customer_code:str 
    ipaddress:str 
    port:int = 22  
    username:str ='admin'
    password:str = field(repr=False,default="")


    def set_device_status(self,status) -> bool:
        print(self.ipaddress)
        url = "mem.griessels.site"
        api_action = "api/devices/set_status_true"
        # TODO abstractt to env variables 
        response = requests.post(f"https://{url}/api/devices/set_status/",  auth=HTTPBasicAuth('root', 'eentotagt'),data={"ip":self.ipaddress,'status':status})
        return response.json()['success']

    def provision_device(self,provisioner:Provisioner) -> bool: 
        if not provisioner.initialize_tr069(soft_fail=True):
            return False
        self.set_device_status(True)
        return True
      


def main():
    mikrotik = Device("CUS001", "188.166.34.31", username="root", password="een1T0T8agt")
    provisioner = MirkotikProvisioner(mikrotik.ipaddress,username=mikrotik.username,password=mikrotik.password)
    if mikrotik.provision_device(provisioner):
        print("success")
        return 0
    return 1

    
if __name__ == "__main__":
   main()
