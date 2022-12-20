import random
import time


import socketio
from locust import HttpLocust, TaskSet, task, between
from locust.events import request_success, request_failure


class UserBehavior(TaskSet):
    def on_start(self):
        start_at = time.time()
        self.sio = socketio.Client()
        try:
            self.sio.connect(self.locust.host, socketio_path=self.locust.path, transports='websocket', wait_timeout=5)
        except Exception as e:
            request_failure.fire(
                request_type="socketio",
                name="Connect",
                response_time=0,
                response_length=0,
                exception=e
            )
            self.sio = None
            return

        # generate uuid user id string
        self.user_id = str(uuid.uuid4())
        self.sio.emit("session_request", {"session_id":  self.user_id })
        # Wait for the session to be confirmed
        self.sio.wait_for("session_confirmed")
        request_success.fire(
            request_type='socketio',
            name='Connect',
            response_time=int((time.time() - start_at) * 1000),
            response_length=len(body),
            )

    def on_quit(self):
        self.sio.disconnect()

    @task(1)
    def trigger_welcome_menu(self):
        if self.sio is None:
            return

        start_at = time.time()
        try:
            self.sio.emit('user_uttered', {"message": "hello, how are you ?"})
        except Exception as e:
            request_failure.fire(
                request_type="socketio",
                name='Welcome Menu',
                response_time=0,
                response_length=0,
                exception=e
            )
            return
        response = self.sio.wait_for("bot_uttered")
        request_success.fire(
            request_type='socketio',
            name='Welcome Menu',
            response_time=int((time.time() - start_at) * 1000),
            response_length=len(body),
        )

    @task(2)
    def submit_welcome_form(self):
        start_at = time.time()

        body = {"message": "/welcomeForm{\"slots\":{\"name\":\"Alfred Francis\",\"email\":\"alfed@xyz.com\",\"mobile\":\"8714349616\"}}"}

        self.sio.emit('user_uttered', body)

        response = self.sio.wait_for("bot_uttered")

        request_success.fire(
            request_type='Welcome Form',
            name='Welcome Form Submit',
            response_time=int((time.time() - start_at) * 1000),
            response_length=len(body),
        )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1, 2)
    host = 'https://bots.cogniassist.com'
    socketio_path = '/61126f22624f978214b20966/default/socket.io'