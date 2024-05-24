ARG PYTHON_VERSION=3.10-bullseye 


FROM python:${PYTHON_VERSION} as python 

# stage 01: build dependency wheel 
FROM python as python-build-stage 

ARG BUILD_ENVIRONMENT=dev 

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential

COPY ./requirements . 

RUN pip wheel --wheel-dir /usr/src/app/wheel \
        -r ${BUILD_ENVIRONMENT}.txt 


# stege 02: run the app 

FROM python as python-run-stage 

# args 
ARG BUILD_ENVIRONMENT=dev 
ARG APP_HOME=app 

# env 
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
        gettext \
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
        && rm -rf /var/lib/apt/lists/* 


COPY --from=python-build-stage /usr/src/app/wheel /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
        && rm -rf /wheels/

RUN curl -sSL https://get.docker.com/ | sh

COPY ./docker/dev/django/start.sh /app/docker/dev/django/start.sh 

RUN sed -i 's/\r$//g' /app/docker/dev/django/start.sh

RUN chmod +x /app/docker/dev/django/start.sh

COPY . ${APP_HOME}

ENTRYPOINT [ "sh", "/app/docker/dev/django/start.sh" ]
