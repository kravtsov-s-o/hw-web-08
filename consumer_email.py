import pika
from models import Contact
from db_connect import connect


def callback_email(ch, method, properties, body):
    contact_id = body.decode('utf-8')

    try:
        contact = Contact.objects.get(id=contact_id)

        print(f" [x] Sending email to {contact.full_name} at {contact.email}")

        contact.sent_email = True
        contact.save()
    except Contact.DoesNotExist:
        print(f" [x] Contact with id={contact_id} does not exist.")


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

channel.basic_consume(queue='email_queue', on_message_callback=callback_email, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
