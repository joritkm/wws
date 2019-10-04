#!/bin/sh

#
# serve wws with gunicorn
#

PROCNAME="weddingwebsite"
ADDRESS="0.0.0.0:5000"
WORKERS=$(lscpu | grep ^CPU\(s\) | awk '{print $2}')

ACCESS_LOG="-"
ERROR_LOG=$ACCESS_LOG
LOG_LEVEL="INFO"

export FLASK_ENV="production"
gunicorn -b $ADDRESS -w $WORKERS -n $PROCNAME \
--access-logfile $ACCESS_LOG \
--error-logfile $ERROR_LOG \
--log-level $LOG_LEVEL \
app.wsgi:application

#EOF