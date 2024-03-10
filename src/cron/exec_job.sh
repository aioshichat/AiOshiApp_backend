#!/usr/bin/env bash

DATE=`date`

/usr/local/bin/python3 /usr/src/cron/push_message_job.py

retval=$?

if [ $retval -ge 0 ]
then
    echo "[${DATE}] push_message_job succeeded. count: $retval." >> /usr/src/cron/cron.log
else
    echo "[${DATE}] push_message_job failed." >> /usr/src/cron/cron.log
fi