const express = require('express');
const router = express.Router();

const todos = [
    {no:1, title:'청소하기', done: false},
    {no:2, title:'공부하기', done: true}
];

router.get('/api/todos', (req, res) => {
    // res.end(), res.send(), res.redirect(), res.json() ...
    res.json(todos);
});

module.exports = router;