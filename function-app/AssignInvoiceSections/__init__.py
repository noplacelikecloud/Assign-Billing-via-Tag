    # This application create invoice sections in azure billing per tag on subscriptions. If the section is not present on the invoice, it will be created.
    # If the section is present, subscriptions with the tag will be added to the section.
    # For authentication use a managed identity. If not available, use a service principal.
    #
    # REST API will be used


import os
import json
import requests
import logging
import time
from .AADauth import *
from .helper import *

import azure.functions as func


def main(mytimer: func.TimerRequest, context: func.Context) -> None:
    token = get_access_token()

    # Get environment variables
    BILLING_ACCOUNT_NAME = os.environ["BILLING_ACCOUNT_ID"]


    # Get Billing Profiles
    billing_profiles = list_billing_profiles(BILLING_ACCOUNT_NAME, token)

    for billing_profile_name in billing_profiles:
        
        tag_list = []

        # Get Subscriptions from Billing Profile
        subscriptions = get_subscriptions_from_billingProfile(billing_profile_name["name"], token)

        subscriptionsInScope = []

        for subscripion in subscriptions:
            # Get Tag "InvoiceSection" if exists
            tags = get_tags_from_subscription(subscripion["properties"]["subscriptionId"], token)
            if tags is not None:
                if "InvoiceSection" in tags:
                    subscriptionsInScope.append(subscripion)
                    invoice_section = tags["InvoiceSection"]
                    if invoice_section not in tag_list:
                        tag_list.append(invoice_section)
                else:
                    continue
            else:
                continue

        # Get Invoice Sections and check if all tags are present
        invoice_sections = get_invoice_sections(BILLING_ACCOUNT_NAME,billing_profile_name["name"], token)

        for tag in tag_list:
            tagFlag = False
            for section in invoice_sections:
                if tag == section["properties"]["displayName"]:
                    tagFlag = True
                    logging.info(f"Section {section['name']} is already present in Billing Profile")
                
            if not tagFlag:
                logging.info (f"Section {section['name']} is not present in Billing Profile! Creating new one:")
                # Create invoice section
                if create_invoice_section(BILLING_ACCOUNT_NAME,billing_profile_name["name"], token, tag):
                    logging.info(f"Section {tag} is created in Billing profile")
                else:
                    logging.error(f"Error while creating section {tag}!")
        
        time.sleep(5)
        invoice_sections = get_invoice_sections(BILLING_ACCOUNT_NAME,billing_profile_name["name"], token)

        logging.debug(f'Subscriptions in Scope: {subscriptionsInScope}')

        # Add subscriptions to invoice section
        for subscripion in subscriptionsInScope:
            subscriptionId = subscripion["properties"]["subscriptionId"]
            # Get Tag "InvoiceSection" if exists
            tags = get_tags_from_subscription(subscriptionId, token)
            if "InvoiceSection" in tags:
                invoice_section = tags["InvoiceSection"]
                # Get invoice section id
                for section in invoice_sections:
                    if section["properties"]["displayName"] == invoice_section:
                        invoice_section_id = section["id"]
                        break
                    else:
                        continue
                if invoice_section_id == None:
                    raise Exception("Invoice section not found during assignment")

                # Assign subscription to invoice section
                if assign_subscription_to_invoice_section(BILLING_ACCOUNT_NAME, token, invoice_section_id, subscripion["properties"]["subscriptionId"]):
                    logging.info (f"Subscription {subscriptionId} assigned to invoice section {invoice_section_id}")
                else:
                    logging.error (f"Error while assign Subscription {subscriptionId} to invoice section {invoice_section_id}")
            else:
                logging.info(f'Subscription {subscripionId} has no Tag "InvoiceSection"')
                continue