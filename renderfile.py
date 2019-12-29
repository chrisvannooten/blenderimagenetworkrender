import bpy
import threading
import socket
import time
import math
from PIL import Image

class SendFile(threading.Thread):
    def __init__(self,threadID,name,sock,startx,endx,scene):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name=name
        self.sock=sock
        self.startx=startx
        self.endx=endx
        self.stop_event = threading.Event()
        self.scene = scene
    def run(self):
        filepath = bpy.context.blend_data.filepath
        print('Sending File ' + filepath)
        self.sock.sendall(b'>sendingfile<')
        if filepath != '':
            f = open(filepath,'rb')
            self.sock.sendfile(f)
            self.sock.send(b'>EOF!<')
        print('File sent')
        self.sock.sendall(b'>sendingborder<')
        coords = str(self.startx) + ',' + str(self.endx)
        self.sock.sendall(coords.encode())
        self.sock.sendall(b'>endborder<')
        dat = self.sock.recv(1024)
        f = open('/tmp/{}{}'.format(str(self.threadID),'.png'),'wb')
        while True:
            f.write(dat)
            dat= self.sock.recv(1024)
            if dat.rfind(b'>EOF<') >=0:
                f.write(dat[:dat.rfind(b'>EOF<')])
                break
            if dat == b'':
                break
        self.sock.close()
        for prop in bpy.data.scenes[self.scene].MyServerProps:
            if prop.threadid == self.threadID:
                prop.isdone = True
        print("Connection done")
    def stop(self):
        self.stop_event.set()
    def stopped(self):
        return self.stop_event.is_set()


class RenderFile(bpy.types.Operator):
    bl_idname = 'object.render_file'
    bl_label = "Network render the file"
    bl_options = {"REGISTER"}
    def execute(self,context):
        print("Executing Network Render")
        self.timer = context.window_manager.event_timer_add(0.1, window=context.window)
        tcount = 0
        #Can't send a file if there is no file
        if (bpy.context.blend_data.filepath != ''):
            perc=0
            #We use counter to track the current index
            counter = 0
            autolist=[]
            if context.scene.LocalServerProp.doesrender is True:
                if context.scene.LocalServerProp.isauto is not True:
                    perc += context.scene.LocalServerProp.percentage

            for item in context.scene.MyServerProps:
                if item.isauto == False:
                    perc+=item.percentage
                #We first need to calculate the total percentage before dividing the remainder
                else:
                    autolist.append(counter)
                counter+=1
            if perc>100:
                self.report({'ERROR'}, 'Percentage total exceeds 100! Network render aborted')
                return{'CANCELLED'}
            if perc<100:
                if len(autolist) or context.scene.LocalServerProp.isauto is True:
                    autototal = len(autolist)
                    localauto = context.scene.LocalServerProp.isauto
                    if localauto is True:
                        autototal += 1
                    remperc = math.floor((100-perc)/autototal)
                    if localauto is True:
                        context.scene.LocalServerProp.percentage = remperc
                        perc+=remperc
                    for aut in autolist:
                        context.scene.MyServerProps[aut].percentage=remperc
                        perc+=remperc
                    if perc%100>0:
                        context.scene.MyServerProps[len(context.scene.MyServerProps)-1].percentage +=100%perc 
            lastxend = 0
            if context.scene.LocalServerProp.doesrender is True:
                context.scene.LocalServerProp.startx = lastxend
                context.scene.LocalServerProp.endx = lastxend + (context.scene.LocalServerProp.percentage/100)
                lastxend = context.scene.LocalServerProp.endx
            for item in context.scene.MyServerProps:
                item.isdone=False
                item.startx = lastxend
                item.endx = lastxend + (item.percentage/100)
                item.threadid = tcount
                lastxend = item.endx
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((item.ip_address,item.port))
                mythread = SendFile(tcount,"SendFilethread",s,item.startx,item.endx,context.scene.name)
                mythread.start()
                tcount+=1
            context.scene.render.use_border = True
            context.scene.render.border_min_x = context.scene.LocalServerProp.startx
            context.scene.render.border_max_x = context.scene.LocalServerProp.endx
            context.scene.render.use_crop_to_border = True
            bpy.ops.render.render(scene=context.scene.name,write_still=True)
            context.window_manager.modal_handler_add(self)
            return{'RUNNING_MODAL'}
        self.report({'Warning'}, 'No blend file found, network render aborted!')
        return{'CANCELLED'}

    def modal(self,context,event):
        counter = 0
        for item in context.scene.MyServerProps:
            if item.isdone is True:
                counter += 1
        if counter == len(context.scene.MyServerProps):
            newimg = Image.new('RGB',(int(context.scene.render.resolution_x*(context.scene.render.resolution_percentage/100)),int(context.scene.render.resolution_y*(context.scene.render.resolution_percentage/100))))
            currentpos = 0
            if context.scene.LocalServerProp.doesrender is True:
                ogimg = Image.open("{}{}".format(context.scene.render.filepath,context.scene.render.file_extension))
                newimg.paste(ogimg,(currentpos,0))
                currentpos+=ogimg.width
            for item in context.scene.MyServerProps:
                threadimg = Image.open("{}{}{}".format('/tmp/',item.threadid,context.scene.render.file_extension))
                newimg.paste(threadimg,(currentpos,0))
                currentpos+=threadimg.width
                item.isdone=False
            filepath = context.scene.render.filepath
            #PIL doesn't want to safe a file as just its extension, Linux uses / and Windows \ so we check if it ends on either of those to indicate there is no filename  
            if filepath[len(filepath)-1:] in "/\\":
                filepath+='output'
            fileloc = '{}{}'.format(filepath,context.scene.render.file_extension)
            print(fileloc)
            newimg.save(fileloc)
            bpy.ops.render.view_show('INVOKE_DEFAULT')
            AREA = 'IMAGE_EDITOR'
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if not area.type == AREA:
                        continue
                for s in area.spaces:
                    if s.type == AREA:
                        s.image=bpy.data.images.load(fileloc)
            return {'FINISHED'}
        return {'PASS_THROUGH'}