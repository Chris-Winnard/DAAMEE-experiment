from psychopy import locale_setup
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import psychopy.iohub as io
from psychopy.hardware import keyboard

import Questionnaire_GSMI_Score_Calculator

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
task = 'questionnaire'
expInfo = {'Participant ID': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=task)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['task'] = task
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
dataPath = _thisDir + "/Data/"
groupAssignmentFile = dataPath + "Participant Groups.txt" #Needed for saving to right place:
with open(groupAssignmentFile, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if "Group A1" in line and expInfo['Participant ID'] in line:
            participantPath = dataPath + "Group A1/" + expInfo['Participant ID']
        elif "Group A2" in line and expInfo['Participant ID'] in line:
            participantPath = dataPath + "Group A2/" + expInfo['Participant ID']
        elif "Group B1" in line and expInfo['Participant ID'] in line:
            participantPath = dataPath + "Group B1/" + expInfo['Participant ID']
        elif "Group B2" in line and expInfo['Participant ID'] in line:
            participantPath = dataPath + "Group B2/" + expInfo['Participant ID']
    f.close

filename = participantPath + '/Questionnaire Data'

#In case the code has been run previously for the same participant, handle to delete existing files;
filenameCSV = filename+ '.csv'
filenamePSYDAT = filename+ '.psydat'
filenameLOG = filename+ '.log'

if os.path.isfile(filenameCSV):
    os.remove(filenameCSV)
if os.path.isfile(filenamePSYDAT):
    os.remove(filenamePSYDAT)
if os.path.isfile(filenameLOG):
    os.remove(filenameLOG)

jsonfilename = filename + '_stimuli.json'
jsondata = {}
jsondata['trials'] = []

expInfo['Participant ID'] = "sub-" + expInfo['Participant ID'][-2:] #BIDS format

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=task,
    extraInfo=expInfo, runtimeInfo=None,
    originPath= _thisDir + '/Questionnaire Script.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[2560, 1440], fullscr=True, screen=1, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='HP Monitor', color=[-0.4510, 0.0196, 0.4118], colorSpace='rgb', #Aarhus setup: size=[1920, 1080], monitor='Aarhus DELL Monitor', screen=1 #AIM laptop: size=[1920, 1080], monitor='AIM Laptop'
    blendMode='avg', useFBO=True, 
    units='height')

