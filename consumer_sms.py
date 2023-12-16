import pika
from models import Contact
from db_connect import connect


def callback_sms(ch, method, properties, body):
    contact_id = body.decode('utf-8')

    try:
        contact = Contact.objects.get(id=contact_id)

        print(f" [x] Sending SMS to {contact.full_name} at {contact.phone_number}")

        contact.sent_sms = True
        contact.save()
    except Contact.DoesNotExist:
        print(f" [x] Contact with id={contact_id} does not exist.")


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='sms_queue')

channel.basic_consume(queue='sms_queue', on_message_callback=callback_sms, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
