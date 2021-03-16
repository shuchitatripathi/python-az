import os
import cmd
import json
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

#keyVaultName = os.environ["KEY_VAULT_NAME"]
#KVUri = f"https://{keyVaultName}.vault.azure.net"

#credential = DefaultAzureCredential()
#client = SecretClient(vault_url=KVUri, credential=credential)

#print(f"Retrieving your secret from {keyVaultName}.")
#retrieved_secret = client.get_secret("kvtest1")
#print(f"Your secret is '{retrieved_secret.value}'.")

temp_json = {}
final_json = {}
rt_json = {}
i = 0
vnet = {"id" : "someid", "addressPrefix" : ["someAP", "new AP"]}
rt1 = {"name" : "apimRT", "id" : "apimRT-id"}
rt2 = {"name" : "aseRT", "id" : "aseRT-id"}

rt = [rt1, rt2]
print

#temp_json['testval'] = retrieved_secret.value
#temp_json['vnet-info'] = client.get_secret("routeable-vnet").value
#final_json = json.dumps(temp_json)
#print(final_json)
#print("Json things ahead")
for key,value in vnet.items():
    temp_json[key] = value
    final_json["vnet"] = temp_json
#final_json = json.dumps(final_json)
print(final_json)

temp_json = {}
for r in rt:
    rt_json = {}
    temp_var = ""
    for key, value in r.items():
        if key == 'name':
            temp_var = value
        else:
            rt_json[key] = value
    temp_json[temp_var] = rt_json
    #temp_json = json.dumps(temp_json)
#print(json.loads(temp_json))

final_json["route-table"] = temp_json
final_json = json.dumps(final_json)
print(final_json)
