import json
import nats


async def send_message_to_bot(user_telegram_id: int, message: str):
    nc = await nats.connect("127.0.0.1:4222")

    data = {
        'message': message,
        'telegram_id': user_telegram_id,
    }
    data = json.dumps(data)

    await nc.publish("users_bot", data.encode())
