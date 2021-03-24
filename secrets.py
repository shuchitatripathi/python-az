import os
import json
import datetime
import platform
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

    srg_l = srg()
    final_json["system_resource_group"] = srg_l

    vnet_secret = client.get_secret("vnet")
    vnet = json.loads(vnet_secret.value)
    timeStampFormatted = getFormattedTimestamp()
    for key,value in vnet.items():
        temp_json[key] = value
        final_json["virtual_network"] = temp_json

    vnetp_l = vnetp()
    final_json["virtual_network_peering"] = [vnetp_l]
    
    temp_list = getAllRouteTables()
    final_json["route-tables"] = temp_list

    privdns_l = privdns()
    final_json["private_dns_zone"] = privdns_l

    final_json["network_security_groups"] = []
    final_json["subnets"] = []

    arg_l = arg()
    final_json["application_resource_group"] = arg_l

    iac_l = iac()
    final_json["iac_spn"] = iac_l

    app_spn_l = app_spn()
    final_json["app_spn"] = app_spn_l

    iac_svc_l = iac_svc()
    final_json["iac_svc"] = iac_svc_l

    app_svc_l = app_svc()
    final_json["app_svc"] = app_svc_l

    final_json["network_watcher"] = {}


    final_json["timestamp"] = timeStampFormatted
    #final_json["py_version"] = platform.python_version()
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

def srg():
    temp_json = {}
    temp_json["name"] = "system-rg"
    temp_json["id"] = "/subscription/resourceGruop/system-rg"
    temp_json["resource_type"] = "Microsoft.Network/virtualNetworks"

    return temp_json

def privdns():
    temp_json = {}
    temp_json["name"] = "abc-def.something.com"
    temp_json["id"] = "/subscription/privateDNS/def.something.com"
    temp_json["resource_type"] = "Microsoft.Network/privateDnsZones"

    return temp_json

def vnetp():
    temp_json = dict()
    temp_json["name"] = "vnet-peering-1"
    temp_json["id"] = "/subscription/vnetpeering1"
    temp_json["resource_type"] = "Microsoft.Network/virtualNetworks/virtualNetworkPeerings"

    return temp_json

def arg():
    temp_json = {}
    temp_json["name"] = "application-rg"
    temp_json["id"] = "/subscription/resourceGruop/application-rg"
    temp_json["resource_type"] = "Microsoft.Network/virtualNetworks"

    return temp_json

def iac():
    temp_json = {}
    temp_json["name"] = "spn-1"
    temp_json["clientId"] = "1234-1234"
    temp_json["objectId"] = "2345-2345"
    temp_json["tenantId"] = "3456-3456"
    temp_json["resource_type"] = "Microsoft.DirectoryServices/ServicePrincipal"

    return temp_json

def app_spn():
    temp_json = {}
    temp_json["name"] = "spn-2"
    temp_json["clientId"] = "abcd-1234"
    temp_json["objectId"] = "efgh-2345"
    temp_json["tenantId"] = "ijkl-3456"
    temp_json["resource_type"] = "Microsoft.DirectoryServices/ServicePrincipal"

    return temp_json

def iac_svc():
    temp_json = {}
    temp_json["name"] = "svc-1"
    temp_json["organizationName"] = "MetdataOrg"
    temp_json["projectName"] = "MetadataProj"
    temp_json["subscriptionId"] = "ijkl-3456"
    temp_json["resource_type"] = "Microsoft.DevOps/serviceEndpoints"

    return temp_json

def app_svc():
    temp_json = {}
    temp_json["name"] = "svc-2"
    temp_json["organizationName"] = "MetdataOrg"
    temp_json["projectName"] = "MetadataProj"
    temp_json["subscriptionId"] = "ijkl-3456"
    temp_json["resource_type"] = "Microsoft.DevOps/serviceEndpoints"

    return temp_json

def getFormattedTimestamp():
    formatPattern = '{:%Y-%m-%d %H:%M:%S}'
    timeStamp = datetime.datetime.now()
    timeStampFormatted = formatPattern.format(timeStamp)
    return timeStampFormatted
