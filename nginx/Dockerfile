FROM nginx:1.18.0-alpine

COPY nginx.conf /etc/nginx/nginx.conf

COPY static /static

COPY entrypoint.sh entrypoint.sh

RUN sed -i 's/\r$//' entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]