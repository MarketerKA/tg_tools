from pyrogram import Client
from pyrogram.enums.chat_type import ChatType
import config
from pyrogram.raw.types.auth import *

from databases.db_config import UsersBase, get_db


def get_user(telegram_id: str):
    db = next(get_db())

    returned = db.query(UsersBase).filter(UsersBase.tg_id == telegram_id).first()
    db.close()
    return returned


def create_user(telegram_id: str, tg_class : int):
    db = next(get_db())

    user = UsersBase(tg_id=telegram_id, tg_class = tg_class)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()


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

                print("Copy and paste neccessary chat ID. If you want to finish, type 'finish'")

                chat_id = input()

                if chat_id == "finish":
                    print("Finished")
                    break

                import datetime

                today = datetime.datetime.utcnow()

                before = (today - datetime.timedelta(days=30)).timestamp()
                count = 0

                me = await client.get_me()

                async for message in client.get_chat_history(chat_id, offset_id=-1):
                    if message.from_user is not None and message.from_user.id != me.id and not message.from_user.is_bot:
                        if message.date.timestamp() < before:
                            break
                        if not get_user(message.from_user.id):
                            create_user(message.from_user.id, 1)
                            count+=1
                print(f'Added {count} users')



    except Exception as e:
        print(e)
        await asyncio.sleep(30)
        return


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
