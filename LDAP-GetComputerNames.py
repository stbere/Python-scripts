import ldap3
from ldap3 import Server, Connection, ALL, NTLM
import json
import os
import re

# Define file paths
config_file_path = r"C:\data\Python Scripting\config.json"
usernames_file_path = r"C:\data\Python Scripting\usernames1.txt"
output_file_path = r"C:\data\Python Scripting\computer_names.txt"

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

# Function to search for computer names based on username patterns
def search_computer_name(username, connection):
    # Extract the main part of the username (before @)
    user_part = username.split('@')[0]
    
    # Define the search filter for computers starting with "W-10"
    search_filter = f'(cn=W-10*)'
    search_base = 'OU=Accounts,DC=hpinc,DC=com'
    connection.search(search_base, search_filter, attributes=['cn'])
    
    if len(connection.entries) == 0:
        return 'N/A'
    
    # Extract potential computer names
    computer_names = [entry.cn.value for entry in connection.entries]
    
    # Debug: Print the computer names found
    print(f"Computer names found: {computer_names}")
    
    # Define patterns to match the computer names against
    patterns = [
        re.compile(f'W10-{user_part}', re.IGNORECASE),
        re.compile(f'W10-{user_part[0]}{user_part.split(".")[-1]}', re.IGNORECASE),
        re.compile(f'W10-{user_part[:6]}', re.IGNORECASE)
    ]
    
    # Debug: Print the patterns being used
    print(f"Patterns: {[pattern.pattern for pattern in patterns]}")
    
    # Try to find a matching computer name
    for computer_name in computer_names:
        for pattern in patterns:
            if pattern.match(computer_name):
                return computer_name
    
    return 'N/A'

# Read usernames from the file
with open(usernames_file_path, "r") as usernames_file:
    usernames = usernames_file.readlines()

# Open the output file with UTF-8 encoding
with open(output_file_path, "w", encoding="utf-8") as output_file:
    for username in usernames:
        username = username.strip()
        if not username:
            continue
        
        try:
            computer_name = search_computer_name(username, conn)
            output_file.write(f"{username}: {computer_name}\n")
        except Exception as e:
            print(f"Failed to get computer name for {username}: {e}")

print("Computer names have been written to", output_file_path)

# Unbind the connection
conn.unbind()