# Setup ioHub
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# Initialize components for Routine "Demographics"
DemographicsClock = core.Clock()
DemoHeading = visual.TextStim(win=win, name='DemoHeading',
    text='Demographics',
    font='Open Sans',
    pos=(-0.4, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
gender = visual.TextStim(win=win, name='gender',
    text='Q1: What is your gender?',
    font='Open Sans',
    pos=(0.0, 0.32), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
genderResp = visual.Slider(win=win, name='genderResp',
    startValue=None, size=(1.35, 0.02), pos=(0.0, 0.27), units=None,
    labels=("Male", "Female", "Transgender male", "Transgender female", "Other (please specify)"), ticks=(0, 1, 2, 3, 4), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-2, readOnly=False)
genderRespOther = visual.TextBox2(
     win, text=None, font='Open Sans',
     pos=(0.55, 0.14),     letterHeight=0.025,
     size=(0.3, 0.04), borderWidth=2.0,
     color='black', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='center',
     anchor='center',
     fillColor='white', borderColor='black',
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=True,
     name='genderRespOther',
     autoLog=True,
)
age = visual.TextStim(win=win, name='age',
    text='Q2: What is your age in years?',
    font='Open Sans',
    pos=(0.0, 0.06), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
ageResp = visual.TextBox2(
     win, text=None, font='Open Sans',
     pos=(0.0, 0.01),     letterHeight=0.025,
     size=(0.3, 0.04), borderWidth=2.0,
     color='Black', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='center',
     anchor='center',
     fillColor='White', borderColor='Black',
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=True,
     name='ageResp',
     autoLog=True,
)
nationality = visual.TextStim(win=win, name='nationality',
    text='Q3: What is your nationality?',
    font='Open Sans',
    pos=(0.0, -0.07), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-6.0);
nationalityResp = visual.TextBox2(
     win, text=None, font='Open Sans',
     pos=(0.0, -0.12),     letterHeight=0.025,
     size=(0.3, 0.04), borderWidth=2.0,
     color='Black', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='center',
     anchor='center',
     fillColor='White', borderColor='Black',
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=True,
     name='nationalityResp',
     autoLog=True,
)
originCountry = visual.TextStim(win=win, name='originCountry',
    text='Q4: What is your country of origin?',
    font='Open Sans',
    pos=(0.0, -0.2), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-8.0);
originCountryResp = visual.TextBox2(
     win, text=None, font='Open Sans',
     pos=(0, -0.25),     letterHeight=0.025,
     size=(0.3, 0.04), borderWidth=2.0,
     color='Black', colorSpace='rgb',
     opacity=None,
     bold=False, italic=False,
     lineSpacing=1.0,
     padding=0.0, alignment='center',
     anchor='center',
     fillColor='White', borderColor='Black',
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=True,
     name='originCountryResp',
     autoLog=True,
)
nextButton = visual.ImageStim(
    win=win,
    name='nextButton', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-10.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock()

# Initialize components for Routine "Current_Mental_State_pg1"
Current_Mental_State_pg1Clock = core.Clock()
cmpHeading = visual.TextStim(win=win, name='cmpHeading',
    text='Current Mental State',
    font='Open Sans',
    pos=(-0.4, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
text = visual.TextStim(win=win, name='text',
    text='Please remember to ask for clarification if you are unsure of any questions.',
    font='Open Sans',
    pos=(0, 0.31), height=0.03, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
tired = visual.TextStim(win=win, name='tired',
    text='Q5:  How rested do you feel? A rating of 1 indicates not at all, and a rating of 5 indicates very well-rested.',
    font='Open Sans',
    pos=(0.0, 0.23), height=0.03, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
tiredResp = visual.Slider(win=win, name='tiredResp',
    startValue=None, size=(1.35, 0.02), pos=(0.0, 0.16), units=None,
    labels=("1", "2","3","4","5"), ticks=(1, 2, 3, 4, 5), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-3, readOnly=False)
wired = visual.TextStim(win=win, name='wired',
    text='Q6:  How "wired" do you feel? A rating of 1 indicates not at all, and a rating of 5 indicates very "wired".',
    font='Arial',
    pos=(0.0, 0.01), height=0.03, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
wiredResp = visual.Slider(win=win, name='wiredResp',
    startValue=None, size=(1.35, 0.02), pos=(0.0, -0.06), units=None,
    labels=("1", "2","3","4","5"), ticks=(1, 2, 3, 4, 5), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-5, readOnly=False)
nextButton2 = visual.ImageStim(
    win=win,
    name='nextButton2', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-6.0)
mouse2 = event.Mouse(win=win)
x, y = [None, None]
mouse2.mouseClock = core.Clock()

# Initialize components for Routine "Current_Mental_State_pg2"
Current_Mental_State_pg2Clock = core.Clock()
cmpHeading_2 = visual.TextStim(win=win, name='cmpHeading_2',
    text='Current Mental State: Emotions',
    font='Open Sans',
    pos=(-0.4, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
text_2 = visual.TextStim(win=win, name='text_2',
    text='Please remember to ask for clarification if you are unsure of any questions.',
    font='Open Sans',
    pos=(-0.345, 0.34), height=0.03, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, anchorVert='top',
    languageStyle='LTR',
    depth=-1.0);
clickForEmotionInfo = visual.TextBox2(
     win, 
     text='                                                                                                                                  Click here for more information on how the\nscales relate to particular emotions.', font='Open Sans',
     pos=(0, 0.3095), letterHeight=0.03, size=(2.6, 0.051),
     color=[-1, 1, -1], colorSpace='rgb',
     opacity=None,
     bold=True, italic=False, lineSpacing=0.72,
     padding=0.0, alignment='center', anchor='centre',
     fillColor=None, borderColor=None,
     flipHoriz=False, flipVert=False, languageStyle='LTR',
     editable=False,
     name='clickForEmotionInfo',
     autoLog=False,
)
moodValence = visual.TextStim(win=win, name='moodValence',
    text='Q7: How positive/negative is your current emotion?\n',
    font='Open Sans',
    pos=(0.0, 0.23), height=0.03, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-6.0);
moodValenceResp = visual.Slider(win=win, name='moodValenceResp',
    startValue=None, size=(1.35, 0.02), pos=(0.0, 0.16), units=None,
    labels=("Very negative", "Neutral", "Very positive"), ticks=(0,1,2,3,4,5,6,7,8,9,10), granularity=0.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Arial', labelHeight=0.03,
    flip=False, ori=0.0, depth=-7, readOnly=False)
moodArousal = visual.TextStim(win=win, name='moodArousal',
    text='Q8: How active (energetic)/passive is your current emotion? For example, a sleepy person feels passive, whereas an excited person feels active.',
    font='Open Sans',
    pos=(0.0, 0.01), height=0.03, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
moodArousalResp = visual.Slider(win=win, name='moodArousalResp',
    startValue=None, size=(1.35, 0.02), pos=(0.0, -0.06), units=None,
    labels=("Very passive", "Neutral", "Very active"), ticks=(0,1,2,3,4,5,6,7,8,9,10), granularity=0.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Arial', labelHeight=0.03,
    flip=False, ori=0.0, depth=-6, readOnly=False)
moodDominance = visual.TextStim(win=win, name='moodDominance',
    text='Q9: How dominant/submissive is your current emotion? Fear is negative/active/submissive, but anger is negative/active/dominant. Positive emotions are not always dominant. For example, when a person fulfils an assignment for a boss, they may feel positive/active/submissive.',
    font='Open Sans',
    pos=(0.0, -0.21), height=0.03, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-7.0);
moodDominanceResp = visual.Slider(win=win, name='moodDominanceResp',
    startValue=None, size=(1.35, 0.02), pos=(0.0, -0.28), units=None,
    labels=("Very submissive", "Neutral", "Very dominant"), ticks=(0,1,2,3,4,5,6,7,8,9,10), granularity=0.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Arial', labelHeight=0.03,
    flip=False, ori=0.0, depth=-8, readOnly=False)
nextButton2_2 = visual.ImageStim(
    win=win,
    name='nextButton2_2', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-9.0)
mouse2_2 = event.Mouse(win=win)
x, y = [None, None]
mouse2_2.mouseClock = core.Clock()

# Initialize components for Routine "Categorical_Emotions_to_VAD_Mapping"
Categorical_Emotions_to_VAD_MappingClock = core.Clock()
Emotions_Mapping_Figure = visual.ImageStim(
    win=win,
    name='Emotions_Mapping_Figure', 
    image=_thisDir + '/V-A-D to Ekman model mapping.png', mask=None, anchor='center',
    ori=0.0, pos=(0, 0.06), size=(1.07117, 0.8),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)
nextButton_3 = visual.ImageStim(
    win=win,
    name='nextButton_3', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-10.0)
mouse_3 = event.Mouse(win=win)
x, y = [None, None]
mouse_3.mouseClock = core.Clock()
text_3 = visual.TextStim(win=win, name='text_3',
    text='Image adapted from Buechel and Hahn, 2016. Used under the terms of the Creative Commons Attribution Non-Commercial License 4.0.\n',
    font='Open Sans',
    pos=(0, -0.47), height=0.02, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);

# Initialize components for Routine "Personal_Responses_to_Music__Perception_pg1"
Personal_Responses_to_Music__Perception_pg1Clock = core.Clock()
personalResponsesHeadingP = visual.TextStim(win=win, name='personalResponsesHeadingP',
    text='Personal Responses to Music: Perception\n',
    font='Open Sans',
    pos=(-0.4, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
Q10 = visual.TextStim(win=win, name='Q10',
    text='Q10: I am able to judge whether someone is a good singer or not.',
    font='Open Sans',
    pos=(-0.38, 0.33), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
Q10Resp = visual.Slider(win=win, name='Q10Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.33), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-2, readOnly=False)
Q11 = visual.TextStim(win=win, name='Q11',
    text="Q11: I usually know when I'm hearing a song for the first time.",
    font='Open Sans', pos=(-0.38, 0.185), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=-3.0);
Q11Resp = visual.Slider(win=win, name='Q11Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.185), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-4, readOnly=False)
Q12 = visual.TextStim(win=win, name='Q12',
    text='Q12: I find it difficult to spot mistakes in a performance of a song even if I know the tune.',
    font='Open Sans',
    pos=(-0.38, 0.04), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=-5.0);
Q12Resp = visual.Slider(win=win, name='Q12Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.04), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-6, readOnly=False)
Q13 = visual.TextStim(win=win, name='Q13',
    text='Q13: I can compare and discuss differences between two performances or versions of the same piece of music.',
    font='Open Sans',
    pos=(-0.38, -0.105), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-7.0);
Q13Resp = visual.Slider(win=win, name='Q13Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, -0.105), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-8, readOnly=False)
Q14 = visual.TextStim(win=win, name='Q14',
    text='Q14: I have trouble recognizing a familiar song when played in a different way or by a different performer.',
    font='Open Sans',
    pos=(-0.38, -0.25), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-9.0);
Q14Resp = visual.Slider(win=win, name='Q14Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, -0.25), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-10, readOnly=False)
nextButton_2 = visual.ImageStim(
    win=win,
    name='nextButton_2', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-19.0)
mouse_2 = event.Mouse(win=win)
x, y = [None, None]
mouse_2.mouseClock = core.Clock()

# Initialize components for Routine "Personal_Responses_to_Music__Perception_pg2"
Personal_Responses_to_Music__Perception_pg2Clock = core.Clock()
personalResponsesHeadingP = visual.TextStim(win=win, name='personalResponsesHeadingP',
    text='Personal Responses to Music: Perception\n',
    font='Open Sans',
    pos=(-0.4, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
Q15 = visual.TextStim(win=win, name='Q15',
    text='Q15: I can tell when people sing or play out of time with the beat.',
    font='Open Sans',
    pos=(-0.38, 0.33), height=0.03, wrapWidth=1.05, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-11.0);
Q15Resp = visual.Slider(win=win, name='Q15Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.33), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-12, readOnly=False)
Q16 = visual.TextStim(win=win, name='Q16',
    text='Q16: I can tell when people sing or play out of tune.',
    font='Open Sans',
    pos=(-0.38, 0.185), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-13.0);
Q16Resp = visual.Slider(win=win, name='Q16Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.185), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-14, readOnly=False)
Q17 = visual.TextStim(win=win, name='Q17',
    text="Q17: When I sing, I have no idea whether I'm in tune or not.",
    font='Open Sans',
    pos=(-0.38, 0.04), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-15.0);
Q17Resp = visual.Slider(win=win, name='Q17Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.04), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-16, readOnly=False)
Q18 = visual.TextStim(win=win, name='Q18',
    text='Q18: When I hear a music piece, I can usually identify its genre.\n',
    font='Open Sans',
    pos=(-0.38, -0.105), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-17.0);
Q18Resp = visual.Slider(win=win, name='Q18Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, -0.105), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-18, readOnly=False)
nextButton_2 = visual.ImageStim(
    win=win,
    name='nextButton_2', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-19.0)
mouse_2 = event.Mouse(win=win)
x, y = [None, None]
mouse_2.mouseClock = core.Clock()

# Initialize components for Routine "Personal_Responses_to_Music__Emotion_pg1"
Personal_Responses_to_Music__Emotion_pg1Clock = core.Clock()
personalResponsesHeadingE = visual.TextStim(win=win, name='personalResponsesHeadingE',
    text='Personal Responses to Music: Emotion\n',
    font='Open Sans',
    pos=(-0.4, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
Q19 = visual.TextStim(win=win, name='Q19',
    text='Q19: I sometimes choose music that can trigger shivers down my spine. \n',
    font='Open Sans',
    pos=(-0.38, 0.33), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
Q19Resp = visual.Slider(win=win, name='Q19Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.33), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-2, readOnly=False)
Q20 = visual.TextStim(win=win, name='Q20',
    text='Q20: Pieces of music rarely evoke emotions for me.',
    font='Open Sans',
    pos=(-0.38, 0.185), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
Q20Resp = visual.Slider(win=win, name='Q20Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.185), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-4, readOnly=False)
Q21 = visual.TextStim(win=win, name='Q21',
    text='Q21: I often pick certain music to motivate or excite me. ',
    font='Open Sans',
    pos=(-0.38, 0.04), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
Q21Resp = visual.Slider(win=win, name='Q21Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.04), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-6, readOnly=False)
Q22 = visual.TextStim(win=win, name='Q22',
    text='Q22: I am able to identify what is special about a given musical piece.',
    font='Open Sans',
    pos=(-0.38, -0.105), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-7.0);
Q22Resp = visual.Slider(win=win, name='Q22Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, -0.105), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-8, readOnly=False)
Q23 = visual.TextStim(win=win, name='Q23',
    text='Q23: I am able to talk about the emotions that a piece of music evokes for me.',
    font='Open Sans',
    pos=(-0.38, -0.25), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-9.0);
Q23Resp = visual.Slider(win=win, name='Q23Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, -0.25), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-10, readOnly=False)
nextButton_4 = visual.ImageStim(
    win=win,
    name='nextButton_4', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-13.0)
mouse_4 = event.Mouse(win=win)
x, y = [None, None]
mouse_4.mouseClock = core.Clock()

# Initialize components for Routine "Personal_Responses_to_Music__Emotion_pg2"
Personal_Responses_to_Music__Emotion_pg2Clock = core.Clock()
personalResponsesHeadingE = visual.TextStim(win=win, name='personalResponsesHeadingE',
    text='Personal Responses to Music: Emotion\n',
    font='Open Sans',
    pos=(-0.4, 0.4), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
Q24 = visual.TextStim(win=win, name='Q24',
    text='Q24: Music can evoke my memories of past people and places.',
    font='Open Sans',
    pos=(-0.38, 0.33), height=0.03, wrapWidth=0.96, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-11.0);
Q24Resp = visual.Slider(win=win, name='Q24Resp',
    startValue=None, size=(0.6, 0.02), pos=(0.495, 0.33), units=None,
    labels=("Completely\ndisagree", "Neutral", "Completely\nagree"), ticks=(1, 2, 3, 4, 5, 6, 7), granularity=1.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=False, ori=0.0, depth=-12, readOnly=False)
nextButton_4 = visual.ImageStim(
    win=win,
    name='nextButton_4', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-13.0)
mouse_4 = event.Mouse(win=win)
x, y = [None, None]
mouse_4.mouseClock = core.Clock()

# Initialize components for Routine "thisPartComplete"
thisPartCompleteClock = core.Clock()
thisPartCompleteText = visual.TextStim(win=win, name='thisPartCompleteText',
    text='Questionnaire complete.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);


# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "Demographics"-------
continueRoutine = True
# update component parameters for each repeat
genderResp.reset()
genderRespOther.reset()
ageResp.reset()
nationalityResp.reset()
originCountryResp.reset()
# setup some python lists for storing info about the mouse
mouse.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
DemographicsComponents = [DemoHeading, gender, genderResp, genderRespOther, age, ageResp, nationality, nationalityResp, originCountry, originCountryResp, nextButton, mouse]
for thisComponent in DemographicsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
DemographicsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

gotValidGender = False
# -------Run Routine "Demographics"-------
while continueRoutine:
    # get current time
    t = DemographicsClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=DemographicsClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *DemoHeading* updates
    if DemoHeading.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        DemoHeading.frameNStart = frameN  # exact frame index
        DemoHeading.tStart = t  # local t and not account for scr refresh
        DemoHeading.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(DemoHeading, 'tStartRefresh')  # time at next scr refresh
        DemoHeading.setAutoDraw(True)
    
    # *gender* updates
    if gender.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        gender.frameNStart = frameN  # exact frame index
        gender.tStart = t  # local t and not account for scr refresh
        gender.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(gender, 'tStartRefresh')  # time at next scr refresh
        gender.setAutoDraw(True)
    
    # *genderResp* updates
    if genderResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        genderResp.frameNStart = frameN  # exact frame index
        genderResp.tStart = t  # local t and not account for scr refresh
        genderResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(genderResp, 'tStartRefresh')  # time at next scr refresh
        genderResp.setAutoDraw(True)
    
    # *genderRespOther* updates
    if genderRespOther.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        genderRespOther.frameNStart = frameN  # exact frame index
        genderRespOther.tStart = t  # local t and not account for scr refresh
        genderRespOther.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(genderRespOther, 'tStartRefresh')  # time at next scr refresh
        genderRespOther.setAutoDraw(True)
    
    # *age* updates
    if age.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        age.frameNStart = frameN  # exact frame index
        age.tStart = t  # local t and not account for scr refresh
        age.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(age, 'tStartRefresh')  # time at next scr refresh
        age.setAutoDraw(True)
    
    if (genderResp.rating == 0.0) or (genderResp.rating == 1.0) or (genderResp.rating == 2.0) or (genderResp.rating == 3.0) or (genderResp.rating == 4.0 and genderRespOther.text):
            gotValidGender = True
            
    # *ageResp* updates
    if ageResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ageResp.frameNStart = frameN  # exact frame index
        ageResp.tStart = t  # local t and not account for scr refresh
        ageResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ageResp, 'tStartRefresh')  # time at next scr refresh
        ageResp.setAutoDraw(True)
    
    # *nationality* updates
    if nationality.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        nationality.frameNStart = frameN  # exact frame index
        nationality.tStart = t  # local t and not account for scr refresh
        nationality.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nationality, 'tStartRefresh')  # time at next scr refresh
        nationality.setAutoDraw(True)
    
    # *nationalityResp* updates
    if nationalityResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        nationalityResp.frameNStart = frameN  # exact frame index
        nationalityResp.tStart = t  # local t and not account for scr refresh
        nationalityResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nationalityResp, 'tStartRefresh')  # time at next scr refresh
        nationalityResp.setAutoDraw(True)
    
    # *originCountry* updates
    if originCountry.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        originCountry.frameNStart = frameN  # exact frame index
        originCountry.tStart = t  # local t and not account for scr refresh
        originCountry.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(originCountry, 'tStartRefresh')  # time at next scr refresh
        originCountry.setAutoDraw(True)
    
    # *originCountryResp* updates
    if originCountryResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        originCountryResp.frameNStart = frameN  # exact frame index
        originCountryResp.tStart = t  # local t and not account for scr refresh
        originCountryResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(originCountryResp, 'tStartRefresh')  # time at next scr refresh
        originCountryResp.setAutoDraw(True)
    
    # *mouse* updates
    if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mouse.frameNStart = frameN  # exact frame index
        mouse.tStart = t  # local t and not account for scr refresh
        mouse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
        mouse.status = STARTED
        mouse.mouseClock.reset()
        prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
    if mouse.status == STARTED:  # only update if started and not finished!
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if (nextButton.status == STARTED and (genderResp.rating or genderResp.rating == 0.0) and (ageResp.text).isdigit() and nationalityResp.text and originCountryResp.text):
                    try:
                        iter(nextButton)
                        clickableList = nextButton
                    except:
                        clickableList = [nextButton]
                    for obj in clickableList:
                        if obj.contains(mouse):
                            gotValidClick = True
                            mouse.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
                        
    # *nextButton* updates
    if (nextButton.status == NOT_STARTED and gotValidGender and (ageResp.text).isdigit() and nationalityResp.text and originCountryResp.text):
        # keep track of start time/frame for later
        nextButton.frameNStart = frameN  # exact frame index
        nextButton.tStart = t  # local t and not account for scr refresh
        nextButton.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton, 'tStartRefresh')  # time at next scr refresh
        nextButton.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in DemographicsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Demographics"-------
for thisComponent in DemographicsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
#Convert gender to a string and record that:
genderCategories = ["Male", "Female", "Transgender male", "Transgender female", "Other"]
genderIndex = int(genderResp.getRating())
thisExp.addData('genderResp.response', genderCategories[genderIndex])
thisExp.addData('genderRespOther.text',genderRespOther.text)

thisExp.addData('ageResp.text',ageResp.text)
thisExp.addData('nationalityResp.text',nationalityResp.text)
thisExp.addData('originCountryResp.text',originCountryResp.text)
# store data for thisExp (ExperimentHandler)
x, y = mouse.getPos()
# the Routine "Demographics" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Current_Mental_State_pg1"-------
continueRoutine = True
# update component parameters for each repeat
tiredResp.reset()
wiredResp.reset()
# setup some python lists for storing info about the mouse2
mouse2.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
Current_Mental_State_pg1Components = [cmpHeading, text, tired, tiredResp, wired, wiredResp, nextButton2, mouse2]
for thisComponent in Current_Mental_State_pg1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Current_Mental_State_pg1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Current_Mental_State_pg1"-------
while continueRoutine:
    # get current time
    t = Current_Mental_State_pg1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Current_Mental_State_pg1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *cmpHeading* updates
    if cmpHeading.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        cmpHeading.frameNStart = frameN  # exact frame index
        cmpHeading.tStart = t  # local t and not account for scr refresh
        cmpHeading.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(cmpHeading, 'tStartRefresh')  # time at next scr refresh
        cmpHeading.setAutoDraw(True)
    
    # *text* updates
    if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        text.setAutoDraw(True)
    
    # *tired* updates
    if tired.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        tired.frameNStart = frameN  # exact frame index
        tired.tStart = t  # local t and not account for scr refresh
        tired.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(tired, 'tStartRefresh')  # time at next scr refresh
        tired.setAutoDraw(True)
    
    # *tiredResp* updates
    if tiredResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        tiredResp.frameNStart = frameN  # exact frame index
        tiredResp.tStart = t  # local t and not account for scr refresh
        tiredResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(tiredResp, 'tStartRefresh')  # time at next scr refresh
        tiredResp.setAutoDraw(True)
    
    # *wired* updates
    if wired.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        wired.frameNStart = frameN  # exact frame index
        wired.tStart = t  # local t and not account for scr refresh
        wired.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(wired, 'tStartRefresh')  # time at next scr refresh
        wired.setAutoDraw(True)
    
    # *wiredResp* updates
    if wiredResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        wiredResp.frameNStart = frameN  # exact frame index
        wiredResp.tStart = t  # local t and not account for scr refresh
        wiredResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(wiredResp, 'tStartRefresh')  # time at next scr refresh
        wiredResp.setAutoDraw(True)
    
    # *nextButton2* updates
    if (nextButton2.status == NOT_STARTED and tiredResp.rating and wiredResp.rating):
        # keep track of start time/frame for later
        nextButton2.frameNStart = frameN  # exact frame index
        nextButton2.tStart = t  # local t and not account for scr refresh
        nextButton2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton2, 'tStartRefresh')  # time at next scr refresh
        nextButton2.setAutoDraw(True)
    # *mouse2* updates
    if mouse2.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mouse2.frameNStart = frameN  # exact frame index
        mouse2.tStart = t  # local t and not account for scr refresh
        mouse2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse2, 'tStartRefresh')  # time at next scr refresh
        mouse2.status = STARTED
        mouse2.mouseClock.reset()
        prevButtonState = mouse2.getPressed()  # if button is down already this ISN'T a new click
    if mouse2.status == STARTED:  # only update if started and not finished!
        buttons = mouse2.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if (nextButton2.status == STARTED and wiredResp.rating and tiredResp.rating):
                    try:
                        iter(nextButton2)
                        clickableList = nextButton2
                    except:
                        clickableList = [nextButton2]
                    for obj in clickableList:
                        if obj.contains(mouse2):
                            gotValidClick = True
                            mouse2.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
          
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Current_Mental_State_pg1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Current_Mental_State_pg1"-------
for thisComponent in Current_Mental_State_pg1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('tiredResp.response', tiredResp.getRating())
thisExp.addData('wiredResp.response', wiredResp.getRating())
# store data for thisExp (ExperimentHandler)
x, y = mouse2.getPos()

# the Routine "Current_Mental_State_pg1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
moveToPersonalResponses = False #So we can open an information page without skipping ahead to the next section of questions.

moodValenceResp.reset()
moodArousalResp.reset()
moodDominanceResp.reset()
while moveToPersonalResponses == False:
    # ------Prepare to start Routine "Current_Mental_State_pg2"-------
    continueRoutine = True
    # update component parameters for each repeat
    clickForEmotionInfo.reset()
    # setup some python lists for storing info about the mouse2_2
    mouse2_2.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    Current_Mental_State_pg2Components = [cmpHeading_2, text_2, clickForEmotionInfo, moodValence, moodValenceResp, moodArousal, moodArousalResp, moodDominance, moodDominanceResp, nextButton2_2, mouse2_2]
    for thisComponent in Current_Mental_State_pg2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Current_Mental_State_pg2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Current_Mental_State_pg2"-------
    while continueRoutine:
        # get current time
        t = Current_Mental_State_pg2Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Current_Mental_State_pg2Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *cmpHeading_2* updates
        if cmpHeading_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cmpHeading_2.frameNStart = frameN  # exact frame index
            cmpHeading_2.tStart = t  # local t and not account for scr refresh
            cmpHeading_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cmpHeading_2, 'tStartRefresh')  # time at next scr refresh
            cmpHeading_2.setAutoDraw(True)
        
        # *text_2* updates
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            text_2.setAutoDraw(True)
        
        # *clickForEmotionInfo* updates
        if clickForEmotionInfo.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            clickForEmotionInfo.frameNStart = frameN  # exact frame index
            clickForEmotionInfo.tStart = t  # local t and not account for scr refresh
            clickForEmotionInfo.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(clickForEmotionInfo, 'tStartRefresh')  # time at next scr refresh
            clickForEmotionInfo.setAutoDraw(True)
        
        # *moodValence* updates
        if moodValence.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            moodValence.frameNStart = frameN  # exact frame index
            moodValence.tStart = t  # local t and not account for scr refresh
            moodValence.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moodValence, 'tStartRefresh')  # time at next scr refresh
            moodValence.setAutoDraw(True)
        
        # *moodValenceResp* updates
        if moodValenceResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            moodValenceResp.frameNStart = frameN  # exact frame index
            moodValenceResp.tStart = t  # local t and not account for scr refresh
            moodValenceResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moodValenceResp, 'tStartRefresh')  # time at next scr refresh
            moodValenceResp.setAutoDraw(True)
        
        # *moodArousal* updates
        if moodArousal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            moodArousal.frameNStart = frameN  # exact frame index
            moodArousal.tStart = t  # local t and not account for scr refresh
            moodArousal.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moodArousal, 'tStartRefresh')  # time at next scr refresh
            moodArousal.setAutoDraw(True)
        
        # *moodArousalResp* updates
        if moodArousalResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            moodArousalResp.frameNStart = frameN  # exact frame index
            moodArousalResp.tStart = t  # local t and not account for scr refresh
            moodArousalResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moodArousalResp, 'tStartRefresh')  # time at next scr refresh
            moodArousalResp.setAutoDraw(True)
        
        # *moodDominance* updates
        if moodDominance.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            moodDominance.frameNStart = frameN  # exact frame index
            moodDominance.tStart = t  # local t and not account for scr refresh
            moodDominance.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moodDominance, 'tStartRefresh')  # time at next scr refresh
            moodDominance.setAutoDraw(True)
        
        # *moodDominanceResp* updates
        if moodDominanceResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            moodDominanceResp.frameNStart = frameN  # exact frame index
            moodDominanceResp.tStart = t  # local t and not account for scr refresh
            moodDominanceResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(moodDominanceResp, 'tStartRefresh')  # time at next scr refresh
            moodDominanceResp.setAutoDraw(True)
        
        # *mouse* updates
        if mouse2_2.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse2_2.frameNStart = frameN  # exact frame index
            mouse2_2.tStart = t  # local t and not account for scr refresh
            mouse2_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse2_2, 'tStartRefresh')  # time at next scr refresh
            mouse2_2.status = STARTED
            mouse2_2.mouseClock.reset()
            prevButtonState = mouse2_2.getPressed()  # if button is down already this ISN'T a new click
        if mouse2_2.status == STARTED:  # only update if started and not finished!
            buttons = mouse2_2.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    if (nextButton2_2.status == STARTED and moodValenceResp.rating != None and moodArousalResp.rating != None and moodDominanceResp.rating != None): #Only want the next button to be clickable if it's actually been activated!
                        try:
                            iter([nextButton2_2, clickForEmotionInfo])
                            clickableList = [nextButton2_2, clickForEmotionInfo]
                        except:
                            clickableList = [[nextButton2_2, clickForEmotionInfo]]
                        for obj in clickableList:
                            if obj.contains(mouse2_2):
                                gotValidClick = True
                                mouse2_2.clicked_name.append(obj.name)
                                if obj.name == 'nextButton2_2':
                                        moveToPersonalResponses = True
                    else:
                        try:
                            iter([clickForEmotionInfo])
                            clickableList = [clickForEmotionInfo]
                        except:
                            clickableList = [[clickForEmotionInfo]]
                        for obj in clickableList:
                            if obj.contains(mouse2_2):
                                gotValidClick = True
                                mouse2_2.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
        
        # *nextButton* updates
        if (nextButton2_2.status == NOT_STARTED and moodValenceResp.rating != None and moodArousalResp.rating != None and moodDominanceResp.rating != None):
            # keep track of start time/frame for later
            nextButton2_2.frameNStart = frameN  # exact frame index
            nextButton2_2.tStart = t  # local t and not account for scr refresh
            nextButton2_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(nextButton2_2, 'tStartRefresh')  # time at next scr refresh
            nextButton2_2.setAutoDraw(True)
    
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Current_Mental_State_pg2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Current_Mental_State_pg2"-------
    for thisComponent in Current_Mental_State_pg2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('moodValenceResp.response', moodValenceResp.getRating())
    thisExp.addData('moodArousalResp.response', moodArousalResp.getRating())
    thisExp.addData('moodDominanceResp.response', moodDominanceResp.getRating())
    # store data for thisExp (ExperimentHandler)
    x, y = mouse2_2.getPos()
    
    # the Routine "Current_Mental_State_pg2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    if moveToPersonalResponses == False: #This needs to be here as well.
        # ------Prepare to start Routine "Categorical_Emotions_to_VAD_Mapping"-------
        continueRoutine = True
        # update component parameters for each repeat
        # setup some python lists for storing info about the mouse_3
        mouse_3.clicked_name = []
        gotValidClick = False  # until a click is received
        # keep track of which components have finished
        Categorical_Emotions_to_VAD_MappingComponents = [Emotions_Mapping_Figure, nextButton_3, mouse_3, text_3]
        for thisComponent in Categorical_Emotions_to_VAD_MappingComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        Categorical_Emotions_to_VAD_MappingClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Categorical_Emotions_to_VAD_Mapping"-------
        while continueRoutine:
            # get current time
            t = Categorical_Emotions_to_VAD_MappingClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=Categorical_Emotions_to_VAD_MappingClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Emotions_Mapping_Figure* updates
            if Emotions_Mapping_Figure.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Emotions_Mapping_Figure.frameNStart = frameN  # exact frame index
                Emotions_Mapping_Figure.tStart = t  # local t and not account for scr refresh
                Emotions_Mapping_Figure.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Emotions_Mapping_Figure, 'tStartRefresh')  # time at next scr refresh
                Emotions_Mapping_Figure.setAutoDraw(True)
            
            # *nextButton_3* updates
            if nextButton_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                nextButton_3.frameNStart = frameN  # exact frame index
                nextButton_3.tStart = t  # local t and not account for scr refresh
                nextButton_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(nextButton_3, 'tStartRefresh')  # time at next scr refresh
                nextButton_3.setAutoDraw(True)
            # *mouse_3* updates
            if mouse_3.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mouse_3.frameNStart = frameN  # exact frame index
                mouse_3.tStart = t  # local t and not account for scr refresh
                mouse_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse_3, 'tStartRefresh')  # time at next scr refresh
                mouse_3.status = STARTED
                mouse_3.mouseClock.reset()
                prevButtonState = mouse_3.getPressed()  # if button is down already this ISN'T a new click
            if mouse_3.status == STARTED:  # only update if started and not finished!
                buttons = mouse_3.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        # check if the mouse was inside our 'clickable' objects
                        gotValidClick = False
                        try:
                            iter(nextButton)
                            clickableList = nextButton
                        except:
                            clickableList = [nextButton]
                        for obj in clickableList:
                            if obj.contains(mouse_3):
                                gotValidClick = True
                                mouse_3.clicked_name.append(obj.name)
                        if gotValidClick:  
                            continueRoutine = False  # abort routine on response
            
            # *text_3* updates
            if text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_3.frameNStart = frameN  # exact frame index
                text_3.tStart = t  # local t and not account for scr refresh
                text_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_3, 'tStartRefresh')  # time at next scr refresh
                text_3.setAutoDraw(True)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Categorical_Emotions_to_VAD_MappingComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Categorical_Emotions_to_VAD_Mapping"-------
        for thisComponent in Categorical_Emotions_to_VAD_MappingComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store data for thisExp (ExperimentHandler)
        x, y = mouse_3.getPos()
        # the Routine "Categorical_Emotions_to_VAD_Mapping" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

# ------Prepare to start Routine "Personal_Responses_to_Music__Perception_pg1"-------
continueRoutine = True
# update component parameters for each repeat
Q10Resp.reset()
Q11Resp.reset()
Q12Resp.reset()
Q13Resp.reset()
Q14Resp.reset()
# setup some python lists for storing info about the mouse_2
mouse_2.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
Personal_Responses_to_Music__Perception_pg1Components = [personalResponsesHeadingP, Q10, Q10Resp, Q11, Q11Resp, Q12, Q12Resp, Q13, Q13Resp, Q14, Q14Resp, nextButton_2, mouse_2]
for thisComponent in Personal_Responses_to_Music__Perception_pg1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Personal_Responses_to_Music__Perception_pg1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Personal_Responses_to_Music__Perception_pg1"-------
while continueRoutine:
    # get current time
    t = Personal_Responses_to_Music__Perception_pg1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Personal_Responses_to_Music__Perception_pg1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *personalResponsesHeadingP* updates
    if personalResponsesHeadingP.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        personalResponsesHeadingP.frameNStart = frameN  # exact frame index
        personalResponsesHeadingP.tStart = t  # local t and not account for scr refresh
        personalResponsesHeadingP.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(personalResponsesHeadingP, 'tStartRefresh')  # time at next scr refresh
        personalResponsesHeadingP.setAutoDraw(True)
    
    # *Q10* updates
    if Q10.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q10.frameNStart = frameN  # exact frame index
        Q10.tStart = t  # local t and not account for scr refresh
        Q10.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q10, 'tStartRefresh')  # time at next scr refresh
        Q10.setAutoDraw(True)
    
    # *Q10Resp* updates
    if Q10Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q10Resp.frameNStart = frameN  # exact frame index
        Q10Resp.tStart = t  # local t and not account for scr refresh
        Q10Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q10Resp, 'tStartRefresh')  # time at next scr refresh
        Q10Resp.setAutoDraw(True)
    
    # *Q11* updates
    if Q11.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q11.frameNStart = frameN  # exact frame index
        Q11.tStart = t  # local t and not account for scr refresh
        Q11.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q11, 'tStartRefresh')  # time at next scr refresh
        Q11.setAutoDraw(True)
    
    # *Q11Resp* updates
    if Q11Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q11Resp.frameNStart = frameN  # exact frame index
        Q11Resp.tStart = t  # local t and not account for scr refresh
        Q11Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q11Resp, 'tStartRefresh')  # time at next scr refresh
        Q11Resp.setAutoDraw(True)
    
    # *Q12* updates
    if Q12.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q12.frameNStart = frameN  # exact frame index
        Q12.tStart = t  # local t and not account for scr refresh
        Q12.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q12, 'tStartRefresh')  # time at next scr refresh
        Q12.setAutoDraw(True)
    
    # *Q12Resp* updates
    if Q12Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q12Resp.frameNStart = frameN  # exact frame index
        Q12Resp.tStart = t  # local t and not account for scr refresh
        Q12Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q12Resp, 'tStartRefresh')  # time at next scr refresh
        Q12Resp.setAutoDraw(True)
    
    # *Q13* updates
    if Q13.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q13.frameNStart = frameN  # exact frame index
        Q13.tStart = t  # local t and not account for scr refresh
        Q13.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q13, 'tStartRefresh')  # time at next scr refresh
        Q13.setAutoDraw(True)
    
    # *Q13Resp* updates
    if Q13Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q13Resp.frameNStart = frameN  # exact frame index
        Q13Resp.tStart = t  # local t and not account for scr refresh
        Q13Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q13Resp, 'tStartRefresh')  # time at next scr refresh
        Q13Resp.setAutoDraw(True)
    
    # *Q14* updates
    if Q14.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q14.frameNStart = frameN  # exact frame index
        Q14.tStart = t  # local t and not account for scr refresh
        Q14.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q14, 'tStartRefresh')  # time at next scr refresh
        Q14.setAutoDraw(True)
    
    # *Q14Resp* updates
    if Q14Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q14Resp.frameNStart = frameN  # exact frame index
        Q14Resp.tStart = t  # local t and not account for scr refresh
        Q14Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q14Resp, 'tStartRefresh')  # time at next scr refresh
        Q14Resp.setAutoDraw(True)
    
        # *nextButton_2* updates
    if (nextButton_2.status == NOT_STARTED and Q10Resp.rating and Q11Resp.rating and Q12Resp.rating and Q13Resp.rating and Q14Resp.rating):
        # keep track of start time/frame for later
        nextButton_2.frameNStart = frameN  # exact frame index
        nextButton_2.tStart = t  # local t and not account for scr refresh
        nextButton_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton_2, 'tStartRefresh')  # time at next scr refresh
        nextButton_2.setAutoDraw(True)
    # *mouse_2* updates
    if mouse_2.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mouse_2.frameNStart = frameN  # exact frame index
        mouse_2.tStart = t  # local t and not account for scr refresh
        mouse_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse_2, 'tStartRefresh')  # time at next scr refresh
        mouse_2.status = STARTED
        mouse_2.mouseClock.reset()
        prevButtonState = mouse_2.getPressed()  # if button is down already this ISN'T a new click
    if mouse_2.status == STARTED:  # only update if started and not finished!
        buttons = mouse_2.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if (nextButton_2.status == STARTED and Q10Resp.rating and Q11Resp.rating and Q12Resp.rating and Q13Resp.rating and Q14Resp.rating):
                    try:
                        iter(nextButton_2)
                        clickableList = nextButton_2
                    except:
                        clickableList = [nextButton_2]
                    for obj in clickableList:
                        if obj.contains(mouse_2):
                            gotValidClick = True
                            mouse_2.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Personal_Responses_to_Music__Perception_pg1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Personal_Responses_to_Music__Perception_pg1"-------
for thisComponent in Personal_Responses_to_Music__Perception_pg1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
        
thisExp.addData('Q10Resp.response', Q10Resp.getRating())
thisExp.addData('Q11Resp.response', Q11Resp.getRating())
thisExp.addData('Q12Resp.response', Q12Resp.getRating())
thisExp.addData('Q13Resp.response', Q13Resp.getRating())
thisExp.addData('Q14Resp.response', Q14Resp.getRating())
# store data for thisExp (ExperimentHandler)
x, y = mouse_2.getPos()
# the Routine "Personal_Responses_to_Music__Perception_pg1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Personal_Responses_to_Music__Perception_pg2"-------
continueRoutine = True
# update component parameters for each repeat
Q15Resp.reset()
Q16Resp.reset()
Q17Resp.reset()
Q18Resp.reset()
# setup some python lists for storing info about the mouse_2
mouse_2.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
Personal_Responses_to_Music__Perception_pg2Components = [personalResponsesHeadingP, Q15, Q15Resp, Q16, Q16Resp, Q17, Q17Resp, Q18, Q18Resp, nextButton_2, mouse_2]
for thisComponent in Personal_Responses_to_Music__Perception_pg2Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Personal_Responses_to_Music__Perception_pg2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Personal_Responses_to_Music__Perception_pg2"-------
while continueRoutine:
    # get current time
    t = Personal_Responses_to_Music__Perception_pg2Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Personal_Responses_to_Music__Perception_pg2Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *personalResponsesHeadingP* updates
    if personalResponsesHeadingP.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        personalResponsesHeadingP.frameNStart = frameN  # exact frame index
        personalResponsesHeadingP.tStart = t  # local t and not account for scr refresh
        personalResponsesHeadingP.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(personalResponsesHeadingP, 'tStartRefresh')  # time at next scr refresh
        personalResponsesHeadingP.setAutoDraw(True)

    # *Q15* updates
    if Q15.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q15.frameNStart = frameN  # exact frame index
        Q15.tStart = t  # local t and not account for scr refresh
        Q15.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q15, 'tStartRefresh')  # time at next scr refresh
        Q15.setAutoDraw(True)
    
    # *Q15Resp* updates
    if Q15Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q15Resp.frameNStart = frameN  # exact frame index
        Q15Resp.tStart = t  # local t and not account for scr refresh
        Q15Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q15Resp, 'tStartRefresh')  # time at next scr refresh
        Q15Resp.setAutoDraw(True)
        
    # *Q16* updates
    if Q16.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q16.frameNStart = frameN  # exact frame index
        Q16.tStart = t  # local t and not account for scr refresh
        Q16.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q16, 'tStartRefresh')  # time at next scr refresh
        Q16.setAutoDraw(True)
    
    # *Q16Resp* updates
    if Q16Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q16Resp.frameNStart = frameN  # exact frame index
        Q16Resp.tStart = t  # local t and not account for scr refresh
        Q16Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q16Resp, 'tStartRefresh')  # time at next scr refresh
        Q16Resp.setAutoDraw(True)
    
    # *Q17* updates
    if Q17.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q17.frameNStart = frameN  # exact frame index
        Q17.tStart = t  # local t and not account for scr refresh
        Q17.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q17, 'tStartRefresh')  # time at next scr refresh
        Q17.setAutoDraw(True)
    
    # *Q17Resp* updates
    if Q17Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q17Resp.frameNStart = frameN  # exact frame index
        Q17Resp.tStart = t  # local t and not account for scr refresh
        Q17Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q17Resp, 'tStartRefresh')  # time at next scr refresh
        Q17Resp.setAutoDraw(True)
    
    # *Q18* updates
    if Q18.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q18.frameNStart = frameN  # exact frame index
        Q18.tStart = t  # local t and not account for scr refresh
        Q18.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q18, 'tStartRefresh')  # time at next scr refresh
        Q18.setAutoDraw(True)
    
    # *Q18Resp* updates
    if Q18Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q18Resp.frameNStart = frameN  # exact frame index
        Q18Resp.tStart = t  # local t and not account for scr refresh
        Q18Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q18Resp, 'tStartRefresh')  # time at next scr refresh
        Q18Resp.setAutoDraw(True)
    
            # *nextButton_2* updates
    if (nextButton_2.status == NOT_STARTED and Q15Resp.rating and Q16Resp.rating and Q17Resp.rating and Q18Resp.rating):
        # keep track of start time/frame for later
        nextButton_2.frameNStart = frameN  # exact frame index
        nextButton_2.tStart = t  # local t and not account for scr refresh
        nextButton_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton_2, 'tStartRefresh')  # time at next scr refresh
        nextButton_2.setAutoDraw(True)
    # *mouse_2* updates
    if mouse_2.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mouse_2.frameNStart = frameN  # exact frame index
        mouse_2.tStart = t  # local t and not account for scr refresh
        mouse_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse_2, 'tStartRefresh')  # time at next scr refresh
        mouse_2.status = STARTED
        mouse_2.mouseClock.reset()
        prevButtonState = mouse_2.getPressed()  # if button is down already this ISN'T a new click
    if mouse_2.status == STARTED:  # only update if started and not finished!
        buttons = mouse_2.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if (nextButton_2.status == STARTED and Q15Resp.rating and Q16Resp.rating and Q17Resp.rating and Q18Resp.rating):
                    try:
                        iter(nextButton_2)
                        clickableList = nextButton_2
                    except:
                        clickableList = [nextButton_2]
                    for obj in clickableList:
                        if obj.contains(mouse_2):
                            gotValidClick = True
                            mouse_2.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Personal_Responses_to_Music__Perception_pg2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Personal_Responses_to_Music__Perception_pg2"-------
for thisComponent in Personal_Responses_to_Music__Perception_pg2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
        
thisExp.addData('Q15Resp.response', Q15Resp.getRating())
thisExp.addData('Q16Resp.response', Q16Resp.getRating())
thisExp.addData('Q17Resp.response', Q17Resp.getRating())
thisExp.addData('Q18Resp.response', Q18Resp.getRating())
# store data for thisExp (ExperimentHandler)
x, y = mouse_2.getPos()
# the Routine "Personal_Responses_to_Music__Perception_pg2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Personal_Responses_to_Music__Emotion_pg1"-------
continueRoutine = True
# update component parameters for each repeat
Q19Resp.reset()
Q20Resp.reset()
Q21Resp.reset()
Q22Resp.reset()
Q23Resp.reset()
# setup some python lists for storing info about the mouse_4
mouse_4.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
Personal_Responses_to_Music__Emotion_pg1Components = [personalResponsesHeadingE, Q19, Q19Resp, Q20, Q20Resp, Q21, Q21Resp, Q22, Q22Resp, Q23, Q23Resp, nextButton_4, mouse_4]
for thisComponent in Personal_Responses_to_Music__Emotion_pg1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Personal_Responses_to_Music__Emotion_pg1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Personal_Responses_to_Music__Emotion_pg1"-------
while continueRoutine:
    # get current time
    t = Personal_Responses_to_Music__Emotion_pg1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Personal_Responses_to_Music__Emotion_pg1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *personalResponsesHeadingE* updates
    if personalResponsesHeadingE.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        personalResponsesHeadingE.frameNStart = frameN  # exact frame index
        personalResponsesHeadingE.tStart = t  # local t and not account for scr refresh
        personalResponsesHeadingE.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(personalResponsesHeadingE, 'tStartRefresh')  # time at next scr refresh
        personalResponsesHeadingE.setAutoDraw(True)
    
    # *Q19* updates
    if Q19.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q19.frameNStart = frameN  # exact frame index
        Q19.tStart = t  # local t and not account for scr refresh
        Q19.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q19, 'tStartRefresh')  # time at next scr refresh
        Q19.setAutoDraw(True)
    
    # *Q19Resp* updates
    if Q19Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q19Resp.frameNStart = frameN  # exact frame index
        Q19Resp.tStart = t  # local t and not account for scr refresh
        Q19Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q19Resp, 'tStartRefresh')  # time at next scr refresh
        Q19Resp.setAutoDraw(True)
    
    # *Q20* updates
    if Q20.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q20.frameNStart = frameN  # exact frame index
        Q20.tStart = t  # local t and not account for scr refresh
        Q20.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q20, 'tStartRefresh')  # time at next scr refresh
        Q20.setAutoDraw(True)
    
    # *Q20Resp* updates
    if Q20Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q20Resp.frameNStart = frameN  # exact frame index
        Q20Resp.tStart = t  # local t and not account for scr refresh
        Q20Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q20Resp, 'tStartRefresh')  # time at next scr refresh
        Q20Resp.setAutoDraw(True)
    
    # *Q21* updates
    if Q21.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q21.frameNStart = frameN  # exact frame index
        Q21.tStart = t  # local t and not account for scr refresh
        Q21.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q21, 'tStartRefresh')  # time at next scr refresh
        Q21.setAutoDraw(True)
    
    # *Q21Resp* updates
    if Q21Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q21Resp.frameNStart = frameN  # exact frame index
        Q21Resp.tStart = t  # local t and not account for scr refresh
        Q21Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q21Resp, 'tStartRefresh')  # time at next scr refresh
        Q21Resp.setAutoDraw(True)
    
    # *Q22* updates
    if Q22.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q22.frameNStart = frameN  # exact frame index
        Q22.tStart = t  # local t and not account for scr refresh
        Q22.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q22, 'tStartRefresh')  # time at next scr refresh
        Q22.setAutoDraw(True)
    
    # *Q22Resp* updates
    if Q22Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q22Resp.frameNStart = frameN  # exact frame index
        Q22Resp.tStart = t  # local t and not account for scr refresh
        Q22Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q22Resp, 'tStartRefresh')  # time at next scr refresh
        Q22Resp.setAutoDraw(True)
    
    # *Q23* updates
    if Q23.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q23.frameNStart = frameN  # exact frame index
        Q23.tStart = t  # local t and not account for scr refresh
        Q23.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q23, 'tStartRefresh')  # time at next scr refresh
        Q23.setAutoDraw(True)
    
    # *Q23Resp* updates
    if Q23Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q23Resp.frameNStart = frameN  # exact frame index
        Q23Resp.tStart = t  # local t and not account for scr refresh
        Q23Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q23Resp, 'tStartRefresh')  # time at next scr refresh
        Q23Resp.setAutoDraw(True)
    
    # *nextButton_4* updates
    if (nextButton_4.status == NOT_STARTED and Q19Resp.rating and Q20Resp.rating and Q21Resp.rating and Q22Resp.rating and Q23Resp.rating):
        # keep track of start time/frame for later
        nextButton_4.frameNStart = frameN  # exact frame index
        nextButton_4.tStart = t  # local t and not account for scr refresh
        nextButton_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton_2, 'tStartRefresh')  # time at next scr refresh
        nextButton_4.setAutoDraw(True)
    # *mouse_4* updates
    if mouse_4.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mouse_4.frameNStart = frameN  # exact frame index
        mouse_4.tStart = t  # local t and not account for scr refresh
        mouse_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse_4, 'tStartRefresh')  # time at next scr refresh
        mouse_4.status = STARTED
        mouse_4.mouseClock.reset()
        prevButtonState = mouse_4.getPressed()  # if button is down already this ISN'T a new click
    if mouse_4.status == STARTED:  # only update if started and not finished!
        buttons = mouse_4.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if (nextButton_4.status == STARTED and Q19Resp.rating and Q20Resp.rating and Q21Resp.rating and Q22Resp.rating and Q23Resp.rating):
                    try:
                        iter(nextButton_4)
                        clickableList = nextButton_4
                    except:
                        clickableList = [nextButton_4]
                    for obj in clickableList:
                        if obj.contains(mouse_4):
                            gotValidClick = True
                            mouse_4.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Personal_Responses_to_Music__Emotion_pg1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Personal_Responses_to_Music__Emotion_pg1"-------
