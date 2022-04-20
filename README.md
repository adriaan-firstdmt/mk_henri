# Mikenskiet



## Outstanding

####  Task 1 - Ansible [Repo](https://github.com/HGriessel/mk_ansible.git)

1. Fix MySQL user privileges 
2. Implement tags
3. Setup Lets Encrypt certificate for SSL
4. Implement Ansible Vault
5. Setup CRON JOB for TASK 4

#### Task 2
1. Set up Database with native MySQL queries instead of Django builtin


#### Task 3
1. Refactoring of validate_csv_data method on DeviceCSVImport Into
    1. Method that only finds faulty lines
    2. Method that returns whether validation was successful 

###TASK 4 & 5
1. Finish provisioning Class
2. Implement CRONT job that
    1. Uses native SQL query language to get unprovisioned Routers
    2. Then run python script that interfaces with the app's API to configure the said routers provisioning status