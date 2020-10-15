from faker import Faker
import random
import string
from datetime import date, datetime
import time
from locust import HttpUser, task, TaskSet, between
import json
fake = Faker()


def get_date():
    now = datetime.now()

    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")

    return dt_string


def get_alphanum():
    x = ''.join(random.choice(string.ascii_uppercase  + string.digits) for _ in range(12))
    return x


def get_random_num(min, max):
    random_num = fake.random_int(min, max)
    return random_num


def get_random_facility():
    map = [ 'NJLGN','9T904T','35W35R', 'RE4033','E2565f']
    return map[random.randint(0, len(map)-1)]


def mock_data():

    return {
        "config": {
            "tid": get_alphanum(),
            "qrcode": f"{get_random_num(0,99)}-{get_random_num(300, 999999)}-f{random.choice(string.ascii_lowercase)}{get_random_num(0, 99999)}",
            "barcode": fake.ean13(),
            "facility": get_random_facility(),
            "sdate": get_date(),
            "activdate": get_date(),
            "linkdate": get_date(),
            "devstatus": "1",
            "ttype" : "White",
            "tperson": "Parcel",
            "apn": fake.first_name()
        }
    }

def mock_event():
    return {
    "eventData": {
        "cid" : get_alphanum(),
        "ts" : f"{int(time.time())}",
        "rid" : get_alphanum(),
        "scantype" : f"{get_random_num(0, 9999)}",
        "type" : fake.ean13(),
        "pids" : [f"{get_random_num}", "A4", "F6", "87", "AC", f"{get_random_num(0, 99)}"],
        "sTimes" : [f"{get_random_num(1000000, 9999999999)}", f"{get_random_num(1000000, 9999999999)}", f"{get_random_num(1000000, 9999999999)}",f"{get_random_num(1000000, 9999999999)}", f"{get_random_num(1000000, 9999999999)}", "1602309674"]
    }
}

class APIUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def post_tape(self):
        #data = mock_data()
        headers = {'content-type': 'application/json'}
        self.client.post("/tapes/config", headers=headers, json=mock_data())

    @task
    def post_event(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/events", headers=headers, json=mock_event())


   

# tape personility - parcel
# tape type - white
# date format - mm/dd/yy 
# APN in the db
