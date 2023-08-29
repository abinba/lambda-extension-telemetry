FROM python:3.11-alpine

ADD extensions /opt/extensions

ADD telemetry_extension /opt/telemetry_extension
RUN chmod +x /opt/telemetry_extension

RUN pip install --upgrade pip -q && \
    pip install requests -t /opt/extensions/lib -q && \
    pip install python-logging-loki -t /opt/extensions/lib -q
