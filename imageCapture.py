
from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
from gpiozero import Button
from signal import pause

# Kill the gphoto process that starts
# whenever we turn on the camera or
# reboot the raspberry pi

def killGphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    # Search for the process we want to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            # Kill that process!
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime("%Y-%m-%d") # This has been written to the while True loop.
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # This has been written to the while True loop.
picID = "PiShots"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON", \
                "--delete-all-files", "-R"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/Desktop/gphoto/images/" + folder_name
                                                                                                    
def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create new directory.")
    os.chdir(save_location)

def captureImages():
    p = subprocess.Popen(['gphoto2', '--list-ports'], stdout=subprocess.PIPE)
    print(p)
    out, err = p.communicate()

    for line in out.splitlines():
        if b'usb:001' in line:  
            portName = (line.split(None,1)[0])
            print(portName)
            portName = portName.decode('utf-8')
            print(portName)
            triggerPort = "--port=" + portName
            print(triggerPort)
            triggerCommand = [triggerPort, "--trigger-capture"]
            print(triggerCommand)
            gp(triggerCommand)
            sleep(1)
            downloadCommand = [triggerPort ,"--get-all-files"]
            gp(downloadCommand)
            clearCommand = [triggerPort ,"--folder", "/store_00020001/DCIM/100CANON", \
                "--delete-all-files", "-R"]
            gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (filename + " " + shot_time + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".CR2"):
                os.rename(filename, (filename + " " + shot_time + ".CR2"))
                print("Renamed the CR2")




def cameraButtonTrigger():
    print("Program Triggered")
    killGphoto2Process()
    gp(clearCommand)
    createSaveFolder()
    captureImages()
    renameFiles(picID)

button = Button(2)

button.when_pressed = cameraButtonTrigger

pause()
