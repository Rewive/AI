import re
from asyncio import sleep
from os import mkdir, remove
from random import choice, randint

from aiofiles import open
from markovify import NewlineText
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.bot import ChatActionRule, FromUserRule

bot = Bot ('bd8d08c46198ec18b48d753f955f2eb9e146a833c5e99dd2ea76ccb708b39f9930b80dc4d2231764b1d81')


@bot.on.chat_message(ChatActionRule("chat_invite_user"))
async def invited(message: Message) -> None:
    """Приветствие при приглашении бота в беседу."""
    if message.group_id == -message.action.member_id:
        await message.answer(
            """Всем привет!
Для работы мне нужно выдать доступ к переписке или права администратора."""
        )


@bot.on.chat_message(FromUserRule())
async def talk(message: Message) -> None:
    peer_id = message.peer_id
    text = message.text.lower()

    if text:
        
        while "\n\n" in text:
            text = text.replace("\n\n", "\n")

       
        user_ids = tuple(set(pattern.findall(text)))
        for user_id in user_ids:
            text = re.sub(rf"\[id{user_id}\|.*?]", f"@id{user_id}", text)

        
        try:
            mkdir("db")
        except FileExistsError:
            pass

       
        async with open(f"db/base.txt", "a") as f:
            await f.write(f"\n{text}")
            corpus = text.split()


    if randint(1, 100) > 100:
        return


    async with open(f"db/base.txt") as f:
        db = await f.read()
    db = db.strip().lower()


    await sleep(0)


    text_model = NewlineText(input_text=db, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=1000) or choice(db.splitlines())

    await message.answer(sentence)

@bot.on.message(FromUserRule())
async def talk(message: Message) -> None:
    peer_id = message.peer_id
    text = message.text.lower()

    if text:
        
        while "\n\n" in text:
            text = text.replace("\n\n", "\n")

       
        user_ids = tuple(set(pattern.findall(text)))
        for user_id in user_ids:
            text = re.sub(rf"\[id{user_id}\|.*?]", f"@id{user_id}", text)

        
        try:
            mkdir("db")
        except FileExistsError:
            pass

       
        async with open(f"db/base.txt", "a") as f:
            await f.write(f"\n{text}")
            corpus = text.split()


    if randint(1, 100) > 100:
        return


    async with open(f"db/base.txt") as f:
        db = await f.read()
    db = db.strip().lower()


    await sleep(0)


    text_model = NewlineText(input_text=db, well_formed=False, state_size=1)
    sentence = text_model.make_sentence(tries=1000) or choice(db.splitlines())

    await message.answer(sentence)


if __name__ == "__main__":
    pattern = re.compile(r"\[id(\d*?)\|.*?]")
    bot.run_forever()
