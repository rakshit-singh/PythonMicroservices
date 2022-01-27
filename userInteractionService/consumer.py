"""
This is the rabbitmq consumer file. 
To find out more about the methods that are run on retrieveing a message from a rabbitmq queue,
look at DBCleanup.py
"""

import pika, json, os, django, requests

# Intialising django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userInteractionService.settings')
django.setup()



from userInteraction.DBCleanup import createUser, deleteContent, deleteUser
from userInteraction.models import User

print("starting consumer")
url_params = pika.URLParameters('amqps://kszbkeyl:1ZbcKiv4yxsrJKT97IToSpGqXK2VPEcD@puffin.rmq2.cloudamqp.com/kszbkeyl')

conn = pika.BlockingConnection(url_params)

channel = conn.channel()

channel.queue_declare(queue='user')
channel.queue_declare(queue='content')

def userCallback(ch, method, properties, body):
    user_id = json.loads(body)
    print("recieved", properties.content_type, json.loads(body), "in user consumer")
    if properties.content_type == 'create_user':
        s = 'http://docker.for.mac.localhost:9000/api/user/{val}'.format(val = json.loads(body))
        print("string is", s)
        request = requests.post(url='http://docker.for.mac.localhost:9000/api/user', data={'user_id':json.loads(body)})
        print(request.status_code)  
    else:
        request = requests.delete(url='http://docker.for.mac.localhost:9000/api/user/{val}'.format(val = json.loads(body)))
        print(request.status_code)   
        
    
    

def contentCallback(ch, method, properties, body):
    title = json.loads(body)
    print("recieved", properties.content_type, json.loads(body), "in content consumer")
    if properties.content_type == 'delete_content':
        request = requests.delete(url='http://docker.for.mac.localhost:9000/api/content/{val}'.format(val=json.loads(body)))
        print(request.status_code)  

channel.basic_consume(queue='user', on_message_callback=userCallback, auto_ack=True)
channel.basic_consume(queue='content', on_message_callback=contentCallback, auto_ack=True)

print("started consuming")

channel.start_consuming()

channel.close()