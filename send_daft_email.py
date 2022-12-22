import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv
from datetime import datetime
from get_template_response import get_template_response
import urllib.parse

def send_daft_email(properties: list, to: list, num_beds: str):
    '''
    Sends Email notification for the new properties scraped.

    INPUT:
    - properties (list): List of dictionaries relating to each property scraped. Each dictionary contains the daft_id, link, address, price, latitude, and longitude for the property.
    - to (list): list of email addresses of recipients as strings
    - num_beds (str): number of beds in the properties to be used in Subject line of email

    OUTPUT:
    None
    '''

    # Get email address and password from envirnment variables where they are saved as GMAIL_USER and GMAIL_PW respectively
    gmail_user = getenv('GMAIL_USER')
    gmail_pw = getenv('GMAIL_PW')

    # Use MIMEMultipart to construct email with text form and html form
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'New {} Bedroom Apartments On Daft'.format(num_beds)
    msg['From'] = gmail_user
    msg['To'] = "; ".join(to)
    sent_from = gmail_user


    text = 'New Listings:\n\n'
    html_links = ''
    for property in properties:
        # Get user template to send in email
        template = ""
        for user in to:
            db_temp = get_template_response(user)
            db_temp = db_temp.format(num_beds = urllib.parse.quote(num_beds), neighbourhood = urllib.parse.quote(property['address'].split(', ')[1]))
            db_temp = db_temp.replace('\n', '%0A')
            db_temp = db_temp.replace(' ', '%20')
            template = template + f'{user}:%0A%0A{db_temp}%0A%0A%0A'

        text += f"Address: {property['address']} ({property['latitude']}N, {property['longitude']}E)\nPrice: {property['price']}\n{property['link']}\n\n"
        html_links += f'<li><a href="{property["link"]}">{property["address"]} ({property["latitude"]}N, {property["longitude"]}E) - {property["price"]}</a> | <a href="mailto:{gmail_user}?subject=Interested%20In%20Property%20{property["id"]}&body={urllib.parse.quote(property["address"])}%0A%0A{template}">Interested?</a></li>'
    html = f"""\
    <html>
        <head></head>
        <body>
            <p><b>Properties Below:</b><br><br></p>
            <ul>
            {html_links}
            </ul>
        </body>
    </html>"""

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_pw)
        smtp_server.sendmail(sent_from, to, msg.as_string())
        smtp_server.close()
        print('Email sent successfully at {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception as ex:
        print('Error encountered: ',ex)

if __name__ == "__main__":
    send_daft_email(None, None, None)