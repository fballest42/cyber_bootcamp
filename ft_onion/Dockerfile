FROM debian:buster

LABEL mainteiner=fballest@student.42madrid.com

RUN apt-get -y update && apt-get -y install nginx vim tor openssh-server

#AÑADIR LOS ELEMENTOS SSH Y SU CONFIGURACIÓN

WORKDIR /usr

COPY ./conf/nginx.conf /etc/nginx/conf.d/

COPY ./conf/start.sh ./

EXPOSE 80

EXPOSE 4242

EXPOSE 9050

CMD ["nginx", "-g", "daemon off;"]


