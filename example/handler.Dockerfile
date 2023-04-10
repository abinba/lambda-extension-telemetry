FROM railflow/loki-lambda-extension:3.8 AS layer
FROM public.ecr.aws/lambda/python:3.8

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt
COPY --from=layer /opt/ .

WORKDIR ${LAMBDA_TASK_ROOT}
COPY handler/handler.py .

RUN python3 -m pip install --upgrade pip &&  \
    python3 -m pip install requests -q && \
    python3 -m pip install python-logging-loki -q

CMD ["handler.lambda_handler"]