for thisComponent in Personal_Responses_to_Music__Emotion_pg1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('Q19Resp.response', Q19Resp.getRating())
thisExp.addData('Q20Resp.response', Q20Resp.getRating())
thisExp.addData('Q21Resp.response', Q21Resp.getRating())
thisExp.addData('Q22Resp.response', Q22Resp.getRating())
thisExp.addData('Q23Resp.response', Q23Resp.getRating())

# the Routine "Personal_Responses_to_Music__Emotion_pg1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Personal_Responses_to_Music__Emotion_pg2"-------
continueRoutine = True
# update component parameters for each repeat
Q24Resp.reset()
# setup some python lists for storing info about the mouse_4
mouse_4.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
Personal_Responses_to_Music__Emotion_pg2Components = [personalResponsesHeadingE, Q24, Q24Resp, nextButton_4, mouse_4]
for thisComponent in Personal_Responses_to_Music__Emotion_pg1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Personal_Responses_to_Music__Emotion_pg1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Personal_Responses_to_Music__Emotion_pg2"-------
while continueRoutine:
    # get current time
    t = Personal_Responses_to_Music__Emotion_pg2Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Personal_Responses_to_Music__Emotion_pg2Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *personalResponsesHeadingE* updates
    if personalResponsesHeadingE.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        personalResponsesHeadingE.frameNStart = frameN  # exact frame index
        personalResponsesHeadingE.tStart = t  # local t and not account for scr refresh
        personalResponsesHeadingE.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(personalResponsesHeadingE, 'tStartRefresh')  # time at next scr refresh
        personalResponsesHeadingE.setAutoDraw(True)
    
    # *Q24* updates
    if Q24.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q24.frameNStart = frameN  # exact frame index
        Q24.tStart = t  # local t and not account for scr refresh
        Q24.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q24, 'tStartRefresh')  # time at next scr refresh
        Q24.setAutoDraw(True)
    
    # *Q24Resp* updates
    if Q24Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Q24Resp.frameNStart = frameN  # exact frame index
        Q24Resp.tStart = t  # local t and not account for scr refresh
        Q24Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Q24Resp, 'tStartRefresh')  # time at next scr refresh
        Q24Resp.setAutoDraw(True)
    
