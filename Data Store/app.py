import connexion

from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from sleep_stats import SleepStats
from day_stats import DayStats
import datetime
import yaml
from threading import Thread
import json
from pykafka import KafkaClient
import logging
import logging.config
from flask_cors import CORS, cross_origin

try:
    with open('/config/app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())
        db = app_config['datastore']
except IOError:
    with open('app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())
        db = app_config['datastore']

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(db['user'], db['password'], db['hostname'], db['port'], db['db']))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

# def report_sleep_stats(report):
#     """ Adds a sleep stats report """

#     session = DB_SESSION()

#     sleep = SleepStats(report['user_id'],
#                        report['sleep_start_time'],
#                        report['sleep_end_time'],
#                        report['feeling'],
#                        report['notes'])

#     session.add(sleep)
#     session.commit()
#     session.close()


#     return NoContent, 201


def get_sleep_stats(startDate, endDate):
    """ Get sleep stats reports from the data store """

    results_list = []

    session = DB_SESSION()

    results = []

    results = session.query(SleepStats).filter(SleepStats.date_created.between(startDate, endDate))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()

    logger.info(f'Got {len(results_list)} sleep stats from data store')
    return results_list, 200


# def report_day_stats(report):
#     """ Adds a day stats report """

#     session = DB_SESSION()

#     day = DayStats(report['user_id'],
#                    report['mood'],
#                    report['notes'])

#     session.add(day)
#     session.commit()
#     session.close()

#     return NoContent, 201


def get_day_stats(startDate, endDate):
    """ Get day stats reports from the data store """

    results_list = []

    session = DB_SESSION()

    results = session.query(DayStats).filter(DayStats.date_created.between(startDate, endDate))

    for result in results:
        results_list.append(result.to_dict())

    session.close()

    logger.info(f'Got {len(results_list)} day stats from data store')
    return results_list, 200

def process_messages():
    client = KafkaClient(hosts=f"{app_config['kafka']['server']}:{app_config['kafka']['port']}")
    topic = client.topics[f"{app_config['topic']}"]
    consumer = topic.get_simple_consumer(consumer_group="events", auto_commit_enable=True)

    for message in consumer:
        message_string = message.value.decode('utf-8')
        message = json.loads(message_string)
        logger.info(f'New Message: {message_string}')
        if message['type'] == 'ss':
            session=DB_SESSION()
            sleep_stat = SleepStats(message['payload']['user_id'],
                                    message['payload']['sleep_start_time'],
                                    message['payload']['sleep_end_time'],
                                    message['payload']['feeling'],
                                    message['payload']['notes'])

            session.add(sleep_stat)
            session.commit()
            session.close()

        if message['type'] == 'ds':
            session=DB_SESSION()
            day_stat = DayStats(message['payload']['user_id'],
                                    message['payload']['mood'],
                                    message['payload']['notes'])
            session.add(day_stat)
            session.commit()
            session.close()

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    # run our standalone gevent server
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
