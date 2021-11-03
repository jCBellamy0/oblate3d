import tkinter as tk
import math
import os, sys
import time
#import tkFont
class DrawPad(tk.Canvas):
    def __init__(self, can):
        self.canvas=can
        self.abspath = ""
        self.checkboxstate = True
        self.omega = 0
        self.w = 0.0
        self.angle = 0
        self.r0 = 120
        self.r_eq = 120.0
        self.num_points = 0
        self.spectrum, self.spectrum1, self.spectrum2, self.spectrum3, self.spectrum4 = [], [], [], [], []
    def getSpectrum(self, s, hw_omega, ha_angle, angle_la, omega_lw, div, num):#adds spectrum data to spec array, returns spec array and num_points as tuple
        filestr = os.path.join(sys.path[0], s)
        self.num_points=0
        spec=[]
        k=0
        try:#sets up all spectrum arrays faster
            file = open(filestr, 'r')
            for line in file:
                val = int(300*float(line.strip()))
                spec.append(val)
                match num:
                    case 1:#bit hacky but should work in all cases
                        self.spectrum.append(float(val)*float(hw_omega)*float(ha_angle))
                    case 2:
                        self.spectrum[k]=(self.spectrum[k]+(float(val)*float(hw_omega)*float(angle_la)))
                    case 3:
                        self.spectrum[k]=(self.spectrum[k]+(float(val)*float(omega_lw)*float(ha_angle)))
                    case 4:
                        self.spectrum[k]=(int((self.spectrum[k]+(float(val)*float(omega_lw)*float(angle_la)))/div))
                k+=1
            file.close()
        except OSError as e:
            print("File unable to be read")
            raise
        return (spec,k)
    def inputPath(self, s):#path set function
        self.abspath = s
    def inputDoppler(self,b):#doppler set function
        if b==1:
            self.checkboxstate = True
        else:
             self.checkboxstate = False
        self.paint()
    def inputOmega(self,i):#omega set function
        self.omega=i
        self.w = 0.01*self.omega
        self.paint()
    def inputAngle(self,i):#angle set function
        self.angle=i
        self.paint()
    def paint(self):#redraws the image on canvas
        width = WIDTH*.95
        height = HEIGHT*.8
        h_offset=-100
        self.canvas.create_rectangle(0,0,width,height, fill='black')#black background, fix this for scaling in future
        #DRAWS STAR#
        if self.omega == 0:
            self.r_eq = 150.0
        else:
            self.r_eq = self.r0*(3.0/self.w)*math.cos((math.pi+math.acos(self.w))/3.0)
        if self.angle<6:#draws the star
            for ellipse in range(750):
                theta = math.pi - (math.pi*(ellipse/749.0))
                val=int(160*(1-math.pow(self.w,2)*math.pow(math.cos(2*theta),2))+95)
                if theta==0 or theta==math.pi or self.omega==0:
                    z = self.r0*math.cos(theta)*math.cos((self.angle*math.pi)/180.0)
                    x = self.r0*math.sin(theta)
                    minorAxis = 2*self.r0*math.sin(self.angle*math.pi/180.0)*math.sin(theta)
                    red = val
                    green = val
                    blue = 255
                    color_str = "#"+hex(red)[2:]+hex(green)[2:]+hex(blue)[2:]
                    self.canvas.create_oval((width/2)-x,(height/2)-z-(minorAxis/2)+h_offset,((width/2)-x)+(2*x),((height/2)-z-(minorAxis/2))+(minorAxis+1)+h_offset,fill="", outline=color_str)
                else:
                    color_str=""
                    r = self.r0*(3.0/(self.w*math.sin(theta)))*math.cos((math.pi+math.acos(self.w*math.sin(theta)))/3.0)
                    z = r*math.cos(theta)*math.cos(self.angle*math.pi/180.0)
                    x = r*math.sin(theta)
                    red,blue,green=0,0,0
                    minorAxis = 2*r*math.sin(self.angle*math.pi/180.0)*math.sin(theta)
                    if theta <= math.pi/4:
                        red = val
                        green = val
                        blue = 255
                    elif theta>math.pi/4 and theta<=3*math.pi/4:
                        red = 255
                        green = val
                        blue = val
                    elif theta>3*math.pi/4 and theta<=math.pi:
                        red = val
                        green = val
                        blue = 255
                    color_str = "#"+hex(red)[2:]+hex(green)[2:]+hex(blue)[2:]
                    self.canvas.create_oval((width/2)-x, (height/2)-z-(minorAxis/2)+h_offset, ((width/2)-x)+(2*x),((height/2)-z-(minorAxis/2))+(minorAxis+1)+h_offset, outline=color_str)
        else:
            for i in range(150):
                theta=math.pi-(math.pi*(i/149.0))
                val=int(160*(1-math.pow(self.w,2)*math.pow(math.cos(2*theta),2))+95)
                if theta==0 or theta == math.pi or self.omega==0:
                    z = self.r0*math.cos(theta)*math.cos((self.angle*math.pi)/180.0)
                    x = self.r0*math.sin(theta)
                    minorAxis = 2*self.r0*math.sin(self.angle*math.pi/180.0)*math.sin(theta)
                    red = val
                    green = val
                    blue = 255
                    color_str = "#"+hex(red)[2:]+hex(green)[2:]+hex(blue)[2:]
                    self.canvas.create_oval((width/2)-x,(height/2)-z-(minorAxis/2)+h_offset,((width/2)-x)+(2*x),((height/2)-z-(minorAxis/2))+(minorAxis+1)+h_offset,fill=color_str, outline=color_str)
                else:
                    color_str=""
                    r = self.r0*(3.0/(self.w*math.sin(theta)))*math.cos((math.pi+math.acos(self.w*math.sin(theta)))/3.0)
                    z = r*math.cos(theta)*math.cos(self.angle*math.pi/180.0)
                    x = r*math.sin(theta)
                    minorAxis = 2*r*math.sin(self.angle*math.pi/180.0)*math.sin(theta)
                    if theta <= math.pi/4:
                        red = val
                        green = val
                        blue = 255
                        color_str = "#"+hex(red)[2:]+hex(green)[2:]+hex(blue)[2:]
                    elif theta>math.pi/4 and theta<=3*math.pi/4:
                        red = 255
                        green = val
                        blue = val
                        color_str = "#"+hex(red)[2:]+hex(green)[2:]+hex(blue)[2:]
                    elif theta>3*math.pi/4 and theta<=math.pi:
                        red = val
                        green = val
                        blue = 255
                        color_str = "#"+hex(red)[2:]+hex(green)[2:]+hex(blue)[2:]
                    self.canvas.create_oval((width/2)-x, (height/2)-z-(minorAxis/2)+h_offset, ((width/2)-x)+(2*x),((height/2)-z-(minorAxis/2))+(minorAxis+1)+h_offset,fill=color_str, outline=color_str)
        #DRAWS TEXT W/ TEMPERATURES, % CRIT ANGULAR VELOCITY, AND R(eq)/R(pole)
        rProj = int(self.r0*math.cos(self.angle*math.pi/180.0))
        temp0 = 30000
        tempPole = 30000
        if self.omega==0:
            self.canvas.create_text((width/2)-30, (height/2)-rProj-25+h_offset, text=str(temp0)+" K", fill='blue', anchor=tk.W)
        elif self.omega>0 and self.omega<98:
            intgrl = 1.5708-.01744*self.w-.52352*math.pow(self.w,2)-5.66985*math.pow(self.w,3)+35.37376*math.pow(self.w,4)-131.58148*math.pow(self.w,5)+311.41246*math.pow(self.w,6)-469.19815*math.pow(self.w,7)+436.73393*math.pow(self.w,8)-228.96826*math.pow(self.w,9)+51.77397*math.pow(self.w,10)
            tempPole =  int(math.pow(((math.pi/2*math.pow(temp0,4))/intgrl),0.25))
            self.canvas.create_text((width/2)-30, (height/2)-rProj-25+h_offset, text=str(tempPole)+" K", fill='blue', anchor=tk.W)
        elif self.omega==98:
            tempPole =  int(math.pow(((math.pi/2*math.pow(temp0,4))/0.90292),0.25))
            self.canvas.create_text((width/2)-30, (height/2)-rProj-25+h_offset, text=str(tempPole)+" K", fill='blue', anchor=tk.W)
        elif self.omega==99:
            tempPole =  int(math.pow(((math.pi/2*math.pow(temp0,4))/.91078),0.25))
            self.canvas.create_text((width/2)-30, (height/2)-rProj-25+h_offset, text=str(tempPole)+" K", fill='blue', anchor=tk.W)
        elif self.omega==100:
            tempPole =  int(math.pow(((math.pi/2*math.pow(temp0,4))/.95661),0.25))
            self.canvas.create_text((width/2)-30, (height/2)-rProj-25+h_offset, text=str(tempPole)+" K", fill='blue', anchor=tk.W)
        self.canvas.create_text(10,20,text="Percent critical angular velocity = "+str(self.omega)+"%", fill='blue', anchor=tk.W)
        if self.omega==0:
            y=1.0
            self.canvas.create_text(10,40,text="R(equator)/R(pole) = "+str(y), fill='blue', anchor=tk.W)
            self.canvas.create_text(width/2 + self.r0 + 19, height/2+h_offset, text=str(temp0)+" K", fill='blue',anchor=tk.W)
        else:
            y=float(self.r_eq/self.r0)
            self.canvas.create_text(10,40,text="R(equator)/R(pole) = "+str(y), fill='blue', anchor=tk.W)
            temp = int(math.pow((math.pow(tempPole,4)*math.pow((self.r0/self.r_eq),2)*(1-math.pow(self.w,2))),0.25))
            self.canvas.create_text(width/2 + self.r0 + 19, height/2+h_offset, text=str(temp)+" K", fill='blue', anchor=tk.W)
        #RETRIEVES SPECTRUM DATA AND DRAWS SPECTRUM
        if self.omega<=96:
            lw=110
            hw=110
            for i in range(10):
                loww=i*10
                highw=(i+1)*10
                if self.omega<=highw and self.omega>=loww:
                    if lw==110 and hw==110:
                        lw=loww
                        if highw == 100:
                            hw=96
                        else:
                            hw=highw

            la = 100
            ha = 100
            for i in range(9):
                lowa = i*10
                higha = (i+1)*10
                if self.angle <= higha and self.angle >= lowa:
                    if la == 100 and ha == 100:
                        la = 90-lowa
                        ha = 90-higha

            lowt=30000
            hight=30195
            if lw==0:
                lowt=temp0
            else:
                l = .01*lw
                intgrlLow = 1.5708-.01744*l-.52352*math.pow(l,2)-5.66985*math.pow(l,3)+35.37376*math.pow(l,4)-131.58148*math.pow(l,5)+311.41246*math.pow(l,6)-469.19815*math.pow(l,7)+436.73393*math.pow(l,8)-228.96826*math.pow(l,9)+51.77397*math.pow(l,10)
                lowt= int(math.pow(((math.pi/2*math.pow(temp0,4))/intgrlLow),0.25))
            if hw==100:
                hight=int(math.pow(((math.pi/2*math.pow(temp0,4))/.95661),0.25))
            else:
                h = .01*hw
                intgrlHigh = 1.5708-.01744*h-.52352*math.pow(h,2)-5.66985*math.pow(h,3)+35.37376*math.pow(h,4)-131.58148*math.pow(h,5)+311.41246*math.pow(h,6)-469.19815*math.pow(h,7)+436.73393*math.pow(h,8)-228.96826*math.pow(h,9)+51.77397*math.pow(h,10)
                hight=int(math.pow(((math.pi/2*math.pow(temp0,4))/intgrlHigh),0.25))
            specFileLowla=""
            specFileLowha=""
            if lw==0:
                specFileLowla="T"+str(lowt)+"G400W00"+str(lw)+"A"+str(la)
                specFileLowha="T"+str(lowt)+"G400W00"+str(lw)+"A"+str(ha)
            else:
                specFileLowla="T"+str(lowt)+"G400W0"+str(lw)+"A"+str(la)
                specFileLowha="T"+str(lowt)+"G400W0"+str(lw)+"A"+str(ha)
            specFileHighla="T"+str(hight)+"G400W0"+str(hw)+"A"+str(la)
            specFileHighha="T"+str(hight)+"G400W0"+str(hw)+"A"+str(ha)

            la=90-la
            ha=90-ha
            specdir=""
            if self.checkboxstate==False:
                specdir="spectrum2/"
            else:
                specdir="spectrum/"
            self.spectrum, self.spectrum1, self.spectrum2, self.spectrum3, self.spectrum4 = [], [], [], [], []
            temp_num1, temp_num2, temp_num3, temp_num4=0,0,0,0
            hw_omega=float(hw-self.omega)
            ha_angle=float(ha-self.angle)
            angle_la=float(self.angle-la)
            omega_lw=float(self.omega-lw)
            div=float(hw-lw)*float(ha-la)
            #retrives spectrum data and writes it to arrays
            (self.spectrum1,temp_num1)=self.getSpectrum(self.abspath+specdir+specFileLowla,hw_omega,ha_angle,angle_la,omega_lw,div,1)
            (self.spectrum2,temp_num2)=self.getSpectrum(self.abspath+specdir+specFileLowha,hw_omega,ha_angle,angle_la,omega_lw,div,2)
            (self.spectrum3,temp_num3)=self.getSpectrum(self.abspath+specdir+specFileHighla,hw_omega,ha_angle,angle_la,omega_lw,div,3)
            (self.spectrum4,temp_num4)=self.getSpectrum(self.abspath+specdir+specFileHighha,hw_omega,ha_angle,angle_la,omega_lw,div,4)
            if(temp_num1<temp_num2):
                self.num_points=temp_num1
            else:
                self.num_points=temp_num2
            if(temp_num3<self.num_points):
                self.num_points=temp_num3
            if(temp_num4<self.num_points):
                self.num_points=temp_num4
            x_offset=(width-self.num_points)-300
            y_offset=80
            #draws the spectrum
            for i in range(self.num_points-2):
                self.canvas.create_line(x_offset+i, 700-self.spectrum[i]+y_offset, x_offset+(i+1),700-self.spectrum[i+1]+y_offset, fill='white')
            #draws text indicating the helium absorption lines
            self.canvas.create_text(x_offset+int((21/110.0)*self.num_points)-10, 378+y_offset, text="He I", fill='white')
            self.canvas.create_text(x_offset+int((21/110.0)*self.num_points)-14, 390+y_offset, text="4471", fill='white')
            self.canvas.create_text(x_offset+int((91/110.0)*self.num_points)-10, 378+y_offset, text="He II", fill='white')
            self.canvas.create_text(x_offset+int((91/110.0)*self.num_points)-12, 390+y_offset, text="4541", fill='white')
            #draws axis and labels
            self.canvas.create_line(x_offset-3,400+y_offset,x_offset-3,580+y_offset, fill="white")
            self.canvas.create_text(x_offset-15,405+y_offset,text="1",fill='white')
            self.canvas.create_text(x_offset-20,555+y_offset,text=".5",fill="white")
            for i in range(7):
                mark=400+(30*i)
                self.canvas.create_line(x_offset-6, mark+y_offset, x_offset-3, mark+y_offset, fill="white")
        else:
            self.canvas.create_text((width/2)-75,(3*height)/4,text="Spectrum not available",fill='white')

