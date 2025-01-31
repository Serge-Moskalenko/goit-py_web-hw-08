import pika
from models import Contact


def send_email_stub(contact):
    print(f"Sending Email to {contact.email}... Done!")


def send_sms_stub(contact):
    print(f"Sending SMS to {contact.phone}... Done!")


def callback_email(ch, method, properties, body):
   
    contact_id = body.decode()
    print(f"[email_queue] Received contact_id={contact_id}")

    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.is_sent:
        send_email_stub(contact)
        contact.is_sent = True
        contact.save()
    else:
        print("Contact not found or already sent.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback_sms(ch, method, properties, body):
    
    contact_id = body.decode()
    print(f"[sms_queue] Received contact_id={contact_id}")

    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.is_sent:
        send_sms_stub(contact)
        contact.is_sent = True
        contact.save()
    else:
        print("Contact not found or already sent.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

   
    channel.queue_declare(queue="email_queue", durable=True)
    channel.queue_declare(queue="sms_queue", durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="email_queue", on_message_callback=callback_email)
    channel.basic_consume(queue="sms_queue", on_message_callback=callback_sms)

    print("Waiting for messages in 'email_queue' and 'sms_queue'. Press CTRL+C to exit.")
    channel.start_consuming()


if __name__ == "__main__":
    main()

