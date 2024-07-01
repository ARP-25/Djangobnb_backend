FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/djangobnb.conf /etc/nginx/conf.d/djangobnb.conf
