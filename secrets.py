import os
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def getSecret():
   
    temp_json = {}
    final_json = {}
    rt_json = {}
    vnet = {"id" : "someid", "addressPrefix" : ["someAP", "new AP"]}

    for key,value in vnet.items():
        temp_json[key] = value
        final_json["vnet"] = temp_json
         
    final_json = json.dumps(final_json)
    return final_json
    #return "Test"
