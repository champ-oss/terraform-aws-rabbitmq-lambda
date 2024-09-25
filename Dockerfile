FROM public.ecr.aws/lambda/python:3.12

COPY src/ "${LAMBDA_TASK_ROOT}"

COPY src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "main.handler" ]