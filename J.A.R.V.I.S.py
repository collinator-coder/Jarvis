from vosk import Model, KaldiRecognizer
import wave
import json
import os
from posixpath import dirname
dirname = os.path.dirname(__file__)
in_file_name = os.path.join(dirname, 'Wav', 'Recording.wav')
out_file_text = os.path.join(dirname, 'Text')
out_file_results = os.path.join(dirname, 'Results')
'''
this script reads a mono wav file (inFileName) and writes out a json file (outfileResults) with the speech to text conversion results.  It then writes out another json file (outfileText) that only has the "text" values.
'''

wf = wave.open(in_file_name, "r")

# initialize a str to hold results
results = ""
text_results = []

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
        result_dict = json.loads(recognizerResult)
        # save the 'text' value from the dictionary into a list
        text_results.append(result_dict.get("text", ""))

##    else:
##        print(recognizer.PartialResult())
        
# process "final" result
results = results + recognizer.FinalResult()
result_dict = json.loads(recognizer.FinalResult())
text_results.append(result_dict.get("text", ""))

# write results to a file
filestr='JVStext'
file="JVStext"
with open(out_file_results, 'w') as output:
    print(results, file, output)

# write text portion of results to a file
with open(out_file_text, filestr) as output:
    print(json.dumps(text_results, indent=4))
