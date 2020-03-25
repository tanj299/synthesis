const express = require('express');
const app = express.Router();
const db = require('./db');

app.get('/plantsdata', (req, res, next) => {
    db.readJSON('db.json').then(data => res.send(data));
});

app.get('/plantsdata/:id', (req, res, next) => {
    db.readJSON('db.json').then(data => res.send(data.find(item => item.id === req.params.id)));
});

module.exports = app;
