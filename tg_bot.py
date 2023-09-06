import asyncio
import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from databases.db_config import Worker, get_db, UsersBase

TOKEN = '6351209823:AAHW4R7A5vaSe-AEtL-XVvv5IPNbvCsIVNI'

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


def get_wroker(tg_id: int):
    db = next(get_db())
    returned = db.query(Worker).filter(Worker.tg_id == tg_id).first()

    if returned:
        return returned.time
    else:
        return None


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    worker = get_wroker(message.from_user.id)
    photo_link = 'https://ibb.co/KhV8tr3'
    text = f"ДОРОГО💰💰💰\n" \
           f"- Привет, у тебя было такое, что хочешь чему-то научиться, но КУРС слишком дорогой?😶\n\n" \
           f"- У меня было!\n\n" \
           f"❤️Я нашел <a href='https://t.me/+dUJDdVBF-XQ0M2Uy'>канал</a> где СЛИТЫ " \
           f"все КУРСЫ абсолютно БЕСПЛАТНО, для всех пользователей❤️\n\n" \
           f"Вот парочка курсов, которые мне зашли:\n\n" \
           f"🧷<a href='https://t.me/c/1436052668/48'>Яндекс.Практикум - Python-разработчик Плюс</a>" \
           f" (можно просмотреть после подписки)\n\n" \
           f"🧷<a href='https://t.me/c/1436052668/40'>Алексей Арестович - Искусство общаться</a>" \
           f" (можно просмотреть после подписки)\n\n" \
           f"🧷<a href='https://t.me/c/1436052668/35'>Яндекс Практикум. Графический дизайнер</a>" \
           f" (можно просмотреть после подписки)\n\n" \
           f"❗️<a href='https://t.me/+dUJDdVBF-XQ0M2Uy'>Подписывайся</a>, чтобы не потерять канал, " \
           f"а также чтобы получить доступ к курсам!"
    if not worker:

        await bot.send_photo(message.from_user.id, photo_link, caption=text)
        await bot.send_message(message.from_user.id, "\n".join(get_8_users_from_db()))
        worker = Worker(tg_id=message.from_user.id, time=datetime.datetime.utcnow().timestamp())
        db = next(get_db())
        db.add(worker)
        db.commit()
        db.refresh(worker)
    else:
        now = datetime.datetime.utcnow().timestamp()
        difference = now - worker
        if difference > 86400:
            await bot.send_photo(message.from_user.id, photo_link, caption=text)
            await bot.send_message(message.from_user.id, "\n".join(get_8_users_from_db()))
            worker.time = datetime.datetime.utcnow().timestamp()
            db = next(get_db())
            db.commit()
            db.refresh(worker)
        else:
            await bot.send_message(message.from_user.id,
                                   f"До нового задания осталось: {round((86400 - difference) / (60 * 60), 1)} часов")

def get_8_users_from_db():
    db = next(get_db())
    users = db.query(UsersBase).limit(8).all()
    for user in users:
        db.delete(user)
    db.commit()
    array = []
    for user in users:
        array.append(f"@{user.tg_id}")
    return array
if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
