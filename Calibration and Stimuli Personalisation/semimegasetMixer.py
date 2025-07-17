import numpy as np
import pathlib
from numpy.random import default_rng
rng = default_rng() 
import os


#EXCLUDING NEUTRAL ONES:
positiveValenceSets = np.array(["01-Harm", "01-Keyb", "01-Vibr", "03-Harm","03-Keyb","03-Vibr", "05-Harm","05-Keyb","05-Vibr","09-Harm","09-Keyb","09-Vibr","10-Harm", "10-Vibr", "10-Keyb"]) 
negativeValenceSets = np.array(["02-Harm", "02-Keyb", "02-Vibr", "04-Harm", "04-Keyb", "04-Vibr", "06-Harm", "06-Keyb", "06-Vibr", "07-Harm", "07-Keyb", "07-Vibr", "08-Harm", "08-Keyb", "08-Vibr","11-Harm", "11-Keyb", "11-Vibr"])

activeArousalSets = np.array(["01-Harm", "01-Keyb", "01-Vibr", "02-Harm", "02-Keyb", "02-Vibr", "06-Harm", "06-Keyb", "06-Vibr", "08-Harm","08-Keyb","08-Vibr", "10-Harm","10-Keyb","10-Vibr", "11-Harm","11-Keyb","11-Vibr"])
passiveArousalSets = np.array(["03-Harm","03-Keyb","03-Vibr", "04-Harm", "04-Keyb", "04-Vibr", "05-Harm","05-Keyb","05-Vibr", "07-Harm", "07-Keyb", "07-Vibr", "09-Harm","09-Keyb","09-Vibr", "12-Harm","12-Keyb","12-Vibr"])

dominantDominanceSets = np.array(["03-Harm","03-Keyb","03-Vibr", "05-Harm","05-Keyb","05-Vibr", "07-Harm", "07-Keyb", "07-Vibr", "09-Harm","09-Keyb","09-Vibr"])
submissiveDominanceSets = np.array(["02-Harm", "02-Keyb", "02-Vibr", "04-Harm", "04-Keyb", "04-Vibr", "06-Harm", "06-Keyb", "06-Vibr", "08-Harm","08-Keyb","08-Vibr", "10-Harm",
                                    "10-Keyb", "10-Vibr", "11-Harm","11-Keyb", "11-Vibr","12-Harm","12-Keyb","12-Vibr"])

sameEmotionCombos1 = np.array(["03-Harm","03-Keyb","03-Vibr", "05-Harm","05-Keyb","05-Vibr", "09-Harm","09-Keyb","09-Vibr"]) #+ve val, high, dom
sameEmotionCombos2 = np.array(["02-Harm", "02-Keyb", "02-Vibr", "06-Harm", "06-Keyb", "06-Vibr", "08-Harm","08-Keyb","08-Vibr", "11-Harm","11-Keyb","11-Vibr"]) #-ve val, low, sub

sameArtists1 = np.array(["08-Harm","08-Keyb","08-Vibr", "09-Harm","09-Keyb","09-Vibr"]) #Kyle and Sebastian
sameArtists2 = np.array(["01-Harm", "02-Harm", "03-Harm","04-Harm"]) # George
sameArtists3 = np.array(["05-Harm","05-Keyb","05-Vibr", "06-Harm", "06-Keyb", "06-Vibr", "07-Harm", "07-Keyb", "07-Vibr", "10-Harm","10-Keyb","10-Vibr", "11-Harm","11-Keyb","11-Vibr", "12-Harm","12-Keyb","12-Vibr"]) #Daksh
sameArtists4 = np.array(["01-Keyb", "01-Vibr", "02-Keyb", "02-Vibr", "03-Keyb","03-Vibr", "04-Keyb", "04-Vibr"]) #Sebastian

validSemiMegasets_A_exclPracticePieces = False
validSemiMegasets_B_exclPracticePieces = False

megasetA_exclPracticePieces = np.array(["02-Harm", "02-Keyb", "02-Vibr", "07-Harm", "07-Keyb", "07-Vibr", "09-Harm","09-Keyb","09-Vibr", "10-Harm","10-Keyb","10-Vibr", "11-Harm","11-Keyb","11-Vibr"])
megasetB_exclPracticePieces = np.array(["03-Harm","03-Keyb","03-Vibr", "05-Harm","05-Keyb","05-Vibr", "06-Harm", "06-Keyb", "06-Vibr", "08-Harm","08-Keyb","08-Vibr", "12-Harm","12-Keyb","12-Vibr"])

megasetA_PracticePieces = np.array(["04-Harm", "04-Keyb", "04-Vibr"])
megasetB_PracticePieces = np.array(["01-Harm", "01-Keyb", "01-Vibr"])

def intersectionCounter(arr1, arr2):
    intersections = np.intersect1d(arr1, arr2)
    return len(intersections)

