import re
from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.subscription import SubscriptionClient
from tabulate import tabulate

credential = AzureCliCredential()

subscription_client = SubscriptionClient(credential)

subscriptions = subscription_client.subscriptions.list()
resource_group = 0
nsg_name = 0

ip_address = ((input("Enter your requested Ip details with range :")))

pattern = r'^10\.(82|92|93|100|108|110|111|112|115|116|117|118|119|120|122|123|124|125|126)\.'
if re.match(pattern, ip_address):   
    for sub in subscriptions:
        subscription_id = sub.subscription_id
        #print(f"Subscription ID: {subscription_id}")
        network_client = NetworkManagementClient(credential, subscription_id)


        vnets = network_client.virtual_networks.list_all()

        for vnet in vnets:
            for subnet in vnet.subnets:
                if subnet.address_prefix == ip_address:
                    nsg_id = subnet.network_security_group
                    print(" NSG assign for intered subnet is ||\t",nsg_id.id.split('/')[8])            
                
                    print(f"IP Address  || {ip_address}  \t VNet: || {vnet.name} \t \n subnet name : || {subnet.name}")
                    #print(f"\n \n VNet ID: \t {vnet.id}")
                    string_value={nsg_id.id.split('/')[4]}
                    resource_group= next(iter(string_value))

                    nsg_v={nsg_id.id.split('/')[8]}
                    nsg_name= next(iter(nsg_v))

                    print ( "\n RG Name : || \t", resource_group, "\t \t NSG name =||", nsg_name )
                
                    break
            else:
                continue
            break
        else:
            continue



        nsg_rules = network_client.security_rules.list(resource_group, nsg_name)

        rules_table = []

        for rule in nsg_rules:
            if rule.priority > 999:
                rule_info = [
                    rule.name,
                    rule.access,
                    rule.protocol,
                    rule.source_address_prefix,
                    rule.destination_address_prefix,
                    rule.priority,
                    rule.direction
                ]
                
                rules_table.append(rule_info)
            

        # define table headers
        headers = [
            "Rule Name",
            "Access",
            "Protocol",
            "Source Address Prefix",
            "Destination Address Prefix",
            "Priority",
            "Direction"
        ]

        # Print table
        print(tabulate(rules_table, headers=headers, tablefmt="grid"))
            
        break
    else:
        print(f"No VNet found containing IP Address: {ip_address}")
else:
    print(f"Opps.. Entered subnet not in azure scope \n \t Kindly check again")