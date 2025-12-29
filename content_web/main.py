from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from datetime import datetime
from typing_extensions import Annotated
import uvicorn

db_connection = create_engine("mysql+pymysql://test:1234@localhost/test")
app = FastAPI()
templates= Jinja2Templates(directory="templates")
#게시판 목록 페이지 라우트
@app.get("/")
# 게시판 목록 페이지 라우트
@app.get("/")
async def list_contents(request: Request):
    # 데이터베이스에서 모든 게시글을 가져옴 (최신순 정렬)
    query = db_connection.execute("SELECT * FROM content ORDER BY c_id DESC")
    contents = query.fetchall()
    
    # 데이터베이스 결과를 딕셔너리 형태로 변환
    result = []
    for content in contents:
        temp = {
            'c_id': content[0],      # 게시글 ID
            'c_title': content[1],   # 게시글 제목
            'c_text': content[2],    # 게시글 내용
            'user_id': content[3],   # 작성자
            'date': content[4]       # 작성일
        }
        result.append(temp)
    
    # list.html 템플릿을 렌더링하여 응답
    return templates.TemplateResponse("list.html", {"request": request, "contents": result})
#게시글 작성 페이지 라우트
@app.get("/write")
async def write_form(request: Request):
    # write.html 템플릿을 렌더링하여 응답
    return templates.TemplateResponse("write.html", {"request": request})
#게시글 작성 처리 라우트
@app.post("/write")
async def write_content(
    request: Request,
    title: Annotated[str, Form()],      # 게시글 제목
    text: Annotated[str, Form()],       # 게시글 내용
    user_id: Annotated[str, Form()]     # 작성자
):
     # 현재 시간을 문자열로 변환
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 새 게시글을 데이터베이스에 저장
    db_connection.execute(
        "INSERT INTO content (c_title, c_text, user_id, date) VALUES (%s, %s, %s, %s)",
        (title, text, user_id, current_date)
    )
    
    # 작성 완료 메시지 반환
    return {"message": "Content created successfully"}
#게시글 상세 페이지 라우트
@app.get("/content/{content_id}")
async def content_detail(request: Request, content_id: int):
    # 특정 ID의 게시글을 데이터베이스에서 조회
    query = db_connection.execute("SELECT * FROM content WHERE c_id = %s", (content_id,))
    content = query.fetchone()
    
    # 게시글이 존재하지 않는 경우 404 에러 반환
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # 데이터베이스 결과를 딕셔너리 형태로 변환
    result = {
        'c_id': content[0],      # 게시글 ID
        'c_title': content[1],   # 게시글 제목
        'c_text': content[2],    # 게시글 내용
        'user_id': content[3],   # 작성자
        'date': content[4]       # 작성일
    }
    
    # detail.html 템플릿을 렌더링하여 응답
    return templates.TemplateResponse("detail.html", {"request": request, "content": result})
#게시글 삭제 라우트
@app.delete("/content/{content_id}")
async def delete_content(content_id: int):
    # 무턱대고 delete 날리는게 아니라 존재 확인 후 삭제
    #content_id = 1000 # 디버깅용
    query = db_connection.execute("SELECT * FROM content WHERE c_id=%s",(content_id,))
    content = query.fetchone()
    #print("test", content,type(content)) # 디버깅용
    # 게시글이 존재하지 않는 겨우 404 에러 반환
    if content is None:
        raise HTTPException(status_code = 404, detail="Content not found")

    # 게시글 삭제
    db_connection.execute("DELETE FROM content WHERE c_id = %s", (content_id,))
    return {"message": "Content deleted successfully"}

if __name__ == '__main__':
    uvicorn.run(app, host="localhost",port=8000)