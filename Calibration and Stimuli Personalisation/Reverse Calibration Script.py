"To calibrate the loudness levels of certain pieces relative to others."

import pathlib
from psychopy import locale_setup
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, prefs
prefs.hardware['audioLatencyMode'] = '3'
#prefs.hardware['audioDevice'] = 'Speakers (DAC8PRO)'
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from pyo import *
import time
from pydub import AudioSegment
import numpy as np
import os
import wx
import psychopy.iohub as io
from psychopy.hardware import keyboard


expName = 'Loudness Calibration'
expInfo = {'Participant ID': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel

#Navigate into Data folder, and find the subfolder for the participant:
currentFolderPath = pathlib.Path(__file__).parent.resolve()
upperFolderPath = currentFolderPath.parent.resolve()
dataPath = str(upperFolderPath) + "/Data/"


groupAssignmentFile = dataPath + "Participant Groups.txt" #Needed for taking collecting stimuli, and saving to right place:
with open(groupAssignmentFile, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if "Group A1" in line and expInfo['Participant ID'] in line:
            participantPath = dataPath + "Group A1/" + expInfo['Participant ID']
            vibrPiece = "Calibration Stimuli (Downsampled in Advance)/Set01-Vibr.wav"
            harmPiece = "Calibration Stimuli (Downsampled in Advance)/Set01-Harm.wav"
            keybPiece = "Calibration Stimuli (Downsampled in Advance)/Set01-Keyb.wav"
        elif "Group A2" in line and expInfo['Participant ID'] in line:
            participantPath = dataPath + "Group A2/" + expInfo['Participant ID']
            vibrPiece = "Calibration Stimuli (Downsampled in Advance)/Set01-Vibr.wav"
            harmPiece = "Calibration Stimuli (Downsampled in Advance)/Set01-Harm.wav"
            keybPiece = "Calibration Stimuli (Downsampled in Advance)/Set01-Keyb.wav"
            
        elif "Group B1" in line and expInfo['Participant ID'] in line:
            participantPath = dataPath + "Group B1/" + expInfo['Participant ID']
            vibrPiece = "Calibration Stimuli (Downsampled in Advance)/Set04-Vibr.wav"
            harmPiece = "Calibration Stimuli (Downsampled in Advance)/Set04-Harm.wav"
            keybPiece = "Calibration Stimuli (Downsampled in Advance)/Set04-Keyb.wav"
        elif "Group B2" in line and expInfo['Participant ID'] in line:
            participantPath = dataPath + "Group B2/" + expInfo['Participant ID']
            vibrPiece = "Calibration Stimuli (Downsampled in Advance)/Set04-Vibr.wav"
            harmPiece = "Calibration Stimuli (Downsampled in Advance)/Set04-Harm.wav"
            keybPiece = "Calibration Stimuli (Downsampled in Advance)/Set04-Keyb.wav"
    f.close
    
harmPieceDEPENDENT = "Calibration Stimuli (Downsampled in Advance)/Set07-Harm.wav"
keybPieceDEPENDENT = "Calibration Stimuli (Downsampled in Advance)/Set07-Keyb.wav"
vibrPieceDEPENDENT = "Calibration Stimuli (Downsampled in Advance)/Set07-Vibr.wav"


##########################################################################################################################################
#PART 1 - SPATIAL BALANCING. Here we also initialise things such as video settings for later parts:
SOUNDCARD_DEVICE_NAME = 'DAC8PRO'

OUT_CHANNELS = 2

volume_level = 0.05

volume_ratio = [1, 1, 5]

spk_volume = [x * volume_level for x in volume_ratio]
 

s = Server(nchnls=OUT_CHANNELS, duplex=0)

devices = pa_get_output_devices()

for name in devices[0]:

    if SOUNDCARD_DEVICE_NAME in name:

        soundcard_idx = devices[1][devices[0].index(name)]

        print('sound card: ', name)

        s.setOutputDevice(soundcard_idx)

        break

s = s.boot()

# Load the audio files
vibraphone = AudioSegment.from_wav(vibrPiece)
harmonica = AudioSegment.from_wav(harmPiece)
piano = AudioSegment.from_wav(keybPiece)

# To control for acquiescence, we randomise the initial settings.
[vibrPan, harmPan, keybPan] = np.random.uniform(-1, 1, 3)

#Set up loudness parameter, apply gain:
vibraphone_loudness = 0.6
vibraphone = vibraphone.apply_gain(20*np.log10(vibraphone_loudness))

harmonica_loudness = 0.6
harmonica = harmonica.apply_gain(20*np.log10(harmonica_loudness))

piano_loudness = 0.6
piano = piano.apply_gain(20*np.log10(piano_loudness))

current_instrument = "Vibraphone"
currentPan = vibrPan
contAdjustingInstP1 = True

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1920, 1080], fullscr=False, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='AIM Laptop', color=[-0.4510, 0.0196, 0.4118], colorSpace='rgb',
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

######## Initialize components for P1/spatial balancing:

# Initialize components for Routine "instructions1"
instructions1Clock = core.Clock()
instr1_txt = visual.TextStim(win=win, name='instr1_txt',
    text=("People can have slightly different perceptions of where the \"centre\" is when they hear music. We are going to run a test to tweak the audio settings to your ears.\n\n"
            "A vibraphone will play from a RANDOM direction, and you will need to adjust the balance so that you hear it as coming from the centre- you can adjust"
          + " as many times as needed. We will then repeat the test twice with other instruments.\n\nWhen you are ready to hear the music for the first time, press \"NEXT\"."),
    font='Open Sans',
    pos=(0, 0.15), height=0.05, wrapWidth=1.8, ori=0.0, 
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

#Initialise components for routine "moveToVibrNote":
moveToVibrNoteClock = core.Clock()
moveToVibrNote_txt = visual.TextStim(win=win, name='moveToVibrNote_txt',
    text="We will now move on to the vibraphone.",
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=1.8, ori=0.0, 
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
    
#Initialise components for routine "moveToHarmNote":
moveToHarmNoteClock = core.Clock()
moveToHarmNote_txt = visual.TextStim(win=win, name='moveToHarmNote_txt',
    text="We will now move on to the harmonica.",
    font='Open Sans',
    pos=(0, 0.0), height=0.05, wrapWidth=1.8, ori=0.0, 
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
    
#Initialise components for routine "moveToKeybNote":
moveToKeybNoteClock = core.Clock()
moveToKeybNote_txt = visual.TextStim(win=win, name='moveToKeybNote_txt',
    text="We will now move on to the piano.",
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=1.8, ori=0.0, 
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
    
# Initialize components for Routine "settingsSavedNote"
#This will also be used in later steps of the calibration
settingsSavedNoteClock = core.Clock()
settingsSavedNote_txt = visual.TextStim(win=win, name='settingsSavedNote_txt',
    text="Your settings have been saved.",
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
    
# Initialize components for Routine "panningFeedbackPg"
panningFeedbackPgClock = core.Clock()
panningFeedbackPg_txt = visual.TextStim(win=win, name='panningFeedbackPg_txt',
    text='Please indicate how much you would like to change the angle that the music is coming from.',
    font='Open Sans',
    pos=(0, 0.34), height=0.05, wrapWidth=1.7, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, anchorVert='top',
    languageStyle='LTR',
    depth=-1.0);
panningChangeResp = visual.Slider(win=win, name='panningChangeResp',
    startValue=0, size=(1.1, 0.025), pos=(0.0, 0.0), units=None,
    labels=("90° left", "No change", "90° right"), ticks=(-90,-80,-70,-60,-50,-40,-30,-20,-10,0,10,20,30,40,50,60,70,80,90), granularity=0.0,
    style='rating', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Arial', labelHeight=0.03,
    flip=False, ori=0.0, depth=-7, readOnly=False)
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

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 


# ------Prepare to start Routine "instructions1"-------
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse_2
mouse_2.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
instructions1Components = [instr1_txt, mouse_2, nextButton_instruct]
for thisComponent in instructions1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
instructions1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "instructions1"-------
while continueRoutine:
    # get current time
    t = instructions1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=instructions1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instr1_txt* updates
    if instr1_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instr1_txt.frameNStart = frameN  # exact frame index
        instr1_txt.tStart = t  # local t and not account for scr refresh
        instr1_txt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instr1_txt, 'tStartRefresh')  # time at next scr refresh
        instr1_txt.setAutoDraw(True)
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
    for thisComponent in instructions1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    
# -------Ending Routine "instructions1"-------
for thisComponent in instructions1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instructions1" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#Run the test:

while True:
    if contAdjustingInstP1 == False and current_instrument == "Vibraphone":
        vibrPan = currentPan
        
        # ------Prepare to start Routine "moveToHarmNote"-------
        
        # update component parameters for each repeat
        # keep track of which components have finished
        continueRoutine = True
    
        moveToHarmNoteComponents = [moveToHarmNote_txt]
        for thisComponent in moveToHarmNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        moveToHarmNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "moveToHarmNote"-------
        while continueRoutine:
            # get current time
            t = moveToHarmNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=moveToHarmNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if moveToHarmNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                moveToHarmNote_txt.frameNStart = frameN  # exact frame index
                moveToHarmNote_txt.tStart = t  # local t and not account for scr refresh
                moveToHarmNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moveToHarmNote_txt, 'tStartRefresh')  # time at next scr refresh
                moveToHarmNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if moveToHarmNoteClock.getTime() > 4:
                moveToHarmNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in moveToHarmNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "moveToHarmNote"-------
        for thisComponent in moveToHarmNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
    
        current_instrument = "Harmonica"
        currentPan = harmPan
        contAdjustingInstP1 = True
    
    #If they said don't continue and the instrument was harm, move onto the piano:
    if contAdjustingInstP1 == False and current_instrument == "Harmonica":
        harmPan = currentPan
        # ------Prepare to start Routine "moveToKeybNote"-------
        
        # update component parameters for each repeat
        # keep track of which components have finished
        continueRoutine = True

        moveToKeybNoteComponents = [moveToKeybNote_txt]
        for thisComponent in moveToKeybNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        moveToKeybNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "moveToKeybNote"-------
        while continueRoutine:
            # get current time
            t = moveToKeybNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=moveToKeybNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if moveToKeybNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                moveToKeybNote_txt.frameNStart = frameN  # exact frame index
                moveToKeybNote_txt.tStart = t  # local t and not account for scr refresh
                moveToKeybNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moveToKeybNote_txt, 'tStartRefresh')  # time at next scr refresh
                moveToKeybNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if moveToKeybNoteClock.getTime() > 4:
                moveToKeybNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in moveToKeybNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "moveToKeybNote"-------
        for thisComponent in moveToKeybNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        current_instrument = "Piano"
        currentPan = keybPan
        contAdjustingInstP1 = True

    if contAdjustingInstP1 == False and current_instrument == "Piano":
        keybPan = currentPan
        #Save the results:        
        pannings = ["Vibraphone: ", vibrPan, " Harmonica: ", harmPan, " Piano: ", keybPan]        
        #Create a new file in the appropriate location. If there's already a file there of the same name, it's wiped:
        File = (participantPath + "\Spatialisation Settings.txt")
        #Open, write to file, and close.
        with open(File, 'w') as f:
            for x in pannings:
                f.write("%s" % x )
            f.close()
            
        # ------Prepare to start Routine "settingsSavedNote"-------
        # update component parameters for each repeat
        # keep track of which components have finished
        continueRoutine = True

        settingsSavedNoteComponents = [settingsSavedNote_txt]
        for thisComponent in settingsSavedNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        settingsSavedNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "settingsSavedNote"-------
        while continueRoutine:
            # get current time
            t = settingsSavedNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=settingsSavedNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if settingsSavedNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                settingsSavedNote_txt.frameNStart = frameN  # exact frame index
                settingsSavedNote_txt.tStart = t  # local t and not account for scr refresh
                settingsSavedNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(settingsSavedNote_txt, 'tStartRefresh')  # time at next scr refresh
                settingsSavedNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if settingsSavedNoteClock.getTime() > 4:
                settingsSavedNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in settingsSavedNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "settingsSavedNote"-------
        for thisComponent in settingsSavedNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        break
        
    #Playing the music (with a blank screen):
    win.flip(clearBuffer=True) #Clear screen
    if current_instrument == "Vibraphone":
        output = vibraphone.pan(currentPan)
    elif current_instrument == "Harmonica":
        output = harmonica.pan(currentPan)
    else:
        output = piano.pan(currentPan)
    output.export("Temp.wav", format="wav")
    
    #Create players for new mix:
    players = []
    for i in range(1, OUT_CHANNELS):
        if i < len(spk_volume):  # check if spk_volume has the correct number of elements
            player = sound.Sound("Temp.wav")
            player.setVolume(spk_volume[i])  # set the volume for the current speaker
        players.append(player)

    # Start the server
    s.start()
    for player in players:
        player.play()
        # Wait until 10 seconds pass
        core.wait(10)
        player.stop()
    
    # Stop the server
    s.stop()
    
# ------Prepare to start Routine "panningFeedbackPg"-------
    continueRoutine = True
# update component parameters for each repeat
    panningChangeResp.reset()
# setup some python lists for storing info about the mouse2_2
    mouse2_2.clicked_name = []
    gotValidClick = False  # until a click is received
# keep track of which components have finished
    panningFeedbackPgComponents = [panningFeedbackPg_txt, panningChangeResp, nextButton2_2, mouse2_2]
    for thisComponent in panningFeedbackPgComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    panningFeedbackPgClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

# -------Run Routine "panningFeedbackPg"-------
    while continueRoutine:
    # get current time
        t = panningFeedbackPgClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=panningFeedbackPgClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
    
    # *panningFeedbackPg_txt* updates
        if panningFeedbackPg_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            panningFeedbackPg_txt.frameNStart = frameN  # exact frame index
            panningFeedbackPg_txt.tStart = t  # local t and not account for scr refresh
            panningFeedbackPg_txt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(panningFeedbackPg_txt, 'tStartRefresh')  # time at next scr refresh
            panningFeedbackPg_txt.setAutoDraw(True)
    
        # *panningChangeResp* updates
        if panningChangeResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            panningChangeResp.frameNStart = frameN  # exact frame index
            panningChangeResp.tStart = t  # local t and not account for scr refresh
            panningChangeResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(panningChangeResp, 'tStartRefresh')  # time at next scr refresh
            panningChangeResp.setAutoDraw(True)
        
        # *mouse2_2* updates
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
                    if nextButton2_2.status == STARTED:
                        try:
                            iter(nextButton2_2)
                            clickableList = nextButton2_2
                        except:
                            clickableList = [nextButton2_2]
                        for obj in clickableList:
                            if obj.contains(mouse2_2):
                                gotValidClick = True
                                mouse2_2.clicked_name.append(obj.name)
                        if gotValidClick:  
                            continueRoutine = False  # abort routine on response
    
        # *nextButton* updates
        if nextButton2_2.status == NOT_STARTED:
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
        for thisComponent in panningFeedbackPgComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "panningFeedbackPg"-------
    for thisComponent in panningFeedbackPgComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "panningFeedbackPg" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
        
    if panningChangeResp.getRating() != None:
        changeDegrees = float(panningChangeResp.getRating())
        currentPan += changeDegrees*(1/90)
        contAdjustingInstP1 = True
    else:
        contAdjustingInstP1 = False
        
    #If we get numbers out of the range (-1, 1), we loop back around from the other side:
    if currentPan < -1:
        diff = - 1 - currentPan
        currentPan = 1 - diff
    elif currentPan > 1:
        diff = currentPan - 1
        currentPan = 1 - diff
    
# Stop the server
s.stop()

########################################################################################################################################################################
#PART 3 - SINGLE-STREAM GAINS

continue_adjusting = True
 
s = s.boot()

#Set default gains. To avoid confusion, these are not necessarily the same as the values which are actually used to control loudness.
#E.g, piano_loudness might be 1, but piano output will be 0 whilst the vibraphone plays.
vibraphone_loudness = 0.5
harmonica_loudness = 0.5
piano_loudness = 0.5

vibraphoneDEPENDENT_loudness = 0.5
harmonicaDEPENDENT_loudness = 0.5
pianoDEPENDENT_loudness = 0.5

# Reload the audio files
vibraphone = AudioSegment.from_wav(vibrPiece)
harmonica = AudioSegment.from_wav(harmPiece)
piano = AudioSegment.from_wav(keybPiece)
vibraphone.pan(vibrPan)
harmonica.pan(harmPan)
piano.pan(keybPan)

vibraphoneDEPENDENT = AudioSegment.from_wav(vibrPieceDEPENDENT)
harmonicaDEPENDENT = AudioSegment.from_wav(harmPieceDEPENDENT)
pianoDEPENDENT = AudioSegment.from_wav(keybPieceDEPENDENT)

vibraphoneDEPENDENT.pan(vibrPan)
harmonicaDEPENDENT.pan(harmPan)
pianoDEPENDENT.pan(keybPan)

current_instrument = "Vibraphone"
currentInstLoudness = vibraphone_loudness
contAdjustingInstP3 = True

# Initialize components for Routine "instructions3"
instructions3Clock = core.Clock()
instr3_txt = visual.TextStim(win=win, name='instr3_txt',
    text=("The final part of the calibration test is to ensure that you can hear and follow the different instruments comfortably when they are playing individually.\n\n"
    + "You will hear the vibraphone playing from the centre, and you will need to adjust the loudness settings until you can hear and focus on it comfortably. This will then be"
    + " repeated with the other instruments.\n\nWhen you are ready to hear the music for the first time, press \"NEXT\"."),
    font='Open Sans',
    pos=(0, 0.15), height=0.05, wrapWidth=1.8, ori=0.0, 
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

#Initialize components for routine "ssVolFeedbackPg":
ssVolFeedbackPgClock = core.Clock()
ssVolFeedbackPg_txt = visual.TextStim(win=win, name='ssVolFeedbackPg_txt',
    text="Please adjust the loudness, so that you can hear and attend to the current instrument comfortably.",
    font='Open Sans',
    pos=(0, 0.315), height=0.05, wrapWidth=1.8, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None,
    languageStyle='LTR',
    depth=0.0); 
ssVolFeedbackResp = visual.TextBox2(
     win, text=currentInstLoudness, font='Open Sans',
     pos=(0, -0.1),     letterHeight=0.025,
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
     name='ssVolFeedbackResp',
     autoLog=True,
)
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

# Initialize components for Routine "contAdjustingQ2"
contAdjustingQ2Clock = core.Clock()
mouse_4 = event.Mouse(win=win)
x, y = [None, None]
mouse_4.mouseClock = core.Clock()
contAdjustingQ2Resp = visual.Slider(win=win, name='contAdjustingQ2Resp',
    startValue=None, size=(0.3, 0.025), pos=(0.0, -0.1), units=None,
    labels=("Yes", "No"), ticks=(0, 1), granularity=1.0,
    style='radio', styleTweaks=(), opacity=None,
    labelColor='LightGray', markerColor='Red', lineColor='White', colorSpace='rgb',
    font='Open Sans', labelHeight=0.025,
    flip=True, ori=0.0, depth=-2, readOnly=False)

#for contAdjustingQ3, we reuse the components from contAdjustingQ2, but slightly change the text:
contAdjustingQ3Txt = visual.TextStim(win=win, name='contAdjustingQ3Txt',
    text="Would you like to continue adjusting the loudness of the current instrument?",
    font='Open Sans',
    pos=(0, 0.15), height=0.05, wrapWidth=1.8, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# ------Prepare to start Routine "instructions3"-------
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse_2
mouse_2.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
instructions3Components = [instr3_txt, mouse_2, nextButton_instruct]
for thisComponent in instructions3Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
instructions3Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "instructions3"-------
while continueRoutine:
    # get current time
    t = instructions3Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=instructions3Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instr3_txt* updates
    if instr3_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        instr3_txt.frameNStart = frameN  # exact frame index
        instr3_txt.tStart = t  # local t and not account for scr refresh
        instr3_txt.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(instr3_txt, 'tStartRefresh')  # time at next scr refresh
        instr3_txt.setAutoDraw(True)
     
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
    for thisComponent in instructions3Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions3"-------
for thisComponent in instructions3Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instructions3" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

firstLoopThisInst = True
while True:
    #Play the music, with a blank screen:
    win.flip(clearBuffer=True) #Clear screen
    if current_instrument == "Vibraphone":
        output = vibraphone.apply_gain(20*np.log10(vibraphone_loudness)) #Apply gain- CONVERT TO DB!
        
    elif current_instrument == "Harmonica":
        output = harmonica.apply_gain(20*np.log10(harmonica_loudness))
    
    elif current_instrument == "Piano":
        output = piano.apply_gain(20*np.log10(piano_loudness))
    
    elif current_instrument == "VibraphoneDEPENDENT":
        output = vibraphoneDEPENDENT.apply_gain(20*np.log10(vibraphoneDEPENDENT_loudness))
    
    elif current_instrument == "HarmonicaDEPENDENT":
        output = harmonicaDEPENDENT.apply_gain(20*np.log10(harmonicaDEPENDENT_loudness))
        
    else:
        output = pianoDEPENDENT.apply_gain(20*np.log10(pianoDEPENDENT_loudness))
    
    output.export("Temp.wav", format="wav")    
    
    #Create players for new mix:
    players = []
    for i in range(1, OUT_CHANNELS):
        if i < len(spk_volume):  # check if spk_volume has the correct number of elements
            player = sound.Sound("Temp.wav")
            player.setVolume(spk_volume[i])  # set the volume for the current speaker
        players.append(player)

    # Start the server
    s.start()
    for player in players:
        player.play()
        # Wait until 10 seconds pass
        core.wait(10)
        player.stop()
    
#Stop the server
    s.stop()    
    
    if firstLoopThisInst == False: #The first time, the participants are encouraged to adjust
        # ------Prepare to start Routine "contAdjustingQ3"-------
        continueRoutine = True
        contAdjustingQ2Resp.reset()
        # update component parameters for each repeat
        # setup some python lists for storing info about the mouse_4
        mouse_4.clicked_name = []
        gotValidClick = False  # until a click is received
        # keep track of which components have finished
        contAdjustingQ2Components = [contAdjustingQ3Txt, mouse_4, contAdjustingQ2Resp]
        for thisComponent in contAdjustingQ2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        contAdjustingQ2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "contAdjustingQ3"-------
        while continueRoutine:
            # get current time
            t = contAdjustingQ2Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=contAdjustingQ2Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if contAdjustingQ3Txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                contAdjustingQ3Txt.frameNStart = frameN  # exact frame index
                contAdjustingQ3Txt.tStart = t  # local t and not account for scr refresh
                contAdjustingQ3Txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(contAdjustingQ3Txt, 'tStartRefresh')  # time at next scr refresh
                contAdjustingQ3Txt.setAutoDraw(True)     
                
            if contAdjustingQ2Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                contAdjustingQ2Resp.frameNStart = frameN  # exact frame index
                contAdjustingQ2Resp.tStart = t  # local t and not account for scr refresh
                contAdjustingQ2Resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(contAdjustingQ2Resp, 'tStartRefresh')  # time at next scr refresh
                contAdjustingQ2Resp.setAutoDraw(True)
                            
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
            if contAdjustingQ2Resp.getRating() == 0:
                contAdjustingInstP3 = True
                continueRoutine = False  # abort routine on response
            if contAdjustingQ2Resp.getRating() == 1:
                contAdjustingInstP3 = False
                continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in contAdjustingQ2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
        
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "contAdjustingQ2"-------
        for thisComponent in contAdjustingQ2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
    firstLoopThisInst = False
    
    if contAdjustingInstP3 == False and current_instrument == "Vibraphone":
    
        # ------Prepare to start Routine "moveToHarmNote"-------
        
        ssVolFeedbackResp.reset()
        
        # update component parameters for each repeat
        # keep track of which components have finished
        continueRoutine = True
    
        moveToHarmNoteComponents = [moveToHarmNote_txt]
        for thisComponent in moveToHarmNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        moveToHarmNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "moveToHarmNote"-------
        while continueRoutine:
            # get current time
            t = moveToHarmNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=moveToHarmNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if moveToHarmNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                moveToHarmNote_txt.frameNStart = frameN  # exact frame index
                moveToHarmNote_txt.tStart = t  # local t and not account for scr refresh
                moveToHarmNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moveToHarmNote_txt, 'tStartRefresh')  # time at next scr refresh
                moveToHarmNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if moveToHarmNoteClock.getTime() > 4:
                moveToHarmNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in moveToHarmNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "moveToHarmNote"-------
        for thisComponent in moveToHarmNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
    
        current_instrument = "Harmonica"
        currentInstLoudness = harmonica_loudness
        firstLoopThisInst = True
        contAdjustingInstP3 = True
    
    #If they said don't continue and the instrument was harm, move onto the piano:
    if contAdjustingInstP3 == False and current_instrument == "Harmonica":
        
        ssVolFeedbackResp.reset()
        
        # ------Prepare to start Routine "moveToKeybNote"-------
        # keep track of which components have finished
        continueRoutine = True

        moveToKeybNoteComponents = [moveToKeybNote_txt]
        for thisComponent in moveToKeybNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        moveToKeybNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "moveToKeybNote"-------
        while continueRoutine:
            # get current time
            t = moveToKeybNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=moveToKeybNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if moveToKeybNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                moveToKeybNote_txt.frameNStart = frameN  # exact frame index
                moveToKeybNote_txt.tStart = t  # local t and not account for scr refresh
                moveToKeybNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moveToKeybNote_txt, 'tStartRefresh')  # time at next scr refresh
                moveToKeybNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if moveToKeybNoteClock.getTime() > 4:
                moveToKeybNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in moveToKeybNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "moveToKeybNote"-------
        for thisComponent in moveToKeybNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        current_instrument = "Piano"
        currentInstLoudness = piano_loudness
        firstLoopThisInst = True
        contAdjustingInstP3 = True
        
        #If they said don't continue and the instrument was keyb, move onto VibraphoneDEPENDENT:
    if contAdjustingInstP3 == False and current_instrument == "Piano":
        
        ssVolFeedbackResp.reset()
        
        # ------Prepare to start Routine "moveToVibrNote"-------
        # update component parameters for each repeat
        # keep track of which components have finished
        continueRoutine = True

        moveToVibrNoteComponents = [moveToVibrNote_txt]
        for thisComponent in moveToVibrNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        moveToKeybNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "moveToVibrNote"-------
        while continueRoutine:
            # get current time
            t = moveToKeybNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=moveToKeybNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if moveToVibrNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                moveToVibrNote_txt.frameNStart = frameN  # exact frame index
                moveToVibrNote_txt.tStart = t  # local t and not account for scr refresh
                moveToVibrNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moveToVibrNote_txt, 'tStartRefresh')  # time at next scr refresh
                moveToVibrNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if moveToVibrNoteClock.getTime() > 4:
                moveToVibrNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in moveToVibrNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "moveToVibrNote"-------
        for thisComponent in moveToVibrNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        current_instrument = "VibraphoneDEPENDENT"
        currentInstLoudness = vibraphoneDEPENDENT_loudness
        firstLoopThisInst = True
        contAdjustingInstP3 = True

    if contAdjustingInstP3 == False and current_instrument == "VibraphoneDEPENDENT":
        
        ssVolFeedbackResp.reset()
        
        # ------Prepare to start Routine "moveToHarmNote"-------
        # update component parameters for each repeat
        # keep track of which components have finished
        continueRoutine = True
    
        moveToHarmNoteComponents = [moveToHarmNote_txt]
        for thisComponent in moveToHarmNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        moveToHarmNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "moveToHarmNote"-------
        while continueRoutine:
            # get current time
            t = moveToHarmNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=moveToHarmNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if moveToHarmNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                moveToHarmNote_txt.frameNStart = frameN  # exact frame index
                moveToHarmNote_txt.tStart = t  # local t and not account for scr refresh
                moveToHarmNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moveToHarmNote_txt, 'tStartRefresh')  # time at next scr refresh
                moveToHarmNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if moveToHarmNoteClock.getTime() > 4:
                moveToHarmNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in moveToHarmNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "moveToHarmNote"-------
        for thisComponent in moveToHarmNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
    
        current_instrument = "HarmonicaDEPENDENT"
        currentInstLoudness = harmonicaDEPENDENT_loudness
        firstLoopThisInst = True
        contAdjustingInstP3 = True
    
    #If they said don't continue and the instrument was harmDEPENDENT, move on to pianoDEPENDENT:
    if contAdjustingInstP3 == False and current_instrument == "HarmonicaDEPENDENT":
        
        ssVolFeedbackResp.reset()
        
        # ------Prepare to start Routine "moveToKeybNote"-------
        # keep track of which components have finished
        continueRoutine = True

        moveToKeybNoteComponents = [moveToKeybNote_txt]
        for thisComponent in moveToKeybNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        moveToKeybNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "moveToKeybNote"-------
        while continueRoutine:
            # get current time
            t = moveToKeybNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=moveToKeybNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if moveToKeybNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                moveToKeybNote_txt.frameNStart = frameN  # exact frame index
                moveToKeybNote_txt.tStart = t  # local t and not account for scr refresh
                moveToKeybNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(moveToKeybNote_txt, 'tStartRefresh')  # time at next scr refresh
                moveToKeybNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if moveToKeybNoteClock.getTime() > 4:
                moveToKeybNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in moveToKeybNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "moveToKeybNote"-------
        for thisComponent in moveToKeybNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)

        current_instrument = "PianoDEPENDENT"
        currentInstLoudness = pianoDEPENDENT_loudness
        firstLoopThisInst = True
        contAdjustingInstP3 = True       

    if contAdjustingInstP3 == False and current_instrument == "PianoDEPENDENT":
        
        #Save the results:        
        gains = ["Vibraphone: ", vibraphone_loudness, " Harmonica: ", harmonica_loudness, " Piano: ", piano_loudness, 
        " Vibraphone Set-07: ", vibraphoneDEPENDENT_loudness, " Harmonica Set-07: ", harmonicaDEPENDENT_loudness, " Piano Set-07: ", pianoDEPENDENT_loudness]        
        #Create a new file in the appropriate location. If there's already a file there of the same name, it's wiped:
        File = (participantPath + "\Single-stream Gains CALIBRATING PARTICULAR PIECES.txt")
        #Open, write to file, and close.
        with open(File, 'w') as f:
            for x in gains:
                f.write("%s" % x )
            f.close
            
        # ------Prepare to start Routine "settingsSavedNote"-------
        # update component parameters for each repeat
        # keep track of which components have finished
        continueRoutine = True

        settingsSavedNoteComponents = [settingsSavedNote_txt]
        for thisComponent in settingsSavedNoteComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        settingsSavedNoteClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
        # -------Run Routine "settingsSavedNote"-------
        while continueRoutine:
            # get current time
            t = settingsSavedNoteClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=settingsSavedNoteClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
    
            if settingsSavedNote_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                settingsSavedNote_txt.frameNStart = frameN  # exact frame index
                settingsSavedNote_txt.tStart = t  # local t and not account for scr refresh
                settingsSavedNote_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(settingsSavedNote_txt, 'tStartRefresh')  # time at next scr refresh
                settingsSavedNote_txt.setAutoDraw(True) 
        
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
    
            if settingsSavedNoteClock.getTime() > 4:
                settingsSavedNote_txt.status = FINISHED
        
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in settingsSavedNoteComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
    
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "settingsSavedNote"-------
        for thisComponent in settingsSavedNoteComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        break
    
    if firstLoopThisInst == False:
    # ------Prepare to start Routine "ssVolFeedbackPg"-------
        continueRoutine = True
    # setup some python lists for storing info about the mouse2_2
        mouse2_2.clicked_name = []
        gotValidClick = False  # until a click is received
    # keep track of which components have finished
        ssVolFeedbackPgComponents = [ssVolFeedbackPg_txt, ssVolFeedbackResp, nextButton2_2, mouse2_2]
        for thisComponent in ssVolFeedbackPgComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        panningFeedbackPgClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
    
    # -------Run Routine "ssVolFeedbackPg"-------
        while continueRoutine:
        # get current time
            t = ssVolFeedbackPgClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=ssVolFeedbackPgClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
        
        # *ssVolFeedbackPg_txt* updates
            if ssVolFeedbackPg_txt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                ssVolFeedbackPg_txt.frameNStart = frameN  # exact frame index
                ssVolFeedbackPg_txt.tStart = t  # local t and not account for scr refresh
                ssVolFeedbackPg_txt.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(ssVolFeedbackPg_txt, 'tStartRefresh')  # time at next scr refresh
                ssVolFeedbackPg_txt.setAutoDraw(True)
        
            # *ssVolFeedbackResp* updates
            if ssVolFeedbackResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                ssVolFeedbackResp.frameNStart = frameN  # exact frame index
                ssVolFeedbackResp.tStart = t  # local t and not account for scr refresh
                ssVolFeedbackResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(ssVolFeedbackResp, 'tStartRefresh')  # time at next scr refresh
                ssVolFeedbackResp.setAutoDraw(True)
            
            # *mouse2_2* updates
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
                        if nextButton2_2.status == STARTED:
                            try:
                                iter(nextButton2_2)
                                clickableList = nextButton2_2
                            except:
                                clickableList = [nextButton2_2]
                            for obj in clickableList:
                                if obj.contains(mouse2_2):
                                    gotValidClick = True
                                    mouse2_2.clicked_name.append(obj.name)
                            if gotValidClick:  
                                continueRoutine = False  # abort routine on response
        
            # *nextButton* updates
            if nextButton2_2.status == NOT_STARTED:
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
            for thisComponent in ssVolFeedbackPgComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
    
        # -------Ending Routine "ssVolFeedbackPg"-------
        for thisComponent in ssVolFeedbackPgComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # the Routine "ssVolFeedbackPg" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
            
        currentInstLoudness = float(ssVolFeedbackResp.text)
        
        if current_instrument == "Vibraphone":
            vibraphone_loudness = currentInstLoudness
        elif current_instrument == "Harmonica":
            harmonica_loudness = currentInstLoudness
        elif current_instrument == "Piano":
            piano_loudness = currentInstLoudness
        elif current_instrument == "VibraphoneDEPENDENT":
            vibraphoneDEPENDENT_loudness = currentInstLoudness
        elif current_instrument == "HarmonicaDEPENDENT":
            harmonicaDEPENDENT_loudness = currentInstLoudness
        elif current_instrument == "PianoDEPENDENT":
            pianoDEPENDENT_loudness = currentInstLoudness    
            
########################################################################################################################################################################
#Tell the participant when finished:

# Initialize components for Routine "thisPartComplete"
thisPartCompleteClock = core.Clock()
thisPartCompleteText = visual.TextStim(win=win, name='thisPartCompleteText',
    text='Calibration complete.',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

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

# Flip one final time so any remaining win.callOnFlip() and win.timeOnFlip() tasks get executed before quitting
win.flip()

s.stop()
s.shutdown()

os.remove("Temp.wav") #Not strictly needed, keeps things terse.

##########################################################################################################################################

win.close()
core.quit()