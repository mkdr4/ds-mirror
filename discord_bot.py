from decouple import config 
from discord.utils import get
from discord import utils

import discord
import sys
import json
import re


MIRRORS = json.load(open("mirror.json", "r"))
ID_ROLES = json.loads(config("id_roles"))


class MyClient(discord.Client):

    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        print('<-------------------------------------------------->')
    
    async def on_message(self, message):
        if str(message.channel.id) in MIRRORS:
            for id_channel, id_role in zip(MIRRORS[str(message.channel.id)], ID_ROLES):
                if id_channel:
                    channel = self.get_channel(id_channel)
                    print(f"New message in the channel >{message.channel.name}<")

                    embed_hook = discord.Embed(title=f"**{message.channel.name}**", color=0xFF6F00)
                    await channel.send(embed=embed_hook)
                    
                    # text
                    if message.content:
                        if "<@&" in message.content:
                            text = message.content
                            result = re.findall("\<@&.*?\>", message.content)
                            for i in result:
                                text = text.replace(i, f"<@&{id_role}>")
                            await channel.send(text)
                        else:
                            await channel.send(message.content)
                        print("| Сontent sent")
                    
                    # embed
                    embeds = message.embeds
                    for embed in embeds:
                        await channel.send(embed = embed)
                        print("| Embed sent")
                    
                    # image
                    images = message.attachments
                    for image in images:
                        await channel.send(image)
                        print("| Image sent")
                    
                    print('<-------------------------------------------------->')

class Mirror:

    def add_new_mirror():
        try:
            channel1 = str(input("From: "))
            channel2 = int(input("In: "))
            MIRRORS[channel1] = channel2
            open("mirror.json", "w").write(json.dumps(MIRRORS, indent = 4))
            print("Successful addition of a new mirror!")
        except:
            print("Error in adding a new mirror")

    def del_mirror():
        try:
            for mirror in MIRRORS:
                print(mirror, "->", MIRRORS[mirror])
            mirror_for_del = input("Enter the tracked channel id: ")
            MIRRORS.pop(mirror_for_del)
            open("mirror.json", "w").write(json.dumps(MIRRORS, indent = 4))
            print("Successful delete mirror!")
        except:
            print("Error in delete mirror")


try:
    func = sys.argv[1]
    if func == "run_bot":
        token = config("discord_token")
        client = MyClient(intents = discord.Intents.all())
        client.run(str(token))
    
    elif func == "add_mirror":
        Mirror.add_new_mirror()
    
    elif func == "delete_mirror":
        Mirror.del_mirror()
except:
    print("To run the file you need to specify an action (run_bot / add_mirror / delete_mirror)\n$ python discord_bot.py run_bot")