#!/usr/bin/env python3

import os
import sys
from os import path
from pydub import AudioSegment

def mp3_to_wav(source, destination):
    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(source)
    sound.export(destination, format="wav")

if __name__ == "__main__":
    source = sys.argv[1]
    destination = sys.argv[2]
    
    mp3_to_wav(source, destination)
    
