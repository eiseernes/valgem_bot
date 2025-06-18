import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineQuery, InlineQueryResultGame, CallbackQuery

bot = Bot(token=os.getenv("BOT_TOKEN", ""))
dp = Dispatcher()
games_conf = {
    "snake": "https://eiseernes.github.io/games/snake",
}


def get_str_games() -> str:
    return "\n".join(games_conf.keys())


@dp.message(CommandStart())
async def start(msg: Message) -> None:
    await msg.answer(text=(f"Welcome!\nGames: {get_str_games()}"))


@dp.message(Command("games"))
async def games(msg: Message) -> None:
    await msg.answer(text=get_str_games())


@dp.inline_query()
async def inline(q: InlineQuery) -> None:
    await q.answer(
        results=[
            InlineQueryResultGame(id=str(i), game_short_name=g)
            for i, g in enumerate(games_conf.keys())
        ],
        cache_time=900,
    )


@dp.callback_query()
async def game_cb(cb: CallbackQuery) -> None:
    if cb.game_short_name in games_conf:
        await cb.answer(url=games_conf[cb.game_short_name])
    else:
        await cb.answer(text="Error")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s"
    )
    dp.run_polling(bot)
