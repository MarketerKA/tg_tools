from pyrogram import Client
from pyrogram.enums.chat_type import ChatType
import config
from pyrogram.raw.types.auth import *

from databases.db_config import User, get_db


def get_user(telegram_id: str):
    db = next(get_db())
    return db.query(User).filter(User.tg_id == telegram_id).first()


def create_user(telegram_id: str):
    db = next(get_db())

    user = User(tg_id=telegram_id, spammed=True)
    db.add(user)
    db.commit()
    db.refresh(user)


async def main():
    try:
        api_id = config.api_id
        api_hash = config.api_hash
        phone_number = config.phone_number

        if config.scheme != 'None':
            proxy = {
                "scheme": config.proxy,
                "hostname": config.hostname,
                "port": int(config.port),
                "username": config.username,
                "password": config.proxy_password
            }

        else:
            proxy = None

        async with Client(f'sessions/{phone_number}', api_id, api_hash, proxy=proxy) as client:

            print("Successfully signed in!")

            dialogs: dict = {}

            async for dialog in client.get_dialogs():
                if dialog.chat.title and dialog.chat.type != ChatType.CHANNEL and dialog.chat.type != ChatType.BOT:
                    dialogs[dialog.chat.title] = dialog.chat.id
            while True:
                for dialog in dialogs.keys():
                    print(dialog + ', ID: ' + str(dialogs[dialog]))

                print("Copy and paste neccessary chat ID. If you want to spam all chats, type 'finish'")

                chat_id = input()

                if chat_id == "finish":
                    print("Finished")
                    break

                text = config.text.replace("\delpop", "\n")
                me = await client.get_me()
                async for member in client.get_chat_members(chat_id):

                    if me.id != member.user.id and get_user(member.user.id) is None:
                        try:
                            await client.send_message(member.user.id, text=text)
                            create_user(member.user.id)
                            await asyncio.sleep(60)

                        except Exception as e:
                            print("Unable to send message to " + member.user.username)
                            print(f'Caused by: {e}')
                            await asyncio.sleep(60)
                print("Spam is done!")

    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
