import discord
from discord.ext import commands
from SirDanBot import SirDan
import logging

class Commands( commands.Cog ):
    def __init__( self, _bot ):
        self.bot = _bot

    @commands.command()
    async def ping( self, ctx ):
        await ctx.send( "pong" )

    @commands.command()
    async def deal( self, ctx: commands.Context, *_game ):
        game_name = " ".join( _game ).title()
        link_end = "+".join( _game )
        await ctx.send( f"Recherche Is There Any Deal: **[{ game_name }](<https://isthereanydeal.com/search/?q={ link_end }>)**")


async def setup( _bot ):
    log = logging.getLogger("SDBCommands")
    log.info( "Commands setup." )
    await _bot.add_cog( Commands( _bot ) )