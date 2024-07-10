import os
import subprocess

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

def reencode_video(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v','libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-movflags', 'faststart',
        output_path
    ]
    subprocess.run(command, check = True)

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
        prompt='''
            You are a talented content creator for Spillmate, a cutting-edge AI chatbot dedicated to mental health support. Spillmate combines proven psychological techniques, machine learning, and natural language processing to provide empathetic and effective conversations. You will receive a video, and your task is to:

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
            'top_p' : 0.95,
        }
        caption = model.generate_content([prompt + data, video_file], generation_config=config)
        print("Uploaded successfully to Google AI Studio")
        return JSONResponse(content={'message' : caption.text}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=501)
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
        prompt='''
        You are an excellent content writer for Spillmate. Spillmate is your personalized AI chatbot for mental health support. Spillmate leverages proven techniques in psychology, machine learning and natural language processing to understand concerns and emotions and have supportive conversations.
        You will receive a request from the user. You need to make a captivating instagram post with an attractive caption and content with respect to the topics asked by the user. The caption must be short and crisp (Maximum 5 sentences).
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
    
@app.post("/generate-reply")
async def create_post(comment : str = Form(...)):
    try:
        genai.configure(api_key=GOOGLE_GEMINI_KEY)
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        prompt='''
        You are an excellent content writer for Spillmate. Spillmate is your personalized AI chatbot for mental health support. Spillmate leverages proven techniques in psychology, machine learning and natural language processing to understand concerns and emotions and have supportive conversations.
        You will receive a comment from a user, which will be from Instagram. You need to give a professional reply to the comment keeping in mind the goals and aims of Spillmate.
        '''
        config = {
        'max_output_tokens' : 2048,
        'temperature' : 2,
        'top_p' : 0.95,
        }
        content = model.generate_content([prompt, comment], generation_config=config)
        reply = content.text
        return JSONResponse(content={'message' : reply}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message' : str(e)}, status_code=501)

if __name__=="__main__":
    uvicorn.run("fast_server:app", host="localhost", port=5000, reload=True)