#!/usr/bin bash

docker create --name dummy -p 80:80 -p 4242:4242 ft_onion
docker cp dummy:/etc/tor/torrc ~/42/otros_cursos/doing/cyber_bootcamp/ft_onion/files/torrc
docker cp dummy:/etc/nginx/sites-available/default ~/42/otros_cursos/doing/cyber_bootcamp/ft_onion/files/nginx.conf
docker cp dummy:/var/www/html/index.nginx-debian.html ~/42/otros_cursos/doing/cyber_bootcamp/ft_onion/files/index.htmml
docker cp dummy:/var/lib/tor/hidden_service/hostname ~/42/otros_cursos/doing/cyber_bootcamp/ft_onion/files/hostname
docker rm -f dummy
echo cat ~/42/otros_cursos/doing/cyber_bootcamp/ft_onion/files/hostname