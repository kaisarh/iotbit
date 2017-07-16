######################################################################
##
## IoT for BBC Micro:bit
## Reads comma separted data from BBC Micro:bit over serial port
## Hosts a website using Flask and Google chart
## Serves live data
## 
## Author: Kaisar H
##
## Date: 16th July, 2017
##
######################################################################

from flask import Flask, request, render_template
from time import sleep
import serial
import SerialData
import gviz_api

MAX_DATA_COUNT = 100
COM_PORT = "COM9"
COM_BAUD = 115200

app = Flask(__name__)

#following are temporary description and data
description = {"t": ("number", "T"), "y": ("number", "Y")}
ser_data = [{"t" : 0, "y": 0}]
col_order = ["t", "pitch"]

desc_done = False
t_pos = 0
ser = None

@app.route('/')
def index():
    return 'Data Plotter'

@app.route('/bit')
def bit():
    return render_template('line.html')

@app.route('/data')
def data():
	global t_pos, ser, desc_done, description, col_order
	t_pos = t_pos + 1
	
	if not ser:
		ser = SerialData.SerialData(COM_PORT, COM_BAUD, bytesize=serial.EIGHTBITS, 
			parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, xonxoff=0, rtscts=0, debug=False )
			
	if ser:
		#description, col_order
		if not desc_done:
			description = {"t": ("number", "T")}
			col_order = ["t"]
		
		val_dict = {"t" : t_pos}

		#get comma seperated data from serial
		pair_ar = ser.getstr().split(',')
		
		#for each data
		for pair in pair_ar:
		
			#get title and value
			title = pair.split(':')[0]
			val = pair.split(':')[1]
			
			#add to val and description
			val_dict[title] = int(val)
			
			if not desc_done:
				description[title] = ("number", title)
				col_order.append(title)
			
		desc_done = True
		
		#add to data and resize if needed
		print val_dict
		ser_data.append(val_dict)
		if len(ser_data) > MAX_DATA_COUNT:
			del ser_data[0]
	
	#prepare datatable
	data_table = gviz_api.DataTable(description)
	data_table.LoadData(ser_data)
	
	#handle request id and return json data
	reqid = request.args.get("tqx").split(':')[1]
	print "Request Id:", reqid
	return data_table.ToJSonResponse(req_id=reqid, columns_order=col_order)
	
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
	