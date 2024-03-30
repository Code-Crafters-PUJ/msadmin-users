import pika
import config.settings as settings

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    return connection


def create_jwt_validation_queue():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue='jwt_validation_queue')
    connection.close()
