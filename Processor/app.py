import connexion
from connexion import NoContent

from datetime import datetime
import yaml
import json
import logging
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
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

def populate_stats():
    """ Periodically update stats """
    logger.info("Started Periodic Processing")

    if os.path.exists(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as f:
            json_data = json.loads(f.read())
    else:
        json_data = {
            "num_sleep_stats": 0,
            "num_day_stats": 0,
            "num_good_sleeps": 0,
            "num_good_days": 0,
            "updated_timestamp": str(datetime.now())
        }

    parameters = {'startDate': json_data['updated_timestamp'], 'endDate': str(datetime.now())}
    sleep_data = requests.get(app_config['eventstore']['url']+'/report/sleep_stats', params=parameters)
    day_data = requests.get(app_config['eventstore']['url']+'/report/day_stats', params=parameters)
    
    sleep_data_json = sleep_data.json()
    day_data_json = day_data.json()
    good_sleeps = 0
    good_days = 0

    for event in sleep_data_json:
        if event['feeling'] == 'Good':
            good_sleeps += 1

    for event in day_data_json:
        if event['mood'] == 'Good':
            good_days += 1

    if sleep_data.status_code == 200:
        logger.info('{} new sleep stats.'.format(len(sleep_data_json)))
    else:
        logger.error('Error: Did not receive 200 response from sleep stats request')
    
    if day_data.status_code == 200:
        logger.info('{} new day stats.'.format(len(day_data_json)))
    else:
        logger.error('Error: Did not receive 200 response from day stats request')

    if json_data.get('num_sleep_stats'):
        json_data['num_sleep_stats'] = json_data['num_sleep_stats'] + len(sleep_data_json)
    else:
        json_data['num_sleep_stats'] = len(sleep_data_json)

    if json_data.get('num_day_stats'):
        json_data['num_day_stats'] = json_data['num_day_stats'] + len(day_data_json)
    else:
        json_data['num_day_stats'] = len(day_data_json)

    if json_data.get('num_good_sleeps'):
        json_data['num_good_sleeps'] = json_data['num_good_sleeps'] + good_sleeps
    else:
        json_data['num_good_sleeps'] = good_sleeps

    if json_data.get('num_good_days'):
        json_data['num_good_days'] = json_data['num_good_days'] + good_days
    else:
        json_data['num_good_days'] = good_days
    
    json_data['updated_timestamp'] = str(datetime.now())

    with open(app_config['datastore']['filename'], "w") as f:
        f.write(json.dumps(json_data))

    logger.debug("Total sleep stats: {}. Total day stats: {}. Total good sleeps: {}. Total good days: {}. New timestamp: {}."
                .format(json_data['num_sleep_stats'], json_data['num_day_stats'], json_data['num_good_sleeps'],
                 json_data['num_good_days'], json_data['updated_timestamp']))

    logger.info("Periodic Processing Complete")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                    'interval',
                    seconds=app_config['scheduler']['period_sec'])
    sched.start()
    logger.info('Started scheduler')


def get_statistics():
    """ Get statistics from the data store """
    logger.info("Started request")
    if os.path.exists(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as f:
            data = json.loads(f.read())

        logging.debug("Request data: {}".format(data))
        logging.info("Request completed")

        return data, 200
    else:
        logger.error("File not found")
        return 404

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)
