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
    ContextTypes,
    filters
)


from database import *



TOKEN = os.getenv("BOT_TOKEN")



menu = InlineKeyboardMarkup([

[
InlineKeyboardButton(
"🔍 Cari Match",
callback_data="search"
)
],

[
InlineKeyboardButton(
"🌍 Negara",
callback_data="country"
)
],

[
InlineKeyboardButton(
"❌ End Chat",
callback_data="end"
)
]

])



countries = InlineKeyboardMarkup([

[
InlineKeyboardButton(
"🇮🇩 Indonesia",
callback_data="Indonesia"
)
],

[
InlineKeyboardButton(
"🇲🇾 Malaysia",
callback_data="Malaysia"
)
],

[
InlineKeyboardButton(
"🇸🇬 Singapore",
callback_data="Singapore"
)
],

[
InlineKeyboardButton(
"🇹🇭 Thailand",
callback_data="Thailand"
)
],

[
InlineKeyboardButton(
"🇰🇭 Cambodia",
callback_data="Cambodia"
)
]

])



async def start(update,context):

    user = update.effective_user


    add_user(user.id)


    await update.message.reply_text(

f"""
👋 Halo {user.first_name}

💙 ANONYMOUS MATCH

Cari teman baru secara anonim.

Command:

/next - cari teman
/end - akhiri chat

Silahkan pilih menu:
""",

reply_markup=menu

)



async def search_match(update,context):

    user = update.effective_user.id


    set_search(
        user,
        1
    )


    partner = find_match(
        user
    )



    if partner:


        set_search(user,0)
        set_search(partner,0)


        set_partner(user,partner)
        set_partner(partner,user)



        await update.message.reply_text(

"""
🎉 MATCH DITEMUKAN!

Kamu sudah terhubung.

Mulai chat sekarang.
"""
)


        await context.bot.send_message(

            partner,

"""
🎉 MATCH DITEMUKAN!

Kamu sudah terhubung.

Mulai chat sekarang.
"""
)


    else:


        await update.message.reply_text(

"""
🔎 Sedang mencari teman...

Tunggu pengguna lain.
"""
)





async def next_match(update,context):


    user = update.effective_user.id


    old = get_partner(user)



    if old:


        remove_partner(user)
        remove_partner(old)



        await context.bot.send_message(
            old,
"""
🔄 Teman kamu mencari pasangan baru.
"""
        )



    await search_match(update,context)





async def end_chat(update,context):


    user = update.effective_user.id


    partner = get_partner(user)



    if partner:


        remove_partner(user)
        remove_partner(partner)



        await context.bot.send_message(

            partner,

"""
❌ Chat sudah diakhiri.
Gunakan /next untuk mencari teman baru.
"""

        )


        await update.message.reply_text(

"""
❌ Chat selesai.
Gunakan /next untuk mencari teman baru.
"""

        )


    else:


        await update.message.reply_text(

"""
Tidak ada chat aktif.
"""

        )





async def button(update,context):


    q = update.callback_query

    await q.answer()


    user = q.from_user.id



    if q.data=="search":

        await search_match(
            update,
            context
        )



    elif q.data=="country":


        await q.message.reply_text(

            "Pilih negara:",

            reply_markup=countries

        )




    elif q.data in [

        "Indonesia",
        "Malaysia",
        "Singapore",
        "Thailand",
        "Cambodia"

    ]:


        save_country(
            user,
            q.data
        )


        await q.message.reply_text(

f"""
✅ Negara dipilih:

🌍 {q.data}
""",

reply_markup=menu

)




    elif q.data=="end":


        await end_chat(
            update,
           context
        )





async def relay(update,context):


    user = update.effective_user.id


    partner = get_partner(
        user
    )



    if partner:


        await context.bot.send_message(

            partner,

            update.message.text

        )


    else:


        await update.message.reply_text(

"""
Kamu belum mempunyai pasangan.

Gunakan /next.
"""

        )





def main():


    init_db()


    app = Application.builder().token(TOKEN).build()



    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "next",
            next_match
        )
    )


    app.add_handler(
        CommandHandler(
            "end",
            end_chat
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            relay
        )
    )



    print(
        "BOT ONLINE"
    )


    app.run_polling()



if __name__=="__main__":

    main()
