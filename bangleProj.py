# import the opencv library
import cv2
from ultralytics import YOLO


vid = cv2.VideoCapture(r"D:\chrome download\Broken Bangles).mp4")

# model load

model = YOLO("bangel.pt")


def bangle_detect(IMAGE):

    data = {"rect": "", "score": "","names":""}

    result = model.predict(IMAGE)
    
    print("***************************************************************************",result)

    result = result[0]

    rect_list = result.boxes.xyxy

    score = result.boxes.conf
    
    name=result.names

    data["rect"] = rect_list

    data["score"] = score
    
    data["names"] = name

    return data


while True:

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # model prediction

    data = bangle_detect(IMAGE=frame)

    print("----------")

    if len(data["rect"]) > 0:

        for sublist in data["rect"]:
            x1, y1, x2, y2 = (
                int(sublist[0]),
                int(sublist[1]),
                int(sublist[2]),
                int(sublist[3]),
            )

            ####### Drawing rectangel

            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            
            #circle
            
            cx=int((x1+x2)/2)
            #cx=int(x2/2)
            cy=int((y1+y2)/2)
            #cy=int(y2/2)
            cv2.circle(frame,center=(cx,cy),radius=(50),color=(0,255,0),thickness=-1)
            
            
            
        if data["names"]==0:
            name="good"
        else:
            name="broken" 
                   
            #text
            cv2.putText(frame, text=name, org=(100,100), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale= 4,
            color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)

    else:
        print("no bangle detected.....")

    print("----------")

    print("***********************", data["score"], "*********************")

    # Display the resulting frame

    cv2.imshow("color image", frame)

    if cv2.waitKey(1) & 0xFF == ord("x"):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()