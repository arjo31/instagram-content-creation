import os

import google.generativeai as genai
import uvicorn
import whisper
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from moviepy.editor import VideoFileClip, concatenate_videoclips

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

@app.post("/transcript-video")
async def transcript(file: UploadFile = File(...), id: str = Form(...), name: str = Form(...)):
    try:
        video_file_path = os.path.join(".", file.filename)
        audio_file_name = f"{os.path.splitext(file.filename)[0]}.mp3"
        audio_file_path = os.path.join(".", audio_file_name)

        with open(video_file_path, "wb") as video_file:
            video_file.write(await file.read())

        video_clip = VideoFileClip(video_file_path)
        video_clip.audio.write_audiofile(audio_file_path)
        video_clip.close()

        os.remove(video_file_path)

        model = whisper.load_model('base')
        result = model.transcribe(audio_file_path, verbose = True)
        
        os.remove(audio_file_path)
        return JSONResponse(content={'message' : result['text']}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=501)

@app.post("/create-caption")
async def create_caption(transcription: str = Form(...)):
    try:
        genai.configure(api_key=GOOGLE_GEMINI_KEY)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        prompt='''
        You are an excellent content writer for Spillmate. Spillmate is your personalized AI chatbot for mental health support. Spillmate leverages proven techniques in psychology, machine learning and natural language processing to understand concerns and emotions and have supportive conversations.
        You will recieve a video transcription. You need to extract the important points from the video and since you are an axcellent content creator for Instagram, you will create a captivating and engaging content for the reel, along with a beautiful caption. Provide relevant hashtags as well.
        '''
        config = {
            'max_output_tokens' : 2048,
            'temperature' : 1,
            'top_p' : 0.95,
        }
        caption = model.generate_content([prompt, transcription], generation_config=config)
        return JSONResponse(content={'message' : caption.text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=501)
    
@app.post("/create-caption-from-video")
async def create_caption_from_video(file : UploadFile = File(...), data: str = Form(...)):
    try:
        video_file_path = os.path.join(".", file.filename)

        with open(video_file_path, "wb") as video_file:
            video_file.write(await file.read())

        video_clip = VideoFileClip(video_file_path)
        video_clip = concatenate_videoclips([video_clip])
        video_clip.write_videofile(r"temp.mp4")

        genai.configure(api_key=GOOGLE_GEMINI_KEY)
        video_file = genai.upload_file(path=video_file_path)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        prompt='''
        You are an excellent content writer for Spillmate. Spillmate is your personalized AI chatbot for mental health support. Spillmate leverages proven techniques in psychology, machine learning and natural language processing to understand concerns and emotions and have supportive conversations.
        You will recieve a video. You need to extract the important points from the video and since you are an axcellent content creator for Instagram, you will create a captivating and engaging content for the reel, along with a beautiful caption. Provide relevant hashtags as well.
        Follow a fixed pattern while providing content for each video.
        Pattern is as follows :
        Heading:
        Visual:
        Music:
        Caption:
        Hashtags: 
        '''
        config = {
            'max_output_tokens' : 2048,
            'temperature' : 2,
            'top_p' : 0.95,
        }
        caption = model.generate_content([prompt + data, video_file], generation_config=config)
        os.remove(video_file_path)
        os.remove(r"temp.mp4")
        return JSONResponse(content={'message' : caption.text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=501)

@app.post("/create-post")
async def create_post(user_input : str = Form(...)):
    try:
        genai.configure(api_key=GOOGLE_GEMINI_KEY)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        prompt='''
        You are an excellent content writer for Spillmate. Spillmate is your personalized AI chatbot for mental health support. Spillmate leverages proven techniques in psychology, machine learning and natural language processing to understand concerns and emotions and have supportive conversations.
        You will recieve a request from the user. You need to make a captivating instagram post with an attractive caption and content with respect to the topics asked by the user. The caption must be short and crisp (Maximum 5 sentences).
        Give relevant hashtags as well.
        '''
        config = {
        'max_output_tokens' : 2048,
        'temperature' : 2,
        'top_p' : 0.95,
        }
        content = model.generate_content([prompt, user_input], generation_config=config)
        post_content = content.text
        return JSONResponse(content={'message' : post_content}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=501)

if __name__=="__main__":
    uvicorn.run("fast_server:app", host="localhost", port=5000, reload=True)