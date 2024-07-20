import discord
from discord.ext import commands
import json
import logging
from BeReal import BeReal


# "Constant" variables
CONFIG_FILE = 'config.json'

CFG_TOKEN = 'Token'


# ============================================================================
# SIR DANIEL BOTESQUE
# ============================================================================
class SirDan( commands.Bot ):
	m_token: str = ''
	m_log: logging.Logger = None

# FUNCTIONS ------------------------------------------------------------------
	def __init__( self, _intents ):
		super().__init__( command_prefix = "/", intents = _intents )
		self.m_log = logging.getLogger( "SDB - Sir Dan" )

		# Reading bot token from config file
		file = open( CONFIG_FILE )
		json_data: dict = json.load( file )
		self.m_token = json_data[ CFG_TOKEN ]

		self.m_bereal = BeReal()
		self.m_bereal.load_config( json_data )

		file.close()
		self.save_bot_config()



	def save_bot_config( self ):
		with open( CONFIG_FILE, "w" ) as outfile:
			self.m_log.info( "Saving bot config...")
			bot_config = {}
			bot_config[ CFG_TOKEN ] = self.m_token
			self.m_bereal.save_config( bot_config )

			outfile.write( json.dumps( bot_config, sort_keys = False, indent = 4 ) )


	def generate_next_bereal( self ):
		self.m_bereal.generate_next_bereal()
		self.save_bot_config()

	# ---------------------------------
	# Always on thread managing bereal calls and sending alert to the channel
	# ---------------------------------
	async def remain_legitimate_thread( self ):
		self.m_log.info( "Entering thread.")
		while True:
			if self.m_bereal.are_date_and_time_valid() == False:
				self.generate_next_bereal()

			await self.m_bereal.manage_bereal()
			await self.get_channel( self.m_bereal.m_channel_id ).send( f"c'est l'heure du <@&{self.m_bereal.m_role_id}> ! :camera_with_flash:" )

			self.generate_next_bereal()


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