def change_omega(event):#functions for when inputs change
    draw.inputOmega(scl_1_var.get())
def change_angle(event):
    draw.inputAngle(scl_2_var.get())
def change_doppler():
    draw.inputDoppler(check_var.get())
root=tk.Tk()
global WIDTH
global HEIGHT
WIDTH = root.winfo_screenwidth()#window/frame setup
HEIGHT = root.winfo_screenheight()
can = tk.Canvas(root,width=WIDTH*.95,height=HEIGHT*.8)
draw = DrawPad(can)
can.grid(row=0, column=0)
frm_p1 = tk.Frame(master=root)
frm_p2 = tk.Frame(master=root)
lbl_p1 = tk.Label(master=frm_p1, text="Percent critical angular velocity")
lbl_p2 = tk.Label(master=frm_p2, text="Viewing angle")
lbl_p1.pack()
lbl_p2.pack()
check_var=tk.IntVar()
scl_1_var=tk.IntVar()
scl_2_var=tk.IntVar()
scl_1 = tk.Scale(master=frm_p1, from_=0, to_=100, orient=tk.HORIZONTAL, tickinterval=10, length=0.94*WIDTH, variable=scl_1_var, command=change_omega, repeatdelay=10, repeatinterval=5)
checkbox = tk.Checkbutton(master=root, variable=check_var, command=change_doppler)
scl_2 = tk.Scale(master=frm_p2, from_=90, to_=0, orient=tk.VERTICAL, tickinterval=10, length=0.80*HEIGHT, variable=scl_2_var, command=change_angle)
scl_1.pack(side=tk.TOP)
scl_2.pack(side=tk.RIGHT)
frm_p1.grid(row=1,column=0)
frm_p2.grid(row=0,column=1)
checkbox.grid(row=1,column=1)
root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(1,weight=1)
root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=1)
draw.paint()

root.mainloop()
