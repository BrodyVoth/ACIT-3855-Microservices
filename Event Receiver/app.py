import connexion
from connexion import NoContent
import requests
import datetime
import json
import yaml
from pykafka import KafkaClient
from flask_cors import CORS, cross_origin
import logging
import logging.config

try:
    with open('/config/app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except IOError:
    with open('app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

client = KafkaClient(hosts=f"{app_config['kafka']['server']}:{app_config['kafka']['port']}")
topic = client.topics[f"{app_config['topic']}"]
producer = topic.get_sync_producer()

def report_sleep_stats(sleepStats):

    msg = { "type" : "ss",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": sleepStats }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info('Sleep Stat Produced: ' + msg_str)
    print(sleepStats)
    # headers = {'Content-Type': 'application/json'}
    # request = requests.post('http://localhost:8090/report/sleep_stats', data=json.dumps(sleepStats), headers=headers)
    return NoContent, 201


def report_day_stats(dayStats):
    msg = { "type" : "ds",
            "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "payload": dayStats }
    msg_str = json.dumps(msg)

    producer.produce(msg_str.encode('utf-8'))
    logger.info('Day Stat Produced: ' + msg_str)

    print(dayStats)
    # headers = {'Content-Type': 'application/json'}
    # request = requests.post('http://localhost:8090/report/day_stats', data=json.dumps(dayStats), headers=headers)
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)
