Run Guniron
===============

::

    $ gunicorn -c guniconr.py app.wsgi:application  -b 0.0.0.0:9990

Nginx
========

::

    upstream django-apps{
      ip_hash;
      server unix:/vagrant/projects/wpauth/djpress/sample/logs/gunicorn.sock;
    }

    server {
        //... port and other settings
 
        location /apps/assets {
            alias /vagrant/projects/wpauth/djpress/sample/assets;
        }  
        
        location /apps {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header SCRIPT_NAME /apps;
            proxy_redirect off;
            if (!-f $request_filename) {
                proxy_pass http://django-apps;
                break;
            }   
        }    
    }
