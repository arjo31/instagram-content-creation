# Instagram Content Creation Using AI

# About
An AI Tool which makes automatic content creation for Instagram, LinkedIn and Twitter (X) posts, which supports caption generation for posts, reels and also can generate replies for a comment. Built using Streamlit and utilizes FastAPI for API integration with frontend. Also uses Google Gemini API for content generation. MongoDB Database is used to store user details.

Website : [https://spillmatecontentcreation.streamlit.app/]

Note : The backend server which is hosted on Render (free version) takes about 1 minute and 30 seconds to spring back to life due to inactivity. So if you try out my website, please wait for about 1 minute and 30 seconds to use the application efficiently. Thanks for your patience!!

# Tech Stack
1. Python
2. Streamlit
3. FastAPI
4. Google Gemini API
5. MongoDB
6. MoviePy

## Steps To Run:

1. Install a virtual environment.

2. Install the required dependencies for running the app

```bash
pip install -r requirements.txt
```

3. Set up your .env file with the following key value pair

```bash
GOOGLE_GEMINI_API_KEY = <Your_Key>
MONGO_DB_URI = <Mongo_Db server key>
```

You will get the key from Google's AI Studio.

4. Start the frontend by running the command :

```bash
streamlit run app.py
```

5. Start the FastAPI Server by running the command :

```bash
cd src/server

python fast_server.py
```
