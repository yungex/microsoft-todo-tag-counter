# Microsoft To Do Tag Counter
*A Microsoft To Do companion app that shows you every hastag in your Microsoft To Do account and how often it's used.*

## The Problem
The Microsoft To Do app does not have a feature that allows the user to see all the tags they have assigned to their tasks, making it difficult to recall which tags have been used in the past. This makes it harder to stay organised and potentially causes duplicate/similar tags to occur. 

## Tech Stack
- Python
- Flask
- MSAL (Microsoft Authentication Library)
- Microsoft Graph API
- Jinja2 (templating)

## How It Works

1. User logs in with their Microsoft account via OAuth 2.0
2. The app fetches all task lists and tasks from Microsoft To Do using Graph API
3. Task titles and notes are scanned for #hashtags using regex
4. Tags are counted and displayed sorted by frequency

## Setup
1. Clone this repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with:
    - CLIENT_ID=your-client-id
    - CLIENT_SECRET=your-client-secret
6. Run `python app_web.py`
7. visit `http://localhost:5000`

## Challenges & What I learned
- Microsoft personal account app registration has been deprecated so I had to register with Azure directly.
- I had to learn the difference between public and confidential OAuth clients when my flask app required a client secret that my earlier CLI script didn't need.
- I accidently committed my .env file containing that secret to Git. GitHub's push protection caught this before it went public, which taught me to rewrite git history safely and properly rotate exposed credentials.

## Future improvements
- Improved front end
- Live updates
- Implement concurrent requests with asyncio to reduce latency
- Click a tag to see related tasks