import ldap3
from ldap3 import Server, Connection, ALL, NTLM
import json
import os

# Define file paths
config_file_path = r"C:\data\Python Scripting\config.json"
usernames_file_path = r"C:\data\Python Scripting\usernames1.txt"
output_file_path = r"C:\data\Python Scripting\active-directory-user-fullinfo.txt"

# Read credentials from the config file
with open(config_file_path, "r") as config_file:
    config = json.load(config_file)

ad_domain = config['domain']
ad_user = config['username']
ad_password = config['password']

# Construct the full username with domain
ad_user_with_domain = f"{ad_domain}\\{ad_user}"

# Connect to the AD server
server = Server(ad_domain, get_info=ALL)
conn = Connection(server, user=ad_user_with_domain, password=ad_password, authentication=NTLM, auto_bind=True)

# Function to get all attributes of a user from Active Directory
def get_user_attributes(username, connection):
    search_filter = f'(userPrincipalName={username})'
    connection.search('dc=hpinc,dc=com', search_filter, attributes=ldap3.ALL_ATTRIBUTES)
    if len(connection.entries) == 0:
        return None
    user_entry = connection.entries[0]
    return user_entry

# Read usernames from the file
with open(usernames_file_path, "r") as usernames_file:
    usernames = usernames_file.readlines()

# Open the output file
with open(output_file_path, "w") as output_file:
    for username in usernames:
        username = username.strip()
        if not username:
            continue
        
        try:
            user_attributes = get_user_attributes(username, conn)
            if user_attributes:
                output_file.write(f"{username}: {user_attributes}\n")
            else:
                output_file.write(f"{username}: N/A\n")
        except Exception as e:
            print(f"Failed to get attributes for {username}: {e}")

print("User attributes have been written to", output_file_path)

# Unbind the connection
conn.unbind()