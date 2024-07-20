import discord
from discord.ext import commands
from SirDanBot import SirDan
import logging
from datetime import datetime
from datetime import date
from datetime import time


ROLE_ADMIN = 'test1'
ROLE_MOD = 'test2'


def is_date_valid( _date: str ):
	try:
		date.fromisoformat( _date )
	except:
		return False
	return True

def is_time_valid( _time: str ):
	try:
		time.fromisoformat( _time )
	except:
		return False
	return True

# ============================================================================
# MOD COMMANDS
# ============================================================================
class ModCommands( commands.Cog ):
	m_log: logging.Logger = None

	def __init__( self, _bot: SirDan ):
		self.m_log = logging.getLogger( "SDB - Mod Commands" )
		self.m_sir_dan = _bot

	# ---------------------------------
	# Set a new channel for the BeReal alerts
	# ---------------------------------
	@commands.command()
	@commands.has_any_role( ROLE_ADMIN, ROLE_MOD )
	async def bereal_set_channel( self, ctx: commands.Context ):
		if not ctx.message.channel_mentions:
			await ctx.send( "Il faut mentionner un chan pour utiliser cette commande. `/bereal_set_channel #chan`" )
			return
		
		channel = ctx.message.channel_mentions[ 0 ]

		member: discord.Member = None
		permissions = discord.Permissions()

		for guild in self.m_sir_dan.guilds:
			if guild.id == ctx.guild.id:
				member = guild.get_member( self.m_sir_dan.user.id )

		if member != None:
			permissions = channel.permissions_for( member )

		if permissions.read_messages == False:
			await ctx.send( f"Je ne peux pas utiliser le chan <#{channel.id}> car je ne le vois pas." )
			return
		
		if permissions.send_messages == False:
			await ctx.send( f"Je ne peux pas utiliser le chan <#{channel.id}> car je n'ai pas la permission d'y envoyer des messages." )
			return

		self.m_log.info( f"New BeReal chan set via command: {channel.guild.name} - {channel.name}" )
		self.m_sir_dan.bereal_set_channel( channel.id )
		await ctx.send( f"J'utiliserai désormais le chan <#{channel.id}> pour le BeReal. :+1:" )

	# ---------------------------------
	# Set the role to mention when it's BeReal time
	# ---------------------------------
	@commands.command()
	@commands.has_any_role( ROLE_ADMIN, ROLE_MOD )
	async def bereal_set_role( self, ctx: commands.Context ):
		if not ctx.message.role_mentions:
			await ctx.send( "Il faut mentionner un role pour utiliser cette commande. `/bereal_set_role @role`" )
			return
		
		role: discord.Role = ctx.message.role_mentions[ 0 ]
		self.m_log.info( f"New BeReal role set via command: {ctx.message.guild.name} - {role.name}" )
		self.m_sir_dan.bereal_set_role( role.id )
		await ctx.send( f"Je mentionnerai désormais le role <@&{role.id}> quand ce sera l'heure du BeReal. :+1:" )


	# ---------------------------------
	# Set the lower bound for BeReal time generation
	# ---------------------------------
	@commands.command()
	@commands.has_any_role( ROLE_ADMIN, ROLE_MOD )
	async def bereal_set_min_time( self, ctx: commands.Context, _time: str ):
		if is_time_valid( _time ) == False:
			await ctx.send( "Le temps donné n'est pas valide. Il faut suivre ce format: `/bereal_set_min_time 00:00`" )
			return
		
		new_min_time = time.fromisoformat( _time )
		self.m_log.info( f"New BeReal time lower bound set via command: {_time}" )
		self.m_sir_dan.bereal_set_min_time( new_min_time )
		await ctx.send( f"À partir de maintenant, il n'y aura plus d'alertes BeReal avant {_time}. :+1:" )

	# ---------------------------------
	# Set the upper bound for BeReal time generation
	# ---------------------------------
	@commands.command()
	@commands.has_any_role( ROLE_ADMIN, ROLE_MOD )
	async def bereal_set_max_time( self, ctx: commands.Context, _time: str ):
		if is_time_valid( _time ) == False:
			await ctx.send( "Le temps donné n'est pas valide. Il faut suivre ce format: `/bereal_set_max_time 00:00`" )
			return
		
		new_max_time = time.fromisoformat( _time )
		self.m_log.info( f"New BeReal time upper bound set via command: {_time}" )
		self.m_sir_dan.bereal_set_max_time( new_max_time )
		await ctx.send( f"À partir de maintenant, il n'y aura plus d'alertes BeReal après {_time}. :+1:" )

	# ---------------------------------
	# Display Sir Dan's current status in everything
	# ---------------------------------
	@commands.command()
	@commands.has_any_role( ROLE_ADMIN, ROLE_MOD )
	async def get_status( self, ctx: commands.Context ):
		await ctx.send( "# État courant" )

		bereal = self.m_sir_dan.m_bereal
		role = ctx.guild.get_role( bereal.m_role_id )

		bereal_status:str = "## BeReal"
		bereal_status += f"\n**Chan:** <#{bereal.m_channel_id}>"
		bereal_status += f"\n**Role:** {role.name}"
		bereal_status += f"\n**Heure min:** {bereal.m_min_time.isoformat()}"
		bereal_status += f"\n**Heure max:** {bereal.m_max_time.isoformat()}"

		now = datetime.now()
		delta = bereal.m_datetime - now

		seconds = delta.total_seconds()

		bereal_status += f"\n**Date et heure du prochain BeReal:** ||{bereal.m_datetime}, dans {delta} ({seconds} secondes)||" 

		await ctx.send( f"{bereal_status}" )
# ============================================================================


async def setup( _bot ):
	log = logging.getLogger("SDB - Mod Commands")
	log.info( "Mod commands setup." )
	await _bot.add_cog( ModCommands( _bot ) )