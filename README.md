# Azure Function - AssignInvoiceSections

This repository contains a Python Azure Function that creates invoice sections in Azure Billing based on tags assigned to subscriptions. If the section is not present on the invoice, it will be created. If the section is already present, subscriptions with the specified tag will be added to the section.


## Function Description

The Azure Function performs the following tasks:

1. Authenticates against the Azure REST API using either a managed identity or a service principal.
2. Retrieves the billing profiles associated with the specified billing account.
3. Retrieves the subscriptions associated with each billing profile.
4. Checks if each subscription has a specific tag ("InvoiceSection") assigned to it.
5. If the tag is present, adds the subscription to the corresponding invoice section.
6. If the invoice section does not exist, creates a new invoice section and assigns the subscription to it.

## Prerequisites

To run this Azure Function, ensure the following prerequisites are met:

1. Azure subscription
2. Azure billing account with the necessary permissions
3. Python 3.10 or later installed
4. Azure Functions Core Tools installed
5. Azure CLI installed (for deployment)

## Setup Instructions

Follow these steps to set up and deploy the Azure Function:

1. Clone this repository: `git clone https://github.com/noplacelikecloud/Assign-Billing-via-Tag.git`
2. Navigate to the cloned repository: `cd Assign-Billing-via-Tag`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Configure the necessary environment variables:
   - `TENANT_ID`: Azure Active Directory tenant ID (optional, if using a service principal)
   - `CLIENT_ID`: Azure Active Directory client ID (optional, if using a service principal)
   - `CLIENT_SECRET`: Azure Active Directory client secret (optional, if using a service principal)
   - `BILLING_ACCOUNT_ID`: ID of the Azure billing account to use for billing
5. Test the function locally: `func start` (optional)
6. Deploy the function resource in Azure using Bicep in the infra folder or this Button:
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fnoplacelikecloud%2FAssign-Billing-via-Tag%2Fmaster%2Finfra%2Fmain_DtAButton.json)
8. Deploy the function to Azure:
   - Log in to Azure CLI: `az login`
   - Set the Azure subscription: `az account set --subscription <subscription_id>`
   - Deploy the function: `func azure functionapp publish <function_app_name>`

## Usage

Once the Azure Function is deployed, it will run automatically based on the specified schedule. It will check the assigned tags on the subscriptions and create or update the invoice sections accordingly.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please submit an issue or pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- This Azure Function was developed by [Your Name].
- The code for authenticating against the Azure REST API is based on the [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python).
- Special thanks to [Any additional acknowledgments].
