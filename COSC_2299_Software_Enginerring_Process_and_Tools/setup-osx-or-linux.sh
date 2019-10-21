#!/bin/bash

cp env-local-osx-or-linux .env
touch storage/database.sqlite
#chmod -R g+w bootstrap storage
#sudo chgrp -R _www bootstrap storage
composer install
php artisan migrate
php artisan db:seed

