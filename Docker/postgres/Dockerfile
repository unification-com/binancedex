FROM postgres:10.8

WORKDIR /app

USER postgres

RUN rm -rf /var/lib/postgresql/data/*

COPY Docker/postgres/data/0init-user-db.sh /docker-entrypoint-initdb.d/
COPY Docker/postgres/data/binancedex-01.sql /docker-entrypoint-initdb.d/

ENTRYPOINT ["/docker-entrypoint.sh"]

RUN echo "alias ll='ls -la'" >> /var/lib/postgresql/.bashrc

EXPOSE 5432
CMD ["postgres"]
