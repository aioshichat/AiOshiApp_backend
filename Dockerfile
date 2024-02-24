FROM python:3.11 AS backend

WORKDIR /

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /usr/src

WORKDIR /usr/src

EXPOSE 80

CMD ["python3","app.py"]

