import bs4, requests, smtplib
import os
import smtplib
import imghdr
from email.message import EmailMessage











# Using requests to download the menu and checking for error.

getPage = requests.get('http://www.sczg.unizg.hr/prehrana/restorani/sd-s-radic/#')
getPage.raise_for_status()

# Using BeautifulSoup to parse the text

menu = bs4.BeautifulSoup(getPage.text, 'html.parser')
foods = menu.select('.content')


the_one = 'juneći gulaš'
flenght = len(the_one)
available = False

for food in foods:
    for i in range(len(food.text)):
        chunk = food.text[i:i+flenght].lower()
        if chunk == the_one:
            available = True
if available == True:
    # set enviroment variables for e-mails, and password!
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    EMAIL_TO = os.environ.get('EMAIL_TO')

    

    msg = EmailMessage()
    msg['Subject'] = 'MRŠ U MENZU ODMAH!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_TO

    msg.set_content('This is a plain text email')

    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
    <body>
        <h1 style="color:SlateGray;">Huraa, danas je na meniu juneći gulaš!!</h1>
        </body>
    </html>
    """, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

else:
    print('Nije Vaše jelo na meni-u!')
    