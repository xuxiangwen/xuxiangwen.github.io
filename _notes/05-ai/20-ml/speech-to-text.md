## Resouce

- https://zhuanlan.zhihu.com/p/70246657  DeepSpeech

- https://www.jiqizhixin.com/articles/2019-07-30-9  PyTorch-Kaldi

- [语音识别技术的前世今生](https://zhihu-live.zhimg.com/0af15bfda98f5885ffb509acd470b0fa)

  



## PyTorch-Kaldi

https://github.com/mravanelli/pytorch-kaldi



### Next Version: SpeechBrain

下一个版本是[SpeechBrain](https://speechbrain.github.io/)。下图看起来，第一个Release要2021年6月才发布。

![image-20200301090248055](images/image-20200301090248055.png)

## DeepSpeech

https://github.com/mozilla/DeepSpeech

### Install

#### CPU & GPU

0.6.1版本好像不好用

~~~shell
pip uninstall deepspeech deepspeech-gpu
pip install deepspeech
pip install deepspeech-gpu
~~~

#### Test

~~~shell
# Download pre-trained English model and extract
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.1/deepspeech-0.6.1-models.tar.gz
tar xvf deepspeech-0.6.1-models.tar.gz

# Download example audio files
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.1/audio-0.6.1.tar.gz
tar xvf audio-0.6.1.tar.gz

# Transcribe an audio file
deepspeech --model deepspeech-0.6.1-models/output_graph.pbmm --scorer deepspeech-0.6.1-models/kenlm.scorer --audio audio/2830-3980-0043.wav

~~~



## MP3 to WAV

### 安装

- ubuntu

  ~~~
  pip install pydub
  
  add-apt-repository ppa:mc3man/trusty-media  
  apt-get update  
  apt-get install ffmpeg  
  apt-get install frei0r-plugins  
  ~~~

- centos

  ~~~
  pip install pydub
  
  add-apt-repository ppa:mc3man/trusty-media  
  apt-get update  
  apt-get install ffmpeg  
  apt-get install frei0r-plugins 
  ~~~

  

### 创建程序

~~~python
cat << EOF > mp3towav.py
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
    
EOF
chmod 755 mp3towav.py
~~~

测试

~~~shell
/tf/eipi10/xuxiangwen.github.io/_notes/05-ai/20-dl//mp3towav.py \
"/home/grid/eipi10/xuxiangwen.github.io/_notes/05-ai/20-dl/data/deepspeech/audio/Captura/2020-02-27-11-34-42.mp3" \
"/home/grid/eipi10/xuxiangwen.github.io/_notes/05-ai/20-dl/data/deepspeech/audio/Captura/2020-02-27-11-34-42.wav" 

/tf/eipi10/xuxiangwen.github.io/_notes/05-ai/20-dl//mp3towav.py \
"/tf/eipi10/xuxiangwen.github.io/_notes/05-ai/20-dl/data/deepspeech/audio/Captura/2020-02-28-12-31-39.mp3" \
"/tf/eipi10/xuxiangwen.github.io/_notes/05-ai/20-dl/data/deepspeech/audio/Captura/2020-02-28-12-31-39.wav" 
~~~

Wav变成文本

~~~
cd /tf/eipi10/xuxiangwen.github.io/_notes/05-ai/20-dl/data/deepspeech/

deepspeech --model deepspeech-0.6.1-models/output_graph.pbmm \
--audio audio/Captura/2020-02-27-11-34-42.wav 

# 查看wav文件的头信息
sox -V audio/Captura/2020-02-28-12-31-39-deepark.wav   -n 
sox -V audio/8455-210777-0068.wav -n 
sox -b audio/Captura/20200228_123139_deepark.wav -n 
sox -V audio/Captura/*.wav   -n 
sox -V audio/*.wav   -

deepspeech --model deepspeech-0.6.1-models/output_graph.pbmm \
--audio audio/Captura/20200228_123139_deepark.wav 
~~~





~~~
cd C:\Users\xu6\Documents\Captura
scp 20200228_123139_deepark.wav grid@aa00:/home/grid/eipi10/xuxiangwen.github.io/_notes/05-ai/20-dl/data/deepspeech/audio/Captura
~~~

