FROM python:3.11.8-slim
WORKDIR /usr/src/application
COPY app ./app
COPY data ./data
COPY requirements.txt .
COPY main.py .
COPY dev.env .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD [ "python", "./main.py" ]