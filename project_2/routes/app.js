const http = require('http');
const express = require('express');
const app = express();
const path = require('path'); // 기본 모듈
const fs = require('fs'); // 기본 모듈

app.set('port', 3000);

// 파일을 동깃식 IO로 읽어 들이기
var data = fs.readFileSync('./package.json', 'utf8');  // 파일 읽기 작업 수행 전까지는 다음 과정 진행 안됨.

// 파일을 다 읽으면 읽은 데이터 출력.
console.log(data);

const server = http.createServer(app);
server.listen(app.get('port'), () =>{
    console.log(`Run on server, http://localhost:${app.get('port')}`);
});