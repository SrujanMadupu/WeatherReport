import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='mobigo123')

citynames = [{"name":"New York"},{"name":"London"},{"name":"California"}]
channel.basic_publish(exchange="",routing_key="mobigo123",body=json.dumps(citynames))
print("[x] sent 'Hello srujan'")
connection.close()