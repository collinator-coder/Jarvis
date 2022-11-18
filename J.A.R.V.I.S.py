
#!/usr/bin/env python3

import argparse
import json
import queue
import sys

import requests
import sounddevice as sd
from vosk import KaldiRecognizer, Model

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])

    model = Model(lang="en-us")

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                # print(rec.Result())
                result_text = rec.Result()
                # print(result_text)
                parsed_data = json.loads(result_text)
                # print(parsed_data['text'])

                # Server Stuff
                print(parsed_data['text'])
                if parsed_data['text'].startswith('jarvis'):
                    print("Jarvis Detected.")

                if not parsed_data['text'].startswith('jarvis'):
                    print("Not Accepted.")
                try:
                    headers = {'Content-Type': 'text/plain', 'Accept': '*/*'}
                    r = requests.post('http://openhab.local:8080/rest/habot/chat', auth=('oh.CollinToken.ucpZzjkoWnhxg9P6lkmIdKJl11rQT0UN6Ky6rxuE99n87SwyEMptvCHurYZ9GlfmU636B2mSaxRHs6js4mg', ''), data=(parsed_data['text']), headers=headers)
                    print(r.reason)
                    print(r.status_code)
                except requests.RequestException as e:
                    print(e.strerror)

                if parsed_data['text'] == "jarvis stop recording":
                    print("Done")
                    parser.exit(0)

            if dump_fn is not None:
                dump_fn.write(data)
except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)

except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))