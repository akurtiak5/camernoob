import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import random
import json,os,argparse

intents = discord.Intents(messages=True,guilds=True)
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = discord.Client(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
	await send_message()
	await bot.close()

async def send_message():
	args = await getArgs()
	channel = bot.get_channel(args.channel)
	if not channel:
		print(f"Channel {args.channel} not found")
		exit(1)
	
	if args.function == "reflection":
		content = await getDay()
	elif not args.message:
		content = None
	elif not os.path.exists(args.message):
		print(f"File {args.message} not found")
		exit(1)
	else:
		content = open(args.message, "r").read()

	if not args.attachment:
		file = None
	elif not os.path.exists(args.attachment):
		print(f"File {args.attachment} not found")
		exit(1)
	else:
		file = discord.File(open(args.attachment, "rb"))

	if not content and not file:
		print("No payload for message")
		exit(1)

	if args.reply:
		reply = await channel.fetch_message(args.reply)
		if not reply:
			print(f"Message {args.reply} not found")
			exit(1)
		await reply.reply(content=content,file=file)
		print(f'Message sent to channel {channel.name} at {datetime.now()}')
	else:
		await channel.send(content=content,file=file)
		print(f'Message sent to channel {channel.name} at {datetime.now()}')

async def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v','--verb',dest='verb',action='count',default=0)
	parser.add_argument('-c','--channel',dest='channel',action='store',default=None,required=True,type=int)
	parser.add_argument('-r','--reply',dest='reply',action='store',default=None,type=int)
	parser.add_argument('-a','--attachment',dest='attachment',action='store',default=None)
	parser.add_argument('-m','--message',dest='message',action='store',default=None)
	parser.add_argument('-f','--function',dest='function',action='store',choices=["reply", "message","reflection"],default=None)

	args = parser.parse_args()
	return args
	
async def getDay():
	today = datetime.now()
	origin = datetime(2023,6,28)#6/28/23
	#monthCheck(today)
	difference = (today-origin).days
	seed = difference - 7 #we don't want anything from within the week
	selection = random.randint(1,seed)
	return f'#{difference}: {selection}' #{today.strftime("%m/%d/%Y")}

async def monthCheck(today):
	day = today.days
	if day != 1:
		return None
	return ""

if __name__ == "__main__":
	token = json.load(open("/home/archer/scripts/camernoob/.token.json","r"))["token"]
	bot.run(token)
