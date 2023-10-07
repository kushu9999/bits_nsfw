# FROM python
FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["main.handler"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
