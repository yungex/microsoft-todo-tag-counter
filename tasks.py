import msal
import requests

CLIENT_ID = "c25e3463-a244-46b0-b5af-b02c282659da"
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES =["Tasks.Read"]

# Step 1 - Login and get ticket
app = msal.PublicClientApplication(CLIENT_ID, 
                                   authority=AUTHORITY)
result = app.acquire_token_interactive(scopes=SCOPES, 
                                       port=8080)

if "access_token" not in result:
    print("Login failed")
    exit()

token = result["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Step 2: Get all task lists
lists_response = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", 
                              headers=headers)
task_lists = lists_response.json()["value"]

# Step 3: Loop through each list and print tasks
for task_list in task_lists:
    list_id = task_list["id"]
    list_name = task_list["displayName"]
    print(f"\n-- {list_name} --")

    tasks_response = requests.get(f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks", 
                                  headers=headers)
    tasks = tasks_response.json()["value"]

    for task in tasks:
        print(task["title"])