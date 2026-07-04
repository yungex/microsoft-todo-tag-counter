from dotenv import load_dotenv
import os
from flask import Flask, redirect, request, session, render_template
import msal
import requests
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["Tasks.Read"]
REDIRECT_URI = "http://localhost:5000/callback"

def get_tag_counts(headers):
    # Step 1: Get all task lists
    lists_response = requests.get("https://graph.microsoft.com/v1.0/me/todo/lists", 
                                  headers=headers)
    task_lists = lists_response.json()["value"]

    # Step 2: Loop through each list and store tasks
    all_titles_and_bodies = []
    for task_list in task_lists:
        list_id = task_list["id"]

        tasks_response = requests.get(f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks", 
                                    headers=headers)
        tasks = tasks_response.json()["value"]

        for task in tasks:
            all_titles_and_bodies.append(task["title"])
            all_titles_and_bodies.append(task["body"]["content"])

    # Step 3: Extract tags from task titles

    tag_counts = {}

    for title in all_titles_and_bodies:
        tags = re.findall(r"#(\w+)", title)
        for tag in tags:
            if tag in tag_counts:
                tag_counts[tag] += 1
            else:
                tag_counts[tag] = 1


    # Step 4: Sort tags by count
    tag_counts = dict(sorted(tag_counts.items(), key=lambda item: item[1], reverse=True))


    # Step 5: Print tag counts
    return tag_counts

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
        msal_app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
        auth_url = msal_app.get_authorization_request_url(SCOPES, redirect_uri=REDIRECT_URI)
        return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    msal_app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    result = msal_app.acquire_token_by_authorization_code(code, scopes=SCOPES, redirect_uri=REDIRECT_URI)

    session["access_token"] = result["access_token"]
    return redirect("/tags")

@app.route("/tags")
def tags():
    token = session.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    tag_counts = get_tag_counts(headers)
    return render_template("tags.html", tag_counts = tag_counts)

if __name__ == "__main__":
    app.run(debug=True)