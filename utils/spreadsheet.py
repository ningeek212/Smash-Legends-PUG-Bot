import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.config import SCOPES, SL_PUG_ELO_SHEET_ID, DOMINION_TAB_NAME, DUEL_TAB_NAME, DUO_TAB_NAME


creds = None


def setup():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    global creds
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())


def get_dominion_elo():
    global creds
    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SL_PUG_ELO_SHEET_ID, range=(DOMINION_TAB_NAME + "!A2:A"))
            .execute()
        )
        values = result.get("values", [])
        player_names = [name[0] for name in values]
        num_players = len(player_names)

        result = (
            sheet.values()
            .get(spreadsheetId=SL_PUG_ELO_SHEET_ID, range=(DOMINION_TAB_NAME + f"!B2:B{num_players+1}"))
            .execute()
        )
        values = result.get("values", [])
        elo = [int(elo[0]) for elo in values]
        return [(player, elo) for player, elo in zip(player_names, elo)]
    except HttpError as err:
        print(err)


def get_duo_elo():
    global creds
    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SL_PUG_ELO_SHEET_ID, range=(DUO_TAB_NAME + "!A2:A"))
            .execute()
        )
        values = result.get("values", [])
        player_names = [name[0] for name in values]
        num_players = len(player_names)

        result = (
            sheet.values()
            .get(spreadsheetId=SL_PUG_ELO_SHEET_ID, range=(DUO_TAB_NAME + f"!B2:B{num_players+1}"))
            .execute()
        )
        values = result.get("values", [])
        elo = [int(elo[0]) for elo in values]
        return [(player, elo) for player, elo in zip(player_names, elo)]
    except HttpError as err:
        print(err)


def get_duel_elo():
    global creds
    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SL_PUG_ELO_SHEET_ID, range=(DUEL_TAB_NAME + "!A2:A"))
            .execute()
        )
        values = result.get("values", [])
        player_names = [name[0] for name in values]
        num_players = len(player_names)

        result = (
            sheet.values()
            .get(spreadsheetId=SL_PUG_ELO_SHEET_ID, range=(DUEL_TAB_NAME + f"!B2:B{num_players+1}"))
            .execute()
        )
        values = result.get("values", [])
        elo = [int(elo[0]) for elo in values]
        return [(player, elo) for player, elo in zip(player_names, elo)]
    except HttpError as err:
        print(err)

