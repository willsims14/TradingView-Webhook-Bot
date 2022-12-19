FROM python:3.9-alpine

LABEL Auther="willsims14"

WORKDIR /app

COPY requirements.txt ./
COPY main.py config.py ./
COPY wallet/ wallet/

# RUN apk add gcc python3-dev openssl-dev musl-dev libffi-dev &&\
#     pip3 install --no-cache-dir -r requirements.txt

RUN pip install gunicorn
RUN pip install -r requirements.txt

# EXPOSE 80
ENV PORT=80

# ENTRYPOINT [ "python", "main.py" ]
# CMD ["gunicorn", "-w 3", "main:app", "--reload"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD exec gunicorn --bind :$PORT --workers 3 main:app
