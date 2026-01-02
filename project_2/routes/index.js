const express = require('express');
const morgan = require('morgan');
const app = express();
const path = require('path');
const cors = require('cors');
const http = require('http');

app.set('PORT', process.env.PORT || 3000);

// 미들웨어 등록
app.use(morgan('dev'));
app.use(cors());
// body-parser 미들웨어
app.use(express.json());
app.use(express.urlencoded({extended: false}));
// serve-static 미들웨어
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.send('Hello Nodejs world!');
});

const server = http.createServer(app);
server.listen(app.get('PORT'), () => {
    console.log(`server started on http://localhost:${app.get('PORT')}`);
});