import sys, pika

from connect import connectToMQ


connection = connectToMQ()
channel = connection.channel()

QUEUE_NAME = "hello"
channel.queue_declare(
    queue=QUEUE_NAME, 
    durable=True # [1] queue wont be lost if rabbitmq node restarts
)

MESSAGE = " ".join(sys.argv[1:]) or "Hello World."

channel.basic_publish(
    exchange='', # the empty string defines the default / nameless exchange
    # and makes it possible to send messages without defining an exchange
    # by matching the routing key to the queue name
    routing_key=QUEUE_NAME,
    body=MESSAGE,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ) # [2] Messages are marked as persisted saves the messages to disk
    # and (properbly) do not get lost when pod restart,
    # (but it is not really guaranteed that the messages are saved,
    # because there is a short time window when message is accepted,
    # but not saved yet)
    # Stronger alternatvie: publisher confirms
)
print(f" [x] Sent message: {MESSAGE}")    
connection.close()