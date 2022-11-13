from os import path
from pydub import AudioSegment

# files                                                                         
src = "C:\\Users\\xxx\\pyenv\\NLP\\inputfiles\\NOAGENDA\\NA-1348-2021-05-20-Final.mp3"
dst = ""

# start time in seconds
startTime = 60.0
# end time in seconds
endTime = 120.0

# create audiosegment                                                            
sound = AudioSegment.from_mp3(src)
# cut it to length
cut = sound[startTime * 1000:endTime * 1000]
# export sound cut as wav file
cut.export(dst, format="wav")
