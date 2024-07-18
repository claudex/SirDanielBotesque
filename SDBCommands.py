import discord
from discord.ext import commands
from SirDanBot import SirDan
import logging
# testing
from datetime import datetime
from datetime import timedelta
import random
from datetime import time

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
        now = datetime.now()
        random_hour = random.randint( 10, 21 )
        random_minute = random.randint( 0, 59 )
        bereal_time = time( random_hour, random_minute )
        delta = datetime.combine( datetime.today() + timedelta( days=1 ), bereal_time ) - datetime.combine( datetime.today(), datetime.now().time() )
        
        await ctx.send( f"now {now}\nbereal time {bereal_time}\ndelta {delta}" )


async def setup( _bot ):
    log = logging.getLogger("SDBCommands")
    log.info( "Commands setup." )
    await _bot.add_cog( Commands( _bot ) )