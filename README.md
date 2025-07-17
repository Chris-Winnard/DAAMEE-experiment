# Before using the code:
Take care that you are using the correct modules. Some of these are not trivial to install (e.g., for Librosa there are big differences between relatively "close" versions). Advice is given in "Key External Modules.docx".

# When to run the code:
## General preparation for taking data:
The stimuli and participant groups have already been mixed. However, if you would like to redo this, the following files in "Calibration and Stimuli Personalisation" need to be run, in this order. The first three steps are for assigning stimuli to groupings; the final two steps are for assigning participants to groupings, and one of these processes can be done without the other.
* "megasetMixer.py", to mix the sets of stimuli ("Set01, etc.) into two "megasets": A and B. The mixer ensures that these are balanced for e.g., intended emotional classes.
* "megasetMixChecker.py", to check that the balance conditions hold, including when practice stimuli are excluded (as these may be considered less relevant depending on the analysis).
* "semimegasetMixer.py": to split the megasets into "semimegasets": 1 and 2. These are relevant for P3 (an attendance task), where some stimuli are or aren't attended to. It is intended to ensure that: every piece is 'attended' in one semimegaset, and 'unattended' in another semimegaset; each semimegaset has an equal number of attended/unattended (e.g., 7/15 main trials being attended plus the practice trial); and similarly for megasets as a whole, that there is equal balancing of things like emotions, e.g half of the high-valence pieces in megaset A being attended to in semimegaset A1.
* "megasetAssigner.py", to assign each participant a megaset for stimuli.
* "groupAssigner.py", to assign each participant to a group for stimuli and attendance conditions (e.g., if a participant who has had Megaset A assigned will be in Group A1 or A2).

### Reverse calibration:
The Set07 pieces were originally noted as having different perceived loudnesses compared to the other pieces, even with the same normalisation relative to full-scale deflection. To help adjust these, we ran "reverse calibration tests", where participants would listen to the pieces and give feedback. If one wants to run this again, please use "Calibration and Stimuli Personalisation/Reverse Calibration.py". If one wants to change the stimuli used in this, please change the script as well as the files in "Calibration and Stimuli Personalisation/Calibration Stimuli (Downsampled in Advance)". 

### Trigger generation:
Run "Trigger Generation (Not Inc P2 Trial Trigs)/generate_trig.py" to generate the three parts' start/end triggers, and stimuli triggers for Part 1/Part 3.

## Before a specific participant's experimental session:
* Run "Calibration and Stimuli Personalisation/randomOddballCreator.py", with their participant number input (e.g., "P01").
* "oddballTimingTest.py" may also be run to double-check the oddballs are spaced out as intended (early on there were some bugs in randomOddballCreator.py, although these have been resolved "oddballTimingTest.py" is kept in case one wants to edit the former and use the latter for testing).

## During the session:
* Complete the questionnaire: "Questionnaire.py". (Goldsmiths Musical Sophistication Index score results are automatically calculated and logged by calculator).
* Complete the calibration test: "Calibration and Stimuli Personalisation/Calibration and Stimuli Prep Three Instruments GUI.py".
* Run "personalisedStimuliListsTrigs.py" (with the participant number input).
* Complete Part 1 with "Part 1 Script.py".
* Before starting Part 2, it is advisable to show the participant some oddball demos.
* Complete Part 1 with "Part 2 Script.py".
* Complete Part 3 with "Part 3 Script.py".