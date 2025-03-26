FROM python:3.12

WORKDIR /app

COPY main.py requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "main.py"]