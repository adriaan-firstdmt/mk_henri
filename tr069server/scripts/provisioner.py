from typing import List
import mysql.connector
from pathlib import Path
import paramiko
import environ
import requests
from requests.auth import HTTPBasicAuth




class Mirkotik:
    """ Class for handeling mikrotik provisioning"""
    # TODO create parent class to handle multiple types of devices
    # TODO use class in API actions to provision device and set status not just set the status
    def __init__(self,customer_code:str,host:str,ssh_port:int=22,username:str="admin",password:str="") -> None:
        self.host = host
        self.port = ssh_port
        self.username = username
        self.password = password
        self.customer_code = customer_code
    
    def __repr__(self) -> str:
        cls = type(self)
        return f"{cls.__name__} object at {hex(id(self))} {self.customer_code} {self.host}"

    def __str__(self) -> str:
        return f"{self.customer_code} {self.host}"

    def ssh_connect(self,timeout:int=5) -> bool:
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # TODO validate connection in order not to try and provisioned unreacheble devices
        # TODO log errors like auth errors
            # log error where tr069 packages is not installed

        try:
            self.ssh_client.connect(self.host, self.port, self.username, self.password,timeout=timeout)
        except TimeoutError as e:
            return False
        return True


    def set_device_status_true(self) -> bool:
        url = "mem.griessels.site"
        response = requests.post(f"http://{url}/api/devices/set_status_true/",  auth=HTTPBasicAuth('root', 'eentotagt'),data={"ip":self.host})
        return response.json()['success']


    def run_tr069_ssh_command(self) -> bool:
        command = "/tr069-client set acs-url=\\ \nhttp://demo-axtract.firstdmt.com:9675/live/CPEManager/CPEs/genericTR69 \\ \ncheck-certificate=no connection-request-password=Jo68gae2oNhG \\ \nconnection-request-username=ADqV1FkIrAtW enabled=yes \\ \nperiodic-inform-interval=5m"
        if not self.ssh_connect():
            return False
        _stdin, _stdout,_stderr = self.ssh_client.exec_command(f"{command}")
        error =_stderr.read().decode()
        
        # TODO improve error handling

        if error != "": 
            return False
        return True
       
# in normal setting this will have also been a api reqeust to get all unprovisioned devices 
def get_unprovisioned_devices(db_user:str, db_pass:str, db_name,host="localhost")-> List:
    devices = []
    mydb = mysql.connector.connect(
        host=host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    mycursor=mydb.cursor()

    """ SELECT provisioningstatus.ip, provisioningstatus.status,device.customer_code FROM device
             INNER JOIN provisioningstatus 
             ON provisioningstatus.ip = device.ip  ") """

    mycursor.execute("SELECT tr069server_provisioningstatus.ip,tr069server_provisioningstatus.status,tr069server_device.customer_code FROM tr069server_device INNER JOIN tr069server_provisioningstatus ON tr069server_provisioningstatus.ip = tr069server_device.ip WHERE tr069server_provisioningstatus.status = 0")

    for row in mycursor:
        device = Mirkotik(row[2],row[0],username="root",password="een1T0T8agt")
        devices.append(device)
    
    return devices

def main() -> None:
    env = environ.Env()
    path = Path(__file__).resolve().parent.parent.parent
    environ.Env.read_env(f"{path}/.env")
    
    db_name = env("DATABASE_NAME")
    db_user = env("DATABASE_USER")
    db_pass = env("DATABASE_PASS")
    
    devices = get_unprovisioned_devices(db_user,db_pass,db_name)
    
    for device in devices:
        if not device.run_tr069_ssh_command():
            device.set_device_status_true()
    

if __name__ == "__main__":
   main()