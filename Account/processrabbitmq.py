import json
from Account.rabbitmq import get_rabbitmq_connection
# Suponiendo que tienes un módulo para la validación JWT
from JWTValidator import JWTValidator


def process_jwt_validation_requests():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declara la cola que vas a consumir
    channel.queue_declare(queue='jwt_validation_queue')

    # Define la función callback para procesar los mensajes
    def callback(ch, method, properties, body):
        # Decodifica el mensaje
        message = json.loads(body)

        # Extrae el token del mensaje
        token = message.get('token')

        # Valida el token JWT
        jwt_validator = JWTValidator(secret_key="tu_clave_secreta")
        user_data = jwt_validator.validate_token(token)

        # Aquí podrías realizar más acciones, como almacenar los datos del usuario en una base de datos, etc.

        # Envía una respuesta (aquí puedes definir cómo manejar la respuesta)
        if user_data:
            # Si el token es válido, puedes enviar una respuesta de éxito
            print("El token es válido. Datos del usuario:", user_data)
        else:
            # Si el token no es válido, puedes enviar una respuesta de error
            print("El token no es válido.")

    # Consume mensajes de la cola
    channel.basic_consume(queue='jwt_validation_queue',
                          on_message_callback=callback, auto_ack=True)

    # Inicia el consumo
    print('Esperando solicitudes de validación JWT...')
    channel.start_consuming()


def send_jwt_validation_response(response_data):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Define la cola para las respuestas
    response_queue = 'jwt_validation_response_queue'

    # Declara la cola si aún no existe
    channel.queue_declare(queue=response_queue)

    # Publica la respuesta en la cola de respuestas
    channel.basic_publish(
        exchange='', routing_key=response_queue, body=json.dumps(response_data))

    connection.close()
