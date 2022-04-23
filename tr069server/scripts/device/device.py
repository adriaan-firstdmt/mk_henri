from dataclasses import dataclass, field
from enum import Enum, auto
from requests.auth import HTTPBasicAuth
import paramiko
import requests



class DeviceType(Enum):
    MIRKOTIK = auto()
    TP_LINK = auto()
    HAUWEI = auto()

@dataclass
class Device:
    customer_code:str 
    ipaddress: str 
    port: int = 22  
    username:str ='admin'
    password:str = field(repr=False,default="")
    type:DeviceType = DeviceType.MIRKOTIK  


class MirkotikProvisioner(Device):
    """ Class for handeling mikrotik provisioning"""
    # TODO use class in API actions to provision device and set status not just set the status

    def ssh_connect(self,timeout:int=5) -> bool:
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # TODO validate connection in order not to try and provisioned unreacheble devices
        # TODO log errors like auth errors

        try:
            self.ssh_client.connect(self.ipaddress, self.port, self.username, self.password,timeout=timeout)
        except TimeoutError as e:
            return False
        return True

    def set_device_status_true(self) -> bool:
        url = "mem.griessels.site"
        api_action = "api/devices/set_status_true"
        # TODO abstractt to env variables 
        response = requests.post(f"https://{url}/api/devices/set_status_true/",  auth=HTTPBasicAuth('root', 'eentotagt'),data={"ip":self.ipaddress})
        return response.json()['success']

    def ssh_initialize_tr069(self) -> bool:
        tr069_url="http://demo-axtract.firstdmt.com:9675/live/CPEManager/CPEs/genericTR69"
        command = "/tr069-client set acs-url=\\ \n{tr069_url} \\ \ncheck-certificate=no connection-request-password=Jo68gae2oNhG \\ \nconnection-request-username=ADqV1FkIrAtW enabled=yes \\ \nperiodic-inform-interval=5m"
        if not self.ssh_connect():
            return False
        _stdin, _stdout,_stderr = self.ssh_client.exec_command(f"{command}")
        error =_stderr.read().decode()

        if error != "": 
            return False
        return True


def main():
    mikrotik = MirkotikProvisioner("CUS001", "188.166.34.31", username="root", password="een1T0T8agt")
    if mikrotik.ssh_initialize_tr069():
        print("success")
        return 0
    print(mikrotik)
    return 1
if __name__ == "__main__":
   main()
