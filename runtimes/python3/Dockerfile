FROM python:3.8-alpine
LABEL maintainer="Paul (Kyunghan) Lee <contact@paullee.dev>"
RUN git clone https://github.com/ioi/isolate.git isolategit
WORKDIR /isolategit
RUN make install

FROM python:3.8-alpine
COPY --from=0 /usr/local/bin/isolate-check-environment /usr/local/bin/
COPY --from=0 /usr/local/bin/isolate /usr/local/bin/
COPY --from=0 /usr/local/etc/isolate /usr/local/etc/
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3", "executor.py"]
