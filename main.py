import yt_dlp
import yt_dlp_ejs
from subprocess import *
import os
import pyperclip
import requests
import time
import platform
import sys

print("[INFO] Starting iDownload-lite")
time.sleep(0.2)

disclaimerText = """I am not responsible for your usage of this program. A TV Licence is required to access BBC iPlayer content legally."""
print(f"\x1b[38;2;{255};{255};{0}m" + "[WARN] " + disclaimerText + "\x1b[0m")
time.sleep(0.4)

script_dir = os.getcwd()
time.sleep(0.1)
print("[INFO] Running in " + str(script_dir))

# deno check
print("[INFO] Checking for deno runtime")
try:
    denoCheck = check_output(["deno", "--version"])
    print("[INFO] Found deno runtime")
except:
    print("[INFO] Deno runtime not found")
    print("[INFO] Installing deno")
    if platform.system() == "Windows":
        r = requests.get("https://deno.land/install.ps1")
        with open(script_dir + '/deno.ps1', 'wb') as f:
            f.write(r.content)
        p = Popen(f"powershell -ExecutionPolicy Bypass -File {script_dir}/deno.ps1", shell=True)
        p.wait()
        os.remove(script_dir + '/deno.ps1')
    else:
        r = requests.get("https://deno.land/install.sh")
        with open(script_dir + '/deno.sh', 'wb') as f:
            f.write(r.content)
        p = Popen("sh " + script_dir + "/deno.sh", shell=True)
        p.wait()
        print("[INFO] Deno installed")

        print(f"\x1b[38;2;{255};{255};{0}m" + "[WARN] Shell needs to be restarted in order for changes to be applied")
        print("\x1b[0m" + "[INFO] Close and reopen your terminal")
        input("Press ENTER to close iDownload-lite")

        os.remove(script_dir + '/deno.sh')
        sys.exit()

# ffmpeg check
print("[INFO] Checking for ffmpeg")
try:
    denoCheck = check_output(["ffmpeg -version"], shell=True)
    print("[INFO] Found ffmpeg")
except:
    print("[INFO] ffmpeg not found")
    print("[INFO] Installing ffmpeg")
    if platform.system() == "Windows":
        print(f"\x1b[38;2;{255};{255};{0}m" + "[WARN] ffmpeg is not accessible")
        print("\x1b[0m" + "[INFO] You can install it in the following ways:")
        print("  winget install ffmpeg")
        print("  choco install ffmpeg-full")
        print("  scoop install ffmpeg")

        input("Press ENTER to close iDownload-lite")
        sys.exit()
    else:
        print(f"\x1b[38;2;{255};{255};{0}m" + "[WARN] ffmpeg is not accessible")
        print("\x1b[0m" + "[INFO] You can install it in the following ways:")
        print("Mac:  brew install ffmpeg")
        print("Debian:  apt install ffmpeg")
        print("Fedora:  sudo dnf install ffmpeg")
        print("Arch:  sudo pacman -S ffmpeg")
        print("openSUSE:  sudo zypper install ffmpeg")

        input("Press ENTER to close iDownload-lite")
        sys.exit()

hasPastedURL = False
print("[INFO] Initialised variables")

url = ""
quality = 1080
codec = "h.264"
otype = "video"
print("[INFO] Set default download options")

print("[INFO] Loading menu...")
time.sleep(0.5)
print("\033[2J")

class YTDL:
    def download(url, quality, codec, otype):
        if codec == "h.264":
            res = "bestvideo[height<=" + str(quality) + "][vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[ext=mp4]"
        else:
            res = "bestvideo[height<=" + str(quality) + "][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
    
        outtmpl = script_dir + "/downloads/%(title)s.%(ext)s"

        if otype == "audio":
            chosenResolution = "bestaudio/best"
            ydl_opts = {
                'format': chosenResolution,
                "outtmpl": outtmpl,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                        'preferredquality': '0'
                    }],
                'extractor-args': 'youtube:player-client=default,mweb',
                }
        else:
            ydl_opts = {
                'format': res,
                "outtmpl": outtmpl,
                'merge_output_format' : 'mp4',
                'extractor-args': 'youtube:player-client=default,mweb',
                    }
        
        URLS = [url]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLS)
        
        try:
            with open("history.txt", "r") as f:
                tempFile = [f.read()]
        except:
            tempFile = []

        with open("history.txt", "w") as f:
            f.write(str([time.ctime(), url]) + "\n")
        
        Pages.page = "homePage"

