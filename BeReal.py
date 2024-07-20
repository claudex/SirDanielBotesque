from datetime import datetime
from datetime import timedelta
from datetime import time
from datetime import date
import logging
import random
import asyncio


CFG_BEREAL = 'BeReal'
CFG_CHANNEL = 'Channel'
CFG_ROLE = 'Role'
CFG_MIN_TIME = 'MinTime'
CFG_MAX_TIME = 'MaxTime'
CFG_DATETIME = 'DateTime'

DEFAULT_MIN_TIME = "10:00:00"
DEFAULT_MAX_TIME = "22:00:00"


# ============================================================================
# BEREAL
# ============================================================================
class BeReal:
	m_log: logging.Logger = None
	m_channel_id = 0
	m_role_id = 0
	m_min_time = time.fromisoformat( DEFAULT_MIN_TIME )
	m_max_time = time.fromisoformat( DEFAULT_MAX_TIME )
	m_datetime: datetime

	def __init__( self ):
		self.m_log = logging.getLogger( "SDB - Bereal" )


# CONFIG FILE ----------------------------------------------------------------
	def load_config( self, _json: dict ):
		if CFG_BEREAL not in _json:
			self.m_log.warning( "No BeReal section found in config file, using default values and generating a new date..." )
			self.m_min_time = time.fromisoformat( DEFAULT_MIN_TIME )
			self.m_min_time = time.fromisoformat( DEFAULT_MAX_TIME )
			self.generate_next_bereal()
			return
		
		if CFG_CHANNEL in _json[ CFG_BEREAL ]:
			self.m_channel_id = _json[ CFG_BEREAL ][ CFG_CHANNEL ]

		if CFG_ROLE in _json[ CFG_BEREAL ]:
			self.m_role_id = _json[ CFG_BEREAL ][ CFG_ROLE ]

		if CFG_MIN_TIME in _json[ CFG_BEREAL ]:
			self.m_min_time = time.fromisoformat( _json[ CFG_BEREAL ][ CFG_MIN_TIME ] )
		else:
			self.m_min_time = time.fromisoformat( DEFAULT_MIN_TIME )

		if CFG_MAX_TIME in _json[ CFG_BEREAL ]:
			self.m_max_time = time.fromisoformat( _json[ CFG_BEREAL ][ CFG_MAX_TIME ] )
		else:
			self.m_max_time = time.fromisoformat( DEFAULT_MAX_TIME )

		if CFG_DATETIME in _json[ CFG_BEREAL ]:
			self.m_datetime = datetime.fromisoformat( _json[ CFG_BEREAL ][ CFG_DATETIME ] )
		else:
			self.m_log.warning( "No datetime found in config file, generating a new date..." )
			self.generate_next_bereal()


	def save_config( self, _json_data: dict ):
		_json_data[ CFG_BEREAL ] = {}
		if self.m_channel_id != 0:
			_json_data[ CFG_BEREAL ][ CFG_CHANNEL ] = self.m_channel_id
		_json_data[ CFG_BEREAL ][ CFG_ROLE ] = self.m_role_id
		_json_data[ CFG_BEREAL ][ CFG_MIN_TIME ] = self.m_min_time.isoformat()
		_json_data[ CFG_BEREAL ][ CFG_MAX_TIME ] = self.m_max_time.isoformat()
		_json_data[ CFG_BEREAL ][ CFG_DATETIME ] = self.m_datetime.isoformat( ' ' )


# FUNCTIONS ------------------------------------------------------------------
	# ---------------------------------
	# Generate a time for the next bereal using the bounds read in the config file
	# ---------------------------------
	def generate_next_bereal( self ):
		self.m_log.info( "Generating new bereal datetime..." )
		bereal_date: date = date.today() + timedelta( days = 1 )

		random_hour = random.randint( self.m_min_time.hour, self.m_max_time.hour )
		random_minute = random.randint( 0, 59 )
		bereal_time = time( random_hour, random_minute )

		if bereal_time < self.m_min_time:
			bereal_time = self.m_min_time

		if bereal_time > self.m_max_time:
			bereal_time = self.m_max_time

		self.m_datetime = datetime.combine( bereal_date, bereal_time )
		self.m_log.info( f"Bereal date and time: {self.m_datetime}" )

	# ---------------------------------
	# Generate BeReal dates and wait for the right time to come
	# ---------------------------------
	async def manage_bereal( self ):
		now = datetime.now()
		delta = self.m_datetime - now

		seconds = delta.total_seconds()
		self.m_log.info( f"Current date: {now} / delta: {delta} / sleeping for {seconds} seconds..." )
		await asyncio.sleep( seconds )
		self.m_log.info( f"It's bereal time !" )


# ACCESSORS ------------------------------------------------------------------
	def are_date_and_time_valid( self ) -> bool:
		if self.m_datetime.day <= 0 or self.m_datetime.month <= 0 or self.m_datetime.year <= 0:
			return False
		
		if self.m_datetime.time() < self.m_min_time or self.m_datetime.time() > self.m_max_time:
			return False

		return True
# ============================================================================