#from AppOpener import close, open as appopen
is_mac = False
try:
    from AppOpener import close, open as appopen
except:
    is_mac = True
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
import re


env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTK00 sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
            "IZ6rdc", "05uR6d LTK00", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
            "LWkfke", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm always here to help you; don't hesitate to ask if you have any other questions.",
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I'm your {os.environ['Username']}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotePad(File):
        if is_mac == False:
            default_text_editor = 'notepad.exe'
            subprocess.Popen([default_text_editor, File])
        elif is_mac == True:
            subprocess.run(['open', f'{File}'], check=True)
        #os.system("open -a TextEdit")      ['open', '-a', '/Applications/TextEdit.app']
        #default_text_editor = "open "/Applications/TextEdit.app""
        #subprocess.Popen([str("/Applications/TextEdit.app"), File])
        #default_text_editor = '/Applications/TextEdit.app'
        #os.system(File)

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic: str = Topic.replace("Content: ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    #webbrowser.open(rf"Data\{Topic.lower().replace(' ','')}.txt")
    OpenNotePad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    #webbrowser.open("Data\applicationforsickleave.txt")
    return True

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    if is_mac == False:
        try:
            appopen(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            def extract_links(html):
                if html is None:
                    return []
                soup = BeautifulSoup(html, 'html.parser')
                links = soup.find_all('a')
                #print(links)
                return [link.get('href') for link in links]
        
            def search_google(query):
                url = f"https://www.google.com/search?q={query}"
                headers = {"User-Agent": useragent}
                response = sess.get(url, headers=headers)

                if response.status_code == 200:
                    return response.text
                else:
                    print("Failed to retrieve search results")
                return None
        
            html = search_google(app)

            if html:
                links = extract_links(html)[1]
                webopen(f"http://www.google.com/{links}")
            return True
    elif is_mac == True:
        try:
            subprocess.run(['open', f'-a', app], check=True)
            return True
        except:
            print("Failed to")
            def extract_links(html):
                if html is None:
                    return []
                soup = BeautifulSoup(html, 'html.parser')
                links = soup.find_all('a')
                #print(links)
                return [link.get('href') for link in links]
            
            def search_google(query):
                url = f"https://www.google.com/search?q={query}"
                headers = {"User-Agent": useragent}
                response = sess.get(url, headers=headers)

                if response.status_code == 200:
                    return response.text
                else:
                    print("Failed to retrieve search results")
                return None
            
            html = search_google(app)

            if html:
                links = extract_links(html)[1]
                webopen(f"http://www.google.com/{links}")
            return True
    
def CloseApp(app):
    if 'chrome' in app:
        pass
    else:
        try:
            #Change this for mac
            if is_mac == False:
                close(app, match_closest=True, output=True, throw_error=True)
            elif is_mac == True:
                os.system(f"close /Applications/{app}.app")
            return True
        except:
            return False
        
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

async def TranslateAndExecute(commands: list[str]):

    funcs = []

    for command in commands:

        if command.startswith("open "):

            if "open it" in command:
                pass

            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass

        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"No Command Found. For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):
        pass

    return True


