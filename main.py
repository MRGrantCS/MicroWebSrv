try:
  import usocket as socket
except:
  import socket

import aioCon

try:
  import uos as os
except:
  import os

import network

try:
  import utime as time
except:
  import time

from umqtt.robust import MQTTClient

import esp
esp.osdebug(None)

import gc
gc.collect()

from settingsGetSet import setWifi, getWifi

from microWebSrv import MicroWebSrv

#initialise variables
AP = False
filename = 'settings.json'
ssid = ''
password = ''


#--- Set up wifi connection
try:
  #--- Try to connect as Station
  ssid , password = getWifi(filename, AP)
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  #--- timed retries to allow esp32 to connect to network
  tries = 0  
  while tries < 5 and station.isconnected() == False:
    tries += 1
    print("Connection unsuccessful. Attempt:", tries)
    time.sleep(3)
  #--- raise exception if unable to connect to an AP
  if station.isconnected() == False:
    print('Could not connect as Station')  
    raise Exception
  print('Station Connection successful')
  #--- Print IP details
  print(station.ifconfig())

except Exception:
  #--- switch to AP mode, using AP details in settings.json
  AP = True
  ssid , password = getWifi(filename, AP)
  ap = network.WLAN(network.AP_IF)
  ap.active(True)
  while ap.active() == False:
    pass
  ap.config(essid=ssid, password=password)
  print('Access Point Created')
  #--- Print IP details
  print(ap.ifconfig())

finally:
  print("Network details:")
  print("SSID =",ssid)
  print("Password =",password)

#--- aiocon

if aioTest() == True & AP == False:
  aioCon()

# ----------------------------------------------------------------------------




@MicroWebSrv.route('/settings')
def _httpHandlerSettingsGet(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>Settings GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Your current IP address = %s
            <br />
			<form action="/test" method="post" accept-charset="ISO-8859-1">
				SSID: <input type="text" name="SSID"><br />
				Password : <input type="text" name="PSK"><br />
        <br />
        ADAIO URL : <input type="text" name="URL"><br />
        ADAIO Username : <input type="text" name="USERNAME"><br />
        ADAIO Key : <input type="text" name="KEY"><br />
        ADAIO Feed Name : <input type="text" name="FEEDNAME"><br />
				<input type="submit" value="Submit">
			</form>
        </body>
    </html>
	""" % httpClient.GetIPAddr()
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )


@MicroWebSrv.route('/set', 'POST')
def _httpHandlerSettingsPost(httpClient, httpResponse) :
	formData  = httpClient.ReadRequestPostedFormData()
	SSID = formData["SSID"]
	PSK  = formData["PSK"]
  URL  = formData["URL"]
  USERNAME = formData["USERNAME"]
  KEY  = formData["KEY"]
  FEEDNAME  = formData["FEEDNAME"]
	content   = """\
	<!DOCTYPE html>
	<html lang=en>
		<head>
			<meta charset="UTF-8" />
            <title>Settings POST</title>
        </head>
        <body>
            <h1>TEST POST</h1>
            SSID = %s<br />
            PSK = %s<br />
            <br />
            ADAIO URL = %s<br />
            ADAIO Username = %s<br />
            ADAIO Key = %s<br />
            ADAIO Feed Name = %s<br />

            Restart after update <br />
        </body>
    </html>
	""" % ( MicroWebSrv.HTMLEscape(SSID), MicroWebSrv.HTMLEscape(PSK) , MicroWebSrv.HTMLEscape(URL), MicroWebSrv.HTMLEscape(USERNAME), MicroWebSrv.HTMLEscape(KEY), MicroWebSrv.HTMLEscape(FEEDNAME))
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )
	setWifi(filename, SSID, PSK)
  setADA(filename, URL, USERNAME, KEY, FEEDNAME)


@MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
@MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
@MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST EDIT</title>
        </head>
        <body>
	"""
	content += "<h1>EDIT item with {} variable arguments</h1>"\
		.format(len(args))
	
	if 'index' in args :
		content += "<p>index = {}</p>".format(args['index'])
	
	if 'foo' in args :
		content += "<p>foo = {}</p>".format(args['foo'])
	
	content += """
        </body>
    </html>
	"""
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg) :
	print("WS RECV TEXT : %s" % msg)
	webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")

# ----------------------------------------------------------------------------

#routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
#]

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(threaded=True)
