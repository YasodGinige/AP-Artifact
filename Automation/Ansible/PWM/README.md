The purpose of this playbook is to install pwm. The pwm server name can be specified by changing the pwm_hostname variable in defaults/main.yml.

This role is still in development and is not currently functional.


Installation on Windows OS
--------------------------
Installation on the Windows platform is rather trivial, and consists of the following stages:

- Download and Install Java from Adoptium.
- Download and Install Tomcat from Apache.
- Download the latest build of PWM Current Build.
- Extract pwm.war from downloaded zip file and explode by copying to Tomcat Webapps folder
- Configure the PWM_APPLICATIONPATH environment variable.
- Start the configuration wizard by going to the default application url.


Role Variables
--------------

- pwm_hostname: hostname that pwm will service, will be set to "pwm" by default
- pwm_port: hostname that pwm will service, will be set to 8888 by default.
- pwm_root_mysql_password: root mysql password, will be set to a random value by default.
- pwm_pwm_mysql_password: pwm mysql password, will be set to a random value by default.
* pwm_admin_login: pwm admin login name, 'root' by default.
- pwm_admin_password: pwm admin password, 'password' by default.


License
-------

GPLv2


Author Information
------------------
Sentinal

