from vosk import Model, KaldiRecognizer
import wave
import json
import os
from posixpath import dirname
dirname = os.path.dirname(__file__)
filein = os.path.join(dirname, 'Wav', 'Recording.wav')
outtxt = os.path.join(dirname, 'Text')
outrec = os.path.join(dirname, 'Results')
'''
this script reads a mono wav file (inFileName) and writes out a json file (outfileResults) with the speech to text conversion results.  It then writes out another json file (outfileText) that only has the "text" values.
'''

inFileName = filein
outfileText = outtxt
outfileResults = outrec

wf = wave.open(inFileName, "rb")

# initialize a str to hold results
results = ""
textResults = []

# build the model and recognizer objects.
model = Model(dirname)
recognizer = KaldiRecognizer(model, wf.getframerate())
recognizer.SetWords(True)

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        recognizerResult = recognizer.Result()
        results = results + recognizerResult
        # convert the recognizerResult string into a dictionary  
        resultDict = json.loads(recognizerResult)
        # save the 'text' value from the dictionary into a list
        textResults.append(resultDict.get("text", ""))

##    else:
##        print(recognizer.PartialResult())
        
# process "final" result
results = results + recognizer.FinalResult()
resultDict = json.loads(recognizer.FinalResult())
textResults.append(resultDict.get("text", ""))

# write results to a file
filestr='JVStext'
file="JVStext"
with open(outfileResults, 'w') as output:
    print(results, file, output)

# write text portion of results to a file
with open(outfileText, filestr) as output:
    print(json.dumps(textResults, indent=4))
    



