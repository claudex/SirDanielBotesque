import discord
from discord.ext import commands
import json


# ============================================================================
# SIR DANIEL BOTESQUE
# ============================================================================
class SirDan( commands.Bot ):
	m_token = ''

# FUNCTIONS ------------------------------------------------------------------
	def __init__( self, _intents ):
		super().__init__( command_prefix = "!", intents = _intents )

		file = open( 'config.json' )
		file_data = json.load( file )
		self.m_token = file_data['token']

# EVENTS ---------------------------------------------------------------------
	async def on_ready( self ):
		print( f'Logged in as {self.user.display_name}.' )


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
sir_dan.run( sir_dan.m_token )
