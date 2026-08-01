import os


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
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



country_menu = InlineKeyboardMarkup([

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
💙 INDOANONYM BOT

Halo {user.first_name} 👋

Temukan teman baru secara anonymous.

Command:

/next - Cari teman baru
/end - Akhiri chat


Gunakan menu dibawah:
""",

reply_markup=menu

)



async def search_match(update,context):


    if update.callback_query:

        user = update.callback_query.from_user.id

        reply = update.callback_query.message.reply_text


    else:

        user = update.effective_user.id

        reply = update.message.reply_text



    set_search(
        user,
        1
    )


    partner = find_match(user)



    if partner:


        set_search(user,0)

        set_search(partner,0)


        set_partner(user,partner)

        set_partner(partner,user)



        await reply(

"""
🎉 MATCH DITEMUKAN!

Kamu sudah terhubung.

Silahkan mulai chat 💬
"""

        )


        await context.bot.send_message(

            partner,

"""
🎉 MATCH DITEMUKAN!

Kamu sudah terhubung.

Silahkan mulai chat 💬
"""

        )



    else:


        await reply(

"""
🔎 Sedang mencari teman...

Tunggu pengguna lain.
"""

        )





async def next_match(update,context):


    user = update.effective_user.id


    partner=get_partner(user)



    if partner:

        remove_partner(user)

        remove_partner(partner)



    await search_match(
        update,
        context
    )





async def end_chat(update,context):


    user=update.effective_user.id


    partner=get_partner(user)



    if partner:


        remove_partner(user)

        remove_partner(partner)



        await context.bot.send_message(

            partner,

"""
❌ Chat telah berakhir.

Gunakan /next untuk mencari teman baru.
"""

        )



        await update.message.reply_text(

"""
❌ Chat selesai.
"""

        )


    else:


        await update.message.reply_text(

"""
Tidak ada chat aktif.
"""

        )





async def button(update,context):


    q=update.callback_query

    await q.answer()


    user=q.from_user.id



    if q.data=="search":

        await search_match(
            update,
            context
        )



    elif q.data=="country":


        await q.message.reply_text(

            "🌍 Pilih negara kamu:",

            reply_markup=country_menu

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
✅ Negara berhasil dipilih

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


    user=update.effective_user.id


    partner=get_partner(user)



    if partner:


        await context.bot.send_message(

            partner,

            update.message.text

        )


    else:


        await update.message.reply_text(

"""
Kamu belum memiliki pasangan.

Klik 🔍 Cari Match atau /next
"""

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
        "💙 INDOANONYM BOT ONLINE"
    )


    app.run_polling()




if __name__=="__main__":

    main()
