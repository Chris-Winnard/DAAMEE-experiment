import os
import argparse
import soundfile as sf
import xlwings as xw #For reading config file
import pathlib
import glob
from utils.SerialTriggerEncoder import SerialTriggerEncoder

# Specify the workbook we are looking at, and the worksheet:
wb = xw.Book("Trigger Config.xlsx")
ws = wb.sheets['Sheet1']

#To parse through this, helpful to know the number of entries for each table section. P2 stim/oddballs considered in their own generator
last_row_SS_Stim = ws.range('A' + str(ws.cells.last_cell.row)).end('up').row
last_row_parts = ws.range('G' + str(ws.cells.last_cell.row)).end('up').row

currentFolderPath = pathlib.Path(__file__).parent.resolve()
upperFolderPath = str(currentFolderPath.parent.resolve())
os.chdir(upperFolderPath)

def getFileList(in_path): #Useful for finding stimuli paths- if a piece is in Megaset A or Megaset B
    filepaths = []
    if os.path.isfile(in_path):
        filepaths.append(in_path)
    elif os.path.isdir(in_path):
        for filename in glob.glob(in_path + '/**/*.*', recursive=True):
            filepaths.append(filename)
    else:
        print("Path is invalid: " + in_path)
        return None
    return filepaths
    
def create_folder(folder):
    full_path = os.mkdir(upperFolderPath + folder)
    os.makedirs(full_path, exist_ok=True)
    

###################################################################################################################################################

#Trial trigs:    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='generate_trig')
  #  parser.add_argument("--in_folder", type=str, required=True, help="input folder containing target and non-target sounds.")
    parser.add_argument("--out_folder", type=str, required=True, help="output folder")
    parser.add_argument("--sr", type=int, default=22050, help="sampling rate. Default value is 22050.")
    parser.add_argument("--channels", type=int, default=1, help="number of output channels. Default value is 1.")
    parser.add_argument("--triggerClk", type=float, default=16.0, help="Clock rate of trigger. Default value is 16.0 Hz.")
    args = parser.parse_args()

    stim_folder =  os.path.abspath("Stimuli")
    out_folder = os.path.abspath(args.out_folder)
    sr = args.sr
    ch = args.channels
    clkSerial = args.triggerClk
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        
    triggerEncoder = SerialTriggerEncoder(sr, clkSerial)
    
    file_list = getFileList(stim_folder)
        
    for i in range(1, last_row_SS_Stim+1):
        cell = 'A' + str(i) #Need to convert 
        cellValue = str(ws[cell].value)
        
        if ".wav start" in cellValue:
            startCode = int(ws['B' + str(i)].value)
            endCode = int(ws['B' + str(i+1)].value)
            
            name = cellValue[:-6] #The cell entry, with " start" removed
            
            for filePath in file_list:
                if name in filePath:
                    nameAndPath = filePath
                    
            f = sf.SoundFile(nameAndPath)
            file_len = f.frames/f.samplerate
            trig_filename = os.path.join(out_folder, 'trigger_' + name[:-4] + ' with Gain Applied.wav')
            trig_metafilename = os.path.join(out_folder,'trigger_' + name[:-4] + ' with Gain Applied.txt')            
            triggerEncoder.resetTrigger()            
            
            [TRIAL_START_CODE, TRIAL_END_CODE] = [startCode, endCode]
            triggerEncoder.encode(TRIAL_START_CODE, 0.0)
            event_metafile = open(trig_metafilename, 'w')
            event_metafile.write("{}\t{}\n".format(TRIAL_START_CODE, 0)) # start trig position in millisecond
            #
            triggerEncoder.encode(TRIAL_END_CODE, file_len)
            event_metafile.write("{}\t{}\n".format(TRIAL_END_CODE, round(file_len*1000))) # end trig position in millisecond
            triggerEncoder.generateTrigger(trig_filename, file_len+1.0)
            event_metafile.close()
 
#####################################################################################################################################################            
    #Part trigs:
    
    for i in range(1, last_row_parts+1):
        cell = 'G' + str(i) #Need to convert 
        cellValue = str(ws[cell].value)
        if "start" in cellValue or "end" in cellValue: #E.g "P1 start"
            location = str(ws.range('G{}'.format(i)).value)
              
            trig_filename = os.path.join(upperFolderPath, location + '_trigger.wav')
            trig_metafilename = os.path.join(upperFolderPath, location + '_trigger.txt')            
            triggerEncoder.resetTrigger()    
            trigNumber = int(ws.range('H{}'.format(i)).value)
        
            triggerEncoder.encode(trigNumber, 0.0)
            event_metafile = open(trig_metafilename, 'w')
            event_metafile.write("{}\t{}\n".format(trigNumber, 0)) #position in millisecond
            triggerEncoder.generateTrigger(trig_filename, 1.0)
            event_metafile.close()


wb.save()
wb.close()