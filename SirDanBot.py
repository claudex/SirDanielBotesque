import discord
from discord.ext import commands
import json
import asyncio
from datetime import datetime
import logging


# "Constant" variables
CONFIG_FILE = 'config.json'

CFG_TOKEN = 'Token'
CFG_BEREAL = 'BeReal'
CFG_BEREAL_CHANNEL = 'Channel'


# ============================================================================
# SIR DANIEL BOTESQUE
# ============================================================================
class SirDan( commands.Bot ):
	m_token = ''
	m_channel_id = 0
	m_log = None
	m_cfg_data = None

# FUNCTIONS ------------------------------------------------------------------
	def __init__( self, _intents ):
		super().__init__( command_prefix = "/", intents = _intents )

		# Reading bot token from config file
		file = open( CONFIG_FILE )
		self.m_cfg_data = json.load( file )
		self.m_token = self.m_cfg_data[ CFG_TOKEN ]
		self.m_channel_id  = self.m_cfg_data[ CFG_BEREAL ][ CFG_BEREAL_CHANNEL ]
		file.close()

		self.m_log = logging.getLogger("SirDanBot")


# BEREAL FUNCTIONS  ----------------------------------------------------------
	def save_bereal_setting( self, _setting, _value ):
		self.m_cfg_data[ CFG_BEREAL ][ _setting ] = _value

		with open( CONFIG_FILE, "w" ) as outfile:
			outfile.write( json.dumps( self.m_cfg_data, sort_keys = True, indent = 4 ) )


	# This function will manage Be.Real type stuff later
	async def remain_legitimate_thread( self, _channel ):
		self.m_log.info( "Entering thread." )
		while True:
			
			
			await asyncio.sleep( 30 )


# EVENTS ---------------------------------------------------------------------
	async def on_ready( self ):
		self.m_log.info( f'Logged in as {self.user.display_name}.' )

		self.m_log.info( "Starting thread.")
		self.loop.create_task(self.remain_legitimate_thread( _channel = self.get_channel( self.m_channel_id ) ) )


	async def on_message( self, _message: discord.Message ) -> None:
		if _message.author == self.user:
			return await super().on_message( _message )
		
		if _message.content.lower() == "ping":
			await _message.channel.send( f'pong :ping_pong:' )
		
		return await super().on_message( _message )
# ============================================================================


sir_dan_intents = discord.Intents.default()
sir_dan_intents.message_content = True

sir_dan = SirDan( _intents = sir_dan_intents )
sir_dan.run( sir_dan.m_token, root_logger=True )