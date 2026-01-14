FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install flask pyjwt flasgger

EXPOSE 5000

CMD ["python", "run.py"]