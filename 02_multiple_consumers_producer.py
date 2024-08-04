import sys, pika

from connect import connectToMQ


connection = connectToMQ()
channel = connection.channel()

# [1] Define the exchange
EXCHANGE_NAME = "test_exchange"
channel.exchange_declare(
    exchange=EXCHANGE_NAME,
    exchange_type="fanout"    
)


MESSAGE = " ".join(sys.argv[1:]) or "Info: Hello World."

channel.basic_publish(
    exchange=EXCHANGE_NAME, # [2] Set the exchange name
    routing_key="", # [5] empty string because exchange type is 'fanout'
    body=MESSAGE,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ) # [2] Messages are marked as persisted saves the messages to disk
    # (but it is not really guaranteed that the messages are saved,
    # because there is a short time window when message is accepted,
    # but not saved yet)
    # Stronger alternatvie: publisher confirms
)
print(f" [x] Sent message: {MESSAGE}")    
connection.close()