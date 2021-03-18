import os
import json
import datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def getSecret():
    temp_json = {}
    rt_json = {}
    final_json = {}
    
    keyVaultName = os.environ["KEY_VAULT_NAME"]
    KVUri = f"https://{keyVaultName}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    vnet_secret = client.get_secret("vnet")
    vnet = json.loads(vnet_secret.value)
    timeStampFormatted = getFormattedTimestamp()

    for key,value in vnet.items():
        temp_json[key] = value
        final_json["vnet"] = temp_json

    final_json["timestamp"] = timeStampFormatted
    final_json = json.dumps(final_json, indent=4)
    return final_json

def getFormattedTimestamp():
    formatPattern = '{:%Y-%m-%d %H:%M:%S}'
    timeStamp = datetime.datetime.now()
    timeStampFormatted = formatPattern.format(timeStamp)
    return timeStampFormatted
