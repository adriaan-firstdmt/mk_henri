# Mikenskiet

## Configurtion
The playbook can be found at [Ansible Repo](https://github.com/HGriessel/mk_ansible.git)

You can run the main.yml for complete installation
Example Inventory File provided 
Global Vars that can be set example file provided all.example 

**database_user**:mysql_database_username  
**database_name**: mysql_database_name  
**app_root_directory**: /var/www/html/appname  
**virtualenv_name**: pythonvenv  
**static_dir**:  /some/path/static  
**app_name**: DjangoProjectName  
**nginx_path**: /etc/nginx/conf.d/  
**system_path**: /etc/systemd/system
**server_name**: app.domain.com  
**letsencrypt_email** : some@mail.com

#### Password variables retrieved from 
**database_password**: {{ vault_database_password }}  
**root_password**: {{ vault_root_password }}  

### DJANGO APP Config
Environment Variables can be set in .env an example file of the required Variable has been provided 

## Outstanding

####  Task 1 - Ansible [Repo](https://github.com/HGriessel/mk_ansible.git)

1. ~~Fix MySQL user privileges~~
1. Implement tags
3. ~~Setup Lets Encrypt certificate for SSL~~
4. ~~Implement Ansible Vault~~
5. ~~Setup CRON JOB for TASK 4~~

#### Task 2
1. Set up Database with native MySQL queries instead of Django builtin


#### Task 3
1. Refactoring of validate_csv_data method on DeviceCSVImport Into 2 Methods
    1. that only finds faulty lines
    2. that returns whether validation was successful 

###TASK 4 & 5
1. Finish provisioning Class
    1. parent class devices
    2. add api action that provisions device not just set its status
    3. Validate SSH connection 
    4. Improve Error handling of running the configuration command
2. Implement a CRON job that
    1. ~~Uses native SQL query language to get unprovisioned Routers~~
    2. ~~Then run a python script that interfaces with the app's API to configure the said routers provisioning status~~
    3. ~~run as Cron see ansible task point 5~~
