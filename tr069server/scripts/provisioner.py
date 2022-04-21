from dataclasses import dataclass
from typing import List
import mysql.connector
from pathlib import Path
import paramiko
import environ
import os




class Mirkotik:
    def __init__(self,host:str,ssh_port:int=22,username:str="admin",password:str="") -> None:
        self.host = host
        self.port = ssh_port
        self.username = username
        self.password = password

    def ssh_connect(self) -> paramiko.SSHClient:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, self.port, self.username, self.password)
    
    # TODO validate connction in order not to try and provisioned unreacheble devices


    def set_device_status(self) -> bool:
        # utilised API to set device status
            #if run_tr069_ssh_command successfull
        return True

    def run_tr069_ssh_command(self) -> bool:
        command = "/tr069-client"
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
    mycursor.execute("SELECT ip,status FROM tr069server_provisioningstatus WHERE status=0")

    for row in mycursor:
        device = Mirkotik(row[0],row[1])
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
        device.run_tr069_command()
    


if __name__ == "__main__":
   main()