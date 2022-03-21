import logging
import datetime
import time
import csv
import yaml
import json
from pyvesync import VeSync

with open('conf.yml') as file:
    conf = yaml.safe_load(file)
    logging.debug("Opened conf.yml")

manager = VeSync(conf['username'], conf['password'])
manager.login()
logging.info("Logged into VeSync")
manager.update()

refrigerator = manager.outlets[0]
logging.info("Found refrigerator:")
logging.info("%s", str(json.dumps(refrigerator.displayJSON(), indent=4)))

with open(conf['output'], 'a', newline='') as csvfile:
    outwriter = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    logging.info("Opened output: %s", conf['output'])
    
    while True:
        refrigerator.get_details()
        outwriter.writerow([datetime.datetime.now(), refrigerator.power])
        csvfile.flush()
        logging.info("Logged power usage of %f watts", refrigerator.power)
        time.sleep(conf['interval'])
