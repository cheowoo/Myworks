from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import FinanceDataReader as fdr
import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import uvicorn
import os

#fastapi 객체
app = FastAPI()
templates = Jinja2Templates(directory="templates")

#우리 학습 pt에 맞는 lstm 클래스
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

# 모델 불러오기
model = LSTMModel(input_size=4, hidden_size=64, num_layers=2, output_size=14)
model.load_state_dict(torch.load("lstm_stock_forecast.pt", map_location=torch.device("cpu")))
model.eval()

# 입력 시퀀스 생성
def create_input_sequence(df, seq_len=60):
    X = df[['Open', 'High', 'Low', 'Volume']].values
    y = df['Close'].values
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

    input_seq = X_scaled[-seq_len:]
    input_seq = torch.FloatTensor(input_seq).unsqueeze(0)  # [1, 60, 4]
    return input_seq, y, scaler_y

def generate_two_plots():
    today = datetime.today()
    start = today - timedelta(days=90)
                                                    #90일전                             #오늘까지
    df = fdr.DataReader('005930', start=start.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
    df = df[['Open', 'High', 'Low', 'Volume', 'Close']].dropna()

    if len(df) < 60:
        return None, None

    input_seq, y_actual, scaler_y = create_input_sequence(df)
    with torch.no_grad():
        pred = model(input_seq).cpu().numpy()
    pred = scaler_y.inverse_transform(pred)[0]

    # 1. 예측 시계열 그래프
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(range(len(y_actual)-14), y_actual[:-14], label='Actual', color='blue')
    ax1.plot(range(len(y_actual)-14, len(y_actual)), pred, label='Predicted', color='orange')
    ax1.set_title("Samsung 14-Day Price Prediction")
    ax1.legend()
    ax1.grid(True)
    plt.tight_layout()
    buf1 = io.BytesIO() # 메모리 내 임시 버퍼 생성 (파일 저장 없이 이미지 저장 가능)
    plt.savefig(buf1, format="png") # 그래프를 PNG 형식으로 버퍼에 저장
    buf1.seek(0) # 버퍼의 시작 위치로 이동 (읽기 준비)
    pred_chart = base64.b64encode(buf1.read()).decode('utf-8') # 이미지를 base64로 인코딩하여 웹에서 <img>로 렌더 가능하게 함
    plt.close()

    # 2. 박스플롯
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.boxplot([df[col] for col in ['Open', 'High', 'Low', 'Close']],
                labels=['Open', 'High', 'Low', 'Close'], patch_artist=True)
    ax2.set_title("OHLC Box Plot (60 Trading Days)")
    ax2.grid(True)
    plt.tight_layout()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format="png")
    buf2.seek(0)
    box_chart = base64.b64encode(buf2.read()).decode('utf-8')
    plt.close()

    return pred_chart, box_chart



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    pred_chart, box_chart = generate_two_plots()
    if pred_chart is None or box_chart is None:
        return HTMLResponse(content="데이터가 부족합니다.", status_code=400)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "pred_chart": pred_chart,
        "box_chart": box_chart
    })
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
