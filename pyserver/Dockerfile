FROM python:3.6

WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80

CMD ["python", "./main.py"]