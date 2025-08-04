#MADE BY SICHANG WANG FOR APPLICATION TO ZSCHOOL INTERNSHIP
#ALL SECRETS SUCH AS TOKENS AND PRIVATE KEYS HAVE BEEN OBSCURED FOR SECURITY PURPOSES

#get most recent response from google sheet linked to google forms
from google.oauth2.service_account import Credentials
import gspread

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = "OBSCURED"
SPREADSHEET_ID = "OBSCURED"

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

def get_latest_response():
    records = sheet.get_all_records()
    if not records:
        return None
    return records[-1]  #last row is most recent response

#----------------------------------------------------------------------------------
#summarize with chatgpt
from openai import OpenAI

OPENAI_API_KEY = "OBSCURED"
client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
  model="gpt-4o-mini-2024-07-18",
  input="SUMMARIZE THIS RESPONSE FROM A GOOGLE FORM: " + get_latest_response()['Write a response to be summarized:']
)

print(response.output_text)
summary = response.output_text

#---------------------------------------------------------------------
#post to slack
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = "OBSCURED"
client = WebClient(token=slack_token)

def post_to_slack(summary):
    try:
        response = client.chat_postMessage(
            channel="#form-summary",  # Replace with your Slack channel name
            text=f"New Google Form Response Summary:\n{summary}"
        )
        print(f"Message posted to Slack: {response['message']['text']}")
    except SlackApiError as e:
        print(f"error posting the message: {e.response['error']}")

post_to_slack(summary)
