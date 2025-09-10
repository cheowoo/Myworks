from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import uvicorn
app = FastAPI()
cap = cv2.VideoCapture(0)  # 웹캠
def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.get("/video")
def video_feed():
    return StreamingResponse(generate_frames(),
                    media_type="multipart/x-mixed-replace; boundary=frame")
@app.get("/test")
def video_feedtest():
    return {"msg":"hi"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8500)