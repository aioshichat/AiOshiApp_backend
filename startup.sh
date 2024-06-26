#!/usr/bin/env bash

# 通常のAPI用のuwsgi起動
# uwsgi --ini wsgi.ini &
# LINEBotのAPI用のuwsgi起動
uwsgi --ini wsgi_line.ini &
# LIFFのAPI用のuwsgi起動
uwsgi --ini wsgi_liff.ini &
# nginx起動
nginx
# cron起動 (環境変数の読み込みでエラーになるのでコメントアウト)
# /etc/init.d/cron start

# コンテナが落ちないように
tail -F /dev/null