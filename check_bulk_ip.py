import requests
import json
import re
import numpy as np

# Uncomment to read the AbuseIP API key from environment variable named ABUSEIP_KEY
# env_var = os.environ
# api_key = env_var["ABUSEIP_KEY"]

# Uncomment to read the AbuseIP API key from a file named k.txt
k_file = open('k.txt', 'r')
api_key = k_file.readline()


def unique(list1):
    x = np.array(list1)
    return np.unique(x)


with open('ips.txt', 'r') as file:
    data = file.read().replace('\n', ' ')

ValidIpAddressRegex = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

ips_l = re.findall(ValidIpAddressRegex,data)
ips = unique(ips_l)

for line in ips:
    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
        'ipAddress': line,
        'maxAgeInDays': '365',
    }
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    # Formatted output
    decodedResponse = json.loads(response.text)

    if decodedResponse["data"]["isPublic"] != False:
    # print(decodedResponse)
        if(len(decodedResponse["data"]["domain"]) != 0):
            dmm = decodedResponse["data"]["domain"]
        else:
            dmm = decodedResponse["data"]["hostnames"]
        print("  - "+ line.ljust(15)[:15] +" (" + decodedResponse["data"]["countryCode"].ljust(2)[:2] + ")  [ "+ str(decodedResponse["data"]["isp"]).ljust(20)[:20] +" ]  [ Reports: " + str(decodedResponse["data"]["totalReports"]).ljust(4)[:4] + "| Abuse Conf: " + str(decodedResponse["data"]["abuseConfidenceScore"]).ljust(4)[:4] + "]   " + str(dmm))
