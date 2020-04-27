import sys
import argparse
from rabbit_conenction import Connection


def print_message(channel, method, properties, message):
    print(f"Message from the rabbit: {message}")


def receive_from_fan(exchange="fan"):
    with Connection() as connection:
        connection.channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        result = connection.channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        connection.channel.queue_bind(exchange=exchange, queue=queue_name)
        connection.channel.basic_consume(
            queue=queue_name, auto_ack=True, on_message_callback=print_message
        )
        connection.channel.start_consuming()


def receive_from_queue(queue):
    with Connection() as connection:
        connection.channel.queue_declare(queue)
        connection.channel.basic_consume(
            queue=queue, auto_ack=True, on_message_callback=print_message
        )
        connection.channel.start_consuming()


def main(command_line_arguments):
    parser = argparse.ArgumentParser("Receive messages from RabbitMQ")
    parser.add_argument("--queue", "-q", default=None, help="Receive this queue")
    parser.add_argument("--route", "-r", default=None, help="Receive this route")
    parser.add_argument(
        "--fan", "-f", action="store_true", help="Receive from fanout exchange"
    )

    arguments = parser.parse_args(command_line_arguments)
    if arguments.queue is not None:
        receive_from_queue(arguments.queue)
    if arguments.fan:
        receive_from_fan()


if __name__ == "__main__":
    main(sys.argv[1:])
