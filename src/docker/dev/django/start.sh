#!/bin/bash 

set -o errexit

# set -o pipefail 

set -o nounset 

# As the RCE Engine is only meant to execute the cpp code of users and it doesnot have any 
# model, hence, no need to run the server and no need of admin.  
# hence, makemigrations and migrate will run on sqlite3 which is not required, but for consistency in the django app, 
# the option is kept. 

python manage.py makemigrations --no-input 
python manage.py migrate --no-input 
python manage.py collectstatic --no-input 
exec python manage.py consume_messages