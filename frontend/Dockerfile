FROM httpd:latest

COPY index.html /usr/local/apache2/htdocs/
COPY myscript.sh /

RUN chmod +x /myscript.sh

ENTRYPOINT ["/myscript.sh"]