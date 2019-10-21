#!/bin/bash

vendor/bin/phpunit --log-junit log.unit.junit.xml
rm -rf report-unit-tests
mkdir report-unit-tests
vendor/bin/phing -f phing-test-report-unit.xml

