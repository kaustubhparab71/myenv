from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.subscription import SubscriptionClient
from tabulate import tabulate
import csv

credential = AzureCliCredential()

subscription_client = SubscriptionClient(credential)

subscriptions = subscription_client.subscriptions.list()

#subscription_id= '9100e0c3-b7eb-47b9-aad8-7d55e49d5eac'

data = []

for sub in subscriptions:
    subscription_id = sub.subscription_id
    network_client = NetworkManagementClient(credential, subscription_id)

    virtual_networks = network_client.virtual_networks.list_all()
    for vnet in virtual_networks:
        # Get all subnets within each virtual network
        subnets = network_client.subnets.list(
            vnet.id.split('/')[4],
            vnet.name
        )
        
        for subnet in subnets:
            # Check if the subnet has a Network Security Group attached
            if subnet.network_security_group is not None:
                nsg_id = subnet.network_security_group.id


                # Get NSG details
                vid = nsg_id.split('/')[4]
                nid = nsg_id.split('/')[-1]
                #print (f"{nsg_id} \n {vid} \n {nid}")
                nsg = network_client.network_security_groups.get(vid,nid)  # Extract the NSG name
                

                # Check if the NSG has any security rules
                if not nsg.security_rules:
                    data.append({
                        'Subscription ID': subscription_id,
                        'Resource Group': vnet.id.split('/')[4],
                        'Virtual Network': vnet.name,
                        'Subnet': subnet.name,
                        'NSG Name': nsg.name
                    })
        
csv_file = 'subnet_nsg_data.csv'
csv_columns = ['Subscription ID', 'Resource Group', 'Virtual Network', 'Subnet', 'NSG Name']

try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    print(f"Data written to {csv_file} successfully!")
except IOError:
    print("I/O error occurred while writing to the CSV file.")
