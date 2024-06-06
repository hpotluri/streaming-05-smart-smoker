from collections import deque
import pika
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from util_logger import setup_logger

# Setting up logger
logger, logname = setup_logger(__file__)

# Constants for queues
QUEUE1 = "SmokerTemps"
QUEUE2 = "FoodATemps"
QUEUE3 = "FoodBTemps"

# TODO: Add your own email and password
sender_email = 'hpotluri672@gmail.com'
sender_password = 'zxrv byqm dhpt svst'

# Queues for storing data
smokerQueue = deque(maxlen=5)
foodAQueue = deque(maxlen=20)
foodBQueue = deque(maxlen=20)
currentTimeStamp = 0

# Function to send email alert
def send_email_alert(sender_email, sender_password, recipient_email, subject, message):
    # Set up SMTP server details
    smtp_server = 'smtp.gmail.com'  # Set your SMTP server here
    smtp_port = 587  # Set the appropriate port for your SMTP server
    smtp_username = sender_email

    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, sender_password)

    # Send the email
    server.send_message(msg)

    # Close the connection
    server.quit()

# Callback functions for message processing
def timecallback(ch, method, properties, body):
    global currentTimeStamp 
    currentTimeStamp = body.decode()
    ch.basic_ack(delivery_tag=method.delivery_tag)

def smokercallback(ch, method, properties, body):
    if body.decode() == '':
        return
    currentSmokerTemp = float(body.decode())
    print(f" [x] Received Smoker temp {currentSmokerTemp} at Time {currentTimeStamp}")
    smokerQueue.append(currentSmokerTemp)
    if len(smokerQueue) == smokerQueue.maxlen:
        if smokerQueue[0] - currentSmokerTemp >= 15:
            # Send email alert if smoker temperature has fallen by 15 degrees
            message = f"**************\nSMOKER TEMP ALERT\nTEMP HAS FALLEN 15 DEGREES\n{currentTimeStamp}\nCURRENT TEMP {currentSmokerTemp}\n**************"
            subject = "Smoker Alert"
            logger.info(message)
            send_email_alert(sender_email, sender_password, sender_email, subject, message)
    print(f" [x] Done with Smoker Reading\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def foodAcallback(ch, method, properties, body):
    if body.decode() == '':
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    currentFoodATemp = float(body.decode())
    print(f" [x] Received Food A temp {currentFoodATemp} at Time {currentTimeStamp}")
    foodAQueue.append(currentFoodATemp)
    if len(foodAQueue) == foodAQueue.maxlen:
        if foodAQueue[0] - currentFoodATemp == 1 or foodAQueue[0] - currentFoodATemp == -1:
            # Send email alert if food A temperature has changed by 1 degree
            message = f"**************\nFOOD A TEMP ALERT\nTEMP HAS CHANGED BY 1 DEGREE\n{currentTimeStamp}\nCURRENT TEMP {currentFoodATemp}\n**************"
            subject = "Food A Alert"
            logger.info(message)
            send_email_alert(sender_email, sender_password, sender_email, subject, message)
    print(f" [x] Done with Food A Reading\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def foodBcallback(ch, method, properties, body):
    if body.decode() == '':
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    currentFoodBTemp = float(body.decode())
    print(f" [x] Received Food B temp {currentFoodBTemp} at Time {currentTimeStamp}")
    foodBQueue.append(currentFoodBTemp)
    if len(foodBQueue) == foodAQueue.maxlen:
        if foodBQueue[0] - currentFoodBTemp == 1 or foodBQueue[0] - currentFoodBTemp == -1:
            # Send email alert if food B temperature has changed by 1 degree
            message = f"**************\nFOOD B TEMP ALERT\nTEMP HAS CHANGED BY 1 DEGREE\n{currentTimeStamp}\nCURRENT TEMP {currentFoodBTemp}\n**************"
            subject = "Food B Alert"
            logger.info(message)
            send_email_alert(sender_email, sender_password, sender_email, subject, message)
    print(f" [x] Done with Food B Reading\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Main function to listen for task messages
def main(hn: str = "localhost", qn1: str = "task_queue", qn2: str = "task_queue2", qn3: str = "task_queue3", qn4: str = "task_queue4"):
    try:
        # Establish connection to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))
    except Exception as e:
        print("ERROR: Connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        sys.exit(1)

    try:
        channel = connection.channel()
        # Declare durable queues for message persistence
        channel.queue_declare(queue=qn1, durable=True)
        channel.queue_declare(queue=qn2, durable=True)
        channel.queue_declare(queue=qn3, durable=True)
        channel.queue_declare(queue=qn4, durable=True)
        # Set prefetch count to limit concurrent message processing
        channel.basic_qos(prefetch_count=1)
        # Register callback functions for message consumption
        channel.basic_consume(queue=qn4, on_message_callback=timecallback)
        channel.basic_consume(queue=qn1, on_message_callback=smokercallback)
        channel.basic_consume(queue=qn2, on_message_callback=foodAcallback)
        channel.basic_consume(queue=qn3, on_message_callback=foodBcallback)
        print(" [*] Ready for work. To exit press CTRL+C")
        # Start consuming messages
        channel.start_consuming()
    except Exception as e:
        print("ERROR: Something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()

# Entry point of the program
if __name__ == "__main__":
    main("localhost", "SmokerTemps", "FoodATemps", "FoodBTemps", "TimeStamp")
