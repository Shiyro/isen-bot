from asyncio import sleep
from datetime import datetime, timezone
from glob import glob

from ..bot import config

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord import Intents
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
								  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions


#from ..db import db

OWNER_IDS = [238039924178157568]
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]
cfg=config.load_config()
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class Bot(BotBase):
	def __init__(self):
		self.ready = False

		self.guild = None
		self.TOKEN=cfg["token"]
		self.scheduler = AsyncIOScheduler(timezone="Europe/Paris")

		super().__init__(command_prefix=cfg["prefix"], owner_ids=OWNER_IDS, intents=Intents().all(),help_command=None)

		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f"Loading cog : {cog}")


	def run(self, version):
		self.VERSION = version
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print("Connected to Discord. Not ready to receive commands.")
		await self.register_commands()

	async def on_disconnect(self):
		print("Disconnected")

	async def on_ready(self):
		if not self.ready:
		
			self.scheduler.start()

			self.ready = True
			print("Now ready to receive commands")

		else:
			print("The bot has reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)
			
			if 'hei' in message.content.lower():
				await message.channel.send('**Enculé !**')
			
			if 'quoi' in message.content.lower():
				await message.channel.send('**Feur !**')

bot = Bot()