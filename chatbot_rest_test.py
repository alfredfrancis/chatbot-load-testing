import logging
import requests
import time
import uuid
from locust import HttpLocust, TaskSet, task, between
from locust.events import request_success
from typing import Dict

BOT_URL = "https://bots.cogniassist.com/61126f22624f978214b20966/default/webhooks/rest/webhook/"


def send_message(payload: Dict):
    logging.debug(f"Request Sent To Bot Server: {payload}")
    response = requests.post(BOT_URL, json=payload)
    logging.debug(f"Response From Bot Server: {response.text}")
    return response


def get_session_id():
    return str(uuid.uuid4())


class UserBehavior(TaskSet):
    statements = ['Do you provide covid coverage ?', 'I want to buy health insurance', 'Insurance']

    def on_start(self):
        self.session_id = str(uuid.uuid4())

    def on_quit(self):
        logging.info("Exited")

    @task(1)
    def trigger_welcome_menu(self):
        start_at = time.time()

        payload = {
            "message": "/default/welcome",
            "sender": get_session_id()
        }
        response = send_message(payload)
        if response.status_code == 200:
            request_success.fire(
                request_type='Welcome Menu',
                name='Welcome Menu',
                response_time=int((time.time() - start_at) * 1000000),
                response_length=len(response.text),
            )

    @task(2)
    def trigger_welcome_menu(self):
        start_at = time.time()

        payload = {
            "message": "Hi",
            "sender": get_session_id()
        }
        response = send_message(payload)
        if response.status_code == 200:
            request_success.fire(
                request_type='Smalltalk',
                name='Smalltalk',
                response_time=int((time.time() - start_at) * 1000000),
                response_length=len(response.text),
            )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)
