"attnOneInstNoOBs"

from psychopy import locale_setup
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, prefs
prefs.hardware['audioLatencyMode'] = '3'
prefs.hardware['audioDevice'] = 'Speakers (DAC8PRO)'
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import psychopy.iohub as io
from psychopy.hardware import keyboard
from pyo import *
import random
import json

sys.path.append('.')
from constants import *

SOUNDCARD_DEVICE_NAME = 'DAC8PRO'

volume_level = 0.05
volume_ratio = [1, 1, 7.5]
spk_volume = [x * volume_level for x in volume_ratio]
PART_3_OUT_CHANNELS = 3
TRIGGER_CHN = 2

s = Server(nchnls=PART_3_OUT_CHANNELS, duplex=0)
devices = pa_get_output_devices()
indx = []
#for name in devices[0]:
for i in range(len(devices[0])):
    name = devices[0][i]
    if SOUNDCARD_DEVICE_NAME in name:
        soundcard_idx = devices[1][devices[0].index(name)]
        s.setOutputDevice(soundcard_idx)
        indx.append(devices[1][i])
        break
s = s.boot()
s.start()

mm = Mixer(outs=PART_3_OUT_CHANNELS)

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.2'
task = 'attnOneInstNoOBs'
expInfo = {'Participant ID': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=task)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['task'] = task
expInfo['psychopyVersion'] = psychopyVersion

## Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
dataPath = _thisDir + "/Data/"
groupAssignmentFile = dataPath + "Participant Groups.txt" #Needed for taking collecting stimuli, and saving to right place:
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

