import msal

CLIENT_ID = "c25e3463-a244-46b0-b5af-b02c282659da"
TENANT_ID = "1436dd5e-4ea4-4d00-9506-a5aff7ac2fe2"

AUTHORITY = f"https://login.microsoftonline.com/common"
SCOPES = ["Tasks.Read"]

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

result = app.acquire_token_interactive(scopes=SCOPES, port=8080)

if "access_token" in result:
    print("Login successful!")
    print(f"Signed in as: {result['id_token_claims']['preferred_username']}")
else:
    print("Login failed.")
    print(result.get("error_description"))