from pyrogram import Client
from pyrogram.enums.chat_type import ChatType
import config


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
                "password": config.password
            }
            client = Client(phone_number, api_id, api_hash, proxy=proxy)
        else:
            client = Client(phone_number, api_id, api_hash)

        await client.connect()

        sent_code_info = await client.send_code(phone_number)

        while True:
            try:
                phone_code = input("Please enter your phone code: ")

                await client.sign_in(phone_number, sent_code_info.phone_code_hash, phone_code)

                break

            except Exception as e:
                print(e)

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
                await client.disconnect()
                break

            text = config.text.replace("\delpop", "\n")
            async for member in client.get_chat_members(chat_id):
                try:
                    await client.send_message(member.user.id, text=text)
                    await asyncio.sleep(60)

                except Exception:
                    print("Unable to send message to " + member.user.username)
                    await asyncio.sleep(60)
            print("Spam is done!")

    except Exception as e:
        print(e)
        return


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
