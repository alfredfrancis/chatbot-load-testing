from locust import HttpLocust, TaskSet, task, between
from locust.events import request_success
import socketio
import time
import random


class UserBehavior(TaskSet):
    statements = ['Do you provide covid coverage ?', 'I want to buy health insurance', 'Insurance']

    def on_start(self):
        sio = socketio.Client()
        ws_url = "bots.cogniassist.com/61126f22624f978214b20966/default/socket.io"
        sio.connect(ws_url, transports="websocket")
        self.ws = sio
        self.user_id = sio.sid
        # body = json.dumps(["session_confirm", self.user_id])
        body = '{"session_request", {"session_id": "' + self.user_id + '"}}'
        self.ws.emit(body)

    def on_quit(self):
        self.ws.disconnect()

    @task(1)
    def trigger_welcome_menu(self):
        start_at = time.time()

        body = {"message": "/default/welcome", "session_id": self.user_id}

        # self.ws.send(body)
        self.ws.emit('user_uttered', data=body)

        request_success.fire(
            request_type='WebSocket Sent',
            name='test/ws/echo',
            response_time=int((time.time() - start_at) * 1000000),
            response_length=len(body),
        )
    
    @task(2)
    def submit_welcome_form(self):
        start_at = time.time()

        body = {"message":"/welcomeForm{\"slots\":{\"name\":\"Alfred Francis\",\"email\":\"alfed@xyz.com\",\"mobile\":\"8714349616\"}}","session_id":self.user_id}

        # self.ws.send(body)
        self.ws.emit('user_uttered', data=body)

        request_success.fire(
            request_type='WebSocket Sent',
            name='test/ws/echo',
            response_time=int((time.time() - start_at) * 1000000),
            response_length=len(body),
        )

    @task(3)
    def say_random(self):
        start_at = time.time()

        statement = random.choice(self.statements)

        body = {"message": statement, "session_id": self.user_id}

        # self.ws.send(body)
        self.ws.emit('user_uttered', data=body)

        request_success.fire(
            request_type='WebSocket Sent',
            name='test/ws/echo',
            response_time=int((time.time() - start_at) * 1000000),
            response_length=len(body),
        )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)