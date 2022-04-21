# Mikenskiet

## Configurtion
The playbook can be found at [Ansible Repo](https://github.com/HGriessel/mk_ansible.git)

You can run the main.yml for complete installation

Global Vars that can be set

**database_user**:mysql_database_username  
**database_password**: **********  
**database_name**: mysql_database_name  
**root_password**: **********  
**app_root_directory**: /var/www/html/appname  
**virtualenv_name**: pythonvenv  
**static_dir**:  /some/path/static  
**app_name**: DjangoProjectName  
**nginx_path**: /etc/nginx/conf.d/  
**system_path**: /etc/systemd/system
**server_name**: app.domain.com

### DJANGO APP Config
Environment Variables can be set in .env an example file of the required Variable has been provided 

## Outstanding

####  Task 1 - Ansible [Repo](https://github.com/HGriessel/mk_ansible.git)

~~1. Fix MySQL user privileges~~
~~4. Implement Ansible Vault~~

1. Implement tags
3. Setup Lets Encrypt certificate for SSL
5. Setup CRON JOB for TASK 4

#### Task 2
1. Set up Database with native MySQL queries instead of Django builtin


#### Task 3
1. Refactoring of validate_csv_data method on DeviceCSVImport Into 2 Methods
    1. that only finds faulty lines
    2. that returns whether validation was successful 

###TASK 4 & 5
1. Finish provisioning Class
2. Implement a CRON job that
    1. Uses native SQL query language to get unprovisioned Routers
    2. Then run a python script that interfaces with the app's API to configure the said routers provisioning status
