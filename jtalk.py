#coding: utf-8
import subprocess

def jtalk(t):
    open_jtalk=['open jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice']
    speed=['-r','1.0']
    outwav=['ow','test.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t.encode('utf-8'))
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','test.wav','-D plughw:2,0']
    wr = subprocess.Popen(aplay)

def main():
    text = 'じゃん、けん、ぽん'
    jtalk(text)

if __name__ == '__main__':
    main()
