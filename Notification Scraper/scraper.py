# Author: Marcel Thio

import requests
import smtplib
import time
from bs4 import BeautifulSoup

# dictionary of the url of the product paired with the price under that we are looking for
url_dict = {
    'https://www.amazon.com/gp/product/B00L1LXOWS/ref=ox_sc_saved_title_6?smid=A37X6SD97CS5LJ&psc=1':100.0,
    'https://www.amazon.com/gp/product/B0002GOE6S/ref=ox_sc_saved_title_4?smid=ATVPDKIKX0DER&psc=1':200.0
}

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

# Function that takes in url and price and checks if the website has updated to show the price has been lowered
# if it has sends email to person with link to purchase
def webChecker(url,my_price):
    page = requests.get(url, headers = headers)
   
    soup = BeautifulSoup(page.content, 'html.parser')
   
    title = soup.find(id="productTitle").get_text().strip()
    price_text = soup.find(id="priceblock_ourprice").get_text()
    their_price = float(price_text[1:]) # convert text to float
    
    # check if my price is less than their price
    if(their_price < my_price):
        # send the email
        send_mail(title,their_price,url)

    print(title,'\n',their_price)


def send_mail(title, price, url):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('email_sent_from@gmail.com', 'jsusttwdsmvfrlul')

    subject = "Price is now $" + str(price) + " for " + title

    msg = f"Subject: {subject}\n\n{url}"
    server.sendmail(
        'email_sent_from@gmail.com',
        'email_sent_to@gmail.com',
        msg
    )
    print("Email has been sent!!!")
    server.quit()
    

while(True):
    for url, price in url_dict.items():
        webChecker(url,price)
    time.sleep(3600*6)