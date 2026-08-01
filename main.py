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
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from database import *


TOKEN=os.getenv("BOT_TOKEN")


NAME,AGE,GENDER,BIO=range(4)


keyboard=[
[
InlineKeyboardButton("🔍 Cari Match",callback_data="search"),
InlineKeyboardButton("👤 Profil",callback_data="profile")
],
[
InlineKeyboardButton("✏️ Edit Profil",callback_data="edit"),
InlineKeyboardButton("❌ Stop",callback_data="stop")
]
]


menu=InlineKeyboardMarkup(keyboard)



async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user=update.effective_user

    add_user(user.id)

    await update.message.reply_text(
f"""
👋 Halo {user.first_name}

Selamat datang di
💙 Indo Anonymous Match

Temukan teman baru secara anonim.

Klik tombol di bawah untuk mulai.
""",
reply_markup=menu
)



async def profile(update,context):

    user=update.effective_user

    data=get_profile(user.id)

    if not data:
        return

    await update.message.reply_text(
f"""
👤 PROFIL KAMU

Nama : {data[1]}
Umur : {data[2]}
Gender : {data[3]}

Bio:
{data[4]}
"""
)



async def button(update,context):

    q=update.callback_query
    await q.answer()

    uid=q.from_user.id


    if q.data=="profile":

        data=get_profile(uid)

        if data and data[1]:

            await q.message.reply_text(
f"""
👤 Profil

Nama: {data[1]}
Umur: {data[2]}
Gender: {data[3]}

Bio:
{data[4]}
"""
)

        else:

            await q.message.reply_text(
                "Kamu belum membuat profil."
            )



    elif q.data=="search":

        set_search(uid,1)

        match=find_match(uid)


        if match:

            set_search(uid,0)
            set_search(match,0)


            await q.message.reply_text(
"""
🎉 MATCH DITEMUKAN!

Kamu sudah mendapatkan teman baru.

Silahkan mulai ngobrol 😊
"""
)

            await context.bot.send_message(
                match,
"""
🎉 MATCH DITEMUKAN!

Ada seseorang yang ingin ngobrol dengan kamu 😊
"""
)

        else:

            await q.message.reply_text(
"""
🔎 Sedang mencari...

Tunggu pengguna lain bergabung.
"""
)


    elif q.data=="stop":

        set_search(uid,0)

        await q.message.reply_text(
            "❌ Pencarian dihentikan."
        )



async def create_profile(update,context):

    await update.message.reply_text(
        "Masukkan nama kamu:"
    )

    return NAME



async def name(update,context):

    context.user_data["name"]=update.message.text

    await update.message.reply_text(
        "Masukkan umur:"
    )

    return AGE



async def age(update,context):

    context.user_data["age"]=update.message.text

    await update.message.reply_text(
        "Masukkan gender:"
    )

    return GENDER



async def gender(update,context):

    context.user_data["gender"]=update.message.text

    await update.message.reply_text(
        "Tulis bio singkat:"
    )

    return BIO



async def bio(update,context):

    uid=update.effective_user.id

    save_profile(
        uid,
        context.user_data["name"],
        context.user_data["age"],
        context.user_data["gender"],
        update.message.text
    )


    await update.message.reply_text(
"""
✅ Profil berhasil dibuat!

Sekarang kamu bisa mencari teman.
""",
reply_markup=menu
)

    return ConversationHandler.END



def main():

    init_db()

    app=Application.builder().token(TOKEN).build()


    conv=ConversationHandler(
        entry_points=[
            CommandHandler("profile",create_profile)
        ],
        states={
            NAME:[MessageHandler(filters.TEXT,name)],
            AGE:[MessageHandler(filters.TEXT,age)],
            GENDER:[MessageHandler(filters.TEXT,gender)],
            BIO:[MessageHandler(filters.TEXT,bio)]
        },
        fallbacks=[]
    )


    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("profile",profile))

    app.add_handler(conv)

    app.add_handler(
        CallbackQueryHandler(button)
    )


    print("BOT ONLINE")

    app.run_polling()



if __name__=="__main__":
    main()
