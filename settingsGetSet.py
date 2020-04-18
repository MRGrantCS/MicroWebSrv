import ujson
def setWifi (filename, SSID, PSK):
  
  try:
    import uos as os
  except:
    import os
  with open(filename, 'r') as settings:
    data = ujson.load(settings)
    data['STATION']['SSID'] = SSID
    data['STATION']['PSK'] = PSK
  os.remove(filename)
  with open(filename, 'w') as settings:
    ujson.dump(data, settings)
  print("Restart after Update")
  #machine.reset()

def getWifi (filename, AP):
  with open(filename, 'r') as settings:
    data = ujson.load(settings)
    if AP == True:
      SSID = data['AP']['SSID']
      PSK = data['AP']['PSK']
    else:
      SSID = data['STATION']['SSID']
      PSK = data['STATION']['PSK']

  return SSID, PSK

def setADA (filename, URL, USERNAME, KEY, FEEDNAME):
  
  try:
    import uos as os
  except:
    import os
  with open(filename, 'r') as settings:
    data = ujson.load(settings)
    data['ADAIO']['URL'] = URL
    data['ADAIO']['USERNAME'] = USERNAME
    data['ADAIO']['KEY'] = KEY
    data['ADAIO']['FEEDNAME'] = FEEDNAME
      
  os.remove(filename)
  with open(filename, 'w') as settings:
    ujson.dump(data, settings)
  print("Restart after Update")

def getADA (filename):
    with open(filename, 'r') as settings:
      data = ujson.load(settings)
      URL = data['ADAIO']['URL']
      USERNAME = data['ADAIO']['USERNAME']
      KEY = data['ADAIO']['KEY']
      FEEDNAME = data['ADAIO']['FEEDNAME']
    return bytes(URL,'utf-8'),bytes(USERNAME,'utf-8'),bytes(KEY,'utf-8'),bytes(FEEDNAME,'utf-8')
