from tkinter import *
import serial
import glob

root = Tk()


def get_serial_ports_list():
    if sys.platform.startswith('win'):
        print(sys.platform.title())
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

root.geometry("%dx%d+%d+%d" % (300, 200, 30, 30))
label_serial = Label(root, text='Select Serial Port:').grid(row=0, sticky=W)
# label_serial.pack()
var = StringVar(root)
if ports:
    var.set(ports[0])
else:
    var.set('null')
    ports = ['null']

ports_list = OptionMenu(root, var, tuple(ports)).grid(row=0, column=1, sticky=W)
# ports_list.pack(side=LEFT)

ser = serial.Serial()


def open_port():
    ser.baudrate = 19200
    ser.port = var.get()
    ser.open()
    pass

if ser.is_open:
    connected = Label(root, text="Connected", fg='green')


    def request_temp():
        temp = ser.readline()
        temp_str = str(temp)
        return temp_str


    temp_label = Label(root, text=request_temp(), font="arial 14").grid(row=4)

else:
    connected = Label(root, text="Disconnected", fg='red')
    temp_label = Label(root, text="NULL", font="arial 14").grid(row=4)

connected.grid(row=1)
open_port_btn = Button(root, text="Open Port", command=open_port).grid(row=0, column=2)


def close_port():
    ser.close()
    pass


close_port_btn = Button(root, text="Close Port", command=close_port).grid(row=0, column=3)

root.mainloop()
