#!/usr/bin/env bash

uwsgi --ini wsgi.ini &
nginx

tail -F /dev/null