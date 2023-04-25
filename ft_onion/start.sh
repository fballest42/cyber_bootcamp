#!/usr/bin bash

echo "HiddenServiceDir /var/lib/tor/my_website/" >> /etc/tor/torrc
echo "HiddenServicePort 80 127.0.0.1:80 /var/lib/tor/my_website/" >> /etc/tor/torrc

