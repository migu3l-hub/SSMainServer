FROM python:3.8

RUN apt-get -y update
RUN apt install -y postgresql postgresql-contrib
RUN mkdir /dependencias
COPY requirements.txt /dependencias
RUN pip install -r /dependencias/requirements.txt
ENV SECRET_KEY=""
ENV DB_NAME=""
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DB_HOST=""
ENV DB_PORT=5432
RUN mkdir /codigo
RUN mkdir /start

COPY ./inicioProyecto.sh /start
RUN useradd -s /bin/bash limitado
RUN chown -R limitado /codigo
RUN chown -R limitado /start
USER limitado
RUN chmod +x  /start/inicioProyecto.sh


WORKDIR /codigo
CMD /start/inicioProyecto.sh


