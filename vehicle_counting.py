import cv2
import glob
from vehicle_detector import VehicleDetector
length_min = 80
height_min = 80
offset = 6  #
pos_linha = 500

delay = 10  # FPS do vídeo

detec = []
car_ros = 0
car_down=0


def pega_centro_1(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# Load Veichle Detector
vd = VehicleDetector()



vehicles_folder_count = 0
cap=cv2.VideoCapture("video.mp4")
# Loop through all the images
while True:
    ret,img=cap.read()


    vehicle_boxes = vd.detect_vehicles(img)
    vehicle_count = len(vehicle_boxes)

    # Update total count
    vehicles_folder_count += vehicle_count
    cv2.line(img, (25, pos_linha), (1200, pos_linha), (0, 127, 0), 3)
    for box in vehicle_boxes:
        x, y, w, h = box

        cv2.rectangle(img, (x, y), (x + w, y + h), (25, 0, 180), 1)

        ##cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        centro = pega_centro_1(x, y, w, h)
        detec.append(centro)
        cv2.circle(img, centro, 4, (0, 0, 255), -1)
        print(detec)
        for (x, y) in detec:
            if y < (pos_linha + offset) and y > (pos_linha - offset) and x<40: ## centroid range for IN
                car_ros += 1
                cv2.line(img, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
                detec.remove((x, y))
                print("car is detected : " + str(car_ros))
            elif y < (pos_linha + offset) and y > (pos_linha - offset) and x>40 and x<=100:  ## centroid range for OUT
                car_down += 1
                cv2.line(img, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
                detec.remove((x, y))
                print("car goin out is detected : " + str(car_down))



        cv2.putText(img, "Vehicles: " + str(vehicle_count), (20, 50), 0, 0.8, (100, 200, 0), 3)

        cv2.putText(img, "Vehicles cost: " + str(vehicle_count*15), (20, 100), 0, 0.8, (00, 00, 255), 3)

    cv2.imshow("Cars", img)
    cv2.waitKey(1)
cost=vehicle_count*15
print("Total current count", vehicles_folder_count)
print("Total cost", cost)


cv2.destroyAllWindows()
cap.release()