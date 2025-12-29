from sqlalchemy import create_engine
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
import uvicorn

templates = Jinja2Templates(directory = "templates")
app = FastAPI()

db_con = create_engine("mysql+pymysql://test:1234@localhost/test")

@app.get("/mysqltest")
def mysqltest(request:Request):
    query = db_con.execute("select * from player")
    result_db=query.fetchall()

    result = []
    for data in result_db:
        temp = {'player_name':data[1],'HEIGHT' :data[-2], 'WEIGHT' : data[-1]}
        result.append(temp)
    return templates.TemplateResponse("index.html",{'request':request,'result_table': result})

if __name__ == '__main__':
    uvicorn.run(app, host="localhost",port = 8000)    