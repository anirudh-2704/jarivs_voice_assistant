import os
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound 
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assistant sound function
import pywhatkit as kit
import pvporcupine
from engine.helper import extract_yt_term
from hugchat import hugchat
import json

def chatBot(query):
    try:
        # Get the absolute path to the cookies.json file
        cookie_path = os.path.join(os.getcwd(), "engine", "cookies.json")
        
        # Initialize the chatbot
        chatbot = hugchat.ChatBot(cookie_path=cookie_path)
        
        # Start a new conversation
        conversation_id = chatbot.new_conversation()
        chatbot.change_conversation(conversation_id)
        
        # Process the query and get a response
        user_input = query.lower()
        print(f"User Input: {user_input}")  # Debugging input
        response = chatbot.chat(user_input)
        
        if response:
            print(f"Chatbot response: {response}")  # Debugging response
            speak(response)
            return response
        else:
            print("Chatbot did not return a response.")
            speak("I'm sorry, I couldn't fetch a response.")
            return "I'm sorry, I couldn't fetch a response."
    
    except Exception as e:
        print(f"Error with chatbot: {str(e)}")
        speak("Sorry, I couldn't get a response right now.")
        return "I'm sorry, I couldn't fetch a response."





con=sqlite3.connect("jarvis.db")
cursor=con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)
    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()
    
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")
        
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)
    
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


#chat bot 
# def chatBot(query):
#     user_input = query.lower()
#     chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
#     id = chatbot.new_conversation()
#     chatbot.change_conversation(id)
#     response =  chatbot.chat(user_input)
#     print(response)
#     speak(response)
#     return response