while validSemiMegasets_A_exclPracticePieces == False:
    semiMegasets_A = rng.choice(megasetA_exclPracticePieces, size=15, replace=False)
    semiMegaset_A1 = semiMegasets_A[0:8]
    semiMegaset_A2 = semiMegasets_A[8:15]
    
    #Enough +ve/-ve pieces for each (Change to account for neutral ones?):
    if 5 >= intersectionCounter(positiveValenceSets, semiMegaset_A1) >= 3 and 5 >= intersectionCounter(negativeValenceSets, semiMegaset_A1) >= 3:
        
        if 4 >= intersectionCounter(positiveValenceSets, semiMegaset_A2) >= 3 and 4 >= intersectionCounter(negativeValenceSets, semiMegaset_A2) >= 3:

    #Enough active/passive pieces for each:
            if (5 >= intersectionCounter(activeArousalSets, semiMegaset_A1) >= 3) and (5 >= intersectionCounter(passiveArousalSets, semiMegaset_A1) >= 3):
            
                if 4 >= intersectionCounter(activeArousalSets, semiMegaset_A2) >= 3 and 4 >= intersectionCounter(passiveArousalSets, semiMegaset_A2) >= 3:
        
    #Enough dom/sub pieces for each (Change to account for neutral ones?):
                    if (5 >= intersectionCounter(dominantDominanceSets, semiMegaset_A1) >= 3) and (5 >= intersectionCounter(submissiveDominanceSets, semiMegaset_A1) >= 3):
                    
                        if 4 >= intersectionCounter(dominantDominanceSets, semiMegaset_A2) >= 3 and 4 >= intersectionCounter(submissiveDominanceSets, semiMegaset_A2) >= 3:                    
                       
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
                      
                      #It does not appear possible to have maximum "spread" in the artists as well
                       #   if intersectionCounter(sameArtists1, semiMegaset_A1) == 1 and intersectionCounter(sameArtists2, semiMegaset_A1) >= 1 and intersectionCounter(sameArtists3, semiMegaset_A1) >= 1:
                      #        if intersectionCounter(sameArtists1, semiMegaset_A2) == 1 and intersectionCounter(sameArtists2, semiMegaset_A2) >= 1 and intersectionCounter(sameArtists3, semiMegaset_A1) >= 1:
                                    validSemiMegasets_A_exclPracticePieces = True

semiMegaset_A2 = np.append(semiMegaset_A2, megasetA_PracticePieces) #For the main trials, group A2 only has 7/15 attended. So, make the practice ones attended.

while validSemiMegasets_B_exclPracticePieces == False:
    semiMegasets_B = rng.choice(megasetB_exclPracticePieces, size=15, replace=False)
    semiMegaset_B1 = semiMegasets_B[0:8]
    semiMegaset_B2 = semiMegasets_B[8:15]
    
    #Enough +ve/-ve pieces for each (Change to account for neutral ones?):
    if 5 >= intersectionCounter(positiveValenceSets, semiMegaset_B1) >= 3 and 5 >= intersectionCounter(negativeValenceSets, semiMegaset_B1) >= 3:
        
        if 4 >= intersectionCounter(positiveValenceSets, semiMegaset_B2) >= 3 and 4 >= intersectionCounter(negativeValenceSets, semiMegaset_B2) >= 3:
    
    #Enough active/passive pieces for each:
            if (5 >= intersectionCounter(activeArousalSets, semiMegaset_B1) >= 3) and (5 >= intersectionCounter(passiveArousalSets, semiMegaset_B1) >= 3):
            
                if 4 >= intersectionCounter(activeArousalSets, semiMegaset_B2) >= 3 and 4 >= intersectionCounter(passiveArousalSets, semiMegaset_B2) >= 3:
        
    #Enough dom/sub pieces for each (Change to account for neutral ones?):
                    if (5>= intersectionCounter(dominantDominanceSets, semiMegaset_B1) >= 3) and (5 >= intersectionCounter(submissiveDominanceSets, semiMegaset_B1) >= 3):
                    
                        if 4 >= intersectionCounter(dominantDominanceSets, semiMegaset_B2) >= 3 and 4 >= intersectionCounter(submissiveDominanceSets, semiMegaset_B2) >= 3:                    
                       
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
                      
                      #It does not appear possible to have maximum "spread" in the artists as well
                       #   if intersectionCounter(sameArtists1, semiMegaset_A1) == 1 and intersectionCounter(sameArtists2, semiMegaset_A1) >= 1 and intersectionCounter(sameArtists3, semiMegaset_A1) >= 1:
                      #        if intersectionCounter(sameArtists1, semiMegaset_A2) == 1 and intersectionCounter(sameArtists2, semiMegaset_A2) >= 1 and intersectionCounter(sameArtists3, semiMegaset_A1) >= 1:
                                    validSemiMegasets_B_exclPracticePieces = True
                                    
semiMegaset_B2 = np.append(semiMegaset_B2, megasetB_PracticePieces) #For the main trials, group B2 only has 7/15 attended. So, make the practice ones attended.

#Find the data path:
currentFolderPath = pathlib.Path(__file__).parent.resolve()
upperFolderPath = currentFolderPath.parent.resolve()
dataPath = str(upperFolderPath) + "/Data/"
semiMegasetFile = (dataPath + "\semimegasets.txt")
with open(semiMegasetFile, 'w') as f:
    f.write("Semimegaset A1 - the sets to be attended to in part 3 by group A1: ")
    f.write(str(semiMegaset_A1))
    f.write("\n")
    f.write("Semimegaset A2 - the sets to be attended to in part 3 by group A2: ")
    f.write(str(semiMegaset_A2))
    f.write("\n")
    f.write("Semimegaset B1 - the sets to be attended to in part 3 by group B1: ")
    f.write(str(semiMegaset_B1))
    f.write("\n")
    f.write("Semimegaset B2 - the sets to be attended to in part 3 by group B2: ")    
    f.write(str(semiMegaset_B2))
    f.close