import os
import json
import datetime
import ast
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

#keyVaultName = os.environ["KEY_VAULT_NAME"]
#KVUri = f"https://{keyVaultName}.vault.azure.net"

#credential = DefaultAzureCredential()
#client = SecretClient(vault_url=KVUri, credential=credential)

def allresources(client):
    allresources = {}    
    temp_list = []
    secretname = os.environ["SECRET_NAME"]
    all_resources_str = client.get_secret(secretname)
    all_resources=ast.literal_eval(all_resources_str.value)
    for resources in all_resources:
        for key,value in resources.items():
            res_type = resources['type']
            res_type_shortend = res_type.split('/')[-1] # Splits the string and gives the last value of the separated list
            if res_type_shortend in allresources:
                temp_json = dict()
                temp_json["name"] = resources['name']
                temp_json["type"] = resources['type']
                temp_list.append(temp_json)
                allresources[res_type_shortend] = temp_list
            else:
                temp_json = {}
                temp_list = []
                temp_json["name"] = resources['name']
                temp_json["type"] = resources['type']
                temp_list.append(temp_json)
                allresources[res_type_shortend] = temp_list
            break
    
    #print(allresources)
    return allresources


def getJson(keyvault):
    KVUri = f"https://{keyvault}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    
    if keyvault == "testhpest":
        return "This is a test response for testhpest keyvault"
    
    final_json = dict()
    allresources_json = allresources(client)
       
    for key, value in allresources_json.items():
        if key == "resourceGroups":
            temp_json = dict()
            for val in value:
                for res_name, res_type in val.items():
                    if "system" in val["name"]:
                        secret_property = client.get_secret(val["name"])
                        temp_json["name"] = val["name"]
                        temp_json["id"] = secret_property.value
                        temp_json["resource_type"] = val["type"]
                        final_json["system_resource_group"] = temp_json
                    elif "app" in val["name"]:
                        secret_property = client.get_secret(val["name"])
                        temp_json["name"] = val["name"]
                        temp_json["id"] = secret_property.value
                        temp_json["resource_type"] = val["type"]
                        final_json["application_resource_group"] = temp_json
                    elif "dashboard" in val["name"]:
                        secret_property = client.get_secret(val["name"])
                        temp_json["name"] = val["name"]
                        temp_json["id"] = secret_property.value
                        temp_json["resource_type"] = val["type"]
                        final_json["dashboard_resource_group"] = temp_json
                    break
            
        elif key == "routeTables":
            temp_json = dict()
            temp_list = list()
            for val in value:
                for res_name, res_type in val.items():
                    secret_property = client.get_secret(val['name'])
                    temp_json["name"] = val["name"]
                    temp_json["id"] = secret_property.value
                    temp_json["resource_type"] = val["type"]
                    temp_list.append(temp_json.copy())
                    break
            final_json["route_tables"] = temp_list

        elif key == "virtualNetworks":
            temp_json = dict()
            for val in value:
                for res_name, res_type in val.items():
                    secret_property = client.get_secret(val['name'])
                    secret = json.loads(secret_property.value)
                    temp_json["name"] = val["name"]
                    temp_json["id"] = secret["id"]
                    temp_json["address_space"] = secret["addressPrefix"]
                    temp_json["resource_type"] = val["type"]
                    break
            final_json["virtual_network"] = temp_json

        elif key == "privateDnsZones":
            temp_json = dict()
            for val in value:
                for res_name, res_type in val.items():
                    secret_property = client.get_secret(val['name'])
                    secret = json.loads(secret_property.value)
                    temp_json["name"] = secret["name"]
                    temp_json["id"] = secret["id"]
                    temp_json["resource_type"] = val["type"]
                    break
            final_json["private_dns_zone"] = temp_json

        elif key == "virtualNetworkPeerings":
            temp_json = dict()
            temp_list = list()
            for val in value:
                for res_name, res_type in val.items():
                    secret_property = client.get_secret(val['name'])
                    temp_json["name"] = val["name"]
                    temp_json["id"] = secret_property.value
                    temp_json["resource_type"] = val["type"]
                    temp_list.append(temp_json.copy())
                    break
            final_json["virtual_network_peerings"] = temp_list

        elif key == "networkSecurityGroup":
            temp_json = dict()
            temp_list = list()
            for val in value:
                for res_name, res_type in val.items():
                    secret_property = client.get_secret(val['name'])
                    temp_json["name"] = val["name"]
                    temp_json["id"] = secret_property.value
                    temp_json["resource_type"] = val["type"]
                    temp_list.append(temp_json.copy())
                    break
            final_json["network_security_groups"] = temp_list
        
        elif key == "subnet":
            temp_json = dict()
            temp_list = list()
            for val in value:
                for res_name, res_type in val.items():
                    secret_property = client.get_secret(val['name'])
                    secret = json.loads(secret_property.value)
                    temp_json["name"] = val["name"]
                    temp_json["id"] = secret["id"]
                    temp_json["address_space"] = secret["addressPrefix"]
                    temp_json["resource_type"] = val["type"]
                    temp_list.append(temp_json.copy())
                    break
            final_json["subnets"] = temp_list

        elif key == "ServicePrincipal":
            temp_json = dict()
            for val in value:
                for res_name, res_type in val.items():
                    if "spn-1" in val["name"]:
                        secret_property = client.get_secret(val['name'])
                        secret = json.loads(secret_property.value)
                        print("IAC: ", secret)
                        temp_json["name"] = secret["name"]
                        temp_json["clientId"] = secret["clientID"]
                        temp_json["objectId"] = secret["objectID"]
                        temp_json["tenantId"] = secret["tenantID"]
                        temp_json["resource_type"] = val["type"]
                        final_json["iac-spn"] = temp_json 
                        break
                    elif "spn-2" in val["name"]:
                        secret_property = client.get_secret(val['name'])
                        secret = json.loads(secret_property.value)
                        print("App: ", secret)
                        temp_json["name"] = secret["name"]
                        temp_json["clientId"] = secret["clientID"]
                        temp_json["objectId"] = secret["objectID"]
                        temp_json["tenantId"] = secret["tenantID"]
                        temp_json["resource_type"] = val["type"]
                        final_json["app-spn"] = temp_json
                        break
                    break 
    
    final_json = json.dumps(final_json, indent=4)
    #print(final_json)

    return final_json


def getFormattedTimestamp():
    formatPattern = '{:%Y-%m-%d %H:%M:%S}'
    timeStamp = datetime.datetime.now()
    timeStampFormatted = formatPattern.format(timeStamp)
    return timeStampFormatted
