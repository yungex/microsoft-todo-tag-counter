import msal
import requests
import re

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

# Step 3: Loop through each list and store tasks
all_titles_and_bodies = []
for task_list in task_lists:
    list_id = task_list["id"]

    tasks_response = requests.get(f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks", 
                                  headers=headers)
    tasks = tasks_response.json()["value"]

    for task in tasks:
        all_titles_and_bodies.append(task["title"])
        all_titles_and_bodies.append(task["body"]["content"])

# Step 4: Extract tags from task titles

tag_counts = {}

for title in all_titles_and_bodies:
    tags = re.findall(r"#(\w+)", title)
    for tag in tags:
        if tag in tag_counts:
            tag_counts[tag] += 1
        else:
            tag_counts[tag] = 1


# Step 5: Sort tags by count
tag_counts = dict(sorted(tag_counts.items(), key=lambda item: item[1], reverse=True))


# Step 6: Print tag counts
print(tag_counts)


# TODO: implement concurrent requests with asyncio to reduce latency
# TODO: calendar for planned
# TODO: AI intergration