FROM nginx:alpine

RUN apk add --no-cache gettext

# RUN rm /etc/nginx/conf.d/default.conf 
COPY nginx.conf.template /etc/nginx/conf.d/default.conf.template

CMD envsubst '$DJANGO_PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'