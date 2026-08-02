import os
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from database import *

TOKEN = os.getenv("BOT_TOKEN")

# =========================
# MENU UTAMA
# =========================
menu = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🔎 Search", callback_data="search"),
        InlineKeyboardButton("⏭ Next", callback_data="next"),
    ],
    [
        InlineKeyboardButton("❌ End", callback_data="end"),
        InlineKeyboardButton("🌍 Atur Region", callback_data="region"),
    ]
])

# =========================
# MENU REGION
# =========================
region_menu = InlineKeyboardMarkup([
    [InlineKeyboardButton("🇮🇩 Sumatra", callback_data="Sumatra")],
    [InlineKeyboardButton("🇮🇩 Jawa", callback_data="Jawa")],
    [InlineKeyboardButton("🇮🇩 Kalimantan", callback_data="Kalimantan")],
    [InlineKeyboardButton("🇮🇩 Bali & Nusa Tenggara", callback_data="Bali & Nusa Tenggara")],
    [InlineKeyboardButton("🇮🇩 Sulawesi", callback_data="Sulawesi")],
    [InlineKeyboardButton("🇮🇩 Maluku & Papua", callback_data="Maluku & Papua")],
])

# =========================
# START
# =========================
async def start(update, context):
    user = update.effective_user
    add_user(user.id)

    await update.message.reply_text(
f"""
💙 **INDOANONYM BOT**

Halo {user.first_name} 👋

**Kamu cari teman baru yang asik?**

Temukan teman ngobrol anonim dari region yang sama dan mulai percakapan tanpa ribet.

**Join group & channel public**

👥 Group:
https://t.me/sirkelindoanonym

📢 Channel:
https://t.me/infomutualan

Silakan gunakan menu di bawah ini.
""",
        reply_markup=menu,
        parse_mode="Markdown"
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

    region = get_region(user)

    if not region:
        await send(
            "🌍 Kamu belum memilih region. Silakan pilih **Atur Region** terlebih dahulu.",
            reply_markup=region_menu,
            parse_mode="Markdown"
        )
        return

    set_search(user, 1)
    partner = find_match(user, region)

    if partner:
        set_search(user, 0)
        set_search(partner, 0)

        set_partner(user, partner)
        set_partner(partner, user)

        await send(
f"""
🎉 **MATCH DITEMUKAN!**

🌍 Region: **{region}**

Kamu sudah terhubung dengan pengguna dari region yang sama.

Silakan mulai chat 💬
""",
            reply_markup=menu,
            parse_mode="Markdown"
        )

        await context.bot.send_message(
            partner,
f"""
🎉 **MATCH DITEMUKAN!**

🌍 Region: **{region}**

Kamu sudah terhubung dengan pengguna dari region yang sama.

Silakan mulai chat 💬
""",
            reply_markup=menu,
            parse_mode="Markdown"
        )
    else:
        await send(
f"""
🔎 **Sedang mencari partner...**

🌍 Region: **{region}**

Mohon tunggu sebentar, kami sedang mencari teman yang cocok untukmu.
""",
            reply_markup=menu,
            parse_mode="Markdown"
        )

# =========================
# NEXT
# =========================
async def next_match(update, context):
    user = update.effective_user.id
    old_partner = get_partner(user)

    if old_partner:
        remove_partner(user)
        remove_partner(old_partner)

        await context.bot.send_message(
            old_partner,
            "⏭ Partner kamu telah mencari teman baru.",
            reply_markup=menu
        )

    await search_match(update, context)

# =========================
# END
# =========================
async def end_chat(update, context):
    user = update.effective_user.id
    partner = get_partner(user)

    if partner:
        remove_partner(user)
        remove_partner(partner)

        await context.bot.send_message(
            partner,
            "❌ Chat telah berakhir.\\n\\nMau mencari teman baru?",
            reply_markup=menu
        )

    if update.callback_query:
        await update.callback_query.message.reply_text(
            "❌ Chat selesai.\\n\\nPilih menu di bawah ini.",
            reply_markup=menu
        )
    else:
        await update.message.reply_text(
            "❌ Chat selesai.\\n\\nPilih menu di bawah ini.",
            reply_markup=menu
        )

# =========================
# BUTTON
# =========================
async def button(update, context):
    query = update.callback_query
    await query.answer()
    user = query.from_user.id

    if query.data == "search":
        await search_match(update, context)

    elif query.data == "next":
        await next_match(update, context)

    elif query.data == "end":
        await end_chat(update, context)

    elif query.data == "region":
        await query.message.reply_text(
            "🌍 **Pilih region kamu**",
            reply_markup=region_menu,
            parse_mode="Markdown"
        )

    elif query.data in [
        "Sumatra",
        "Jawa",
        "Kalimantan",
        "Bali & Nusa Tenggara",
        "Sulawesi",
        "Maluku & Papua"
    ]:
        save_region(user, query.data)

        await query.message.reply_text(
f"""
✅ Region berhasil disimpan

🌍 **{query.data}**

Sekarang kamu akan dipasangkan dengan pengguna dari region yang sama.
""",
            reply_markup=menu,
            parse_mode="Markdown"
        )

# =========================
# RELAY CHAT
# =========================
async def relay(update, context):
    user = update.effective_user.id
    partner = get_partner(user)

    if partner:
        await context.bot.send_message(partner, update.message.text)
    else:
        await update.message.reply_text(
            "Kamu belum memiliki partner.\\n\\nKlik **🔎 Search** untuk mencari teman baru.",
            reply_markup=menu,
            parse_mode="Markdown"
        )

# =========================
# MAIN
# =========================
def main():
    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("next", next_match))
    app.add_handler(CommandHandler("end", end_chat))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))

    print("💙 INDOANONYM BOT ONLINE")
    app.run_polling()

if __name__ == "__main__":
    main()
