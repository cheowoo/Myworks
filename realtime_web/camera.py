from ultralytics import YOLO
import cv2
import math

# pretrain된 yolov8 small 모델을 model변수에 정의.
model = YOLO('yolov8n.pt')

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                    "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                    "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                    "teddy bear", "hair drier", "toothbrush"
                    ]



class VideoCamera(object):
    def __init__(self):
                    #웹캠 프레임을 가져올때 쓰는 비디오객체 인자에 넣는 숫자는 몇번째 웹캠이냐
        
        win_ip = "192.168.200.189"
        stream_url = f"http://{win_ip}:8600/video"
        self.video = cv2.VideoCapture(stream_url)

    def __del__(self):
        self.video.release()
    
    def get_frame(self): # 객체탐지 결과 프레임을 반환하는 함수
                        # VideoCapture에서 read 내장함수를 호출해야만 실시간 프레임 1장을 가져온다. 
        success, image = self.video.read()

                 #모델에다가 실시간 프레임을 때려박음.
        results = model(image, stream=True)

        # model에 1장을주면 results는 길이가 1, model에게 2장을 주면 results는 길이가 2
        for r in results:
            # 프레임 1장에 있는 객체 객수 만큼 bbox가 있을 거다.
            boxes = r.boxes
            for box in boxes: # bbox 하나하나 정성들여서 이미지에 drawing 할거다.
                # bounding box에 bbox의 좌표가 들어있다. 
                x1, y1, x2, y2 = box.xyxy[0]

                # int 타입으로 변환. 
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
                # 이미지에 box 정보 넣기
                # image 즉, 프레임에다가 바운딩박스를 그리는데,(255, 0, 255) 색깔로 draw하고, 2 line width  
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 2)
                # 예측 클래스 confidence
                confidence = math.ceil((box.conf[0]*100))/100
                # 예측 클래스 이름
                cls = int(box.cls[0])
                # 텍스트 정보
                org = [x1, y1-10]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                cv2.putText(image, classNames[cls]+" "+str(confidence), org, font, fontScale, color, thickness)
                
                # image 즉, 텍스트와 바운딩 박스가 draw된 상태로 jpg 인코딩으로 반환함. 
        return cv2.imencode('.jpg', image)[1].tobytes()