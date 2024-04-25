import json
import pika
import threading
import logging.config
import functools

from datetime import datetime
from uuid import UUID, uuid4
from asyncio import ensure_future
from typing import List, Literal, Optional, Tuple, TypedDict

from inspect import currentframe
from classes import Settings, MessageBody

from utils import configure_logging

_set = Settings()
log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())

Role = Literal["system", "user", "assistant"]


def get_amqp_connection():
    log.info(f"Starting: {currentframe().f_code.co_name}")
    credentials = pika.credentials.PlainCredentials(username=_set.qms_user, password=_set.qms_password)
    conn_parameters = pika.ConnectionParameters(host=_set.qms_server, credentials=credentials)
    log.info(f"Ending: {currentframe().f_code.co_name}")
    return pika.BlockingConnection(conn_parameters)


def on_message(_channel, method_frame, header_frame, body, args):
    log.info(f"Starting: {currentframe().f_code.co_name}")
    (_connection, _threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(_connection, _channel, delivery_tag, body))
    t.start()
    _threads.append(t)
    log.info(f"Ending: {currentframe().f_code.co_name}")


def do_work(connection, channel, delivery_tag, body):
    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
    log.info(fmt1.format(thread_id, delivery_tag, body))
    _body = json.loads(body.decode("utf-8"))

    try:
        # TODO: make this message body jwe, got some issues with the key management
        # msg = MessageBody(_body)
        cb = functools.partial(ack_message, channel, delivery_tag)
        connection.add_callback_threadsafe(cb)

    except Exception as e:
        log.error(e.__str__())
        pass


def ack_message(channel, delivery_tag):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass

