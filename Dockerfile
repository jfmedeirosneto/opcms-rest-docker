FROM python:3
ENV PYTHONUNBUFFERED 0
WORKDIR /var/www/opcms-rest-docker
COPY requirements.txt /var/www/opcms-rest-docker
RUN pip install -r requirements.txt
COPY . /var/www/opcms-rest-docker