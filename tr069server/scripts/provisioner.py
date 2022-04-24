from dataclasses import dataclass,field
from typing import List
import mysql.connector
from pathlib import Path
import environ
from device.device import Device, MirkotikProvisioner, Provisioner

env = environ.Env()
path = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(f"{path}/.env")

DB_NAME = env("DATABASE_NAME")
DB_USER = env("DATABASE_USER")
DB_PASS = env("DATABASE_PASS")
DEVICE_USER = env("DEVICE_USER")
DEVICE_PASS = env("DEVICE_PASS")





# in normal Django/Django Rest Framework setting this will have also been a api reqeust to get all unprovisioned devices 
def get_unprovisioned_devices(db_user:str, db_pass:str, db_name,host="localhost")-> List:
    devices: List[Device] = []
    mydb = mysql.connector.connect(
        host=host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    mycursor=mydb.cursor()

    """ SELECT provisioningstatus.ip, 
               provisioningstatus.status,
               device.customer_code 
            FROM device
            INNER JOIN provisioningstatus 
            ON provisioningstatus.ip = device.ip  ") """

    mycursor.execute("SELECT tr069server_provisioningstatus.ip,tr069server_provisioningstatus.status,tr069server_device.customer_code FROM tr069server_device INNER JOIN tr069server_provisioningstatus ON tr069server_provisioningstatus.ip = tr069server_device.ip WHERE tr069server_provisioningstatus.status = 0")

    for row in mycursor:
        device = Device(customer_code=row[2],ipaddress = row[0],username=DEVICE_USER,password=DEVICE_PASS)
        devices.append(device)
    
    return devices

def main() -> None:
    devices = get_unprovisioned_devices(DB_USER,DB_PASS,DB_NAME)
    for device in devices:
        provisioner = MirkotikProvisioner(device.ipaddress,username=device.username,password=device.password)  
        if not device.provision_device(provisioner):
            print(f"{device.ipaddress} provisioning Failed")
            continue
        print(f"{device.ipaddress} provisioning succesfull")

            
    

if __name__ == "__main__":
   main()