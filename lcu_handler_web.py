"""LCU handler for web-based League PhD application."""
import asyncio
import json
import logging
from typing import Callable, Optional, Dict, Any

from lcu_driver import Connector
from ChampSelect import ChampSelect
from config import LCU_CHAMP_SELECT_SESSION


class LCUHandlerWeb:
    """Web-based LCU API handler with callback system."""
    
    def __init__(
        self,
        champ_select: ChampSelect,
        on_champ_select_update: Callable[[Dict[str, Any], Dict[str, Any]], None],
        on_connection_status: Callable[[bool], None],
        logger: Optional[logging.Logger] = None
    ):
        """Initialize LCU handler with callback functions."""
        self.champ_select = champ_select
        self.on_champ_select_update = on_champ_select_update
        self.on_connection_status = on_connection_status
        self.logger = logger or logging.getLogger(__name__)
        
        self.connected = False
        self.connector: Optional[Connector] = None
    
    async def start(self):
        """Start the LCU connector and event handling."""
        loop = asyncio.get_event_loop()
        self.connector = Connector(loop=loop)
        
        # Register event handlers
        self._register_handlers()
        
        # Start connector
        self.logger.info("Starting LCU connector...")
        self.connector.start()
    
    def _register_handlers(self):
        """Register LCU API event handlers."""
        if not self.connector:
            raise RuntimeError("Connector not initialized")
        
        @self.connector.ready
        async def on_connect(connection):
            """Handle LCU API connection."""
            self.logger.info('Connected to League Client')
            self.connected = True
            self.on_connection_status(True)
            
            # Check for existing session
            await self._check_existing_session(connection)
        
        @self.connector.close
        async def on_disconnect(_):
            """Handle LCU API disconnection."""
            self.logger.info('Disconnected from League Client')
            self.connected = False
            self.on_connection_status(False)
            # Note: We don't exit the app, just update status
        
        @self.connector.ws.register(
            LCU_CHAMP_SELECT_SESSION,
            event_types=('CREATE', 'UPDATE', 'DELETE')
        )
        async def on_champ_select_event(connection, event):
            """Handle champion select session events."""
            await self._handle_champ_select_event(event)
    
    async def _check_existing_session(self, connection):
        """Check if there's an existing champion select session."""
        try:
            response = await connection.request('get', LCU_CHAMP_SELECT_SESSION)
            
            if response.status == 200:
                data = await response.json()
                self.logger.info("Found existing champion select session")
                self.logger.debug(f"Session data: {data}")
                
                self.champ_select.reset()
                updated, dict_updated = self.champ_select.update(data)
                
                if updated:
                    self.on_champ_select_update(
                        self.champ_select.__repr__(),
                        dict_updated
                    )
            else:
                self.logger.info("No active champion select session")
        except Exception as e:
            self.logger.error(f"Error checking existing session: {e}")
    
    async def _handle_champ_select_event(self, event):
        """Handle different types of champion select events."""
        try:
            if event.type == 'Create':
                await self._handle_session_create(event.data)
            elif event.type == 'Update':
                await self._handle_session_update(event.data)
            elif event.type == 'Delete':
                await self._handle_session_delete()
        except Exception as e:
            self.logger.error(f"Error handling champion select event: {e}")
    
    async def _handle_session_create(self, data: Dict[str, Any]):
        """Handle champion select session creation."""
        self.logger.info("Champion select session created")
        self.logger.debug(f"Session data: {json.dumps(data)}")
        
        self.champ_select.reset()
        # Emit reset state
        self.on_champ_select_update(
            self.champ_select.__repr__(),
            {'mode': 'reset', 'insert_list': [], 'to_pick_phase': False}
        )
    
    async def _handle_session_update(self, data: Dict[str, Any]):
        """Handle champion select session updates."""
        self.logger.debug(f"Session update: {json.dumps(data)}")
        
        updated, dict_updated = self.champ_select.update(data)
        
        if updated:
            self.logger.info(f"Champion select updated: {dict_updated}")
            self.on_champ_select_update(
                self.champ_select.__repr__(),
                dict_updated
            )
    
    async def _handle_session_delete(self):
        """Handle champion select session deletion."""
        self.logger.info("Champion select session ended")
        self.champ_select.reset()
        
        # Emit reset state
        self.on_champ_select_update(
            self.champ_select.__repr__(),
            {'mode': 'ended', 'insert_list': [], 'to_pick_phase': False}
        )
