import pika

from connect import connectToMQ 

connection = connectToMQ()
channel = connection.channel()

# EXCHANGE is created before in UI
# channel.exchange_declare(
#     exchange="logging",
#     exchange_type="direct"
# )

channel.basic_publish(
    exchange="test",
    routing_key="error",
    body="[ERROR]: this is an error log")