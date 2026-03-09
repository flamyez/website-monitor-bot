import asyncio
import database.main as db
import request.main as req
from aiogram import Bot

async def main(bot: Bot, time):
    while True:
        await asyncio.sleep(time)
        for user in db.usr_list():
            print(f"[AUTOCHECK] Checking user {user}.")
            usr_id = user[0]
            send = db.get_send(usr_id)
            if send[0] == 1:
                link = db.get_link(usr_id)
                status = await req.chk_website(link[0])
                usr_status = db.get_status(usr_id)[0]

                if usr_status == 1:
                    usr_status = True
                else:
                    usr_status = False

                if status != usr_status:
                    if not usr_status:
                        await bot.send_message(chat_id=usr_id, text=f"⚠️ Сайт {link[0]} перестал работать!")
                        db.chg_status(usr_id, 0)
                    else:
                        await bot.send_message(chat_id=usr_id, text=f"✅ Сайт {link[0]} снова работает.")
                        db.chg_status(usr_id, 1)