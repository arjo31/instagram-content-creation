import sys

sys.dont_write_bytecode = True

import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import google.generativeai as genai
import uvicorn
from bson.json_util import dumps
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from moviepy.editor import VideoFileClip, concatenate_videoclips

from db.config import ConfigDB
from models.model import User

load_dotenv()

GOOGLE_GEMINI_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')

app = FastAPI()

origins = ["http://localhost:8501"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = ConfigDB()
db = client.createDB()
    
@app.post("/create-caption-from-video")
async def create_caption_from_video(file : UploadFile = File(...), data: str = Form(...)):
    try:
        video_file_path = os.path.join(".", file.filename)
        print(file)
        with open(video_file_path, "wb") as video_file:
            video_file.write(await file.read())

        if os.path.getsize(video_file_path)==0:
            raise Exception("Uploaded file is empty or corrupted")

        with VideoFileClip(video_file_path) as video_clip:
            video_clip = concatenate_videoclips([video_clip])
            video_clip.write_videofile("Temp.mp4")

        genai.configure(api_key=GOOGLE_GEMINI_KEY)
        video_file = genai.upload_file(path="Temp.mp4")
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        system_prompt='''
            You are a very talented and popular content creator for Spillmate, a cutting-edge AI chatbot dedicated to mental health support. Spillmate combines proven psychological techniques, machine learning, and natural language processing to provide empathetic and effective conversations.  Spillmate is a project aimed to provide quality mental health support for everyone right on your fingertips.
            Spillmate is your pocket therapist, an AI assistant who is empathetic, supportive and judgement-free, and backed by science. It uses Cognitive Behavioral Therapy (CBT) principles and provides effective advice based on tried and tested CBT methods.

            You will receive a video, and your task is to:

            1. Extract Key Points: Identify the most significant moments and themes from the video.
            2. Create Engaging Content: Craft an engaging and captivating narrative that is perfect for Instagram reels.
            3. Write a Beautiful Caption: Compose a thoughtful and attention-grabbing caption that resonates with the audience.
            4. Include Relevant Hashtags: Add appropriate and trending hashtags to maximize reach and engagement.
            Please adhere to the following format for the output:

            1. Music Recommendation: (Optional - Suggest background music that fits the video's mood)
            2. Caption: (Write a compelling caption that encourages interaction and shares the video's essence)
            3. Hashtags: (Include relevant and popular hashtags to boost visibility)

            Ensure that the content is visually appealing, emotionally engaging, and maintains a consistent tone suitable for Spillmate's supportive and uplifting brand.
        '''
        config = {
            'max_output_tokens' : 4096,
            'temperature' : 2,
            'top_p' : 0.99,
        }
        caption = model.generate_content([system_prompt + data, video_file], generation_config=config)
        print("Uploaded successfully to Google AI Studio")
        return JSONResponse(content={'message' : caption.text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=500)
    finally:
        if os.path.exists(video_file_path):
            os.remove(video_file_path)
        if os.path.exists(r"Temp.mp4"):
            os.remove(r"Temp.mp4")

@app.post("/create-post")
async def create_post(user_input : str = Form(...)):
    try:
        genai.configure(api_key=GOOGLE_GEMINI_KEY)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        system_prompt='''
            You are a talented and popular content creator for Spillmate, a cutting-edge AI chatbot dedicated to mental health support. Spillmate combines proven psychological techniques, machine learning, and natural language processing to provide empathetic and effective conversations.Spillmate is your pocket therapist: an AI assistant who is empathetic, supportive, judgment-free, and backed by science. It uses Cognitive Behavioral Therapy (CBT) principles to provide effective advice based on tried and tested CBT methods.

            You will receive a request from the user regarding a specific topic. Your task is to create a captivating Instagram post with an attractive caption and engaging content based on the user's requested topic. The content must be absolutely related to the subject matter of the topic. The caption must be short and crisp (maximum 5 sentences). Include relevant hashtags to maximize engagement.
        '''
        config = {
        'max_output_tokens' : 4096,
        'temperature' : 1,
        'top_p' : 0.99,
        }
        content = model.generate_content([system_prompt, user_input], generation_config=config)
        post_content = content.text
        return JSONResponse(content={'message' : post_content}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=500)
    
@app.post("/generate-reply")
async def create_post(comment : str = Form(...)):
    try:
        genai.configure(api_key=GOOGLE_GEMINI_KEY)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        system_prompt='''
        You are a very talented and popular content creator for Spillmate, a cutting-edge AI chatbot dedicated to mental health support. Spillmate combines proven psychological techniques, machine learning, and natural language processing to provide empathetic and effective conversations.  Spillmate is a project aimed to provide quality mental health support for everyone right on your fingertips.
        Spillmate is your pocket therapist, an AI assistant who is empathetic, supportive and judgement-free, and backed by science. It uses Cognitive Behavioral Therapy (CBT) principles and provides effective advice based on tried and tested CBT methods.

        You will receive a comment from a user on Instagram. Your task is to provide a short (2-3 sentences) and professional reply to the comment, ensuring that it aligns with the goals and aims of Spillmate, also ensuring that it is absolutely relevant to the subject matter of the comment. Avoid using hashtags in your response.
        '''
        config = {
        'max_output_tokens' : 4096,
        'temperature' : 2,
        'top_p' : 0.99,
        }
        content = model.generate_content([system_prompt, comment], generation_config=config)
        reply = content.text
        return JSONResponse(content={'message' : reply}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=500)
    
@app.post("/generate-linkedin-content")
async def linkedin_post(prompt : str = Form(...), max_length : int = Form(...)):
    try:
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

        model = genai.GenerativeModel(model_name="gemini-1.5-pro")

        system_prompt = '''
        You are an AI assistant for Spillmate, a personalized AI chatbot for mental health support, tasked with creating professional and engaging LinkedIn content.

        Spillmate's brand voice is empathetic, supportive, and non-judgmental. It communicates with gentle confidence, using clear and accessible language. The tone should be professional yet personalized, always encouraging and respectful. Maintain an optimistic outlook while acknowledging the challenges of mental health.

        Key content guidelines for LinkedIn:
        1. Professional tone that aligns with Spillmate's brand voice
        2. Focus on mental health insights, supportive content, and company updates
        3. Encourage engagement through thoughtful questions and supportive calls-to-action
        4. Use appropriate hashtags (usually 3-5) related to mental health and wellbeing
        5. Keep post length within the user-specified character range
        6. Use line breaks for readability
        7. Ensure all content is sensitive to mental health issues and avoids potentially triggering language
        8. Promote the benefits of AI support in mental health while maintaining a human touch
        9. Share success stories or testimonials (anonymized) to build trust and credibility
        10. Provide practical tips for mental wellbeing that align with Spillmate's supportive approach'''

        response = model.generate_content(system_prompt + f"\n\nGenerate content within {max_length} characters:\n\n" + prompt)
        ans = response.text[:max_length]
        return JSONResponse(content={'message' : ans}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=500)

@app.post("/generate-twitter-content")
async def twitter_post(prompt : str = Form(...)):
    try:
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

        model = genai.GenerativeModel(model_name="gemini-1.5-pro")

        system_prompt = '''
            You are one of the best and popular content creators of Spillmate on Twitter.
            Spillmate is a project aimed to provide quality mental health support for everyone right on your fingertips.
            Spillmate is your pocket therapist, an AI assistant who is empathetic,
            supportive and judgement-free, and backed by science. It uses Cognitive Behavioral Therapy (CBT) principles
            and provides effective advice based on tried and tested CBT methods.
            The key content guidelines for Twitter content creation:
            1. Stick to the maximum linit of 280 characters per tweet and reply.
            2. Align with the empathetic brand image of Spillmate.
            3. The main focus is on insights, coping mechanisms and adaptive measures to take care of your mental health.
            4. Company updates, brand insights and relevant content which endorse Spillmate.
            5. Use three to five appropriate hashtags related to the brand, mental health awareness and wellbeing.
            6. Avoid using line breaks. Use suitable emojis.
            7. Avoid potentially triggering, explicit or offensive language
            8. Provide testimonials and success stories to build trust and credibility.
            9. Engagement through thoughtful questions and supportive calls-to-action.
            10. Write only the post or reply. Do not explain with headings.'''
        MAX_LENGTH = 280

        response = model.generate_content(system_prompt + prompt)
        ans = response.text[:MAX_LENGTH]
        return JSONResponse(content={'message' : ans}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=501)
    
@app.post("/login")
async def login(username : str = Form(...), password : str = Form(...)):
    try:
        user = {'username' : username, 'password' : password}
        if db.find_one({"username" : user['username']}):
            user_records = db.find_one({"username" : user['username']})
            if user['password']==user_records['password']:
                return JSONResponse(content={'message' : "Login successful", 'name' : user_records['name']}, status_code=200)
            else:
                return JSONResponse(content={'message' : "Password is incorrect"}, status_code=401)
        return JSONResponse(content = {'message' : "Username not found"}, status_code=401)
    except Exception as e:
        return JSONResponse(content = {"message" : str(e)}, status_code=500)

@app.post("/signup")
async def signup(name : str = Form(...), username : str = Form(...), email : str = Form(...), password : str = Form(...)):
    try:
        user = {
            'name' : name,
            'username' : username,
            'email' : email,
            'password' : password,
            'chats' : []
        }
        if db.find_one({'username' : user['username']}):
            return JSONResponse(content={'message' : "Username already exists"}, status_code=401)
        else:
            db.insert_one(user)
            return JSONResponse(content = {'message' : "Signup successful"}, status_code=200)
    except Exception as e:
        return JSONResponse(content = {"message" : str(e)}, status_code=500)
    
@app.get("/details")
async def get_details():
    try:
        details = []
        for doc in db.find():
            id = str(doc['_id'])
            det = dict(list(dict(doc).items())[1:])
            det['id'] = id
            details.append(det)
        return JSONResponse(content={'message': details}, status_code=200)
    except Exception as e:
        return JSONResponse(content = {"message" : str(e)}, status_code=500)

@app.get("/delete")
async def delete_records():
    db.delete_many({})
    return JSONResponse(content={'message' : "Deleted all records"}, status_code=200)

if __name__=="__main__":
    uvicorn.run("fast_server:app", host="0.0.0.0", port=5000, reload=True)