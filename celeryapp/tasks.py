from celery import Celery

app = Celery('tasks', broker='amqp://localhost', backend='amqp://localhost')

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def reverse(mystring):
	return mystring[::-1]


def getWeatherReport(q):
	import requests
	key = "ab403d318b214a6cb8a124633181306"
	num_of_days = "2"
	url = "http://api.worldweatheronline.com/premium/v1/weather.ashx?key="+key+"&q="+q+"&format=json&num_of_days="+num_of_days
	response = requests.get(url)
	print(response)
	return response


@app.task
def showcities():
	import pika
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='mobigo123')
	mycities = []

	def callback(ch, method, properties, body):
		import json
		print("[x] Received %r" % body)
		decode_body =  body.decode('utf-8')
		mycities = json.loads(decode_body)
		for city in mycities:
			print("[x] City name %r" % city['name'])
			response = getWeatherReport(str(city['name']))
			print("[x] weather response %r" % response)
			connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
			channel = connection.channel()
			channel.queue_declare(queue='newweatherReport')
			channel.basic_publish(exchange="",routing_key="newweatherReport",body=json.dumps(response.json()))
			print("[x] sent 'saved weather report in queue'")
		connection.close()
		#channel.queue_declare(queue='weatherReport')


	channel.basic_consume(callback, queue='mobigo123', no_ack=True)
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()
	# connection.close()
	return "Successfuly stored weather report in queue."