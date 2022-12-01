FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Audio tools
  && apt-get install -y ffmpeg libvorbis-dev \
  # Additional dependencies
  && apt-get install -y telnet netcat nasm \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./compose/local/flask/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/flask/daemon/start /start-daemon
RUN sed -i 's/\r$//g' /start-daemon
RUN chmod +x /start-daemon

RUN mkdir /datastore

WORKDIR /app
COPY . .

CMD ["/start-daemon"]
