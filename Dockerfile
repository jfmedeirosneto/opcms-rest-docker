FROM python:3
ENV PYTHONUNBUFFERED 0
WORKDIR /var/www/opcms-rest-docker
COPY requirements.txt /var/www/opcms-rest-docker
RUN pip install -r requirements.txt
RUN mkdir app-data
RUN mkdir admin-dist
RUN mkdir templates
COPY *.py /var/www/opcms-rest-docker/
COPY admin-dist /var/www/opcms-rest-docker/admin-dist
COPY templates /var/www/opcms-rest-docker/templates