'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

import smtplib


# For this to work with google smtp you must allow access from less secure apps
# on google's account site.  Otherwise one will not be able to log in.
def com_net_send_email(user, pwd, recipient, subject, body, smtp_server='smtp.gmail.com',
                       smtp_port=587):
    """
    Send email smtp server
    """
    TO = recipient if type(recipient) is list else [recipient]
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (user, ", ".join(TO), subject, body)
    if smtp_port == 465:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(user, pwd)
        server.sendmail(user, TO, message)
        server.quit()
    else:
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.sendmail(user, TO, message)
            server.close()
            return True
        except:
            return False
