import random
import discord
import asyncio
from concurrent.futures import ProcessPoolExecutor
import aiohttp

#intents = discord.Intents.all()
import threading

async def fetch(url, name, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"name": name, "input": data}) as response:
            return await response.json(content_type=None)

class ChatBot(discord.Client):
    """ChatBot handles discord communication. This class runs its own thread that
    persistently watches for new messages, then acts on them when the bots username
    is mentioned. It will use the ChatAI class to generate messages then send them
    back to the configured server channel.

    ChatBot inherits the discord.Client class from discord.py
    """

    def __init__(self) -> None:
        self.set_response_chance()
        super().__init__()
        #super().__init__(intents=intents)

    async def get_chat_logs(self):
        for guild in self.guilds:
            for channel in guild.channels:
                file = open(f"{channel.id} - {channel.name}.txt", "a+", encoding='utf-8')
                lastauthor = None
                wholemsg = ""
                try:
                    async for msg in channel.history(limit=None, oldest_first=True):
                        if lastauthor == None:
                            wholemsg += f"{msg.author.name}: {msg.content} "
                        elif lastauthor.id == msg.author.id:
                            wholemsg += msg.content + " "
                        elif lastauthor.id != msg.author.id:
                            file.write(wholemsg + "\n\n")
                            wholemsg = f"{msg.author.name}: {msg.content} "
                        lastauthor = msg.author
                except AttributeError:
                    continue
                file.write(wholemsg + "\n\n")

    async def on_ready(self) -> None:
        """ Initializes the GPT2 AI on bot startup """
        print("Logged on as", self.user)
        #await self.get_chat_logs()

    def send_message_to_ai(self, message, name, processed_input):
        response = "None"

        rawdata = self.chat_ai.get_bot_response(self.model_name, name, processed_input)
        data = rawdata.split("me:", 1)[1]
        print(data)
        data = data.splitlines()
        print("\n\n\n")
        print(data)
        response = data[0]
        return response

    async def on_message(self, message: discord.Message) -> None:
        """ Handle new messages sent to the server channels this bot is watching """

        if message.author == self.user:
            # Skip any messages sent by ourselves so that we don't get stuck in any loops
            return

        # Check to see if bot has been mentioned
        has_mentioned = False
        for mention in message.mentions:
            if str(mention) == self.user.name+"#"+self.user.discriminator:
                has_mentioned = True
                break

        processed_input = self.process_input(message.content)

        # Only respond randomly (or when mentioned), not to every message
        if random.random() > float(self.response_chance) and has_mentioned == False:
            return
        if has_mentioned:
            async with message.channel.typing():
                found = await fetch("http://localhost:6969", message.author.nick, processed_input)
                await message.channel.send(found["message"])
    
    def process_input(self, message: str) -> str:
        """ Process the input message """
        processed_input = message
        # Convert user ids to just nick names
        processed_input.replace("<@"+str(self.user.id)+">", "")
        return processed_input


    def check_if_should_respond(self, has_been_mentioned) -> bool:
        """ Check if the bot should respond to a message """
        should_respond = random.random() < self.response_chance

        return should_respond


    def set_response_chance(self, response_chance: float = 0.25) -> None:
        """ Set the response rate """
        self.response_chance = response_chance


    def set_model_name(self, model_name: str = "355M") -> None:
        """ Set the GPT2 model name """
        self.model_name = model_name
        
if __name__ == "__main__":
    bot = ChatBot()
    bot.run(open("token.txt", 'r').readlines()[0])