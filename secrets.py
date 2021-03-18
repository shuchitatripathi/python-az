import os
import json
import datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

def getSecret():
    final_json = {}
    temp_json = {}
    rt_json = {}
    temp_list = []
    i = 0

    vnet_secret = client.get_secret("vnet")
    vnet = json.loads(vnet_secret.value)
    timeStampFormatted = getFormattedTimestamp()

    for key,value in vnet.items():
        temp_json[key] = value
        final_json["vnet"] = temp_json

    temp_list = getAllRouteTables()

    final_json["route-tables"] = temp_list
    final_json["timestamp"] = timeStampFormatted
    final_json = json.dumps(final_json, indent=4)
    return final_json

def getAllRouteTables():
    temp_json = {}
    rt_json = {}
    rt_list = []
    i = 0

    secret_properties = client.list_properties_of_secrets()
    for secret in secret_properties:
        rt_json = {}
        if "RT" in secret.name:
            rt_json[secret.name] = client.get_secret(secret.name).value
            temp_json[i] = rt_json
            i+=1
    #print("TempJSON :", temp_json)

    for value in temp_json.values():
        #print("Value: ", value)
        rt_json = {}
        for key_rt, value_rt in value.items():
            rt_json['name'] = key_rt
            rt_json['id'] = value_rt
            rt_list.append(rt_json)

    return rt_list

def getFormattedTimestamp():
    formatPattern = '{:%Y-%m-%d %H:%M:%S}'
    timeStamp = datetime.datetime.now()
    timeStampFormatted = formatPattern.format(timeStamp)
    return timeStampFormatted
