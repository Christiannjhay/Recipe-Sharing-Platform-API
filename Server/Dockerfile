FROM mcr.microsoft.com/mssql/server:2019-latest

ENV SA_PASSWORD=@Qweasd78912345 \
    ACCEPT_EULA=Y

EXPOSE 1433

COPY ./initialize.sql /docker-entrypoint-initdb.d

CMD ["/opt/mssql/bin/sqlservr"]