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



TOKEN=os.getenv(
    "BOT_TOKEN"
)



menu=InlineKeyboardMarkup([

[
InlineKeyboardButton(
"🔍 Cari Match",
callback_data="search"
)
],

[
InlineKeyboardButton(
"🌍 Pilih Negara",
callback_data="country"
)
],

[
InlineKeyboardButton(
"❌ Stop Chat",
callback_data="stop"
)
]

])



country_menu=InlineKeyboardMarkup([

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


    user=update.effective_user


    add_user(user.id)


    await update.message.reply_text(

f"""
👋 Halo {user.first_name}

💙 Welcome To Anonymous Match

Cari teman baru secara anonim.

Gunakan tombol dibawah.
""",

reply_markup=menu

)




async def button(update,context):


    query=update.callback_query

    await query.answer()


    user=query.from_user.id



    if query.data=="country":


        await query.message.reply_text(

            "Pilih negara kamu:",

            reply_markup=country_menu

        )




    elif query.data in [

        "Indonesia",
        "Malaysia",
        "Singapore",
        "Thailand",
        "Cambodia"

    ]:


        save_country(
            user,
            query.data
        )


        await query.message.reply_text(

f"""
✅ Negara dipilih:

🌍 {query.data}

Sekarang klik 🔍 Cari Match
""",

reply_markup=menu

)





    elif query.data=="search":


        set_search(
            user,
            1
        )


        partner=find_match(
            user
        )



        if partner:


            set_search(
                user,
                0
            )


            set_search(
                partner,
                0
            )


            set_partner(
                user,
                partner
            )


            set_partner(
                partner,
                user
            )


            await query.message.reply_text(

"""
🎉 MATCH BERHASIL!

Kamu sudah terhubung.

Silahkan mulai chat.
""",

reply_markup=menu

)



            await context.bot.send_message(

                partner,

"""
🎉 MATCH BERHASIL!

Kamu sudah terhubung.

Silahkan mulai chat.
"""

)


        else:


            await query.message.reply_text(

"""
🔎 Mencari teman...

Tunggu pengguna lain.
""",

reply_markup=menu

)




    elif query.data=="stop":


        partner=get_partner(user)



        remove_partner(user)



        if partner:


            remove_partner(partner)


            await context.bot.send_message(

                partner,

"""
❌ Teman mengakhiri chat.

Klik 🔍 Cari Match untuk mencari teman baru.
"""

)


        await query.message.reply_text(

"""
❌ Chat dihentikan.
""",

reply_markup=menu

)




async def relay(update,context):


    user=update.effective_user.id


    partner=get_partner(
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
Kamu belum memiliki pasangan.

Klik 🔍 Cari Match.
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
