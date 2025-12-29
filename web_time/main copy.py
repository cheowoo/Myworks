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

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class LSTMModel(nn.Module):
    
# 모델 불러오기
model = LSTMModel(input_size=4, hidden_size=64, num_layers=2, output_size=14)
model.load_state_dict(torch.load("lstm_stock_forecast.pt", map_location=torch.device("cpu")))
model.eval()

# 입력 시퀀스 생성
def create_input_sequence(df, seq_len=60):

    return input_seq, y, scaler_y

def generate_two_plots():


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
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
