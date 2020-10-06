from common import common_network_cifs

# works fine against my main samba array

cifs_inst = common_network_cifs.CommonCIFSShare()
cifs_inst.com_cifs_open('th-zfs-1.beaverbay.local')
print(cifs_inst.com_cifs_share_list_by_connection())
for data in cifs_inst.com_cifs_walk(share_name='TankAll', file_path='Backups'):
    print(data)


# smb_stuff = common_network_cifs.CommonCIFSShare()
# addr, share, path = common_string.com_string_unc_to_addr_path(dir_path)
# smb_stuff.com_cifs_connect(addr)
# for dir_data in smb_stuff.com_cifs_walk(share, path):
#     pass

# new way, but can't get guest to work
# cifs_inst = common_network_cifs.CommonNetworkCIFS('th-zfs-1.beaverbay.local', 'TankAll')
# cifs_inst.com_cifs_directory_file_list(r'\\th-zfs-1.beaverbay.local\TankAll\Backups')
# cifs_inst.com_cifs_file_walk(r'\\th-zfs-1.beaverbay.local\TankAll\Backups')