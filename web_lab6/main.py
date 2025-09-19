from fastapi import FastAPI, Request 
from fastapi.templating import Jinja2Templates 
import uvicorn 
from typing_extensions import Annotated
from fastapi import Form

templates = Jinja2Templates(directory = "templates")

app = FastAPI()

@app.get("/page") 
def test(request : Request):
      return templates.TemplateResponse("test.html", context = {"request": request})



@app.post("/signup")
def test_post(request:Request, uid:Annotated[str,Form()], pwd :Annotated[str,Form()],name :Annotated[str,Form()],gender :Annotated[str,Form()],
              email :Annotated[str,Form()]):
     print(uid,pwd,name,gender,email)





if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000) #웹서버 실행