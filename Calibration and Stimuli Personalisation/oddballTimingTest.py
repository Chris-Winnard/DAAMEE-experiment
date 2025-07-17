"Code to read through oddball start times list and check they are not too close."

import pathlib
import glob
import os
import soundfile as sf
import numpy as np
import math
from pydub import AudioSegment
import re
import xlsxwriter
from utils.SerialTriggerEncoder import SerialTriggerEncoder


#Find participant full path just from their ID
participantID = "P03"

idealOB_segmentLength = 1808*0.1/2205
idealOB_length = 6*idealOB_segmentLength
StrictTolerance = idealOB_length
LaxTolerance= 1+StrictTolerance

#Find the stimuli path:
currentFolderPath = pathlib.Path(__file__).parent.resolve()
upperFolderPath = currentFolderPath.parent.resolve()

#Create output path:
dataPath = str(upperFolderPath) + "/Data/"
TriggerConfigFile = str(upperFolderPath) + "Trigger Generation (Not Inc P2 Trial Trigs)\Trigger Config.xlsx"

groupAssignmentFile = dataPath + "/Participant Groups.txt" #Needed for taking collecting stimuli, and saving to right place:
with open(groupAssignmentFile, 'r') as f:
    lines = f.readlines()
    for line in lines:
        if "Group A1" in line and participantID in line:
            participantPath = str(upperFolderPath) + "/Data/Group A1/" + participantID + "/"
        elif "Group A2" in line and participantID in line:
            participantPath = str(upperFolderPath) + "/Data/Group A2/" + participantID + "/"
            
        elif "Group B1" in line and participantID in line:
            participantPath = str(upperFolderPath) + "/Data/Group B1/" + participantID + "/"
        elif "Group B2" in line and participantID in line:
            participantPath = str(upperFolderPath) + "/Data/Group B2/" + participantID + "/"
    f.close

##########################################################################################################################    
#Let's read and convert the start time data
startTimesFile = participantPath + "\Oddball Start Times.txt"
startTimesData = open(startTimesFile, 'r')
lines = startTimesData.readlines()
startTimesData.close()

def checkTrigTimes(participantPath):
        
    #################################################################################################################################################

    def oddballTrigs(filename):
        
        attendedInst = filename[-17:-13]
        
        thisMixVibr = filename[0:6] + "Vibr Oddball Test-" + filename[-17:] #E.g, Set01-Oddball Test Mix-Harm Attended.wav -> Set01-Vibr Oddball Test-Harm Attended.wav
        thisMixHarm = filename[0:6] + "Harm Oddball Test-" + filename[-17:] #E.g, Set01-Oddball Test Mix-Harm Attended.wav -> Set01-Harm Oddball Test-Harm Attended.wav
        thisMixKeyb = filename[0:6] + "Keyb Oddball Test-" + filename[-17:] 
        
        linesReadFrom = 0        
        for line in lines:
            if thisMixVibr in line:
                vibrOddballStartTimes = re.findall("\d+\.\d+", line) 
                linesReadFrom += 1
            elif thisMixHarm in line:
                harmOddballStartTimes = re.findall("\d+\.\d+", line)
                linesReadFrom += 1
            elif thisMixKeyb in line:
                keybOddballStartTimes = re.findall("\d+\.\d+", line)
                linesReadFrom += 1
            
            if linesReadFrom == 3:
                break
        
        allOBTimes = vibrOddballStartTimes + harmOddballStartTimes + keybOddballStartTimes
        
        return allOBTimes
        
    ########################################################################################################################################################
    minorProblems = 0
    majorProblems = 0
    oddballOverlaps_FirstTime = []
    
    for file in os.scandir(participantPath):
     if "Oddball Test Mix" in file.name:
        name = file.name
        oddballTimes = oddballTrigs(name)
        for i in range(len(oddballTimes)):
            for j in range(i, len(oddballTimes)):
                if i != j:
                    time1 = float(oddballTimes[i])
                    time2 = float(oddballTimes[j])
                    testBool_LAX = math.isclose(time1, time2,abs_tol = LaxTolerance)
                    testBool_STRICT = math.isclose(time1, time2,abs_tol = StrictTolerance)
                    
                    if testBool_LAX == True and testBool_STRICT == False:
                        print("Warning - found two oddballs within one second plus an oddball length of each other. They are NOT likely to be"
                              + " directly overlapping.")
         
                        print("These are in file: " + name)
                        print("\n")
                        minorProblems += 1
                        
                    if testBool_STRICT == True:
                        print("Warning - found two oddballs LIKELY TO BE DIRECTLY OVERLAPPING.")
                        print("These are in file: " + name)
                        print("\n")
                        majorProblems += 1
                        
                        fileAndFirstOddball = [file.name, time1]
                        oddballOverlaps_FirstTime.append(fileAndFirstOddball)
            
    return minorProblems, majorProblems, oddballOverlaps_FirstTime

