import pika 

def connectToMQ():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost',
            port='8090',
            credentials=pika.PlainCredentials(
                username="user", password="password"
            )
            )
        )
    except Exception as e:
        raise Exception from e 
    else:
        print("Connecting to mq succesfully")
        return connection