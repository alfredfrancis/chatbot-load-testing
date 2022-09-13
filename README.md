# Chatbot Stress Testing

#### Setup

```shell script
python -m venv venv
source venv/bin/activate
```

Install the dependencies:

```shell script
 install -r requirements.txt
```

Configure your socket.io configuration in `chatbot_test_script.py`:

```python
ws_url = "https://bots.cogniassist.com/61126f22624f978214b20966/default/socket.io"
```

Fire up Locust.io

```shell script
locust --host 127.0.0.1 --port 8080 --locustfile chatbot_test_script.py
```

#### Docker-compose Setup

start a master node and 4 workers using the following command:

```shell script
docker-compose up --scale worker=4
```

#### Using Locust Admin Panel

Now browse to your local machine

```web2py
http://localhost:8080
```

You'll be presented with the New Swarm window. Set the number of hosts, and hatch rate, and then click Start Swarming
You can see from the dashboard, how many users are spawned, how many connections are made, and how many failures.
All being well, you can then browse to the Charts menu and see how your swarm is doing
