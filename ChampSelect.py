"""Champion Select data model for League of Legends draft phase."""
from typing import Dict, List, Optional, Tuple, Any
from config import (
    TEAM_SIZE, MAX_BANS, BLUE_TEAM, RED_TEAM,
    POSITION_MAP, DRAFT_TYPE_SOLO, DRAFT_TYPE_TOURNAMENT
)


class ChampSelect:
    """Manages champion select session data and updates."""
    
    def __init__(self):
        """Initialize champion select with default values."""
        self.active: bool = False
        self.draft_type: Optional[str] = None
        self.my_side: Optional[int] = None
        self.num_banned: int = 0
        self.bans: List[Optional[int]] = [None] * MAX_BANS
        self.num_picked: int = 0
        self.picks: List[List[Dict[str, Optional[Any]]]] = self._init_picks()
        self.has_pick_started: bool = False
    
    def _init_picks(self) -> List[List[Dict[str, Optional[Any]]]]:
        """Initialize picks structure for both teams."""
        return [
            [{'champion_id': None, 'role': None} for _ in range(TEAM_SIZE)],
            [{'champion_id': None, 'role': None} for _ in range(TEAM_SIZE)]
        ]

    def __repr__(self) -> Dict[str, Any]:
        """Return dictionary representation of champion select state."""
        return {
            'active': self.active,
            'draft_type': self.draft_type,
            'my_side': self.my_side,
            'num_banned': self.num_banned,
            'num_picked': self.num_picked,
            'bans': self.bans,
            'picks': self.picks,
            'has_pick_started': self.has_pick_started,
        }

    def __str__(self) -> str:
        """Return string representation of champion select state."""
        return str(self.__repr__())

    def reset(self) -> None:
        """Reset champion select to initial state."""
        self.active = False
        self.draft_type = None
        self.my_side = None
        self.num_banned = 0
        self.bans = [None] * MAX_BANS
        self.num_picked = 0
        self.picks = self._init_picks()
        self.has_pick_started = False

    def update(self, session: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Update champion select state based on session data.
        
        Args:
            session: Session data from LCU API
            
        Returns:
            Tuple of (updated, dict_updated) where updated is bool indicating
            if state changed and dict_updated contains update details
        """
        updated = False
        dict_updated = {
            'mode': None,
            'insert_list': [],
            'to_pick_phase': False,
        }

        # Activate champion select if not simultaneous picks
        if not self.active and not session['hasSimultaneousPicks']:
            self.active = True
            self.draft_type = self._determine_draft_type(session)

        if not self.active:
            return updated, dict_updated

        # Set player's team side
        if self.my_side is None:
            self.my_side = self._determine_my_side(session['localPlayerCellId'])
            updated = True

        # Update bans
        ban_updated = self._update_bans(session['actions'])
        if ban_updated:
            updated = True
            dict_updated['mode'] = 'ban'

        # Update picks
        pick_updated, pick_dict = self._update_picks(session)
        if pick_updated:
            updated = True
            dict_updated.update(pick_dict)

        # Deactivate if all picks are done
        if self.num_picked > 9:
            self.active = False

        return updated, dict_updated
    
    def _determine_draft_type(self, session: Dict[str, Any]) -> str:
        """Determine if draft is solo/flex or tournament type."""
        return DRAFT_TYPE_SOLO if len(session['actions'][0]) == 10 else DRAFT_TYPE_TOURNAMENT
    
    def _determine_my_side(self, local_player_cell_id: int) -> int:
        """Determine which team side the player is on."""
        return BLUE_TEAM if local_player_cell_id <= 4 else RED_TEAM
    
    def _map_position_to_role(self, position: str) -> Optional[str]:
        """Map assigned position to role abbreviation."""
        return POSITION_MAP.get(position)
    
    def _get_action_by_type(self, actions: List[List[Dict[str, Any]]], action_type: str) -> List[Dict[str, Any]]:
        """Extract actions of specific type from actions list."""
        result = []
        for action_group in actions:
            for action in action_group:
                if action['type'] == action_type:
                    result.append(action)
        return result
    
    def _update_bans(self, actions: List[List[Dict[str, Any]]]) -> bool:
        """Update ban information and return if any changes occurred."""
        ban_actions = self._get_action_by_type(actions, 'ban')
        new_num_banned = 0
        new_bans = self.bans.copy()
        
        ban_counters = {BLUE_TEAM: 0, RED_TEAM: 0}
        
        for action in ban_actions:
            action_side = self._determine_my_side(action['actorCellId'])
            
            if action['completed']:
                if action_side == BLUE_TEAM:
                    ban_slot = ban_counters[BLUE_TEAM]
                else:
                    ban_slot = 5 + ban_counters[RED_TEAM]
                
                new_bans[ban_slot] = action['championId']
                new_num_banned += 1
            
            ban_counters[action_side] += 1
        
        if new_num_banned > self.num_banned:
            self.bans = new_bans
            self.num_banned = new_num_banned
            return True
        
        return False
    
    def _update_picks(self, session: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Update pick information and return if any changes occurred."""
        pick_actions = self._get_action_by_type(session['actions'], 'pick')
        updated = False
        dict_updated = {
            'insert_list': [],
            'to_pick_phase': False,
        }
        
        # Check if pick phase has started
        if not self.has_pick_started:
            for action in pick_actions:
                if action['completed'] or action['isInProgress']:
                    self.has_pick_started = True
                    dict_updated['to_pick_phase'] = True
                    updated = True
                    break
        
        if not self.has_pick_started:
            return updated, dict_updated
        
        new_num_picked = 0
        
        for action in pick_actions:
            if action['completed']:
                new_num_picked += 1
                
                picks_team = self._determine_my_side(action['actorCellId'])
                picks_slot = action['actorCellId'] if action['actorCellId'] <= 4 else action['actorCellId'] - 5
                
                # Only update if this pick slot is empty
                if self.picks[picks_team][picks_slot]['champion_id'] is None:
                    self.picks[picks_team][picks_slot]['champion_id'] = action['championId']
                    
                    # Update role if it's an ally action
                    if action['isAllyAction']:
                        role = self._get_player_role(session, action['actorCellId'])
                        self.picks[picks_team][picks_slot]['role'] = role
                    
                    # Add to update list
                    dict_updated['insert_list'].append({
                        'side': picks_team,
                        'slot': picks_slot,
                        'champion_id': self.picks[picks_team][picks_slot]['champion_id'],
                        'role': self.picks[picks_team][picks_slot]['role']
                    })
        
        if new_num_picked > self.num_picked:
            self.num_picked = new_num_picked
            updated = True
        
        return updated, dict_updated
    
    def _get_player_role(self, session: Dict[str, Any], actor_cell_id: int) -> Optional[str]:
        """Get player role from session data."""
        try:
            team_index = actor_cell_id if self.my_side == BLUE_TEAM else actor_cell_id - 5
            player_data = session['myTeam'][team_index]
            return self._map_position_to_role(player_data['assignedPosition'])
        except (KeyError, IndexError):
            return None
