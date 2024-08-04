import time
import sys, os

from connect import connectToMQ

def main():
    connection = connectToMQ()
    channel = connection.channel()
    
    # [1] Define the exchange
    EXCHANGE_NAME = "test_exchange"
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="fanout"    
    )

    # [2] Create queue 
    result = channel.queue_declare(
        queue="", # [3] empty string to randomly generate queue names
        durable=True,
        exclusive=True # [4] delete queue once consumer connection is closed
    )
    queueName = result.method.queue
    
    # [3] Bind queue to exchange
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=queueName    
    )

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(f" [x] Done")
        # [3] Send a proper acknowledgement from the worker / consumer
        # in order to deliver a task to another worker if one
        # worker dies -> if the consumer dies the task is NOT lost
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1) # [4] Rabbitmq does only move
    # one message at a time to the worker / consumer. If the worker is still busy
    # rabbitmq dispatch the message to another worker
    # this helps to divide the messages with different complexity fair
    # between the workers. 
    # DEFAULT BEHAVIOUR: Every n-th messages is dispatched to the n-th consumer.
    channel.basic_consume(
        queue=queueName, # [] 
        on_message_callback=callback,
        #auto_ack=True
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)