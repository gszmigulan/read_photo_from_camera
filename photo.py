from harvesters.core import Harvester
import cv2
import datetime
import ctypes
import os.path

PATH_TO_SAVE_PHOTO = "C:\\Users\gszmi\\"
PATH_TO_CTI = "C:\Program Files\MATRIX VISION\mvIMPACT Acquire\\bin\\x64\mvGenTLProducer.cti"

def get_date():
    today = datetime.date.today()
    d = today.strftime("%d/%m/%Y")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    date = str(d) + " " + str(current_time)
    d2 = today.strftime("%d-%m-%Y")
    current_time2 = now.strftime("%H-%M-%S")
    name = d2 + "_" + current_time2
    return str(date), str(name)

# main function uses Harvesters to connect my program with Matrix Vision cti software finds my Baluff camera nad
# connect it with my program. Program reads image from camera, adds date and save it as phot_day_time.
def main():
    h = Harvester()
    try:
        h.add_cti_file(PATH_TO_CTI)
        h.update_device_info_list()
        if len(h.device_info_list) == 0:
            ctypes.windll.user32.MessageBoxW(None, u"No camera detected. Please connect your camera.", u"Error", 0)
            exit(3)
        ia = h.create_image_acquirer(0) # it will use only first connected camera
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(None, u"Wrong path to .cti file.", u"Error", 0)
        exit(4)
    try:
        ia.start_image_acquisition()
        with ia.fetch_buffer() as buffer:
                img = buffer.payload.components[0].data
                img = img.reshape(buffer.payload.components[0].height, buffer.payload.components[0].width)
                date, name = get_date()
                cv2.putText(img, date, (30, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
                filename = PATH_TO_SAVE_PHOTO + "photo_" + name +".jpg"
                print(filename)
                cv2.imwrite(filename, img)

    except Exception as e:
        ctypes.windll.user32.MessageBoxW(None, u"Image acquisition error.", u"Error", 0)
        exit(5)
    finally:
        ia.stop_image_acquisition()
        ia.destroy()
        cv2.destroyAllWindows()
        h.reset()

if __name__ == "__main__":
    if os.path.isfile(PATH_TO_CTI) == False:
        ctypes.windll.user32.MessageBoxW(None, u"Path to cti: " + PATH_TO_CTI + " doesn't exist.", u"Error", 0)
        exit(1)
    if os.path.isdir(PATH_TO_SAVE_PHOTO) == False:
        ctypes.windll.user32.MessageBoxW(None, u"Path to photos directory: " + PATH_TO_SAVE_PHOTO + " doesn't exist.", u"Error", 0)
        exit(2)
    main()


