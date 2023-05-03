FROM debian:buster

ARG ONI_USR
ARG ONI_PASS

LABEL mainteiner=fballest@student.42madrid.com

RUN apt-get -y update && apt-get -y install nginx vim tor openssh-server

RUN echo "RunAsDaemon 1" >> etc/tor/torrc
RUN echo "Log notice file /var/log/tor/log" >> etc/tor/torrc
RUN echo "DataDirectory /var/lib/tor/hidden_service/" >> etc/tor/torrc
RUN echo "HiddenServiceDir /var/lib/tor/hidden_service/" >> /etc/tor/torrc
RUN echo "HiddenServicePort 80 127.0.0.1:80" >> /etc/tor/torrc
RUN echo "Port 4242" >> /etc/ssh/sshd_config
RUN echo "AuthorizedKeysFile /.ssh/fbskey.pub" >> /etc/ssh/sshd_config

RUN adduser ${ONI_USR}; echo "${ONI_USR}:${ONI_PASS}" | chpasswd

COPY /conf/fbskey.pub /.ssh/fbskey.pub
RUN chmod 600 /.ssh/fbskey.pub

RUN service tor start

EXPOSE 80 4242

CMD service tor start; cat /var/lib/tor/hidden_service/hostname; service ssh start; nginx -g 'daemon off;';