# *nextButton_4* updates
    if (nextButton_4.status == NOT_STARTED and Q24Resp.rating):
        # keep track of start time/frame for later
        nextButton_4.frameNStart = frameN  # exact frame index
        nextButton_4.tStart = t  # local t and not account for scr refresh
        nextButton_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton_2, 'tStartRefresh')  # time at next scr refresh
        nextButton_4.setAutoDraw(True)
    # *mouse_4* updates
    if mouse_4.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mouse_4.frameNStart = frameN  # exact frame index
        mouse_4.tStart = t  # local t and not account for scr refresh
        mouse_4.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse_4, 'tStartRefresh')  # time at next scr refresh
        mouse_4.status = STARTED
        mouse_4.mouseClock.reset()
        prevButtonState = mouse_4.getPressed()  # if button is down already this ISN'T a new click
    if mouse_4.status == STARTED:  # only update if started and not finished!
        buttons = mouse_4.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                if (nextButton_4.status == STARTED and Q24Resp.rating):
                    try:
                        iter(nextButton_4)
                        clickableList = nextButton_4
                    except:
                        clickableList = [nextButton_4]
                    for obj in clickableList:
                        if obj.contains(mouse_4):
                            gotValidClick = True
                            mouse_4.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Personal_Responses_to_Music__Emotion_pg2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Personal_Responses_to_Music__Emotion_pg2"-------
