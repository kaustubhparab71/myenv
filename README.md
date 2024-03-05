<div style="font-family: Arial, sans-serif;">

# Azure NSG Checker

## Introduction

<p style="font-size: 16px;">This Python script automates the process of checking Network Security Group (NSG) details for specified subnets within the Azure environment. It eliminates the need for manual checks on the Azure portal, providing convenience and efficiency.</p>

## Script Initiative

- **Automated Subnet Verification**: The script automatically verifies whether the requested subnets belong to the Azure environment.
- **Efficient NSG Exploration**: Eliminates manual exploration on the Azure portal by fetching NSG details programmatically.
- **Comprehensive Details**: Provides information on VNet, Resource Group, Subnet Range, global rules, default rules, and custom rules associated with the NSG.

## Script Benefits

- **Streamlined Data Collection**: Easily gather NSG data by simply entering the requested subnets.
- **Automated Environment Check**: No manual verification needed to determine if entered subnets are within the Azure environment.
- **Quick Insights**: Obtain comprehensive NSG details with just a single click.
- **Reduced Manual Effort**: Eliminates the need for frequent logins to the Azure portal for NSG details.

## Script Usage

1. **Installation**: Install required Azure packages and Azure CLI.
2. **Run Script**: Execute the Python script in the terminal.
3. **Enter Subnet**: Input the requested subnet(s) when prompted (format: `x.x.x.x/x`).
    (*Note - there are some specific subnet range are belong to Azure Cloud so for that filteration we use python RE module)
    ![image](https://github.com/kaustubhparab71/kvp-pendharkar/assets/33633535/1fd0b419-4437-4bdb-8c48-f8f4006d1eea)
   
5. **Retrieve Details**: Hit Enter to fetch NSG details (may take some time for searching across subscriptions).
6. **Outcome**: Receive details of NSG associated with the specified subnet(s).
   
  [![Watch the video](https://github.com/kaustubhparab71/kvp-pendharkar/assets/33633535/543ce3d4-9186-4668-9e6f-548a563db771)

## Prerequisites

- **Azure CLI**: Install Azure CLI on your system.
- **Python 3.11 or lower**: Ensure Python is installed.
- **VS Code**: Install Visual Studio Code.
- **Python Packages**: Install required packages using pip:
  - `pip install re`
  - `pip install azure.identity`
  - `pip install azure.mgmt.network`
  - `pip install azure.mgmt.subscription`
  - `pip install tabulate`

## Azure Account Connection

1. Run the following command in the command prompt:
 -'AZ login'
