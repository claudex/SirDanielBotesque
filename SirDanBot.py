import discord
from discord.ext import commands
import json
import asyncio
from datetime import datetime
from datetime import timedelta
from datetime import time
import logging
import random
from BeReal import BeReal


# "Constant" variables
CONFIG_FILE = 'config.json'

CFG_TOKEN = 'Token'
CFG_BEREAL = 'BeReal'
CFG_BEREAL_CHANNEL = 'Channel'
CFG_BEREAL_DATE = 'Date'
CFG_BEREAL_TIME = 'Time'


# ============================================================================
# SIR DANIEL BOTESQUE
# ============================================================================
class SirDan( commands.Bot ):
	m_token = ''
	m_channel_id = 0
	m_log = None
	m_cfg_data = None
	m_bereal = BeReal()

# FUNCTIONS ------------------------------------------------------------------
	def __init__( self, _intents ):
		super().__init__( command_prefix = "/", intents = _intents )

		# Reading bot token from config file
		file = open( CONFIG_FILE )
		self.m_cfg_data = json.load( file )
		self.m_token = self.m_cfg_data[ CFG_TOKEN ]
		self.m_channel_id  = self.m_cfg_data[ CFG_BEREAL ][ CFG_BEREAL_CHANNEL ]

		self.m_bereal.load_config( self.m_cfg_data )

		file.close()

		self.m_log = logging.getLogger( "SDB - Sir Dan" )

	def save_bot_config( self ):
		with open( CONFIG_FILE, "w" ) as outfile:
			outfile.write( json.dumps( self.m_cfg_data, sort_keys = True, indent = 4 ) )


	async def remain_legitimate_thread( self ):
		await self.m_bereal.update()


# EVENTS ---------------------------------------------------------------------
	async def on_ready( self ):
		self.m_log.info( f'Logged in as {self.user.display_name}.' )

		self.m_log.info( "Starting thread.")
		self.loop.create_task(self.remain_legitimate_thread() )

		await self.load_extension( "SDBCommands" )


	async def on_message( self, _message: discord.Message ) -> None:
		if _message.author == self.user:
			return await super().on_message( _message )
		
		if _message.content.lower() == "ping":
			await _message.channel.send( f'pong :ping_pong:' )
		
		return await super().on_message( _message )
# ============================================================================
