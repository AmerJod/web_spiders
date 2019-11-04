FROM python:3.7.4

WORKDIR /usr/src/spiders

COPY . .

# install the requirements
RUN pip install -r requirements.txt


COPY common .
# install the common lib
RUN pip install .

CMD [ "python", "legalist_spider/main.py" ]
