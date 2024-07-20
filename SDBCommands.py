import discord
from discord.ext import commands
from SirDanBot import SirDan
import logging
# testing
import random

# ============================================================================
# COMMANDS
# ============================================================================
class Commands( commands.Cog ):
	def __init__( self, _bot: commands.Bot ):
		self.bot = _bot

	# ---------------------------------
	# Simple test command
	# ---------------------------------
	@commands.command()
	async def ping( self, ctx ):
		await ctx.send( "pong" )

	# ---------------------------------
	# Generate a Is There Any Deal search link from given game name
	# ---------------------------------
	@commands.command()
	async def deal( self, ctx: commands.Context, *_game ):
		game_name = " ".join( _game ).title()
		link_end = "+".join( _game )
		await ctx.send( f"Recherche Is There Any Deal: **[{ game_name }](<https://isthereanydeal.com/search/?q={ link_end }>)**")

	# ---------------------------------
	# Synchronize command tree with discord
	# ---------------------------------
	@commands.command( name = "sync_commands" )
	async def sync_command_tree( self, ctx ):
		await self.bot.tree.sync()
# ============================================================================


async def setup( _bot ):
	log = logging.getLogger("SDB - Commands")
	log.info( "Commands setup." )
	await _bot.add_cog( Commands( _bot ) )