FROM nginx:1.18.0-alpine

COPY nginx.conf /etc/nginx/nginx.conf

ARG NICE_PROJECT_HOST
ARG NICE_PROJECT_PORT
ARG NGINX_LISTEN_PORT

RUN sed -i -e "s/\${NICE_PROJECT_HOST}/${NICE_PROJECT_HOST}/" \
  -e "s/\${NICE_PROJECT_PORT}/${NICE_PROJECT_PORT}/" \
  -e "s/\${NGINX_LISTEN_PORT}/${NGINX_LISTEN_PORT}/" /etc/nginx/nginx.conf

COPY static /static