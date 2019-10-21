#!/bin/bash

php artisan migrate:rollback
php artisan migrate
php artisan db:seed
vendor/bin/phpunit -c phpunit.acceptance.xml --log-junit log.acceptance.junit.xml
rm -rf report-acceptance-tests
mkdir report-acceptance-tests
vendor/bin/phing -f phing-test-report-acceptance.xml

