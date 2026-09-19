#!/bin/bash

# Check env variable value exists
if [[ -n "${IP:-}" ]]; then
    echo "IP is set and non-empty"
else
    echo "IP is missing or empty"
    exit 1
fi

if [[ -n "${PORT:-}" ]]; then
    echo "PORT is set and non-empty"
else
    echo "PORT is missing or empty"
    exit 1
fi

if [[ -n "${PROTOCOL:-}" ]]; then
    echo "PROTOCOL is set and non-empty"
else
    echo "PROTOCOL is missing or empty"
    exit 1
fi

# Replace IP and PORT in the index.html
sed -i "s/{IP}/${IP}/g" /usr/local/apache2/htdocs/index.html

sed -i "s/{PORT}/${PORT}/g" /usr/local/apache2/htdocs/index.html

sed -i "s/{PROTOCOL}/${PROTOCOL}/g" /usr/local/apache2/htdocs/index.html

# Start httpd
httpd-foreground