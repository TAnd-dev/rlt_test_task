import asyncio
import logging
import sys
import json
from json import JSONDecodeError

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from config import settings
from script import get_salaries_by_group

TOKEN = settings.TOKEN
dp = Dispatcher()


@dp.message()
async def get_salaries(message: Message) -> None:
    try:
        data = json.loads(message.text)
        dt_from = data['dt_from']
        dt_upto = data['dt_upto']
        group_type = data['group_type']
        res = await get_salaries_by_group(dt_from, dt_upto, group_type)
        await message.answer(str(res).replace("'", '"'))
    except JSONDecodeError:
        await message.answer('Invalid message. You must provide json data')
    except KeyError:
        await message.answer('Invalid data. Incorrect key or group type')
    except ValueError:
        await message.answer('Invalid data. Invalid date')
    except Exception as e:
        await message.answer('Error')
        print(e)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())