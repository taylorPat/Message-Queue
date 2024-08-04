import sys, os
from connect import connectToMQ

def main():
    connection = connectToMQ()
    channel = connection.channel()

    # QUEUE is created before in UI
    # result = channel.queue_declare(
    #     queue="",
    #     exclusive=True    
    # )

    # queueName = result.method.queue

    # channel.queue_bind(
    #     exchange="test",
    #     queue="test-queue",
    #     routing_key="error"   
    # )

    def callback(ch, method, properties, body):
        print(f"{method.routing_key}: {body.decode()}")
        
    channel.basic_consume(
        queue="test-queue", 
        on_message_callback=callback, 
        auto_ack=True)

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