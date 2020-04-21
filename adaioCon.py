from umqtt.robust import MQTTClient
import os
import sys

from gpioCon import relayOn, relayOff

from settingsGetSet import getADA

# the following function is the callback which is 
# called when subscribed data is received
def cb(topic, msg):
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    free_heap = str(msg,'utf-8')
    print('free heap size = {} bytes'.format(free_heap))
    if free_heap.lower() == "on":
      relayOn()
    elif free_heap.lower() == "off":
      relayOff()
    else:
      relayOff()

def aioTest (filename):
  aioSuccess = False
  
  # create a random MQTT clientID 
  random_num = int.from_bytes(os.urandom(3), 'little')
  mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

  # connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
  # 
  # To use a secure connection (encrypted) with TLS: 
  #   set MQTTClient initializer parameter to "ssl=True"
  #   Caveat: a secure connection uses about 9k bytes of the heap
  #         (about 1/4 of the micropython heap on the ESP8266 platform)
  
  
  ADAFRUIT_IO_URL, ADAFRUIT_USERNAME, ADAFRUIT_IO_KEY, ADAFRUIT_IO_FEEDNAME = getADA(filename)

  client = MQTTClient(client_id=mqtt_client_id, 
                      server=ADAFRUIT_IO_URL, 
                      user=ADAFRUIT_USERNAME, 
                      password=ADAFRUIT_IO_KEY,
                      ssl=False)
      
  try:      
      client.connect()
  except Exception as e:
      print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
      return aioSuccess
      #sys.exit()

  
  mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')    
  client.set_callback(cb)                    
  client.subscribe(mqtt_feedname)  

  # following two lines is an Adafruit-specific implementation of the Publish "retain" feature 
  # which allows a Subscription to immediately receive the last Published value for a feed,
  # even if that value was Published two hours ago.
  # Described in the Adafruit IO blog, April 22, 2018:  https://io.adafruit.com/blog/  
  mqtt_feedname_get = bytes('{:s}/get'.format(mqtt_feedname), 'utf-8')    
  client.publish(mqtt_feedname_get, '\0')  
  


  #Check if connection worked and return success/fail
  
  try:
      client.wait_msg()
      print("Connected to ADAIO")
      aioSuccess = True
  except Exception as e:
    print('could not connect to ADAIO {}{}'.format(type(e).__name__, e))
  return aioSuccess

def aioCon (filename):
  # create a random MQTT clientID 
  random_num = int.from_bytes(os.urandom(3), 'little')
  mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

  # connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
  # 
  # To use a secure connection (encrypted) with TLS: 
  #   set MQTTClient initializer parameter to "ssl=True"
  #   Caveat: a secure connection uses about 9k bytes of the heap
  #         (about 1/4 of the micropython heap on the ESP8266 platform)
  
  
  ADAFRUIT_IO_URL, ADAFRUIT_USERNAME, ADAFRUIT_IO_KEY, ADAFRUIT_IO_FEEDNAME = getADA(filename)

  print (ADAFRUIT_IO_URL, ADAFRUIT_USERNAME, ADAFRUIT_IO_KEY, ADAFRUIT_IO_FEEDNAME)
  print (filename)

  client = MQTTClient(client_id=mqtt_client_id, 
                      server=ADAFRUIT_IO_URL, 
                      user=ADAFRUIT_USERNAME, 
                      password=ADAFRUIT_IO_KEY,
                      ssl=False)
      
  try:      
      client.connect()
  except Exception as e:
      print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
      #sys.exit()

  mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')    
  client.set_callback(cb)                    
  client.subscribe(mqtt_feedname)  

  # following two lines is an Adafruit-specific implementation of the Publish "retain" feature 
  # which allows a Subscription to immediately receive the last Published value for a feed,
  # even if that value was Published two hours ago.
  # Described in the Adafruit IO blog, April 22, 2018:  https://io.adafruit.com/blog/  
  mqtt_feedname_get = bytes('{:s}/get'.format(mqtt_feedname), 'utf-8')    
  client.publish(mqtt_feedname_get, '\0')  


  # wait until data has been Published to the Adafruit IO feed
  while True:
      try:
          client.wait_msg()
      except KeyboardInterrupt:
          print('Ctrl-C pressed...exiting')
          client.disconnect()
          sys.exit()

'''
  ADAFRUIT_IO_URL = b"io.adafruit.com"
  ADAFRUIT_USERNAME= b"Scytale86"
  ADAFRUIT_IO_KEY = b"aio_WAXD90YR4PiWD5EGCS0EVHcG2Olf"
  ADAFRUIT_IO_FEEDNAME = b"onoff"
'''