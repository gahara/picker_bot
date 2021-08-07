from pyrogram import Client
import random
import os
import json

token = os.environ['BOT_TOKEN']
api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
bot_username = os.environ['BOT_USER_NAME']

app = Client(
    session_name=':memory:',
    bot_token=token,
    api_id=api_id,
    api_hash=api_hash)

filters = (['/кто?', '/кто', '/who?', '/who'])


def pick(client, message):
    chat = message.get('chat')
    try:
        app.start()
    except BaseException:
        print('Already started')

    users = app.get_chat_members(chat.get('id'))
    app.stop()
    formatted_users = []
    for user in users:
        if not user.user.is_bot:
            formatted_users.append(
                user.user.username if user.user.username else f'[{user.user.first_name}](tg://user?id={user.user.id})')
    return f'@{random.choice(formatted_users)}'


def runner(event, context):
    body = json.loads(event.get('body'))
    message = body.get('message')
    chat = message.get('chat')

    if message.get('text') in filters:
        answer = {
            'method': 'sendMessage',
            'chat_id': chat.get('id'),
            'reply_to_message_id': message.get('message_id'),
            'text': pick('', message)
        }

        res = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(answer)
        }
        return res
    else:
        answer = {
            'method': 'sendMessage',
            'chat_id': chat.get('id'),
            'reply_to_message_id': message.get('message_id'),
            'text': 'Unknown command'
        }
        res = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(answer)
        }
        return res
