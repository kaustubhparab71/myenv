from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient
from tabulate import tabulate
import csv

# Your Azure subscription ID
subscription_id = '9100e0c3-b7eb-47b9-aad8-7d55e49d5eac'

credential = AzureCliCredential()

network_client = NetworkManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

# Dictionary to store NSG information
nsg_data = {}

# Get all NSGs in the subscription
nsgs = network_client.network_security_groups.list_all()

for nsg in nsgs:
    # Get NSG rules
    #print (nsg.id.split('/')[4],nsg.name)

    nsg_rules = network_client.security_rules.list(
        nsg.id.split('/')[4],
        nsg.name
    )

    # Store NSG data with rules in the dictionary
    nsg_data[nsg.id] = {
        'nsg_name': nsg.name,
        'nsg_rules': list(nsg_rules)
    }

resource_groups = resource_client.resource_groups.list()

for resource_group in resource_groups:
    print(f"Resource Group: {resource_group.name}")
    subnets = network_client.subnets.list(resource_group.name)

# Get all subnets in the subscription
    #subnets = network_client.subnets.list_all()

    # Iterate through subnets and check if their IPs are not in any NSG rules
    for subnet in subnets:
        print (subnet)
        subnet_ip = subnet.address_prefix
        nsg_id = subnet.network_security_group.id if subnet.network_security_group else None

        if nsg_id:
            # Check if subnet IP is not present in any NSG rule
            found = False
            for nsg_id, nsg_info in nsg_data.items():
                for rule in nsg_info['nsg_rules']:
                    if rule.destination_address_prefix == subnet_ip:
                        found = True
                        break
                if found:
                    break

            # If the subnet IP is not present in any NSG rule, display the NSG data
            if not found:
                print(f"Subnet {subnet.name} in {subnet.id.split('/')[4]} has an NSG ({nsg_id}) without the subnet IP in any rules.")
