import numpy as np
import pathlib
from numpy.random import default_rng
rng = default_rng() 
import os

allParticipants = np.arange(1, 32) #If 32 participants

halfParticipants = round(len(allParticipants)/2)

megasetA_participants = rng.choice(allParticipants, size=halfParticipants, replace=False)
megasetA_participants = megasetA_participants.tolist() #Convert to list

megasetB_participants = np.setdiff1d(allParticipants, megasetA_participants)
megasetB_participants = megasetB_participants.tolist()

for i in range(0, len(megasetA_participants)):
    x = megasetA_participants[i]
    if x < 10:
        x = "P0" + str(x)
    else:
        x = "P" + str(x)
    megasetA_participants[i] = x
    
for i in range(0, len(megasetB_participants)):
    x = megasetB_participants[i]
    if x < 10:
        x = "P0" + str(x)
    else:
        x = "P" + str(x)
    megasetB_participants[i] = x

#Find the data path:
currentFolderPath = pathlib.Path(__file__).parent.resolve()
upperFolderPath = currentFolderPath.parent.resolve()
dataPath = str(upperFolderPath) + "/Data/"
File = (dataPath + "\Megaset Assignment.txt")


#Set it up so that we can assign new participants without contradicting what was already written:
A_alreadyAssigned = []
B_alreadyAssigned = []


with open(File,"r") as f:     
    
    lines = f.readlines()
    for line in lines:
        if "Megaset A" in line:
            megasetA_original = line.rstrip("\n")
        
        if "Megaset B" in line:
            megasetB_original = line
            
        words = line.rstrip("\n")
        words = words.rsplit(" ")
        
        for word in megasetA_participants:
            if word in words:
                A_alreadyAssigned.append(word)
        
        for word in megasetB_participants:
            if word in words:
                B_alreadyAssigned.append(word)

    megasetA_participants_new = set(megasetA_participants) - set(A_alreadyAssigned)
    megasetA_participants_new = " ".join(str(x) for x in megasetA_participants_new) #String format
    megasetA_participants_updated = megasetA_original + " " + megasetA_participants_new
    
    megasetB_participants_new = set(megasetB_participants) - set(B_alreadyAssigned)
    megasetB_participants_new = " ".join(str(x) for x in megasetB_participants_new)    
    megasetB_participants_updated = megasetB_original + " " + megasetB_participants_new
    
    f.close()
    
#Finally, write to file:
with open(File,"w") as f:    
    f.write(str(megasetA_participants_updated))
    f.write("\n")
    f.write(str(megasetB_participants_updated))   
    f.close