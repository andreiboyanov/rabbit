import sys
import argparse
from rabbit_conenction import Connection


def send_to_queue(queue, message):
    with Connection() as connection:
        connection.channel.queue_declare(queue)
        connection.channel.basic_publish(exchange="", routing_key=queue, body=message)


def send_to_fan(message, exchange="fan"):
    with Connection() as connection:
        connection.channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        connection.channel.basic_publish(exchange=exchange, routing_key='', body=message)


def main(command_line_arguments):
    parser = argparse.ArgumentParser("Send messages to defined route in RabbitMQ")
    parser.add_argument("message", help="Message to send")
    parser.add_argument(
        "--queue", "-q", default=None, help="Send the message to this queue"
    )
    parser.add_argument(
        "--route", "-r", default=None, help="Send the message to this route"
    )

    parser.add_argument(
        "--all", "-a", action="store_true", help="Send the message messages to all queues"
    )
    arguments = parser.parse_args(command_line_arguments)
    if arguments.queue is not None:
        send_to_queue(arguments.queue, arguments.message)
    if arguments.all:
        send_to_fan(arguments.message)


if __name__ == "__main__":
    main(sys.argv[1:])
