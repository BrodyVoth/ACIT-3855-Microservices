import connexion
from connexion import NoContent
import requests
import datetime
import json
import yaml
from pykafka import KafkaClient
import logging
import logging.config
from flask_cors import CORS, cross_origin

try:
    with open('/config/app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except IOError:
    with open('app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def sleep_stat_offset(offset):
    client = KafkaClient(hosts=f"{app_config['kafka']['server']}:{app_config['kafka']['port']}")
    topic = client.topics["events"]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)

    message_list = []
    for message in consumer:
        message_string = message.value.decode('utf-8')
        message = json.loads(message_string)
        if message['type'] == 'ss':
            message_list.append(message)
    
    if len(message_list) < offset:
        logger.error('Offset greater than list length')
        return NoContent, 404

    logger.info('Returned sleep stat message: ' + str(message_list[offset]))
    return message_list[offset], 200

def get_oldest_day_stat():
    client = KafkaClient(hosts=f"{app_config['kafka']['server']}:{app_config['kafka']['port']}")
    topic = client.topics[f"{app_config['topic']}"]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)

    message_list = []
    for message in consumer:
        message_string = message.value.decode('utf-8')
        print(message_string)
        message = json.loads(message_string)
        if message['type'] == 'ds':
            message_list.append(message)

        if len(message_list) == 0:
            return NoContent, 404
            logger.error("First message not found")

        logger.info('Returned day stat message: ' + str(message_list[-1]))
        return message_list[-1], 200

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8120)

# def process_messages():
#     client = KafkaClient("localhost:9092")
#     topic = client.topics["events"]
#     consumer = topic.get_simple_consumer(consumer_group=events, auto_commit_enable=true, auto_commit_interval_ms=1000)

# for msg in consumer:
#     print(msg.offset)
#     msg_str = msg.value.decode('utf-8')
#     msg = json.loads(msg_str)
#     print(msg)
#     #msg.commit()
#     #consumer.commit()