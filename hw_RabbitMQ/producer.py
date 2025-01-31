import pika
import random
from models import Contact
from faker import Faker

fake = Faker()


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="email_queue", durable=True)
    channel.queue_declare(queue="sms_queue", durable=True)

    methods = ["sms", "email"]

    for _ in range(5):
        best_delivery_method = random.choice(
            methods
        )

        c = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone=str(fake.phone_number()),
            best_delivery_method=best_delivery_method,
        ).save()

        message = str(c.id)

        if c.best_delivery_method == "sms":
            queue_name = "sms_queue"
        else:
            queue_name = "email_queue"

        channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f"Sent contact_id={message} to {queue_name}")

    connection.close()

if __name__ == "__main__":
    main()
