from mongoengine import (
    connect,
    Document,
    StringField,
    EmailField,
    BooleanField,
)

connect(
    db="hw08", host="mongodb+srv://Python_Mongo:1234567890@cluster0.qs4wa.mongodb.net/"
)

class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    is_sent = BooleanField(default=False)
    phone = StringField()
    best_delivery_method = StringField(choices=("sms", "email"), default="email")

    meta = {"collection": "contacts"}
