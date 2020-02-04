import geop.distance as ps
import pandas as pd
import gspread

from oauth2client.service_account import ServicAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)
sheet = client.open("Data name").sheet1
data = sheet.get_all_records()
listdata = pd.DataFrame(data)
print(listdata)
