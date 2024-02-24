FROM python:3.11 AS backend

WORKDIR /

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get -y install nginx

RUN rm /etc/nginx/sites-enabled/default
COPY conf/uwsgi.conf /etc/nginx/sites-enabled/

COPY src /usr/src

WORKDIR /usr/src

EXPOSE 80

CMD ["uwsgi", "--ini", "wsgi.ini", "&"]

