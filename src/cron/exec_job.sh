#!/usr/bin/env bash

DATE=`date`

/usr/local/bin/python3 /usr/src/cron/push_message_job.py 1>>/proc/1/fd/1 2>>/proc/1/fd/2

retval=$?

if [ $retval -ge 0 ]
then
    echo "[${DATE}] push_message_job succeeded. count: $retval." 1>>/proc/1/fd/1 2>>/proc/1/fd/2
else
    echo "[${DATE}] push_message_job failed." 1>>/proc/1/fd/1 2>>/proc/1/fd/2
fi
