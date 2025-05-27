"""Mock LCU handler for testing without League Client."""
import asyncio
import logging
from typing import Callable, Optional, Dict, Any

from ChampSelect import ChampSelect


class LCUHandlerWeb:
    """Mock LCU handler for testing purposes."""
    
    def __init__(
        self,
        champ_select: ChampSelect,
        on_champ_select_update: Callable[[Dict[str, Any], Dict[str, Any]], None],
        on_connection_status: Callable[[bool], None],
        logger: Optional[logging.Logger] = None
    ):
        """Initialize mock LCU handler."""
        self.champ_select = champ_select
        self.on_champ_select_update = on_champ_select_update
        self.on_connection_status = on_connection_status
        self.logger = logger or logging.getLogger(__name__)
        self.connected = False
    
    async def start(self):
        """Start mock LCU handler."""
        self.logger.info("Starting Mock LCU handler (no League Client required)")
        
        # Simulate connection after a delay
        await asyncio.sleep(2)
        self.connected = True
        self.on_connection_status(True)
        self.logger.info("Mock connection established")
        
        # Simulate some champion select events
        await self._simulate_champion_select()
    
    async def _simulate_champion_select(self):
        """Simulate a champion select session for demo purposes."""
        await asyncio.sleep(5)  # Wait 5 seconds before starting demo
        
        # Simulate session creation
        self.logger.info("Simulating champion select session creation")
        self.champ_select.reset()
        
        # Create mock session data
        mock_session = {
            'hasSimultaneousPicks': False,
            'actions': [
                [
                    {'type': 'ban', 'actorCellId': 0, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 5, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 1, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 6, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 2, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 7, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 3, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 8, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 4, 'completed': False, 'championId': None},
                    {'type': 'ban', 'actorCellId': 9, 'completed': False, 'championId': None},
                ]
            ],
            'localPlayerCellId': 0,  # Blue team
            'myTeam': [
                {'assignedPosition': 'top'},
                {'assignedPosition': 'jungle'},
                {'assignedPosition': 'middle'},
                {'assignedPosition': 'bottom'},
                {'assignedPosition': 'utility'},
            ]
        }
        
        # Update with mock data
        updated, dict_updated = self.champ_select.update(mock_session)
        if updated:
            self.on_champ_select_update(
                self.champ_select.__repr__(),
                dict_updated
            )
        
        # Keep running
        while True:
            await asyncio.sleep(10)  # Keep the handler alive
