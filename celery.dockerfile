FROM python:3.5
ENV PYTHONUNBUFFERED 1

#ENV C_FORCE_ROOT true

ENV APP_USER myapp
ENV APP_ROOT /code
ENV DEBUG False
RUN mkdir /code;
RUN groupadd -r ${APP_USER} \
    && useradd -r -m \
    --home-dir ${APP_ROOT} \
    -s /usr/sbin/nologin \
    -g ${APP_USER} ${APP_USER}

WORKDIR ${APP_ROOT}

RUN mkdir /config
ADD requirements.txt /config/
RUN pip install --no-cache-dir -r /config/requirements.txt

USER ${APP_USER}
ADD . ${APP_ROOT}
