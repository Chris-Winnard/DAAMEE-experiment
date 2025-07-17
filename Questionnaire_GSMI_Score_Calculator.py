import pathlib
import glob
import os
import pandas as pd
import numpy as np

def calcAndWrite(questionnaireFile):
    df = pd.read_csv(questionnaireFile)

    def negativeValue(response): #When the answer is a negative. E.g, a rating of 7 for "I find music unemotional" would be converted to 1 for emotion score
        return 8 - response
    
    #######################################################################################################################################################
    #Calculate perception score:
    perceptionResponses = np.zeros(9)
    for x in range(10, 19):        
        perceptionResponses[x-10] = df.iloc[0, x]
        
    #Account for negative values:
    perceptionResponses[2] = negativeValue(perceptionResponses[2])
    perceptionResponses[4] = negativeValue(perceptionResponses[4])
    perceptionResponses[7] = negativeValue(perceptionResponses[7])
    
    perceptionScore = sum(perceptionResponses)
    
    ###########################################################################################################################################################
    #Calculate emotion score:
    emotionResponses = np.zeros(6)
    for x in range(19, 25):        
        emotionResponses[x-19] = df.iloc[0, x]
    #Account for negative values:
    emotionResponses[1] = negativeValue(emotionResponses[1])
    
    emotionScore = sum(emotionResponses)
    
    df.insert(25, "Perception score", perceptionScore)
    df.insert(26, "Emotion score", emotionScore)
    df.to_csv(questionnaireFile)