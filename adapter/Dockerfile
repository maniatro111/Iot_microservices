FROM python:3.8

RUN pip3 install --upgrade pip
RUN pip3 install paho-mqtt
RUN pip3 install influxdb-client

COPY *.py /adapter/
WORKDIR /adapter

ENTRYPOINT ["python3", "adapter.py"]
