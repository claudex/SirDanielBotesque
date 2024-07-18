import discord
from discord.ext import commands
from SirDanBot import SirDan
import logging
# testing
from datetime import datetime
from datetime import timedelta

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

    @commands.command()
    async def bereal( self, ctx: commands.Context ):
        delta = datetime.combine( datetime.today() + timedelta( days=1 ), datetime.min.time() ) - datetime.combine( datetime.today(), datetime.now().time() )
        print( f"{delta}" )
        await ctx.send( "bjr" )


async def setup( _bot ):
    log = logging.getLogger("SDBCommands")
    log.info( "Commands setup." )
    await _bot.add_cog( Commands( _bot ) )