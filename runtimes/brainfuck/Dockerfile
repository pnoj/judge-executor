FROM alpine:latest
LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"
RUN apk add --no-cache git make gcc libc-dev libcap-dev
RUN git clone https://github.com/ioi/isolate.git isolategit
WORKDIR /isolategit
RUN make install

FROM python:3.8-alpine
COPY --from=0 /usr/local/bin/isolate-check-environment /usr/local/bin/
COPY --from=0 /usr/local/bin/isolate /usr/local/bin/
COPY --from=0 /usr/local/etc/isolate /usr/local/etc/
RUN apk add --no-cache libcap
RUN apk add --no-cache ruby gcc libc-dev bash
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
