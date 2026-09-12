import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
import re

TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "links.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"links": [], "posts": [], "post_count": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

bot_data = {
    "header": "",
    "footer": "",
    "button_text": "Join Channel",
    "button_url": "https://t.me/+bBm7s1JtbcM0NmJl",
    "channels": [],
    "my_channel_link": "https://t.me/+bBm7s1JtbcM0NmJl"
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🤗 Welcome! Main aapka Smart Duplicate & Link Replacer Bot hoon.\n\n"
        "🤖 Mera Kaam (What I Do):\n"
        "• DiskWala aur Terabox links ko automatically filter aur manage karta hoon.\n"
        "• Duplicate links aur posts ko detect karke turant remove karta hoon.\n"
        "• Dusre Telegram links ko automatically aapke channel link se replace karta hoon.\n"
        "• Posts me custom Header, Footer, Post Number aur Buttons jodhkar aapke channels par auto-upload karta hoon.\n\n"
        "👇 Sabhi commands aur unke use dekhne ke liye niche diye gaye command par click karein:\n"
        "/help - All commands and their uses"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "🤖 All Commands & Their Uses:\n\n"
        "/add_header [Text] - Post ke upar lagane ke liye Header set karein\n"
        "/remove_header - Set kiya hua Header hatayein\n"
        "/add_footer [Text] - Post ke niche lagane ke liye Footer set karein\n"
        "/remove_footer - Set kiya hua Footer hatayein\n"
        "/set_button [Name | URL] - Post ke niche interactive Inline Button set karein\n"
        "/remove_button - Set kiya hua Button hatayein\n"
        "/add_channel [numeric id ya username dale] - Auto-forwarding ke liye channel jodein (@username ya -100id)\n"
        "/remove_channel [@channel / ID] - Channel list se hatayein\n"
        "/set_mylink [URL] - Incoming posts me Telegram links replace karne ke liye apna link set karein"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['set_mylink', 'setmylink'])
def set_mylink(message):
    link = message.text.replace('/set_mylink', '').replace('/setmylink', '').strip()
    if link:
        bot_data["my_channel_link"] = link
        bot.reply_to(message, f"✅ Replacement Link set ho gaya:\n{link}")
    else:
        bot.reply_to(message, "⚠️ Sahi format: /set_mylink https://t.me/yourlink")

@bot.message_handler(commands=['add_header', 'addheader'])
def add_header(message):
    text = message.text.replace('/add_header', '').replace('/addheader', '').strip()
    if text:
        bot_data["header"] = text
        bot.reply_to(message, f"✅ Header set:\n\n{text}")
    else:
        bot.reply_to(message, "⚠️ Sahi format: /add_header [Header Text]")

@bot.message_handler(commands=['remove_header', 'removeheader'])
def remove_header(message):
    bot_data["header"] = ""
    bot.reply_to(message, "🗑️ Header hata diya gaya hai!")

@bot.message_handler(commands=['add_footer', 'addfooter'])
def add_footer(message):
    text = message.text.replace('/add_footer', '').replace('/addfooter', '').strip()
    if text:
        bot_data["footer"] = text
        bot.reply_to(message, f"✅ Footer set:\n\n{text}")
    else:
        bot.reply_to(message, "⚠️ Sahi format: /add_footer [Footer Text]")

@bot.message_handler(commands=['remove_footer', 'removefooter'])
def remove_footer(message):
    bot_data["footer"] = ""
    bot.reply_to(message, "🗑️ Footer hata diya gaya hai!")

@bot.message_handler(commands=['set_button', 'setbutton'])
def set_button(message):
    try:
        parts = message.text.replace('/set_button', '').replace('/setbutton', '').split('|')
        if len(parts) == 2:
            bot_data["button_text"] = parts[0].strip()
            bot_data["button_url"] = parts[1].strip()
            bot.reply_to(message, f"✅ Button updated!\nText: {bot_data['button_text']}\nURL: {bot_data['button_url']}")
        else:
            bot.reply_to(message, "⚠️ Sahi format: /set_button Name | https://link.com")
    except Exception:
        bot.reply_to(message, "⚠️ Error in format.")

@bot.message_handler(commands=['remove_button', 'removebutton'])
def remove_button(message):
    bot_data["button_text"] = ""
    bot_data["button_url"] = ""
    bot.reply_to(message, "🗑️ Button hata diya gaya hai!")

