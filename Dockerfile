FROM python:3.7.4

WORKDIR /usr/src/spiders

COPY . .

# install the requirements
RUN pip install -r requirements.txt

CMD [ "python", "legalist_spider/main.py" ]
