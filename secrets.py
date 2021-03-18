import os
import json
import datetime
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def getSecret():
    timeStampFormatted = getFormattedTimestamp()
    temp_json = {}
    final_json = {}
    rt_json = {}
    vnet = {"id" : "someid", "addressPrefix" : ["someAP", "new AP"]}

    for key,value in vnet.items():
        temp_json[key] = value
        final_json["vnet"] = temp_json

    final_json["timestamp"] = timeStampFormatted
    final_json = json.dumps(final_json)
    return final_json

def getFormattedTimestamp():
    formatPattern = '{:%Y-%m-%d %H:%M:%S}'
    timeStamp = datetime.datetime.now()
    timeStampFormatted = formatPattern.format(timeStamp)
    return timeStampFormatted
