# Dockerfile

FROM python:3.7-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
COPY requirements.txt /opt/app/
WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN pip install yfinance --upgrade --no-cache-dir
COPY . /opt/app/

# start server
STOPSIGNAL SIGTERM
CMD gunicorn display_stock.wsgi --bind 0.0.0.0:$PORT --timeout 600
