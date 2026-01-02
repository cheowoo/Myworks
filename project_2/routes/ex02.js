const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.type('html').send(`
        <h2>ex02 서브 모듈!</h2>
        <p><a href="/">홈으로</a></p>
    `);
});

// 모듈에 서브 모듈 등록
module.exports = router;