@bot.message_handler(commands=['add_channel', 'addchannel'])
def add_channel(message):
    channel = message.text.replace('/add_channel', '').replace('/addchannel', '').strip()
    if channel.startswith('@') or channel.startswith('-'):
        try:
            if channel.startswith('-'):
                channel = int(channel)
        except ValueError:
            pass
        if channel not in bot_data["channels"]:
            bot_data["channels"].append(channel)
            bot.reply_to(message, f"✅ Channel successfully add ho gaya: {channel}")
        else:
            bot.reply_to(message, "⚠️ Yeh channel pehle se added hai.")
    else:
        error_msg = (
            "⚠️Sahi format!\n\n"
            "Aap numeric ID ya username dono se channel add kar sakte hain.\n"
            "Sahi format:\n"
            "/add_channel [numeric id ya username dale]\n\n"
            "Examples:\n"
            "• /add_channel @yourchannel\n"
            "• /add_channel -100xxxxxxxxxx"
        )
        bot.reply_to(message, error_msg)

@bot.message_handler(commands=['remove_channel', 'removechannel'])
def remove_channel(message):
    channel = message.text.replace('/remove_channel', '').replace('/removechannel', '').strip()
    try:
        if channel.startswith('-'):
            channel = int(channel)
    except ValueError:
        pass
    if channel in bot_data["channels"]:
        bot_data["channels"].remove(channel)
        bot.reply_to(message, f"🗑️ Channel hata diya gaya: {channel}")
    else:
        bot.reply_to(message, "⚠️ Yeh channel list mein nahi mila.")

@bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
def process_post(message):
    if message.text and message.text.startswith('/'):
        return

    original_text = message.text or message.caption or ""
    urls = re.findall(r'(https?://[^\s]+)', original_text)

    db = load_data()
    saved_posts = db.get("posts", [])
    saved_links = db.get("links", [])

    # 1. Exact post content check
    if original_text and original_text in saved_posts:
        try:
            bot.reply_to(message, "🚫 DELETE DUPLICATE LINK AND POST 🚫")
        except Exception:
            pass
        return

    # 2. Individual link duplicate check
    content_links = [u for u in urls if "t.me" not in u.lower() and "telegram.me" not in u.lower()]
    is_link_duplicate = False
    for url in content_links:
        if url in saved_links:
            is_link_duplicate = True
            break

    if is_link_duplicate and content_links:
        try:
            bot.reply_to(message, "🚫 DELETE DUPLICATE LINK AND POST 🚫")
        except Exception:
            pass
        return

    if original_text and original_text not in saved_posts:
        saved_posts.append(original_text)

    link_replaced = False
    processed_text = original_text

    for url in urls:
        if "t.me" in url.lower() or "telegram.me" in url.lower():
            if bot_data["my_channel_link"] not in url:
                processed_text = processed_text.replace(url, bot_data["my_channel_link"])
                link_replaced = True
        else:
            if url not in saved_links:
                saved_links.append(url)

    db["posts"] = saved_posts
    db["links"] = saved_links
    db["post_count"] = db.get("post_count", 0) + 1
    post_number = db["post_count"]
    save_data(db)

    if link_replaced:
        try:
            bot.reply_to(message, "♻️ REPLACE WITH YOUR CHANNEL LINK ♻️")
        except Exception:
            pass

    formatting_prefix = f"📌 Post No: {post_number}\n\n"
    final_message = processed_text

    if bot_data["header"]:
        final_message = f"{bot_data['header']}\n\n{final_message}" if final_message else bot_data['header']

    final_message = f"{formatting_prefix}{final_message}"

    if bot_data["footer"]:
        final_message = f"{final_message}\n\n{bot_data['footer']}"

    markup = InlineKeyboardMarkup()
    if bot_data["button_text"] and bot_data["button_url"]:
        btn = InlineKeyboardButton(bot_data["button_text"], url=bot_data["button_url"])
        markup.add(btn)

    try:
        if message.content_type == 'text':
            if final_message:
                bot.reply_to(message, final_message, reply_markup=markup)
        elif message.content_type == 'photo':
            bot.send_photo(message.chat.id, message.photo[-1].file_id, caption=final_message, reply_markup=markup)
        elif message.content_type == 'video':
            bot.send_video(message.chat.id, message.video.file_id, caption=final_message, reply_markup=markup)
        elif message.content_type == 'document':
            bot.send_document(message.chat.id, message.document.file_id, caption=final_message, reply_markup=markup)
    except Exception:
        pass

    if bot_data["channels"]:
        for ch in bot_data["channels"]:
            try:
                if message.content_type == 'text':
                    if final_message:
                        bot.send_message(ch, final_message, reply_markup=markup)
                elif message.content_type == 'photo':
                    bot.send_photo(ch, message.photo[-1].file_id, caption=final_message[:1024], reply_markup=markup)
                elif message.content_type == 'video':
                    bot.send_video(ch, message.video.file_id, caption=final_message[:1024], reply_markup=markup)
                elif message.content_type == 'document':
                    bot.send_document(ch, message.document.file_id, caption=final_message[:1024], reply_markup=markup)
            except Exception as e:
                print(f"Channel send error to {ch}: {e}")

print("Smart Filter Bot chalu ho gaya hai...")
bot.infinity_polling()
