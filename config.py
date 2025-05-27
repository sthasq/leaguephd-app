"""Configuration constants for League PhD application."""

# Application settings
APP_NAME = "League PhD"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 930

# URLs
BASE_URL = "https://www.leaguephd.com/stats/pick-now/"
GITHUB_API_URL = "https://api.github.com/repos/leaguephd/leaguephd-app/releases/latest"
GITHUB_RELEASES_URL = "https://github.com/leaguephd/leaguephd-app/releases"

# File paths
VERSION_FILE = "version.txt"
ICON_FILE = "assets/icon.ico"
LOG_FILE = "logs/session.log"

# League of Legends constants
TEAM_SIZE = 5
MAX_BANS = 10
BLUE_TEAM = 0
RED_TEAM = 1

# Position mappings
POSITION_MAP = {
    'top': 'TOP',
    'jungle': 'JGL',
    'middle': 'MID',
    'bottom': 'ADC',
    'utility': 'SUP',
}

# Draft types
DRAFT_TYPE_SOLO = 'solo'
DRAFT_TYPE_TOURNAMENT = 'tournament'

# LCU API endpoints
LCU_CHAMP_SELECT_SESSION = '/lol-champ-select/v1/session'
