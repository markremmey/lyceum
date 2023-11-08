import os

b2c_tenant = "lyceummembers"
signupsignin_user_flow = "B2C_1_signup-signin"
editprofile_user_flow = "B2C_1_profileediting1"

resetpassword_user_flow = "B2C_1_passwordreset1"  # Note: Legacy setting.

authority_template = f"https://{b2c_tenant}.b2clogin.com/{b2c_tenant}.onmicrosoft.com/{signupsignin_user_flow}"

CLIENT_ID = "Enter_the_Application_Id_here" # Application (client) ID of app registration

CLIENT_SECRET = "Enter_the_Client_Secret_Here" # Application secret.

AUTHORITY = authority_template.format(
    tenant=b2c_tenant, user_flow=signupsignin_user_flow)
B2C_PROFILE_AUTHORITY = authority_template.format(
    tenant=b2c_tenant, user_flow=editprofile_user_flow)

B2C_RESET_PASSWORD_AUTHORITY = authority_template.format(
    tenant=b2c_tenant, user_flow=resetpassword_user_flow)

REDIRECT_PATH = "/getAToken"  

# This is the API resource endpoint
ENDPOINT = '' # Application ID URI of app registration in Azure portal

# These are the scopes you've exposed in the web API app registration in the Azure portal
SCOPE = []  # Example with two exposed scopes: ["demo.read", "demo.write"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session