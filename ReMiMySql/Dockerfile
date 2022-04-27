FROM python:3.8-slim-buster
RUN apt update && apt -y upgrade \
#     && apt install -y python3 python3-pip \
#    && apt install -y mycli net-tools iputils-ping \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

#CMD ["flask", "run", "-h", "0.0.0.0"]
CMD ["gunicorn", "--bind=0.0.0.0:5000", "app:app"]