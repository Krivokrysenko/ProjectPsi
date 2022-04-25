import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys

import asyncio
from codes import Codes

class Voice:
    def __init__(self, Nona):
        self.Nona = Nona
        self.name = Nona.name
        self.listening = Nona.on
        self.q = queue.Queue()

    def int_or_str(self, text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    async def NonaListener(self):
        # https://github.com/alphacep/vosk-api
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '-l', '--list-devices', action='store_true',
            help='show list of audio devices and exit')
        args, remaining = parser.parse_known_args()
        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[parser])
        parser.add_argument(
            '-f', '--filename', type=str, metavar='FILENAME',
            help='audio file to store recording to')
        parser.add_argument(
            '-m', '--model', type=str, metavar='MODEL_PATH',
            help='Path to the model')
        parser.add_argument(
            '-d', '--device', type=self.int_or_str,
            help='input device (numeric ID or substring)')
        parser.add_argument(
            '-r', '--samplerate', type=int, help='sampling rate')
        args = parser.parse_args(remaining)
        if args.model is None:
            args.model = "model"
        if not os.path.exists(args.model):
            print("Please download a model for your language from https://alphacephei.com/vosk/models")
            print("and unpack as 'model' in the current folder.")
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device, dtype='int16',
                               channels=1, callback=self.callback):
            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while self.listening:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()[14:-3]
                    # print(result)
                    await self.Nona.addToQueue(Codes.INP, result)
                    await asyncio.sleep(0.01)
                else:
                    pass
                    # print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data)