from tkinter import *
import serial
import glob

root = Tk()

def get_serial_ports_list():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


ports = get_serial_ports_list()
print(ports)

root.geometry("%dx%d+%d+%d" % (330, 200, 200, 150))
label_serial = Label(root, text='Select Serial Port:')
label_serial.pack()
var = StringVar(root)
if ports:
    var.set(ports[0])
else:
    var.set('null')
    ports=['null']
ports_list = OptionMenu(root, var, ports)
ports_list.pack()

ser = serial.Serial()


def open_port():
    ser.baudrate = 19200
    ser.port = var.get()
    ser.open()
    if ser.is_open:
        print(var.get()+" is opened")
    pass


open_btn = Button(root, text="Open port", command=open_port)
open_btn.pack()


def close_port():
    if ser.is_open:
        ser.close()
        print(var.get()+" closed")
    else:
        print("port is not opened")
    pass


close_btn = Button(root, text="Close port", command=close_port)
close_btn.pack()


def read_port_value():
    if ser.is_open:
        portval = ser.readline()
        print(portval)

    else:
        portval = "null1"
        print(portval)
    return portval

port_val = Button(root, text="Read port", command=read_port_value)
port_val.pack()

port_val_label = Label(root, textvariable=read_port_value)
port_val_label.pack()


root.mainloop()
