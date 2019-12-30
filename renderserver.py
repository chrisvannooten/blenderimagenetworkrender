import bpy
import socket
import threading

class RenderThread(threading.Thread):
	def __init__(self,threadID,name,sock,writeto):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name=name
		self.sock=sock
		self.stop_event = threading.Event()
		self.writeto = writeto
	def run(self):
		print("Starting Server")
		while not self.stop_event.is_set():
			print("Awaiting Connection")
			conn, address = self.sock.accept()
			with conn:
				currentscenes = bpy.data.scenes.items()
				print('Connected by', address)
				borderdata = ""
				while True:
					data = conn.recv(1024)
					if data == b'>sendingfile<':
						print('recieving file')
						f = open(self.writeto,'wb')
						wrdata = conn.recv(1024)
						while wrdata != b'EOF!':
							if wrdata == b'':
								break
							if wrdata.rfind(b'ENDB') >= 0:
								lastbit = wrdata[:wrdata.rfind(b'ENDB')+4]
								data = wrdata[wrdata.rfind(b'ENDB'):]
								f.write(lastbit)
								break
							if wrdata.rfind(b'>EOF!<') >=0:
								lastbit = wrdata[:wrdata.rfind(b'>EOF!<')]
								data = wrdata[wrdata.rfind(b'>EOF!<'):]
								f.write(lastbit)
								break
							f.write(wrdata)
							wrdata=conn.recv(1024)
						print('File recieved')
						f.close()
					print(data)
					if data.rfind(b'>sendingborder<') >=0:
						print("Getting border")
						brddata = data[data.rfind(b'>sendingborder<')+15:]
						while True:
							print(brddata)
							if brddata.rfind(b'>endborder<'):
								borderdata += brddata[:brddata.rfind(b'>endborder<')].decode("UTF-8")
								break
							borderdata+=brddata.decode("UTF-8")
							brddata = conn.recv(1024)
						print(borderdata)
						borderdata = borderdata.split(',')
						with bpy.data.libraries.load(self.writeto) as (data_from, data_to):
							for attr in dir(data_to):
								if attr != 'workspaces':
									setattr(data_to, attr, getattr(data_from, attr))
						for it in bpy.data.scenes.items():
							if not it in currentscenes:
								filepath = '/tmp/{}'.format(it[0])
								bpy.data.scenes[it[0]].render.filepath = filepath
								bpy.data.scenes[it[0]].render.use_border=True
								print("Rendering")
								print(borderdata)
								xcoord =float(borderdata[0])
								ycoord = float(borderdata[1])
								bpy.data.scenes[it[0]].render.border_min_x=xcoord
								bpy.data.scenes[it[0]].render.border_max_x=ycoord
								bpy.data.scenes[it[0]].render.use_crop_to_border = True
								bpy.ops.render.render(scene=it[0],write_still=True)
								f = open("{}{}".format(filepath,bpy.data.scenes[it[0]].render.file_extension),"rb")
								conn.sendfile(f)
								conn.send(b'>EOF<')
								break
					if not data:
						break
				#bpy.types.Scene.GotFile = True

			print('Conn ended')	
	def stop(self):
		print("Stopping Thread")
		self.stop_event.set()
	def stopped(self):
		return self.stop_event.is_set()

class RenderServer(bpy.types.Operator):
	bl_idname = 'object.render_server'
	bl_label = "Start render server"
	timer = None

	def __init__(self):
		print("Render Server started")
	def __del__(self):
		print("Render Server ended")

	def execute(self,context):
		socket1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		socket1.bind(('',65432))
		socket1.listen()
		mythread = RenderThread(1,'Server Render Thread',socket1,'/tmp/incoming.blend')
		mythread.daemon = True
		mythread.start()
		self.timer = context.window_manager.event_timer_add(0.1, window=context.window)
		
		return{"FINISHED"}
