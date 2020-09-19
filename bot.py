import datetime
import logging
import random
from operator import itemgetter

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

API_TOKEN = '1062436833:AAEPyzbWzZh7-WTQLP6QRhezM-WXd0DpmQA'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# инициализация соединения с бд
db = SQLighter('db.db')


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    db.creator(str(message.chat.id), message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    if not db.subscriber_exists(message.from_user.id, message.chat.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id, message.chat.id, message.from_user.first_name)
    else:
        # если он уже есть оновляем статус подписки
        db.update_subscription(message.from_user.id, message.chat.id, message.from_user.first_name, True)

    await message.answer('Вы успешно подписались!')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    db.creator(str(message.chat.id), message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    if not db.subscriber_exists(message.from_user.id, message.chat.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской
        db.add_subscriber(message.from_user.id, message.chat.id, message.from_user.first_name, False)
        await message.answer('Вы и так не подписаны')
    else:
        # если он уже есть оновляем статус подписки
        db.update_subscription(message.from_user.id, message.chat.id, message.from_user.first_name, False)
        await message.answer('Поздравляю, Вы крыса')


@dp.message_handler(commands=['rat'])
async def rat(message: types.Message):
    db.creator(str(message.chat.id), message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    if db.check_time(str(message.chat.id), str(datetime.date.today())):
        quantity = db.get_subscriptions(message.chat.id)
        print(message.chat.id)
        print(quantity)
        winner = random.randint(0, len(quantity)-1)
        await message.answer('У нас честные выборы!')
        await message.answer('Крыса дня - ' + quantity[winner][0])
        db.choose_rat(message.chat.id, quantity[winner][1])
    else:
        await message.answer('Не торопись, крыса')


@dp.message_handler(commands=['stat'])
async def stat(message: types.Message):
    db.creator(str(message.chat.id), message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    subs = sorted(db.get_subscriptions(message.chat.id), key=itemgetter(2), reverse=True)
    stat2 = ''
    for i in subs:
        stat2 += str(i[0]) + ' - ' + str(i[2]) + '\n'

    await message.answer(stat2)


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('img/14.png', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
