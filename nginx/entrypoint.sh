#!/bin/sh

sed -i -e "s/\${NICE_PROJECT_HOST}/${NICE_PROJECT_HOST}/" \
  -e "s/\${NICE_PROJECT_PORT}/${NICE_PROJECT_PORT}/" \
  -e "s/\${NGINX_LISTEN_PORT}/${NGINX_LISTEN_PORT}/" /etc/nginx/nginx.conf;

exec "$@"