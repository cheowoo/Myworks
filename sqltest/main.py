from sqlalchemy import create_engine
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
import uvicorn

templates =Jinja2Templates(directory="templates")
app = FastAPI()

#db커넥터 객체                       #db종류 + 커넥터 : //db아이디:비번@아이피/데이터베이스명
db_con = create_engine("mysql+pymysql://test:1234@localhost/test")
#             #excute : 쿼리날리기
# query = db_con.execute("select * from player")
#             #결과 가져오기
# result = query.fetchall()

# for data in result:  #결과 for문 돌리면서 언팩킹
#     print (data)

@app.get("/detail")
def detailget(request :Request, id :str , name:str):
    query = db_con.execute(f"select * from player where player_id = {id} and player_name like '{name}' ")
    result_db = query.fetchall()
    result = []
    for data in result_db:
        temp = {"player_id":data[0], 'player_name':data[1],'team_name':data[2],'height':data[-2],'weight':data[-1]}
        result.append(temp)
    return templates.TemplateResponse("detail.html",{'request':request,'result_table':result})

@app.get("/mysqltest")
def mysqltest(request:Request):
    query = db_con.execute("select * from player")
    result_db = query.fetchall()

    result = []
    for data in result_db:
        temp = {'player_id':data[0], 'player_name':data[1]}
        result.append(temp)
    #print(result)
    return templates.TemplateResponse("sqltest.html",{'request':request,'result_table':result})

from typing_extensions import Annotated
from fastapi import Form
@app.post("/update")
def post_update(request:Request, id:str, name:str, pname:Annotated[str,Form()],
                                                   tname:Annotated[str,Form()],
                                                   weight:Annotated[str,Form()],
                                                   height:Annotated[str,Form()]):
    if pname !='':
        db_con.execute("update player set player_name = '{}' where player_id = {} and player_name like '{}'".format(pname,id,name))
    if tname !='':
        db_con.execute("update player set team_id = '{}' where player_id = {} and player_name like '{}'".format(tname,id,name))                   
    if weight !='':
        db_con.execute("update player set weight = {} where player_id = {} and player_name like '{}'".format(weight,id,name))
    if height !='':
        db_con.execute("update player set height = {} where player_id = {} and player_name like '{}'".format(height,id,name))  

        query = db_con.execute(f"select * from player where player_id = {id} and player_name like '{name}'")
        result_db = query.fetchall()
        result = []
        for data in result_db:
            temp = {'player_id':data[0],
                    'player_name':data[1],
                    'team_name':data[2],
                    'height':data[-2],
                    'weight':data[-1],}
            result.append(temp)

        return templates.TemplateResponse("detail.html",{'request':request,'result_table':result})    
            
@app.get("/delete")
def deleteget(request :Request, id :str , name:str):
    db_con.execute(f"delete from player where player_id = {id} and player_name like '{name}'")

    query = db_con.execute("select * from player")
    result_db = query.fetchall()
    result = []

    for data in result_db:
        temp = {"player_id" : data[0],'player_name':data[1]}
        result.append(temp)
    return templates.TemplateResponse("sqltest.html",{'request':request,'result_table':result}) 


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)