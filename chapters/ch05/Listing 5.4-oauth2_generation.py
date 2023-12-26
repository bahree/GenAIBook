# write a function to implement oauth2 authentication for a web application running on azure
def oauth2():
    # import the required libraries
    from azure.identity import ClientSecretCredential
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    import os

    # get the credentials from the environment variables
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]
    tenant_id = os.environ["AZURE_TENANT_ID"]
    keyvault_name = os.environ["KEYVAULT_NAME"]
    secret_name = os.environ["SECRET_NAME"]

    # create the credential object
    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )

    # create the secret client object
    secret_client = SecretClient(
        vault_url=f"https://{keyvault_name}.vault.azure.net",
        credential=credential
    )

    # get the secret from the secret client
    secret = secret_client.get_secret(secret_name)

    # return the secret value
    return secret.value
