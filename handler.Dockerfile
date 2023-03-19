FROM 123456789012.dkr.ecr.eu-west-1.amazonaws.com/lambda-extension-test-repository-6a2cb02:ext-1 AS layer
FROM public.ecr.aws/lambda/python:3.8

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt
COPY --from=layer /opt/ .

WORKDIR ${LAMBDA_TASK_ROOT}
COPY handler/handler.py .

RUN python3 -m pip install --upgrade pip &&  \
    python3 -m pip install requests -q

CMD ["handler.lambda_handler"]
