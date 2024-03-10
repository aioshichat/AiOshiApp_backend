#!/usr/bin/env bash

DATE=`date`

/usr/local/bin/python3 /usr/src/cron/push_message_job.py

retval=$?

if [ $retval -eq 0 ]
then
    echo "[${DATE}] push_message_job succeeded."
else
    echo "[${DATE}] push_message_job failed."
fi