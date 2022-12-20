import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv
from datetime import datetime

def send_daft_email(properties, to, num_beds):
    gmail_user = getenv('GMAIL_USER')
    gmail_pw = getenv('GMAIL_PW')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'New {} Bedroom Apartments On Daft'.format(num_beds)
    msg['From'] = gmail_user
    msg['To'] = "; ".join(to)
    sent_from = gmail_user

    text = 'New Listings:\n\n'
    html_links = ''
    for property in properties:
        text += f"Address: {property['address']} ({property['latitude']}N, {property['longitude']}E)\nPrice: {property['price']}\n{property['link']}\n\n"
        html_links += f'<li><a href="{property["link"]}">{property["address"]} ({property["latitude"]}N, {property["longitude"]}E) - {property["price"]}</a></li>'
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