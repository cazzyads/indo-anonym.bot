import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from database import *


TOKEN=os.getenv("BOT_TOKEN")


menu = InlineKeyboardMarkup([
[
InlineKeyboardButton(
"🔍 Cari Match",
callback_data="search"
),

InlineKeyboardButton(
"🌍 Negara",
callback_data="country"
)
],
[
InlineKeyboardButton(
"❌ Stop",
callback_data="stop"
)
]
])


countries = InlineKeyboardMarkup([
[
InlineKeyboardButton(
"🇮🇩 Indonesia",
callback_data="ID"
),
InlineKeyboardButton(
"🇲🇾 Malaysia",
callback_data="MY"
)
],
[
InlineKeyboardButton(
"🇸🇬 Singapore",
callback_data="SG"
),
InlineKeyboardButton(
"🇹🇭 Thailand",
callback_data="TH"
)
],
[
InlineKeyboardButton(
"🇰🇭 Cambodia",
callback_data="KH"
)
]
])



async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user=update.effective_user

    add_user(user.id)


    await update.message.reply_text(
f"""
👋 Halo {user.first_name}

💙 Welcome to Indo Anonymous Match

Temukan teman baru secara anonim.

Gunakan tombol dibawah:
""",
reply_markup=menu
)



async def button(update,context):

    q=update.callback_query

    await q.answer()


    uid=q.from_user.id



    # PILIH NEGARA

    if q.data=="country":

        await q.message.reply_text(
"""
🌍 Pilih negara kamu:
""",
reply_markup=countries
)



    # SIMPAN NEGARA

    elif q.data in [
        "ID",
        "MY",
        "SG",
        "TH",
        "KH"
    ]:


        data={
        "ID":"🇮🇩 Indonesia",
        "MY":"🇲🇾 Malaysia",
        "SG":"🇸🇬 Singapore",
        "TH":"🇹🇭 Thailand",
        "KH":"🇰🇭 Cambodia"
        }


        save_country(
            uid,
            data[q.data]
        )


        await q.message.reply_text(
f"""
✅ Negara tersimpan

{data[q.data]}
""",
reply_markup=menu
)



    # CARI MATCH

    elif q.data=="search":


        set_search(uid,1)


        match=find_match(uid)



        if match:

            set_search(uid,0)

            set_search(match,0)



            await q.message.reply_text(
"""
🎉 MATCH DITEMUKAN

Kamu sudah mendapatkan teman baru.

Silakan mulai ngobrol 😊
"""
)


            await context.bot.send_message(
                match,
"""
🎉 MATCH DITEMUKAN

Ada teman baru yang ingin ngobrol dengan kamu 😊
"""
)


        else:


            await q.message.reply_text(
"""
🔎 Mencari teman...

Tunggu pengguna lain bergabung.
""",
reply_markup=menu
)




    # STOP


    elif q.data=="stop":

        set_search(uid,0)


        await q.message.reply_text(
"""
❌ Pencarian dihentikan.
""",
reply_markup=menu
)



def main():

    init_db()


    app=Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(button)
    )


    print(
        "BOT ONLINE"
    )


    app.run_polling()



if __name__=="__main__":
    main()