class iPDL:
    def download(url, quality):
        print("[INFO] Started mapping resolutions")
        if quality == 2160:
            tvquality = "fhd"
            print(f"\x1b[38;2;{255};{255};{0}m" + "[WARN] 2160p is not supported by get_iplayer" + "\x1b[0m")
        if quality == 1440:
            tvquality = "fhd"
            print(f"\x1b[38;2;{255};{255};{0}m" + "[WARN] 1440p is not supported by BBC iPlayer" + "\x1b[0m")
        if quality == 1080:
            tvquality = "fhd"
        if quality == 720:
            tvquality = "hd"
        if quality == 480:
            tvquality = "sd"
        print("[INFO] Finished mapping resolutions")
        time.sleep(0.2)
        print("[INFO] Started filling commands")

        if platform.system() == "Windows":
            bbcCommand = """"C:\Program Files\get_iplayer\get_iplayer.cmd" """ + url + " --tvquality " + tvquality + " --force " + f"""--output="{script_dir}/downloads/" """
        else:
            bbcCommand = "/usr/local/bin/get_iplayer " + url + " --tvquality " + tvquality + " --force " + f"""--output="{script_dir}/downloads/" """
        print("[INFO] Starting download of " + url)

        try:
            if platform.system() == "Windows":
                p = Popen(bbcCommand, shell=True)
                p.wait()
                print("[INFO] Download complete for " + url + " at " + tvquality + "p")
            else:
                p = Popen(bbcCommand, shell=True)
                p.wait()
                print("[INFO] Download complete for " + url + " at " + tvquality + "p")
        except:
            print(f"\x1b[38;2;{255};{0};{0}m" + "[ERROR] Download failed, see messages above" + "\x1b[0m")

