FROM python:3.6

WORKDIR /usr/src/app

COPY ./pyserver /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
EXPOSE 443

CMD ["gunicorn", "--chdir", "/usr/src/app", "main:app", "-b", "0.0.0.0:80"]