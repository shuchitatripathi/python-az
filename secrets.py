import os
import json
import datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def getSecret():
    keyVaultName = os.environ["KEY_VAULT_NAME"]
    #AZURE_CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
    #AZURE_CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]
    #AZURE_TENANT_ID = os.environ["AZURE_TENANT_ID"]
    KVUri = f"https://{keyVaultName}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    print(f"Retrieving your secret from {keyVaultName}.")
    retrieved_secret = client.get_secret("kvtest1")
    print(f"Your secret is '{retrieved_secret.value}'.")
    timeStampFormatted = getFormattedTimestamp()
    temp_json = {}
    final_json = {}
    rt_json = {}
    vnet = {"id" : "someid", "addressPrefix" : ["someAP", "new AP"]}

    for key,value in vnet.items():
        temp_json[key] = value
        final_json["vnet"] = temp_json

    final_json["timestamp"] = timeStampFormatted
    final_json["kvtest1"] = retrieved_secret.value
    final_json["test"] = "test_value"
    final_json = json.dumps(final_json)
    return final_json

def getFormattedTimestamp():
    formatPattern = '{:%Y-%m-%d %H:%M:%S}'
    timeStamp = datetime.datetime.now()
    timeStampFormatted = formatPattern.format(timeStamp)
    return timeStampFormatted