class UI:
    def flip():
        inp = input()
        print("\033[2J")
        return inp

    def renderText(text, colour=[255, 255, 255]):
        Code = f"\x1b[38;2;{colour[0]};{colour[1]};{colour[2]}m"
        cReturn = "\x1b[0m"
        print(Code + text + cReturn)

    def renderButtonLabelLine(text, cCode):
        neededSpace = 12 - len(text)
        earlyBlankSpace = ""
        lateBlankSpace = ""

        for i in range(neededSpace // 2):
            earlyBlankSpace = earlyBlankSpace + " "

        for i in range(neededSpace - len(earlyBlankSpace)):
            lateBlankSpace = lateBlankSpace + " "

        txt =  [earlyBlankSpace, text, lateBlankSpace]
        print(cCode + f"|{txt[0]}{txt[1]}{txt[2]}|")
    
    def renderButton(label, colour, length):
        cCode = f"\x1b[38;2;{colour[0]};{colour[1]};{colour[2]}m"
        cReturn = "\x1b[0m"

        print(cCode + "+------------+")
        for i in range(length):
            UI.renderButtonLabelLine(label[i], cCode)
        print(cCode + "+------------+" + cReturn)
    
    def moveToLastObject():
        print("\033[1A")

    def emptyLine(lineNum):
        for i in range(lineNum):
            print()
    
    def handlePage(inp):
        global url
        global quality
        global codec
        global otype
        global hasPastedURL

        if Pages.page == "homePage":
            if inp == "1":
                url = pyperclip.paste()
                hasPastedURL = True
            if inp == "2":
                Pages.page = "ytQualityPage"
            if inp == "3":
                Pages.page = "bbcdlPage"
        elif Pages.page == "ytQualityPage":
            if inp == "1":
                quality = 480
            if inp == "2":
                quality = 720
            if inp == "3":
                quality = 1080
            if inp == "4":
                quality = 1440
            if inp == "5":
                quality = 2160
            if inp == "6":
                Pages.page = "ytCodecPage"
        elif Pages.page == "ytCodecPage":
            if inp == "1":
                codec = "h.264"
            if inp == "2":
                codec = "other"
            if inp == "3":
                Pages.page = "ytAudioPage"
        elif Pages.page == "ytAudioPage":
            if inp == "1":
                otype = "video"
            if inp == "2":
                otype = "audio"
            if inp == "3":
                YTDL.download(url, quality, codec, otype)
        elif Pages.page == "bbcdlPage":
            if inp == "1":
                quality = 480
            if inp == "2":
                quality = 720
            if inp == "3":
                quality = 1080
            if inp == "4":
                iPDL.download(url, quality)

class Pages:
    page = "homePage"
    def homePage():
        UI.renderText("▀█▀ █▀▄ █▀█ █ █ █ █▄ █ █   █▀█ ▄▀▄ █▀▄ ")
        UI.renderText("▄█▄ █▄▀ █▄█ ▀▄▀▄▀ █ ▀█ █▄▄ █▄█ █▀█ █▄▀ ")

        UI.emptyLine(1)

        UI.renderButton(["1. Paste"], [0, 255, 50], 1)
        UI.renderButton(["2. Download", "from YT"], [255, 0, 0], 2)
        UI.renderButton(["3. Download", "from iPlayer"], [255, 0, 255], 2)

        if "http" in url or not hasPastedURL:
            UI.renderText("URL: " + url)
        else:
            UI.renderText("Error in URL, try pasting again.", [255, 0, 0])

        UI.emptyLine(1)
    
    def ytQualityPage():
        UI.renderText("▀▄▀ █▀█ █ █ ▀█▀ █ █ █▄▄ █▀▀ ")
        UI.renderText(" █  █▄█ █▄█  █  █▄█ █▄█ ██▄ ")
        UI.renderText("Step 1 of 3")

        UI.emptyLine(1)

        UI.renderText("Choose Quality:")
        UI.renderButton(["1. 480p"], [255, 0, 121], 1)
        UI.renderButton(["2. 720p"], [255, 0, 121], 1)
        UI.renderButton(["3. 1080p"], [255, 0, 121], 1)
        UI.renderButton(["4. 1440p"], [255, 0, 121], 1)
        UI.renderButton(["5. 2160p"], [255, 0, 121], 1)
        UI.renderButton(["6. Next..."], [0, 255, 50], 1)

        if "http" in url or not hasPastedURL:
            UI.renderText("URL: " + url)
        else:
            UI.renderText("Error in URL, try pasting again.", [255, 0, 0])
        UI.renderText("Quality: " + str(quality))
        UI.emptyLine(1)
    
    def ytCodecPage():
        UI.renderText("▀▄▀ █▀█ █ █ ▀█▀ █ █ █▄▄ █▀▀ ")
        UI.renderText(" █  █▄█ █▄█  █  █▄█ █▄█ ██▄ ")
        UI.renderText("Step 2 of 3")

        UI.emptyLine(1)

        UI.renderText("Codec:")
        UI.renderButton(["1. H.264"], [255, 0, 121], 1)
        UI.renderButton(["2. Other"], [255, 0, 121], 1)
        UI.renderButton(["3. Next..."], [0, 255, 50], 1)

        if "http" in url or not hasPastedURL:
            UI.renderText("URL: " + url)
        else:
            UI.renderText("Error in URL, try pasting again.", [255, 0, 0])
        UI.renderText("Quality: " + str(quality))
        UI.renderText("Codec: " + codec)
        UI.emptyLine(1)
    
    def ytAudioPage():
        UI.renderText("▀▄▀ █▀█ █ █ ▀█▀ █ █ █▄▄ █▀▀ ")
        UI.renderText(" █  █▄█ █▄█  █  █▄█ █▄█ ██▄ ")
        UI.renderText("Step 3 of 3")

        UI.emptyLine(1)

        UI.renderText("Output Type:")
        UI.renderButton(["1. Video", "+ Audio"], [255, 0, 121], 2)
        UI.renderButton(["2. Audio", "Only"], [255, 0, 121], 2)
        UI.renderButton(["3. Download"], [0, 255, 50], 1)

        if "http" in url or not hasPastedURL:
            UI.renderText("URL: " + url)
        else:
            UI.renderText("Error in URL, try pasting again.", [255, 0, 0])
        UI.renderText("Quality: " + str(quality))
        UI.renderText("Codec: " + codec)
        if otype == 'video':
            UI.renderText("Output Type: Video + Audio")
        if otype == 'audio':
            UI.renderText("Output Type: Audio Only")
        UI.emptyLine(1)
    
    def bbcDlPage():
        UI.renderText("▀█▀ █▀█ █   ▄▀▄ ▀▄▀ █▀▀ █▀█ ")
        UI.renderText("▄█▄ █▀▀ █▄▄ █▀█  █  ██▄ █▀▄ ")
        UI.renderText("Step 1 of 1")

        UI.emptyLine(1)

        UI.renderText("Choose Quality:")
        UI.renderButton(["1. 540p"], [255, 0, 121], 1)
        UI.renderButton(["2. 720p"], [255, 0, 121], 1)
        UI.renderButton(["3. 1080p"], [255, 0, 121], 1)
        UI.renderButton(["4. Download"], [0, 255, 50], 1)

        if "http" in url or not hasPastedURL:
            UI.renderText("URL: " + url)
        else:
            UI.renderText("Error in URL, try pasting again.", [255, 0, 0])
        UI.renderText("Quality: " + str(quality))
        UI.emptyLine(1)

running = True
while running:
    start = time.time()

    if Pages.page == "homePage":
        Pages.homePage()
    elif Pages.page == "ytQualityPage":
        Pages.ytQualityPage()
    elif Pages.page == "ytCodecPage":
        Pages.ytCodecPage()
    elif Pages.page == "ytAudioPage":
        Pages.ytAudioPage()
    elif Pages.page == "bbcdlPage":
        Pages.bbcDlPage()

    end = start = time.time()
    time.sleep(1 - (end - start) / 60)
    userInput = UI.flip()
    UI.handlePage(userInput)
