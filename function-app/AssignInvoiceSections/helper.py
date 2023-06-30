import os
import requests
import json
import logging
import re

BILLING_ACCOUNT_NAME = os.environ["BILLING_ACCOUNT_ID"]

# Get all subscriptions from billing profile
def get_subscriptions_from_billingProfile(BillingProfileName,token):
    #Create request
    response = requests.get(f"https://management.azure.com/providers/Microsoft.Billing/billingAccounts/{BILLING_ACCOUNT_NAME}/billingProfiles/{BillingProfileName}/billingSubscriptions?api-version=2020-05-01", headers={"Authorization": f"Bearer {token}"})

    # Get subscriptions
    subscriptions = json.loads(response.text)["value"]

    if subscriptions is None:
        raise Exception("No subscriptions found")
        return None
    else:
        return subscriptions

# Get all invoice sections
def get_invoice_sections(BillingAccountName,BillingProfileName, token):
    #Create request
    response = requests.get(f"https://management.azure.com/providers/Microsoft.Billing/billingAccounts/{BillingAccountName}/billingProfiles/{BillingProfileName}/invoiceSections?api-version=2020-05-01", headers={"Authorization": f"Bearer {token}"})

    # Get invoice sections
    invoice_sections = json.loads(response.text)["value"]

    if invoice_sections is None:
        logging.error(f"No invoice sections with name {BillingAccountName}")
        return None
    else:
        return invoice_sections

# Create invoice section
def create_invoice_section(BillingAccountName,BillingProfileName, token, invoice_section_name:str):
    #Remove whitespaces and special characters from name for id
    invoice_section_id = re.sub(r'[\s\-()\/\\:;,?!\'"’‘“”]', '', invoice_section_name)  
    logging.info(f"Create invoice section {invoice_section_name} with id {invoice_section_id}")
    #Create request
    payload = {
        "properties": {
            "displayName": f'{invoice_section_name}',
            "labels": {},
            "tags": {}
        }
    }
    url = f"https://management.azure.com/providers/Microsoft.Billing/billingAccounts/{BillingAccountName}/billingProfiles/{BillingProfileName}/invoiceSections/{invoice_section_id}?api-version=2020-05-01"
    response = requests.put(url, headers={"Authorization": f"Bearer {token}"}, json=payload)

    if response.status_code == 200 or response.status_code == 202:
        return True
    else:
        logging.error(f"Invoice section {invoice_section_name} not created \n {response.text}")
        return False

# Assign subscription to invoice section
def assign_subscription_to_invoice_section(BillingAccountName, token, invoice_section_id, subscription_id):    
    #Create request
    url = f'https://management.azure.com/providers/Microsoft.Billing/billingAccounts/{BillingAccountName}/billingSubscriptions/{subscription_id}/move?api-version=2020-05-01'
    payload = {
        "destinationInvoiceSectionId": invoice_section_id
    }
    response = requests.post(url, headers={"Authorization": f"Bearer {token}"}, json=payload)

    if response.status_code == (200 or 202):
        return True
    else:
        logging.error(f"Error while assign Subscription {subscription_id}: \n {response.text}")
        return False

# List billing profiles
def list_billing_profiles(BillingAccountName, token):
    #Create request
    response = requests.get(f"https://management.azure.com/providers/Microsoft.Billing/billingAccounts/{BillingAccountName}/billingProfiles?api-version=2020-05-01", headers={"Authorization": f"Bearer {token}"})

    if response.status_code == 200:
        # Get billing profiles
        billing_profiles = json.loads(response.text)["value"]
    else:
        logging.error(f"No billing profiles found! Status Code: {response.status_code} \n {response.text}")
        exit()

    if billing_profiles is None:
        logging.error("No billing profiles found")
        return None
    else:
        l_billing_profiles = []
        for billing_profile in billing_profiles:
            l_billing_profiles.append(billing_profile)
        return l_billing_profiles

# Get tags from subscription
def get_tags_from_subscription(subscription_id, token):
    #Create request
    response = requests.get(f"https://management.azure.com/subscriptions/{subscription_id}?api-version=2020-01-01", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        # Get tags
        tags = json.loads(response.text)["tags"]

        if tags is None:
            raise Exception("No tags found")
            return None
        else:
            return tags
    else:
        (f"Subscription {subscription_id} is not available on resource manager. Continue")
        return None