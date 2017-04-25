'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import smtplib

# http://stackoverflow.com/users/547050/david-okwii
# code from stackoverflow
def com_net_send_email(user, pwd, recipient, subject, body):
    """
    Send email via gmail account
    """
    TO = recipient if type(recipient) is list else [recipient]

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (user, ", ".join(TO), subject, body)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, TO, message)
        server.close()
        logging.info('successfully sent the mail')
        return True
    except:
        logging.info("failed to send mail")
        return False