#################################################################################################################################################

minorProblems, majorProblems, oddballOverlaps_FirstTime = checkTrigTimes(participantPath)
print(minorProblems)
print(majorProblems)

#Now run a very similar test, but just to check if triggers specifically likely to be overlapping:
    
#To deal with practice trials, need to specify the number and the stimuli used. If not run expt yet, leave this blank
practiceTrialStimuliPlayed = ["Set04-Oddball Test Mix-Harm Attended.wav", "Set04-Oddball Test Mix-Vibr Attended.wav"]

practiceTrialStimuliAll = ["Set01-Oddball Test Mix-Keyb Attended.wav", "Set01-Oddball Test Mix-Harm Attended.wav", "Set01-Oddball Test Mix-Vibr Attended.wav", "Set04-Oddball Test Mix-Keyb Attended.wav", "Set04-Oddball Test Mix-Harm Attended.wav", "Set04-Oddball Test Mix-Vibr Attended.wav"]

practiceTrialStimuliNotPlayed = filtered_list = list(set(practiceTrialStimuliAll).difference(practiceTrialStimuliPlayed))



def checkTrigTimes_Specific(participantPath):
    trig_clk = 16.0 #Hz.
    secsPerTrig = 8/16.0 #8 bits per trig
    
    #################################################################################################################################################

    def oddballTrigs_Specific(filename):

        attendedInst = filename[-17:-13]
        
        thisMixVibr = filename[0:6] + "Vibr Oddball Test-" + filename[-17:] #E.g, Set01-Oddball Test Mix-Harm Attended.wav -> Set01-Vibr Oddball Test-Harm Attended.wav
        thisMixHarm = filename[0:6] + "Harm Oddball Test-" + filename[-17:] #E.g, Set01-Oddball Test Mix-Harm Attended.wav -> Set01-Harm Oddball Test-Harm Attended.wav
        thisMixKeyb = filename[0:6] + "Keyb Oddball Test-" + filename[-17:] 
        
        linesReadFrom = 0        
        for line in lines:
            if thisMixVibr in line:
                vibrOddballStartTimes = re.findall("\d+\.\d+", line) 
                linesReadFrom += 1
            elif thisMixHarm in line:
                harmOddballStartTimes = re.findall("\d+\.\d+", line)
                linesReadFrom += 1
            elif thisMixKeyb in line:
                keybOddballStartTimes = re.findall("\d+\.\d+", line)
                linesReadFrom += 1
            
            if linesReadFrom == 3:
                break
        
        allOBTimes = vibrOddballStartTimes + harmOddballStartTimes + keybOddballStartTimes
        
        return allOBTimes
        
    ########################################################################################################################################################
    expectedTrigOverlaps = 0
    oddballOverlaps_FirstTime = []
    
    for file in os.scandir(participantPath):
     if "Oddball Test Mix" in file.name and file.name not in practiceTrialStimuliNotPlayed:
        name = file.name
        oddballTimes = oddballTrigs_Specific(name)
        for i in range(len(oddballTimes)):
            for j in range(i, len(oddballTimes)):
                if i != j:
                    time1 = float(oddballTimes[i])
                    time2 = float(oddballTimes[j])
                    testBool = math.isclose(time1, time2,abs_tol = secsPerTrig)
                    
                    if testBool == True:
                        print("Warning - found a trigger overlap.")
         
                        print("These are in file: " + name)
                        print("\n")
                        expectedTrigOverlaps += 1
                        
                        fileAndFirstOddball = [file.name, time1, time2]
                        oddballOverlaps_FirstTime.append(fileAndFirstOddball)
            
    return expectedTrigOverlaps, oddballOverlaps_FirstTime

expectedTrigOverlaps, oddballOverlaps_FirstTime = checkTrigTimes_Specific(participantPath)

print(oddballOverlaps_FirstTime)
print(expectedTrigOverlaps)