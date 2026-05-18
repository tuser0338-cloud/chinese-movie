import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ပြင်ဆင်ရမည့်နေရာများ (မိမိအချက်အလက်များ ထည့်ပါ)
API_ID = 31610101          # မိမိရဲ့ API ID (နံပါတ်) ပြောင်းရန်
API_HASH = "598cd50daf45b4611208cc7e213bad4d" # မိမိရဲ့ API Hash ပြောင်းရန်
BOT_TOKEN = "8995248582:AAFmiHGg9AuBOs_qBjM2YenHPQrvTHCpYwU" # မိမိရဲ့ Bot Token ပြောင်းရန်

# Bot ကို စတင်ချိတ်ဆက်ခြင်း
app = Client("movie_delete_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Movie Database အကြမ်း (နမူနာအနေနဲ့ File ID သို့မဟုတ် Link တွေ သိမ်းတဲ့နေရာ)
# တကယ့် ဗီဒီယိုဖိုင်တွေကို Channel ထဲတင်ပြီး ရလာတဲ့ File ID သုံးရင် ပိုကောင်းပါတယ်
MOVIE_DATA = {
    "avengers": {
        "title": "Avengers: Endgame",
        "poster": "https://t.me/c/3649958597/2",
        "review": "ဒီဇာတ်ကားကတော့ Marvel ရဲ့ အကောင်းဆုံးဇာတ်ကားကြီး ဖြစ်ပါတယ်...",
        "video_id": "https://t.me/c/3649958597/3" # ဗီဒီယို Link သို့မဟုတ် Telegram File ID
    }
}

# User က /start လို့ ရိုက်ရင် ရုပ်ရှင် Poster နဲ့ Button ပြပေးမည့်အပိုင်း
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    movie = MOVIE_DATA["avengers"]
    
    # Inline Buttons များ ဆောက်ခြင်း
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 ဇာတ်ကားကြည့်ရန်", callback_data="watch_avengers"),
            InlineKeyboardButton("📖 ဇာတ်ကားအညွှန်း", callback_data="review_avengers")
        ]
    ])
    
    await message.reply_photo(
        photo=movie["poster"],
        caption=f"🍿 **{movie['title']}**\n\nကြည့်ရှုလိုပါက အောက်က Button ကို နှိပ်ပါ၊",
        reply_markup=buttons
    )

# Button တွေကို နှိပ်ရင် အလုပ်လုပ်မည့်အပိုင်း
@app.on_callback_query()
async def handle_buttons(client, callback_query):
    data = callback_query.data
    
    # အညွှန်းဖတ်ရန် နှိပ်ခဲ့လျှင်
    if data == "review_avengers":
        await callback_query.answer(MOVIE_DATA["avengers"]["review"], show_alert=True)
        
    # ဇာတ်ကားကြည့်ရန် နှိပ်ခဲ့လျှင်
    elif data == "watch_avengers":
        # ခလုတ်နှိပ်တာ လက်ခံရရှိကြောင်း အကြောင်းပြန်ခြင်း
        await callback_query.answer("ခဏစောင့်ပါ... ဗီဒီယို ပို့ပေးနေပါပြီ။")
        
        # ဗီဒီယိုကို ပို့ပေးခြင်း (ဒီနေရာမှာ ကိုယ့် Channel ထဲက File ID ကို သုံးရင် အကောင်းဆုံး)
        movie_msg = await callback_query.message.reply_video(
            video=MOVIE_DATA["avengers"]["video_id"],
            caption="⚠️ **သတိပေးချက်**\n\nဒီဗီဒီယိုဟာ မူပိုင်ခွင့်ကြောင့် ၅ မိနစ်အတွင်း အလိုအလျောက် ပျက်သွားပါလိမ့်မယ်။ မိမိရဲ့ **Saved Messages** ထဲကို အမြန် Forward လုပ်ပြီး သိမ်းဆည်းထားပါ။"
        )
        
        # မိနစ် ၅ မိနစ် (စက္ကန့် ၃၀၀) စောင့်ဆိုင်းခြင်း
        await asyncio.sleep(300)
        
        # ဗီဒီယိုကို Auto-Delete ပြန်လုပ်ခြင်း
        try:
            await movie_msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

# Bot ကို Run ခြင်း
print("Bot စတင် အလုပ်လုပ်နေပါပြီ...")
app.run()