for thisComponent in Personal_Responses_to_Music__Emotion_pg2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('Q24Resp.response', Q24Resp.getRating())
thisExp.nextEntry()
# store data for thisExp (ExperimentHandler)
x, y = mouse_4.getPos()
# the Routine "Personal_Responses_to_Music__Emotion_pg2" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "thisPartComplete"-------
# update component parameters for each repeat
# keep track of which components have finished
continueRoutine = True

thisPartCompleteComponents = [thisPartCompleteText]
for thisComponent in thisPartCompleteComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
thisPartCompleteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
    
# -------Run Routine "thisPartComplete"-------
while continueRoutine:
    # get current time
    t = thisPartCompleteClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=thisPartCompleteClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    if thisPartCompleteText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        thisPartCompleteText.frameNStart = frameN  # exact frame index
        thisPartCompleteText.tStart = t  # local t and not account for scr refresh
        thisPartCompleteText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(thisPartCompleteText, 'tStartRefresh')  # time at next scr refresh
        thisPartCompleteText.setAutoDraw(True) 
        
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    if thisPartCompleteClock.getTime() > 4:
        thisPartCompleteText.status = FINISHED
        
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thisPartCompleteComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    
# -------Ending Routine "thisPartComplete"-------
for thisComponent in thisPartCompleteComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

#Save csv of data:
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
thisExp.abort()
#Calculate GSMI score:
Questionnaire_GSMI_Score_Calculator.calcAndWrite(filename+'.csv')

#thisExp.abort()  # or data files will save again on exit
logging.flush()

# make sure everything is closed down
win.close()
core.quit()