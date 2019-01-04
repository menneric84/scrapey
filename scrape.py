import requests
from bs4 import BeautifulSoup
import csv
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client


me = 'me@email.com'
you = 'you@email.com'
search = {'searchstring1', 'searchstring2', 'searchstring3'}
account_sid = 'yourSecretKey' #for twilio message sending
auth_token = 'yourSecretKey' #for twilio message sending
client = Client(account_sid, auth_token)
toPhone = '+10000000000'
fromPhone = '+10000000000'
def sendEmail(item, link):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text ).
    text = "New Item Posted: " + item + '  Link: ' + link
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)

    # Send the message via local SMTP server.
    smtpObj = smtplib.SMTP('#yoursmtp', 000) #add your smtp and port
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('username', 'password') #your username and password for smtp. I used gmail
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    smtpObj.sendmail(me, you, msg.as_string())
    smtpObj.quit()
def sendText(item, link):
    message = client.messages \
                .create(
                     body="New Item Posted: " + item + '  Link: ' + link,
                     from_=fromPhone,
                     to=toPhone
                 )

def sendRequest(search):
    search.replace(' ', '%20') #replace spaces in search terms with unicode value
    url = 'siteurlyouwanttoscrape{}'.format(search) #Make sure you have the {} wherever you would like your search term to be
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    results = soup.find_all(class_='result-title')
    #Store data in a CSV
    f = csv.writer(open('{}.csv'.format(search), 'a'))
    #Loop to print 
    for result in results:
        item = result.contents[0]
        link = result.get('href')
        with open('{}.csv'.format(search),'r') as csvfile:
            existingLines = csv.reader(csvfile)
            existingLines = list(existingLines)
            flag = False
            for row in existingLines:
                if row and row[0] == item:
                    flag = True
        if not flag:
            sendEmail(item, link)
            sendText(item, link)
            f.writerow([item, link, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")])
def main():
    #Debugging statement that shows that the cron service is running
    print('Start scrape ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    for item in search:
        sendRequest(item)
main()
