import json
import discord
from datetime import datetime
from datetime import timedelta
from datetime import time
from datetime import date
import logging
import random
import asyncio


CFG_BEREAL = 'BeReal'
CFG_BEREAL_CHANNEL = 'Channel'
CFG_BEREAL_DATE = 'Date'
CFG_BEREAL_TIME = 'Time'
CFG_BEREAL_MIN_TIME = 'MinTime'
CFG_BEREAL_MAX_TIME = 'MaxTime'


# ============================================================================
# BEREAL
# ============================================================================
class BeReal:
	m_log: logging.Logger
	m_date: date
	m_time: time
	m_min_time: time
	m_max_time: time

	def __init__( self ):
		self.m_log = logging.getLogger( "SDB - Bereal" )

	def load_config( self, _json ):
		self.m_channel_id = _json[ CFG_BEREAL ][ CFG_BEREAL_CHANNEL ]

		int_list: list[int] = _json[ CFG_BEREAL ][ CFG_BEREAL_DATE ]

		if int_list[ 0 ] != 0 and int_list[ 1 ] != 0 and int_list[ 2 ] != 0:
			self.m_date = date( int_list[ 0 ], int_list[ 1 ], int_list[ 2 ] )

		int_list = _json[ CFG_BEREAL ][ CFG_BEREAL_TIME ]

		if int_list[ 0 ] != 0 and int_list[ 1 ] != 0 and int_list[ 2 ] != 0:
			self.m_time = time( int_list[ 0 ], int_list[ 1 ], int_list[ 2 ] )

		int_list = _json[ CFG_BEREAL ][ CFG_BEREAL_MIN_TIME ]
		self.m_min_time = time( int_list[ 0 ], int_list[ 1 ], int_list[ 2 ] )

		int_list = _json[ CFG_BEREAL ][ CFG_BEREAL_MAX_TIME ]
		self.m_max_time = time( int_list[ 0 ], int_list[ 1 ], int_list[ 2 ] )


	def are_date_and_time_valid( self ) -> bool:
		if self.m_date.day <= 0 or self.m_date.month <= 0 or self.m_date.year <= 0:
			return False
		
		if self.m_time < self.m_min_time or self.m_time > self.m_max_time:
			return False

		return True


	def generate_next_bereal( self ):
		self.m_date = date.today() + timedelta( days = 1 )

		random_hour = random.randint( self.m_min_time.hour, self.m_max_time.hour )
		random_minute = random.randint( 0, 59 )
		self.m_time = time( random_hour, random_minute )

		if self.m_time < self.m_min_time:
			self.m_time = self.m_min_time

		if self.m_time > self.m_max_time:
			self.m_time = self.m_max_time


	async def update( self ):
		self.m_log.info( "Entering BeReal update." )
		while True:
			if self.are_date_and_time_valid() == False:
				self.generate_next_bereal()

			now = datetime.now()
			bereal = datetime.combine( self.m_date, self.m_time )
			
			self.m_log.info( f"Current time: {now} / Bereal time: {bereal}" )

			await asyncio.sleep( 30 )

			# Invalidating time to generate a new bereal
			self.m_time = time( 0, 0, 0 )
# ============================================================================