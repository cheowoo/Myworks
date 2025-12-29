from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import uvicorn

app = FastAPI()

# 웹캠 객체 0의 의미는 0번째 카메라이다
cap = cv2.VideoCapture(0)

# url을 칠때마다 웹갬의 촬영된 프레임을 반환하는 함수
def generate_frames():
    while True:
        # 웹캠 객체로부터 프레임 1장을 읽어옴
        success, frame = cap.read()
        
        # 읽지 못했다면?
        if not success:
            break
        
        # 프레임을 이지미 인코더로 전달 할거임
        ret, buffer = cv2.imencode('.jpg', frame)
        
        # 바이트 타입
        frame = buffer.tobytes()
        
        # 여드(yield): 순차적 반환,
        # 문자열은 미디어 반환 양식이니.. 이해 or 압기 할 필요는 없다..
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@app.get("/video")
def video_feed():
            # 스트리밍으로 변환
    return StreamingResponse(generate_frames(),
                    media_type="multipart/x-mixed-replace; boundary=frame")
    
@app.get("/test")
def video_feedtest():
    return {"msg":"hi"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8600)