'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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

from ldap3 import Server, Connection, ALL


class CommonLDAP:
    """
    Class for interfacing with ldap server
    """

    def __init__(self, ldap_server, ou_name, dc_name):
        # Initialize connection
        self.ldap_inst = Connection(ldap_server, port=636, use_ssl=True, auto_bind=True)

    def com_ldap_unbind(self):
        # perform the Unbind operation
        self.ldap_inst.unbind()

'''
below is all python-ldap, moving to ldap3
'''
# import ldap
#
# from . import common_global
#
#
# class CommonLDAP:
#     """
#     Class for interfacing with ldap server
#     """
#
#     def __init__(self, ldap_server, ou_name, dc_name):
#         # Initialize connection
#         try:
#             self.con = ldap.initialize('ldap://%s', ldap_server)
#         except ldap.LDAPError as err_code:
#             print((err_code.message['info']))
#             if isinstance(err_code.message, dict) and 'desc' in err_code.message:
#                 print((err_code.message['desc']))
#             else:
#                 print(err_code)
#         # Bind to the server (ie. actually connect) - not needed as simple_bind for check
#         # self.con.simple_bind("ou=People,dc=hotbot,dc=com")
#         self.ou_name = ou_name
#         self.dc_name = dc_name
#
#     def com_ldap_logon(self, user_name, user_password):
#         """
#         Ldap logon check
#         """
#         common_global.es_inst.com_elastic_index('info', {"ldap login": user_name})
#         try:
#             dn_name = "sAMAccountName=" + user_name + ",dc=" + self.dc_name + ",dc=local"
#             self.con.simple_bind_s(dn_name, user_password)
#         except ldap.INVALID_CREDENTIALS as err_code:
#             return "INVALID_LOGIN"
#         except ldap.LDAPError as err_code:
#             print((err_code.message['info']))
#             if isinstance(err_code.message, dict) and 'desc' in err_code.message:
#                 print((err_code.message['desc']))
#             else:
#                 print(err_code)
#
#     def com_ldap_close(self):
#         """
#         Close the connection
#         """
#         self.con.unbind_s()
