import speech_recognition as sr
from threading import Thread, currentThread
from copy import copy
import graphics
from graphics import GraphWin, color_rgb, Text, Point, Circle, Rectangle
from time import sleep
import datetime


def recog(rec_id, audio):
  global toFilter, f
  t_id = copy(rec_id)
  
  text = r.recognize_google(audio, language='ko-KR', show_all=True)
  print(text)

  falt.write(datetime.datetime(1970,1,1).now().isoformat() + str(text) + '\n')

  _max = 0

  if text:
    print("%4d %s" % (t_id, text['alternative'][0]['transcript']))

    del history[0]
    history.append(text['alternative'][0]['transcript'])
    f.write(datetime.datetime(1970,1,1).now().isoformat() + text['alternative'][0]['transcript'] + '\n')

    for a in text['alternative']:
      c = a['transcript'].count(toFilter)
      _max = max(_max, c)

    global yaegiCount
    yaegiCount += _max
    '''
  except:
    print("%4d <No message>" % t_id)

    del history[0]
    history.append('.')'''
  


def record1():
  rec_id = -1
  with mic1 as source:
    while running:
      rec_id += 1
      try:
        audio = r.listen(source, phrase_time_limit=7,  timeout=0)

        Thread(target=recog, args=(rec_id,audio), daemon=True).start()
      except:
        print('%4d <Failed to record>' % rec_id)



def window():
  win = GraphWin("얘기 카운트", 1280, 720)
  win.setBackground(color_rgb(17, 22, 15))

  historyText = Text(Point(480, 360), '')
  historyText.setFill(color_rgb(255, 255, 255))
  historyText.setFace("arial")
  historyText.setSize(16)
  historyText.draw(win)

  rect = Rectangle(Point(960, 0), Point(1280, 720))
  rect.setFill(color_rgb(17, 22, 15))
  rect.draw(win)

  clockText = Text(Point(1117, 16), "")
  clockText.setFill(color_rgb(255, 255, 255))
  clockText.setFace("courier")
  clockText.setSize(16)
  clockText.draw(win)

  yaegiConstText = Text(Point(1117, 300), "%s 횟수" % toFilter)
  yaegiConstText.setFill(color_rgb(255, 255, 255))
  yaegiConstText.setFace("arial")
  yaegiConstText.setSize(36)
  yaegiConstText.draw(win)

  yaegiNumberText = Text(Point(1117, 420), "0")
  yaegiNumberText.setFill(color_rgb(255, 255, 255))
  yaegiNumberText.setFace("arial")
  yaegiNumberText.setSize(36)
  yaegiNumberText.draw(win)

  line = graphics.Line(Point(960, 0), Point(960, 720))
  line.setFill(color_rgb(200, 200, 200))
  line.draw(win)

  while not win.checkMouse():
    clockText.setText("%s KST" % datetime.datetime(2020, 1, 1).now().isoformat().split('.')[0])
    yaegiNumberText.setText(str(yaegiCount))
    historyText.setText('\n'.join(history))

    sleep(1)

  win.close()
  
  running = False

  global f
  f.write('%s count: %d' % (toFilter, yaegiCount))


print(sr.Microphone.list_microphone_names())
input("Press enter to start.")

f = open('output/%s.txt' % datetime.datetime(1970,1,1).now().isoformat().split('.')[0].replace('-','').replace(':',''), 'w', encoding='utf8')
falt = open('output/%s-alt.txt' % datetime.datetime(1970,1,1).now().isoformat().split('.')[0].replace('-','').replace(':',''), 'w', encoding='utf8')

r = sr.Recognizer()
mic1 = sr.Microphone()


running = True

yaegiCount = 0
toFilter = '얘기'

history = ['.'] * 30

recThread1 = Thread(target=record1, daemon=True)

recThread1.start()
window()

f.close()
falt.close()
