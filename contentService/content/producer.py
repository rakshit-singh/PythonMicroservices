#  amqps://kszbkeyl:1ZbcKiv4yxsrJKT97IToSpGqXK2VPEcD@puffin.rmq2.cloudamqp.com/kszbkeyl

import pika, json

url_params = pika.URLParameters('amqps://kszbkeyl:1ZbcKiv4yxsrJKT97IToSpGqXK2VPEcD@puffin.rmq2.cloudamqp.com/kszbkeyl')

conn = pika.BlockingConnection(url_params)

channel = conn.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    print(json.dumps(body))
    channel.basic_publish(exchange='', routing_key='content', body=json.dumps(body), properties=properties)
