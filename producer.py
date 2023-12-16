# producer.py
import pika
from faker import Faker
from models import Contact
from db_connect import connect

fake = Faker('uk_UA')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')


def create_fake_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        has_phone = fake.boolean()  # Randomly decide if the contact has a phone number
        preferred_method = 'sms' if has_phone else 'email'

        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number() if has_phone else None,
            preferred_method=preferred_method,
        )
        contact.save()
        contacts.append((str(contact.id), preferred_method))
    return contacts


contacts_to_send = create_fake_contacts(200)

for contact_id, preferred_method in contacts_to_send:
    queue_name = 'sms_queue' if preferred_method == 'sms' else 'email_queue'
    channel.basic_publish(exchange='', routing_key=queue_name, body=contact_id)

print(f" [x] Sent {len(contacts_to_send)} contacts to the queues")

connection.close()
