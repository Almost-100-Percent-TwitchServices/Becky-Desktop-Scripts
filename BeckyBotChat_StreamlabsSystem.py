# -*- coding: utf-8 -*-
#!/usr/bin/python
# pylint: disable=invalid-name
"""Becky Bot Chatting Script"""
#---------------------------------------
# Libraries and references
#---------------------------------------
import codecs
import json
import os
import winsound
import ctypes
import ast
#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Becky Bot Chat"
Website = "https://www.twitch.tv/almost_100_percent"
Creator = "Duckmaster94 (ref script by twitch.tv/castorr91)"
Version = "1.0"
Description = "Make Becky Bot interact with chat"
#---------------------------------------
# Versions
#---------------------------------------
"""
1.0.0.0     Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6

# chatbot = ChatBot(
#     'Becky',
#     trainer='chatterbot.trainers.ListTrainer'
# )

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsFile=None):
        if settingsFile and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file is found
            self.RespondTwitch = True
            self.OnlyLive = True
            self.Whispers = True
            self.BaseResponse = "[DISCORD] {0}: {1}"
            self.DEnabled = True
            self.NotLive = True
            self.DM = True
            self.Response = "[STREAM] {0}: {1}"
            self.Nicknames = ["becky","Becky_Bot_"]
            # self.Training = [name + " train:" for name in self.Nicknames]


    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    def Save(self, settingsfile):
        """ Save settings contained within the .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")

#---------------------------------------
# Optional functions
#---------------------------------------
def SetDefaults():
    """Set default settings function"""
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to contine?"
                             , u"Reset settings file?", 4)

    if returnValue == MB_YES:

        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)

        MySet = Settings()
        MySet.Save(settingsFile)

def ReloadSettings(jsonData):
    """Reload settings on Save"""
    global MySet
    MySet.Reload(jsonData)

def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """Data on Load, required function"""
    global MySet
    MySet = Settings(settingsFile)

def Tick():
    """Required tick function"""


def Execute(data):
    """Required Execute Data function"""
# Send training request to server ?should string parsing happen here, or on server side.  currently on server side? 
    command = ' train:'
    training = [s + command for s in MySet.Nicknames]
    # Parent.Log("becky",''.join(training))
    if any(x in data.Message for x in training):
        if MySet.RespondTwitch and data.IsChatMessage() and data.IsFromTwitch():
            if not MySet.OnlyLive or Parent.IsLive():
                if MySet.DM or not data.IsWhisper():
                    request = Parent.PostRequest('https://becky-bot.herokuapp.com/',{"Host": "https://becky-bot.herokuapp.com/"},{"Message": data.Message},True)
                    sendBack = ast.literal_eval(request)
                    Parent.SendStreamMessage(MySet.BaseResponse.format(data.UserName, sendBack["response"]))
        if MySet.DEnabled and data.IsChatMessage() and data.IsFromDiscord():
            if not MySet.OnlyLive or Parent.IsLive():
                if MySet.DM or not data.IsWhisper():
                    request = Parent.PostRequest('https://becky-bot.herokuapp.com/',{"Host": "https://becky-bot.herokuapp.com/"},{"Message": data.Message},True)
                    sendBack = ast.literal_eval(request)
                    Parent.SendDiscordMessage(MySet.BaseResponse.format(data.UserName,sendBack["response"] ))
        return
# new update becky alias command.  server communication code in the "if" statements pasted from training above.  Need to update custom server side response.
    command = ' nickname:'
    naming = [s + command for s in MySet.Nicknames]
    if any(x in data.Message for x in naming):
        newName = data.Message.split(command, 1)[-1]
        MySet.Nicknames.append(newName)
        MySet.Save(settingsFile)
        if MySet.RespondTwitch and data.IsChatMessage() and data.IsFromTwitch():
            if not MySet.OnlyLive or Parent.IsLive():
                if MySet.DM or not data.IsWhisper():
                    # request = Parent.PostRequest('https://becky-bot.herokuapp.com/',{"Host": "https://becky-bot.herokuapp.com/"},{"Message": data.Message},True)
                    # sendBack = ast.literal_eval(request)
                    # Parent.SendStreamMessage(MySet.BaseResponse.format(data.UserName, sendBack["response"]))
        if MySet.DEnabled and data.IsChatMessage() and data.IsFromDiscord():
            if not MySet.OnlyLive or Parent.IsLive():
                if MySet.DM or not data.IsWhisper():
                    # request = Parent.PostRequest('https://becky-bot.herokuapp.com/',{"Host": "https://becky-bot.herokuapp.com/"},{"Message": data.Message},True)
                    # sendBack = ast.literal_eval(request)
                    Parent.SendDiscordMessage(MySet.BaseResponse.format(data.UserName,">nickname updated<" ))
        return
# normal talking mode, send a request to server for a response 
    if any(x in data.Message for x in MySet.Nicknames):
        if MySet.RespondTwitch and data.IsChatMessage() and data.IsFromTwitch():
            if not MySet.OnlyLive or Parent.IsLive():
                if MySet.DM or not data.IsWhisper():
                    request = Parent.PostRequest('https://becky-bot.herokuapp.com/',{"Host": "https://becky-bot.herokuapp.com/"},{"Message": data.Message},True)
                    sendBack = ast.literal_eval(request)
                    Parent.SendStreamMessage(MySet.BaseResponse.format(data.UserName, sendBack["response"]))
        if MySet.DEnabled and data.IsChatMessage() and data.IsFromDiscord():
            if not MySet.OnlyLive or Parent.IsLive():
                if MySet.DM or not data.IsWhisper():
                    request = Parent.PostRequest('https://becky-bot.herokuapp.com/',{"Host": "https://becky-bot.herokuapp.com/"},{"Message": data.Message},True)
                    sendBack = ast.literal_eval(request)
                    Parent.SendDiscordMessage(MySet.BaseResponse.format(data.UserName,sendBack["response"] ))
        return