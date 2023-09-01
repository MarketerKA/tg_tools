from pyrogram import Client
from pyrogram.enums.chat_type import ChatType
import config
from pyrogram.raw.types.auth import *


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

        async with Client(phone_number, api_id, api_hash, proxy=proxy) as client:

            print("Successfully signed in!")

            dialogs: dict = {}

            async for dialog in client.get_dialogs():
                if dialog.chat.title and dialog.chat.type != ChatType.CHANNEL and dialog.chat.type != ChatType.BOT:
                    dialogs[dialog.chat.title] = dialog.chat.id
            while True:
                for dialog in dialogs.keys():
                    print(dialog + ', ID: ' + str(dialogs[dialog]))

                text = config.text.replace("\delpop", "\n")

                for dialog in dialogs.values():
                    await client.send_message(dialog, text=text)

                print("Spam is done!")

                print('Again? y/n ?')

                answer = input()

                if answer == 'y':
                    continue
                else:
                    break
        print('Finished')
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
