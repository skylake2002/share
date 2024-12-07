import cv2
import webbrowser
import torch
import pathlib
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# PosixPath를 WindowsPath로 변경
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
# 커스텀 YOLO 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r"C:\Users\skyla\Desktop\Yolo_FoodDeteced-main\best.pt", force_reload=True)

# 아두이노 카메라에서 실시간으로 스트리밍하는 영상 받아오기
url = 'http://192.168.35.149:81/stream'  # ESP32 카메라 IP 주소로 변경

# OpenCV로 MJPEG 스트리밍 캡처
cap = cv2.VideoCapture(url)

webbrowser.open(url, new=2)

# 스트리밍 연결 확인
if not cap.isOpened():
    print("스트리밍 연결 안됨.")
    exit()

# 잔반 객체가 포함된 클래스 ID (예시: 음식을 클래스 ID로 할당한 후 사용)
# YOLOv5 모델에서 각 클래스 ID는 [0, 1, 2, ..., n] 형식으로 할당됨
# '0'은 예시로 사용
food_class_id = 0

while cap.isOpened:
    # 실시간 영상 캡처
    ret, frame = cap.read()
    # 혹시 모를 오류가 발생하면 오류 메시지 출력
    if not ret:
        print("프레임 캡처 실패")
        break
 
    # YOLOv5 모델을 이용하여 객체 탐지
    results = model(frame)


    for *box, conf, cls in results.xyxy[0]:
        label = f'{model.names[int(cls)]} {conf:.2f}'
        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
        cv2.putText(frame, label, (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    # 화면에 실시간 출력
    cv2.imshow("VOLOv5 Detetion", frame)

    # 탐지된 객체의 클래스를 리스트로 가져오기
    detected_classes = results.xywh[0][:, -1].cpu().numpy()

    # 음식을 여러 개 탐지된 경우
    food_detected = sum(detected_classes == food_class_id)

    if food_detected > 1:
        print("경고: 여러 그릇에 잔반이 담겨 있습니다!")
        # 잔반이 여러 개 탐지되었을 때 경고 메시지 출력
        # 경고 음성 메시지를 아두이노로 전송 - 아두이노에서 잔반을 모아달라고 하는 음성 메시지 출력

    # 'q'를 눌러서 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# 캡처 종료
cap.release()
cv2.destroyAllWindows()
