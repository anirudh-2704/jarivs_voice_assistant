import pyttsx3
import speech_recognition as sr
import eel  
import time
import datetime


def speak(text):
    text=str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    #engine.setProperty('voice', voices[0].id) #voices[1] will get voice of David (male)
    engine.setProperty('voice', voices[1].id) #voices[1] will get voice of Zira (female)
    engine.setProperty('rate', 140)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        eel.DisplayMessage("listening....")
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)
        
        audio=r.listen(source,10,6)
        
    try:
        print("recognizing")
        eel.DisplayMessage("recognizing....")
        query=r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        return ""
    
    return query.lower()
        
# text= takeCommand()
# speak(text)

@eel.expose
def allCommands(message=1):
    
    if message==1: #here message comes from "mic"
        query= takeCommand()
        print(query)
        eel.senderText(query)
    else: #here message comes from "chat-box"
        query=message
        eel.senderText(query)
    try:
 
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "what is your name" in query:
            response="My name is Jarvis."
            print(response)
            speak(response)
        elif "who created you" in query:
            response="I was created by Chiti robo."
            print(response)
            speak(response)
        elif "tell me about nie college" in query:
            response="N I E is very very good college, located in mysuru."
            print(response)
            speak(response)
        elif "What's the time now" in query or "what's the time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            response = f"The current time is {current_time}."
            print(response)
            speak(response)
        elif "what is today's date" in query or "what's the date" in query:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            response = f"Today's date is {current_date}."
            print(response)
            speak(response)
        elif "how are you" in query:
            response = "I'm doing great! How can I assist you?"
            print(response)
            speak(response)
        elif "what is the weather" in query:
            response = "I currently can't fetch the weather, but it's a great day to code!"
            print(response)
            speak(response)
        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")
        
    eel.ShowHood()