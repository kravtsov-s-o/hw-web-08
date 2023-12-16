from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(nullable=True)
    phone_number = StringField(nullable=True)
    sent_email = BooleanField(default=False)
    sent_sms = BooleanField(default=False)
    preferred_method = StringField(choices=["email", "sms"], default="email")
