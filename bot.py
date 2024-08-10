import discord
from discord.ext import commands
import openai
from flask import Flask, request, jsonify
from threading import Thread

app = Flask(__name__)

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot ready")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello there {ctx.author.mention}")


# @bot.command()
# async def chatgpt(ctx, *, prompt: str):
#     async with ctx.typing():
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=150,
#                 n=1,
#                 stop=None,
#                 temperature=0.7,
#             )
#             answer = response.choices[0].message['content']
#             await ctx.send(answer)
#         except Exception as e:
#             await ctx.send("Sorry, something went wrong while processing your request.")
#             print(f"Error: {e}")


@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    
    if message:
        if message.startswith('.send'):
            message_to_send = message[len('.send '):]
            channel_id = 1240419054238302230  
            channel = bot.get_channel(channel_id)
            if channel:
                bot.loop.create_task(channel.send(message_to_send))
                return jsonify({"status": "Message sent"}), 200
            else:
                return jsonify({"status": "Channel not found"}), 404
        else:
            return jsonify({"status": "Invalid command"}), 400
    return jsonify({"status": "No message provided"}), 400




def run_flask():
    app.run(host='0.0.0.0', port=5000)




if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    bot.run(
        "MTI3MTkyODI3MDAyNzM2MjQ1NA.GI2qam.K7eZ-v8d8f0c8fDUG3mhGgcEoyQU-VZIs-Whcw"
    )
