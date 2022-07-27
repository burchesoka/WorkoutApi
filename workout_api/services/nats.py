import json
import logging

import nats


logger = logging.getLogger(__name__)


async def send_message_to_bot(subject: str, recipient_telegram_id: int, message: str, **kwargs):
    nc = await nats.connect("127.0.0.1:4222")

    data = {
        'message': message,
        'recipient_telegram_id': recipient_telegram_id,
    }

    for key, value in kwargs.items():
        data[key] = value

    logger.debug(f'Send message: {data} to {subject}')
    data = json.dumps(data)

    await nc.publish(subject, data.encode())
