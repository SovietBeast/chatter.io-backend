FROM postgres
ENV POSTGRES_PASSWORD password
COPY ./schema/init.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
