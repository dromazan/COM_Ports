from tkinter import *
import serial
import glob

from dask.compatibility import apply

root = Tk()

portstate = "Disconnected"


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
label_serial = Label(root, text='Select Serial Port:').grid(row=0, column=0)
#label_serial.pack()
var = StringVar(root)
if ports:
    var.set(ports[0])
else:
    var.set('null')
    ports=['null']
ports_list = apply(OptionMenu, (root, var) + tuple(ports))
ports_list.grid(row=0, column=1)

ser = serial.Serial()

Label(root, text="Disconnected", fg='red').grid(row=1, column=1)


def set_port_state_label(state):
    if state == "Connected":
        Label(root, text=state, fg='green').grid(row=1, column=1)
    else:
        Label(root, text=state, fg='red').grid(row=1, column=1)


def open_port():
    ser.baudrate = 19200
    ser.port = var.get()
    ser.open()
    if ser.is_open:
        print(var.get()+" is opened")
        set_port_state_label("Connected")
    pass


open_btn = Button(root, text="Open port", command=open_port).grid(row=0,column=2)
#open_btn.pack()


def close_port():
    if ser.is_open:
        ser.close()
        print(var.get()+" closed")
        set_port_state_label("Disconnected")
    else:
        print("port is not opened")
    pass


close_btn = Button(root, text="Close port", command=close_port).grid(row=0, column=3)
#close_btn.pack()

state = Label(root, text="Port state: ").grid(row=1)


def read_port_value():
    if ser.is_open:
        portval = ser.readline()
        print(portval)

    else:
        portval = "null"
        print(portval)
    return portval

port_val = Button(root, text="Read port", command=read_port_value).grid(row=2, column=0)
#port_val.pack()

root.mainloop()
