# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 14:36:42 2023

@author: cjwin
"""

import numpy as np
from numpy.random import default_rng
rng = default_rng() 

allSets = np.arange(1, 13)

#EXCLUDING NEUTRAL ONES:
positiveValenceSets = np.array([1, 3, 5, 9, 10]) 
negativeValenceSets = np.array([2, 4, 6, 7, 8, 11])

activeArousalSets = np.array([1, 2, 6, 8, 10, 11])
passiveArousalSets = np.array([3, 4, 5, 7, 9, 12])

dominantDominanceSets = np.array([2, 4, 6, 8, 10, 11])
submissiveDominanceSets = np.array([3, 5, 7, 9])

sameEmotionCombos1 = np.array([3, 5, 9]) #+ve val, high, dom
sameEmotionCombos2 = np.array([2, 6, 8, 11]) #-ve val, low, sub

sameArtists1 = np.array([8, 9]) #Kyle and Sebastian
sameArtists2 = np.array([1, 2, 3, 4]) #Sebastian and George
sameArtists3 = np.array([5, 6, 7, 10, 11, 12]) #Daksh

validMegasets = False

def intersectionCounter(arr1, arr2):
    intersections = np.intersect1d(arr1, arr2)
    return len(intersections)

while validMegasets == False:
    megasets = rng.choice(allSets, size=11, replace=False)
    megasetA = megasets[0:5]
    megasetB = megasets[6:11]
    
    #Enough +ve/-ve pieces for each (Change to account for neutral ones?):
    if 3 >= intersectionCounter(positiveValenceSets, megasetA) >= 2 and 3 >= intersectionCounter(negativeValenceSets, megasetA) >= 2:
    
        if 3 >= intersectionCounter(positiveValenceSets, megasetB) >= 2 and 3 >= intersectionCounter(negativeValenceSets, megasetB) >= 2:
    
    #Enough active/passive pieces for each:
            if (3 >= intersectionCounter(activeArousalSets, megasetA) >= 2) and (3 >= intersectionCounter(passiveArousalSets, megasetA) >= 2):
            
                if 3 >= intersectionCounter(activeArousalSets, megasetB) >= 2 and 3 >= intersectionCounter(passiveArousalSets, megasetB) >= 2:
        
    #Enough dom/sub pieces for each (Change to account for neutral ones?):
                    if (3 >= intersectionCounter(dominantDominanceSets, megasetA) >= 2) and (3 >= intersectionCounter(submissiveDominanceSets, megasetA) >= 2):
                    
                        if 3 >= intersectionCounter(dominantDominanceSets, megasetB) >= 2 and 3 >= intersectionCounter(submissiveDominanceSets, megasetB) >= 2:                    
                       
    #To ensure as much "spread" as possible/reduce conflating emotions, try to forbid identical combinations:       
    #DOESN'T APPEAR TO BE POSSIBLE (OR AT LEAST, V HARD TO FIND ALLOWED COMBINATIONS)                          
                #            if intersectionCounter(sameEmotionCombos1, megasetA) <= 1 and intersectionCounter(sameEmotionCombos2, megasetA) <= 1:
                                
                 #               if intersectionCounter(sameEmotionCombos1, megasetB) <= 1 and intersectionCounter(sameEmotionCombos2, megasetB) <= 1:
                  #                  print(megasetA)
                   #                 print(megasetB)
                   #                 validMegasets = True
                    #            else:
                     #               print(intersectionCounter(sameEmotionCombos1, megasetA))
                      #              print(intersectionCounter(sameEmotionCombos1, megasetB))
                          if intersectionCounter(sameArtists1, megasetA) == 1 and intersectionCounter(sameArtists2, megasetA) >= 1 and intersectionCounter(sameArtists3, megasetA) >= 1:
                              if intersectionCounter(sameArtists1, megasetB) == 1 and intersectionCounter(sameArtists2, megasetB) >= 1 and intersectionCounter(sameArtists3, megasetB) >= 1:
                                    print(megasetA)
                                    print(megasetB)
                                    validMegasets = True