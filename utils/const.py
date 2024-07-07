from interactions import Permissions

# Spreadsheet Related ========================================================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SL_PUG_ELO_SHEET_ID = "1-VjkV52wk492jUwW-DzH26ca2PLQwWsoBAxTT_IsvLY"

DOMINION_TAB_NAME=r"'Dominion ELO & W/L'"
DUO_TAB_NAME=r"'Duo TD ELO & W/L'"
DUEL_TAB_NAME=r"'Duel ELO & W/L'"
# ============================================================================

# PERMISSIONS ================================================================
COMMAND_PERMISIONS = {
    "TASK_LOOP": Permissions.MANAGE_EVENTS
}
# ============================================================================

# Assorted====================================================================
DEV_GUILD_ID = 1253488634254983249
DEV_TASK_CHANNEL_ID = 1258410129498570802
GAME_SIGNUP_INTERVAL = 1 # Minutes
# ============================================================================
