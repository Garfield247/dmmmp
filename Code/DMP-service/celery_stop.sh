#!/bin/sh
cd /home/dmp/dmp-phase1/Code/DMP-service/
celery multi stop w1 w2 w3 -A dmp.extensions.celery -l info --logfile=/home/dmp/dmp_log/celery/celerylog.log
