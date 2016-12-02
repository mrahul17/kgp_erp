import requests
from main import login, urls
import csv
import sys

try:
    s = login()
except:
    sys.exit("Unable to login. Exiting..")

with open('roll_list.csv') as f:
    csvfile = csv.reader(f)
    for row in csvfile:
        r = s.get(urls['CV_URL'].format(row[0]))
        if r.content != '':
            with open("{0}.pdf".format(row[0]),'w+') as pdf:
                pdf.write(r.content)

s.get(urls['LOGOUT_URL'])
s.close()
