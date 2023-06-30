# Module for authenticate against the REST API of Azure

import requests
import json
import os
from azure.identity import ManagedIdentityCredential

# Get access token from managed identity
def get_access_token_from_managed_identity():
    # Create request
    managedIdentity = ManagedIdentityCredential()
    access_token = managedIdentity.get_token("https://management.azure.com/.default").token
    if access_token is None:
        raise Exception("Managed identity and Service principal not available. No authentication method is available")
        return None
    else:
        return access_token

# Get access token
def get_access_token():
    # Get environment variables
    try:
        tenant_id = os.environ["TENANT_ID"]
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]
    except:
        print('No local credentials available; use Managed identity')
        tenant_id = None
        client_id = None
        client_secret = None
    
    # Decide about auth method
    if tenant_id is None or client_id is None or client_secret is None:
        #Get access token from managed identity
        return get_access_token_from_managed_identity()
    else:    
        # Create payload
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "resource": "https://management.azure.com/"
        }

        # Create request
        response = requests.post(f"https://login.microsoftonline.com/{tenant_id}/oauth2/token", data=payload)

        # Get access token
        access_token = json.loads(response.text)["access_token"]

        if access_token is None:
            raise Exception("Managed identity and Service principal not available. No authentication method is available")
            return None

        return access_token