from pyrogram import Client, filters
import yt_dlp
import os

# YEH CHEEZEIN CHANGE KARO
API_ID = 37068941      
API_HASH = '94a6f82cec3ed9775985c4d46bbc44fc'
BOT_TOKEN = '8996732242:AAEdv1JzTZMNZwj4BpFpzpggpolMNHdopmY'

app = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎵 **Music Bot Active!**\n\n/play <song name> - Gaana bajao\n/download <song name> - Gaana download karo")

@app.on_message(filters.command("play"))
async def play(client, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("Example: /play Dilbar Dilbar")
        return
    
    msg = await message.reply("🔍 Searching...")
    
    ydl = yt_dlp.YoutubeDL({'quiet': True})
    info = ydl.extract_info(f"ytsearch1:{query}", download=False)
    song = info['entries'][0]
    
    await msg.edit(f"🎵 **{song['title']}**\n⏳ Downloading...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://youtube.com/watch?v={song['id']}"])
        
    file_path = f"downloads/{song['title']}.mp3"
    await message.reply_audio(file_path, title=song['title'], performer="Music Bot")
    os.remove(file_path)
    await msg.delete()

@app.on_message(filters.command("download"))
async def download(client, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("Example: /download Dilbar")
        return
    
    msg = await message.reply("⏳ Downloading...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        title = info['entries'][0]['title']
        file_path = f"downloads/{title}.mp3"
        await message.reply_document(file_path)
        os.remove(file_path)
        await msg.delete()

print("✅ Bot Start Ho Gaya!")
app.run()