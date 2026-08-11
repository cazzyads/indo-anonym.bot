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


# =========================
# MENU UTAMA
# =========================

menu = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🔎 Search",
            callback_data="search"
        ),
        InlineKeyboardButton(
            "⏭ Next",
            callback_data="next"
        )
    ],
    [
        InlineKeyboardButton(
            "❌ End",
            callback_data="end"
        )
    ]
])


# =========================
# START
# =========================

async def start(update, context):

    user = update.effective_user

    add_user(user.id)


    await update.message.reply_text(
f"""
💙 INDOANONYM BOT

Halo {user.first_name} 👋


Kamu cari teman baru yang asik?


Temukan teman ngobrol baru secara anonymous.


Join group & channel public:


👥 Group:
https://t.me/coustry


📢 Channel:
https://t.me/officiallcoustry


Silakan gunakan menu di bawah 👇
""",
        reply_markup=menu
    )



# =========================
# SEARCH
# =========================

async def search_match(update, context):

    if update.callback_query:

        user = update.callback_query.from_user.id
        send = update.callback_query.message.reply_text

    else:

        user = update.effective_user.id
        send = update.message.reply_text



    set_search(user, 1)


    partner = find_match(user)



    if partner:


        set_search(user, 0)
        set_search(partner, 0)


        set_partner(user, partner)
        set_partner(partner, user)



        await send(
"""
🎉 MATCH DITEMUKAN!

Kamu sudah terhubung dengan teman baru.

Silakan mulai chat 💬
""",
            reply_markup=menu
        )



        await context.bot.send_message(
            partner,
"""
🎉 MATCH DITEMUKAN!

Kamu sudah terhubung dengan teman baru.

Silakan mulai chat 💬
""",
            reply_markup=menu
        )


    else:


        await send(
"""
🔎 Sedang mencari teman...

Mohon tunggu pengguna lain bergabung.
""",
            reply_markup=menu
        )



# =========================
# NEXT
# =========================

async def next_match(update, context):

    user = update.effective_user.id


    partner = get_partner(user)



    if partner:


        remove_partner(user)
        remove_partner(partner)



        await context.bot.send_message(
            partner,
"""
⏭ Partner kamu mencari teman baru.

Chat selesai.
""",
            reply_markup=menu
        )



    await search_match(
        update,
        context
    )



# =========================
# END CHAT
# =========================

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

Terima kasih sudah menggunakan IndoAnonym.
""",
            reply_markup=menu
        )



    if update.callback_query:


        await update.callback_query.message.reply_text(
"""
❌ Chat selesai.

Mau mencari teman baru?
""",
            reply_markup=menu
        )


    else:


        await update.message.reply_text(
"""
❌ Chat selesai.

Mau mencari teman baru?
""",
            reply_markup=menu
        )



# =========================
# BUTTON
# =========================

async def button(update, context):

    query = update.callback_query


    await query.answer()



    if query.data == "search":

        await search_match(
            update,
            context
        )


    elif query.data == "next":

        await next_match(
            update,
            context
        )


    elif query.data == "end":

        await end_chat(
            update,
            context
        )



# =========================
# CHAT RELAY
# =========================

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
Kamu belum memiliki partner.

Klik 🔎 Search untuk mencari teman baru.
""",
            reply_markup=menu
        )



# =========================
# MAIN
# =========================

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
