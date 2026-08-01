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


# MENU UTAMA
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


# MENU NEGARA
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



async def start(update, context):

    user = update.effective_user

    add_user(user.id)


    await update.message.reply_text(
f"""
💙 INDOANONYM BOT

Halo {user.first_name} 👋

Temukan teman baru secara anonymous.

Command:

/next → Cari teman baru
/end → Akhiri chat


Silahkan gunakan menu:
""",
        reply_markup=menu
    )



async def search_match(update, context):

    if update.callback_query:

        user = update.callback_query.from_user.id

        send = update.callback_query.message.reply_text

    else:

        user = update.effective_user.id

        send = update.message.reply_text



    set_search(user,1)


    partner = find_match(user)



    if partner:


        set_search(user,0)
        set_search(partner,0)


        set_partner(user,partner)
        set_partner(partner,user)



        await send(
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
""",
            reply_markup=menu
        )


    else:


        await send(
"""
🔎 Sedang mencari teman...

Tunggu pengguna lain bergabung.
""",
            reply_markup=menu
        )



async def next_match(update, context):

    user = update.effective_user.id


    old_partner = get_partner(user)


    if old_partner:

        remove_partner(user)
        remove_partner(old_partner)


        await context.bot.send_message(
            old_partner,
"""
🔄 Teman kamu mencari pasangan baru.

Chat selesai.
""",
            reply_markup=menu
        )


    await search_match(
        update,
        context
    )



async def end_chat(update, context):

    user = update.effective_user.id


    partner = get_partner(user)



    if partner:


        remove_partner(user)
        remove_partner(partner)


        await context.bot.send_message(
            partner,
"""
❌ Chat telah berakhir.

Mau mencari teman baru?
""",
            reply_markup=menu
        )


        await update.message.reply_text(
"""
❌ Chat selesai.

Mau mencari teman baru?
""",
            reply_markup=menu
        )


    else:


        await update.message.reply_text(
"""
Kamu belum memiliki pasangan.

Silahkan cari teman baru.
""",
            reply_markup=menu
        )



async def button(update, context):

    query = update.callback_query

    await query.answer()


    user = query.from_user.id



    if query.data == "search":

        await search_match(
            update,
            context
        )



    elif query.data == "country":


        await query.message.reply_text(
            "🌍 Pilih negara kamu:",
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
✅ Negara tersimpan

🌍 {query.data}
""",
            reply_markup=menu
        )



    elif query.data == "end":

        await end_chat(
            update,
            context
        )



async def relay(update, context):

    user = update.effective_user.id


    partner = get_partner(user)



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
""",
            reply_markup=menu
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
        "💙 INDOANONYM BOT ONLINE"
    )


    app.run_polling()



if __name__ == "__main__":

    main()