filename = participantPath + '/Part 3 Data'

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
    originPath= _thisDir + '/Part 3 Script.py',
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

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
top_instr_txt = visual.TextStim(win=win, name='top_instr_txt',
    text='You will be told to either attend or NOT attend to some music (let your mind wander), before it plays. Please close your eyes, and try not to move whilst it plays. After this, you will be asked about what you were attending to and you can take a break.\n\nIf you have any questions at all please ask the experimenters.',
    font='Open Sans',
    pos=(0, 0.15), height=0.05, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
mouse_2 = event.Mouse(win=win)
x, y = [None, None]
mouse_2.mouseClock = core.Clock()
nextButton_instruct = visual.ImageStim(
    win=win,
    name='nextButton_instruct', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)

# Initialize components for Routine "practiceReady"
practiceReadyClock = core.Clock()
#One version of the instructions for practice trial, one for later.
practiceReadyTxt = visual.TextStim(win=win, name='practiceReadyTxt',
    text='We are now going to run a practice trial.\n\nWhen you are ready, click "NEXT".',
    font='Open Sans',
    pos=(0, 0.15), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
mouse_4 = event.Mouse(win=win)
x, y = [None, None]
mouse_4.mouseClock = core.Clock()
nextButton_R1B = visual.ImageStim(
    win=win,
    name='nextButton_R1B', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
attendNote = visual.TextStim(win=win, name='attendNote',
    text='Attend to the music\n',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
dontAttendNote = visual.TextStim(win=win, name='dontAttendNote',
    text='Do NOT attend to the music\n',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "QuestionBreakPause"
QuestionBreakPauseClock = core.Clock()
top_instr_txt_4 = visual.TextStim(win=win, name='top_instr_txt_4',
    text='The experimenter will now ask you about the music or your thoughts, and you can take a break. When you are ready for the next trial, click "NEXT".',
    font='Open Sans',
    pos=(0, 0.15), height=0.05, wrapWidth=1.65, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
mouse_4 = event.Mouse(win=win)
x, y = [None, None]
mouse_4.mouseClock = core.Clock()
nextButton_R1B = visual.ImageStim(
    win=win,
    name='nextButton_R1B', 
    image='next.png', mask=None, anchor='center',
    ori=0.0, pos=(0, -0.4), size=(0.15, 0.075),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
    
# Initialize components for Routine "movingToMainTrials"
movingToMainTrialsClock = core.Clock()
movingToMainTrialsText = visual.TextStim(win=win, name='movingToMainTrialsText',
    text='We will now move on to the main trials.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
    
# Initialize components for Routine "thisPartComplete"
thisPartCompleteClock = core.Clock()
thisPartCompleteText = visual.TextStim(win=win, name='thisPartCompleteText',
    text='Part 3 complete.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
    
# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "instructions"-------
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse_2
mouse_2.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
instructionsComponents = [top_instr_txt, mouse_2, nextButton_instruct]
for thisComponent in instructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
instructionsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=instructionsClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *top_instr_txt* updates
    if top_instr_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        top_instr_txt.frameNStart = frameN  # exact frame index
        top_instr_txt.tStart = t  # local t and not account for scr refresh
        top_instr_txt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(top_instr_txt, 'tStartRefresh')  # time at next scr refresh
        top_instr_txt.setAutoDraw(True)
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
                try:
                    iter(nextButton_instruct)
                    clickableList = nextButton_instruct
                except:
                    clickableList = [nextButton_instruct]
                for obj in clickableList:
                    if obj.contains(mouse_2):
                        gotValidClick = True
                        mouse_2.clicked_name.append(obj.name)
                if gotValidClick:  
                    continueRoutine = False  # abort routine on response
    
    # *nextButton_instruct* updates
    if nextButton_instruct.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        nextButton_instruct.frameNStart = frameN  # exact frame index
        nextButton_instruct.tStart = t  # local t and not account for scr refresh
        nextButton_instruct.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton_instruct, 'tStartRefresh')  # time at next scr refresh
        nextButton_instruct.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if attendNote != FINISHED and dontAttendNote != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
x, y = mouse_2.getPos()
buttons = mouse_2.getPressed()
if sum(buttons):
    # check if the mouse was inside our 'clickable' objects
    gotValidClick = False
    try:
        iter(nextButton_instruct)
        clickableList = nextButton_instruct
    except:
        clickableList = [nextButton_instruct]
    for obj in clickableList:
        if obj.contains(mouse_2):
            gotValidClick = True
            mouse_2.clicked_name.append(obj.name)
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "practiceReady"-------
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse_4
mouse_4.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
practiceReadyComponents = [practiceReadyTxt, mouse_4, nextButton_R1B]
for thisComponent in practiceReadyComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
practiceReadyClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "practiceReady"-------
while continueRoutine:
    # get current time
    t = practiceReadyClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=practiceReadyClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *practiceReadyTxt* updates
    if practiceReadyTxt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        practiceReadyTxt.frameNStart = frameN  # exact frame index
        practiceReadyTxt.tStart = t  # local t and not account for scr refresh
        practiceReadyTxt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practiceReadyTxt, 'tStartRefresh')  # time at next scr refresh
        practiceReadyTxt.setAutoDraw(True)
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
                try:
                    iter(nextButton_R1B)
                    clickableList = nextButton_R1B
                except:
                    clickableList = [nextButton_R1B]
                for obj in clickableList:
                    if obj.contains(mouse_4):
                        gotValidClick = True
                        mouse_4.clicked_name.append(obj.name)
                if gotValidClick:  
                    continueRoutine = False  # abort routine on response
    
    # *nextButton_R1B* updates
    if nextButton_R1B.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        nextButton_R1B.frameNStart = frameN  # exact frame index
        nextButton_R1B.tStart = t  # local t and not account for scr refresh
        nextButton_R1B.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(nextButton_R1B, 'tStartRefresh')  # time at next scr refresh
        nextButton_R1B.setAutoDraw(True)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in practiceReadyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "practiceReady"-------
for thisComponent in practiceReadyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# store data for thisExp (ExperimentHandler)
x, y = mouse_4.getPos()
buttons = mouse_4.getPressed()
if sum(buttons):
    # check if the mouse was inside our 'clickable' objects
    gotValidClick = False
    try:
        iter(nextButton_R1B)
        clickableList = nextButton_R1B
    except:
        clickableList = [nextButton_R1B]
    for obj in clickableList:
        if obj.contains(mouse_4):
            gotValidClick = True
            mouse_4.clicked_name.append(obj.name)
# the Routine "practiceReady" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#block0 contains the practice trial. Additional practice trials can be added in.
# set up handler to look after randomisation of conditions etc
#Note we only want ONE piece to be picked for practice trial - later we include a break to deal with this.
block0 = data.TrialHandler(nReps=1.0, method='random', originPath=-1,
    trialList=data.importConditions(participantPath + '\practiceStimuliList.xlsx', selection='0:3'),
    seed=None, name='block0')
thisExp.addLoop(block0)  # add the loop to the experiment
thisBlock0 = block0.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock1.rgb)
if thisBlock0 != None:
    for paramName in thisBlock0:
        exec('{} = thisBlock0[paramName]'.format(paramName))
        
for thisBlock0 in block0:
    trial = {}

# abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock0 != None:
        for paramName in thisBlock0:
            exec('{} = thisBlock0[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "practiceTrial"-------
    continueRoutine = True
    # update stimuliStarted parameter for each repeat
    stimuliStarted = False
    
    # keep track of which components have finished
    trialComponents = [attendNote, dontAttendNote]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    #Logging:
    trigger_filename, trigger_ext = os.path.splitext(trigger)
    trigger_logfile = os.path.abspath(trigger_filename + '.txt')
    trial['trigger'] = os.path.abspath(trigger)
    trial['trigger_log'] = os.path.abspath(trigger_logfile)
    
    trial['stimuli'] = []
    spk_name = f"stimuli_0"
    trial['stimuli'].append(os.path.abspath(globals()[spk_name]))
    
    #Get attendance condition:
    attend = f"{music_attended}"
    
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "practiceTrial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
            
        # *attendNote* updates
        if attend=="Yes" and attendNote.status == NOT_STARTED:
            # keep track of start time/frame for later
            attendNote.frameNStart = frameN  # exact frame index
            attendNote.tStart = t  # local t and not account for scr refresh
            attendNote.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(attendNote, 'tStartRefresh')  # time at next scr refresh
            attendNote.setAutoDraw(True)
        if attendNote.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > attendNote.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                attendNote.tStop = t  # not accounting for scr refresh
                attendNote.frameNStop = frameN  # exact frame index
                win.timeOnFlip(attendNote, 'tStopRefresh')  # time at next scr refresh
                attendNote.setAutoDraw(False)
        
        # *dontAttendNote* updates
        if attend!="Yes" and dontAttendNote.status == NOT_STARTED:
            # keep track of start time/frame for later
            dontAttendNote.frameNStart = frameN  # exact frame index
            dontAttendNote.tStart = t  # local t and not account for scr refresh
            dontAttendNote.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(dontAttendNote, 'tStartRefresh')  # time at next scr refresh
            dontAttendNote.setAutoDraw(True)
        if dontAttendNote.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > dontAttendNote.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                dontAttendNote.tStop = t  # not accounting for scr refresh
                dontAttendNote.frameNStop = frameN  # exact frame index
                win.timeOnFlip(dontAttendNote, 'tStopRefresh')  # time at next scr refresh
                dontAttendNote.setAutoDraw(False)
        
        if stimuliStarted == False and (attendNote.status == FINISHED or dontAttendNote.status == FINISHED):     
            #Play music+trig:
            #Use mixer to play stereo audio, plus mono trigger:
            for i in range(PART_3_OUT_CHANNELS):
                mm.delInput(i) #Ensure any previous inputs are cleared
            
            music_stereo = SfPlayer(stimuli_0)
            mm.addInput(0, music_stereo[0])
            mm.addInput(1, music_stereo[1])
        
            trigger_mono = SfPlayer(trigger)
            mm.addInput(2, trigger_mono)
            
            #As well as inputting the streams, specify amplitudes:
            for i in range(PART_3_OUT_CHANNELS):
                mm.setAmp(i, i, spk_volume[i])
            practiceTrialAudioStartTime = globalClock.getTime()
            block0.addData('Practice Music Start Time', practiceTrialAudioStartTime)
            mm.out()
            stimuliStarted = True
     
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        if tThisFlip >= PART_3_STIMULI_LEN+5.0-frameTolerance:
            continueRoutine = False
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()            
    mm.stop()
    # -------Ending Routine "practiceTrial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    if attend == "Yes":
        print(f'{stimuli_0} was attended')
    else:
        print(f'{stimuli_0} was unattended')
    # the Routine "practiceTrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "QuestionBreakPause"-------
    continueRoutine = True
    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse_4
    mouse_4.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    QuestionBreakPauseComponents = [top_instr_txt_4, mouse_4, nextButton_R1B]
    for thisComponent in QuestionBreakPauseComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    QuestionBreakPauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "QuestionBreakPause"-------
    while continueRoutine:
        # get current time
        t = QuestionBreakPauseClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=QuestionBreakPauseClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *top_instr_txt_4* updates
        if top_instr_txt_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            top_instr_txt_4.frameNStart = frameN  # exact frame index
            top_instr_txt_4.tStart = t  # local t and not account for scr refresh
            top_instr_txt_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(top_instr_txt_4, 'tStartRefresh')  # time at next scr refresh
            top_instr_txt_4.setAutoDraw(True)
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
                    try:
                        iter(nextButton_R1B)
                        clickableList = nextButton_R1B
                    except:
                        clickableList = [nextButton_R1B]
                    for obj in clickableList:
                        if obj.contains(mouse_4):
                            gotValidClick = True
                            mouse_4.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
        
        # *nextButton_R1B* updates
        if nextButton_R1B.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            nextButton_R1B.frameNStart = frameN  # exact frame index
            nextButton_R1B.tStart = t  # local t and not account for scr refresh
            nextButton_R1B.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(nextButton_R1B, 'tStartRefresh')  # time at next scr refresh
            nextButton_R1B.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in QuestionBreakPauseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "QuestionBreakPause"-------
    for thisComponent in QuestionBreakPauseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for thisExp (ExperimentHandler)
    x, y = mouse_4.getPos()
    buttons = mouse_4.getPressed()
    if sum(buttons):
        # check if the mouse was inside our 'clickable' objects
        gotValidClick = False
        try:
            iter(nextButton_R1B)
            clickableList = nextButton_R1B
        except:
            clickableList = [nextButton_R1B]
        for obj in clickableList:
            if obj.contains(mouse_4):
                gotValidClick = True
                mouse_4.clicked_name.append(obj.name)
    
    break
# completed 1.0 repeats of 'block0'   

thisExp.nextEntry() #Next row on the record.
routineTimer.reset()
# ------Prepare to start Routine "movingToMainTrials"-------
# update component parameters for each repeat
# keep track of which components have finished
continueRoutine = True

movingToMainTrialsComponents = [movingToMainTrialsText]
for thisComponent in movingToMainTrialsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
movingToMainTrialsClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
    
# -------Run Routine "movingToMainTrials"-------
while continueRoutine:
    # get current time
    t = movingToMainTrialsClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=movingToMainTrialsClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    if movingToMainTrialsText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        movingToMainTrialsText.frameNStart = frameN  # exact frame index
        movingToMainTrialsText.tStart = t  # local t and not account for scr refresh
        movingToMainTrialsText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(movingToMainTrialsText, 'tStartRefresh')  # time at next scr refresh
        movingToMainTrialsText.setAutoDraw(True) 
        
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    if movingToMainTrialsClock.getTime() > 4:
        movingToMainTrialsText.status = FINISHED
        
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in movingToMainTrialsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    
# -------Ending Routine "movingToMainTrials"-------
for thisComponent in movingToMainTrialsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
        
routineTimer.reset()
        

# playing part starting trig
continueRoutine = True
routineTimer.add(1)
startExpTrigger = SfPlayer('P3_start_trigger.wav')
for i in range(PART_3_OUT_CHANNELS):
    mm.delInput(i) #Ensure any previous inputs are cleared
mm.addInput(0, startExpTrigger) #One input - the start trigger
mm.setAmp(0,TRIGGER_CHN, spk_volume[TRIGGER_CHN])
thisExp.addData('Start Trigger Start Time', globalClock.getTime())
while continueRoutine and routineTimer.getTime() > 0:
    mm.out()
mm.stop()
routineTimer.reset()
# end of playing part starting trig

# set up handler to look after randomisation of conditions etc
block1 = data.TrialHandler(nReps=1.0, method='random', originPath=-1,
    trialList=data.importConditions(participantPath + '\stimuliList.xlsx', selection='0:15'),
    seed=None, name='block1')
thisExp.addLoop(block1)  # add the loop to the experiment
thisBlock1 = block1.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock1.rgb)
if thisBlock1 != None:
    for paramName in thisBlock1:
        exec('{} = thisBlock1[paramName]'.format(paramName))

idx = 0
for thisBlock1 in block1:
    trial = {}
    idx += 1
    print(f'Not counting the practice trial, this is trial {idx}')
    # abbreviate parameter names if possible (e.g. rgb = thisBlock1.rgb)
    if thisBlock1 != None:
        for paramName in thisBlock1:
            exec('{} = thisBlock1[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "trial"-------
    continueRoutine = True
    # update stimuliStarted parameter for each repeat
    stimuliStarted = False
    
    # keep track of which components have finished
    trialComponents = [attendNote, dontAttendNote]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
            
    #Logging:
    trigger_filename, trigger_ext = os.path.splitext(trigger)
    trigger_logfile = os.path.abspath(trigger_filename + '.txt')
    trial['trigger'] = os.path.abspath(trigger)
    trial['trigger_log'] = os.path.abspath(trigger_logfile)
    
    trial['stimuli'] = []
    spk_name = f"stimuli_0"
    trial['stimuli'].append(os.path.abspath(globals()[spk_name]))
    
    #Get attendance condition:
    attend = f"{music_attended}"
    
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
            
        # *attendNote* updates
        if attend=="Yes" and attendNote.status == NOT_STARTED:
            # keep track of start time/frame for later
            attendNote.frameNStart = frameN  # exact frame index
            attendNote.tStart = t  # local t and not account for scr refresh
            attendNote.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(attendNote, 'tStartRefresh')  # time at next scr refresh
            attendNote.setAutoDraw(True)
        if attendNote.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > attendNote.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                attendNote.tStop = t  # not accounting for scr refresh
                attendNote.frameNStop = frameN  # exact frame index
                win.timeOnFlip(attendNote, 'tStopRefresh')  # time at next scr refresh
                attendNote.setAutoDraw(False)
        
        # *dontAttendNote* updates
        if attend!="Yes" and dontAttendNote.status == NOT_STARTED:
            # keep track of start time/frame for later
            dontAttendNote.frameNStart = frameN  # exact frame index
            dontAttendNote.tStart = t  # local t and not account for scr refresh
            dontAttendNote.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(dontAttendNote, 'tStartRefresh')  # time at next scr refresh
            dontAttendNote.setAutoDraw(True)
        if dontAttendNote.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > dontAttendNote.tStartRefresh + 5.0-frameTolerance:
                # keep track of stop time/frame for later
                dontAttendNote.tStop = t  # not accounting for scr refresh
                dontAttendNote.frameNStop = frameN  # exact frame index
                win.timeOnFlip(dontAttendNote, 'tStopRefresh')  # time at next scr refresh
                dontAttendNote.setAutoDraw(False)
        
        if stimuliStarted == False and (attendNote.status == FINISHED or dontAttendNote.status == FINISHED):
            #Play music+trig:
            #Use mixer to play stereo audio, plus mono trigger:
            for i in range(PART_3_OUT_CHANNELS):
                mm.delInput(i) #Ensure any previous inputs are cleared
            
            music_stereo = SfPlayer(stimuli_0)
            mm.addInput(0, music_stereo[0])
            mm.addInput(1, music_stereo[1])
        
            trigger_mono = SfPlayer(trigger)
            mm.addInput(2, trigger_mono)
            
            #As well as inputting the streams, specify amplitudes:
            for i in range(PART_3_OUT_CHANNELS):
                mm.setAmp(i, i, spk_volume[i])
            mainTrialAudioStartTime = globalClock.getTime()
            block1.addData('Main Trial Mus Start Time', mainTrialAudioStartTime)
            mm.out()
            stimuliStarted = True
     
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        if tThisFlip >= PART_3_STIMULI_LEN+5.0-frameTolerance:
            continueRoutine = False
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()            
    mm.stop()
    jsondata['trial_number'] = len(jsondata['trials'])
    # save json file
    with open(jsonfilename, 'w') as fp:
        json.dump(jsondata, fp, separators=(',\n', ': '))
        fp.close()
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    thisExp.nextEntry() #Next row on the record.
    
    if attend == "Yes":
        print(f'{stimuli_0} was attended')
    else:
        print(f'{stimuli_0} was unattended')
        
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "QuestionBreakPause"-------
    continueRoutine = True
    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse_4
    mouse_4.clicked_name = []
    gotValidClick = False  # until a click is received
    # keep track of which components have finished
    QuestionBreakPauseComponents = [top_instr_txt_4, mouse_4, nextButton_R1B]
    for thisComponent in QuestionBreakPauseComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    QuestionBreakPauseClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "QuestionBreakPause"-------
    while continueRoutine:
        # get current time
        t = QuestionBreakPauseClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=QuestionBreakPauseClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *top_instr_txt_4* updates
        if top_instr_txt_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            top_instr_txt_4.frameNStart = frameN  # exact frame index
            top_instr_txt_4.tStart = t  # local t and not account for scr refresh
            top_instr_txt_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(top_instr_txt_4, 'tStartRefresh')  # time at next scr refresh
            top_instr_txt_4.setAutoDraw(True)
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
                    try:
                        iter(nextButton_R1B)
                        clickableList = nextButton_R1B
                    except:
                        clickableList = [nextButton_R1B]
                    for obj in clickableList:
                        if obj.contains(mouse_4):
                            gotValidClick = True
                            mouse_4.clicked_name.append(obj.name)
                    if gotValidClick:  
                        continueRoutine = False  # abort routine on response
        
        # *nextButton_R1B* updates
        if nextButton_R1B.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            nextButton_R1B.frameNStart = frameN  # exact frame index
            nextButton_R1B.tStart = t  # local t and not account for scr refresh
            nextButton_R1B.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(nextButton_R1B, 'tStartRefresh')  # time at next scr refresh
            nextButton_R1B.setAutoDraw(True)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in QuestionBreakPauseComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "QuestionBreakPause"-------
    for thisComponent in QuestionBreakPauseComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for thisExp (ExperimentHandler)
    x, y = mouse_4.getPos()
    buttons = mouse_4.getPressed()
    if sum(buttons):
        # check if the mouse was inside our 'clickable' objects
        gotValidClick = False
        try:
            iter(nextButton_R1B)
            clickableList = nextButton_R1B
        except:
            clickableList = [nextButton_R1B]
        for obj in clickableList:
            if obj.contains(mouse_4):
                gotValidClick = True
                mouse_4.clicked_name.append(obj.name)
    # the Routine "QuestionBreakPause" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
# completed 1.0 repeats of 'block1'

# playing part stopping trig
continueRoutine = True
routineTimer.add(1)
stopExpTrigger = SfPlayer('P3_end_trigger.wav')
for i in range(PART_3_OUT_CHANNELS):
    mm.delInput(i) #Ensure any previous inputs are cleared
mm.addInput(0, stopExpTrigger) #One input - the stop trigger
mm.setAmp(0,TRIGGER_CHN, spk_volume[TRIGGER_CHN])
thisExp.addData('Stop Trigger Start Time', globalClock.getTime())
while continueRoutine and routineTimer.getTime() > 0:
    mm.out()
mm.stop()
routineTimer.reset()
# end of playing part stop trig

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

s.stop()
s.shutdown()

#Save csv of data:
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()

# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()