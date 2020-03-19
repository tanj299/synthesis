const express = require('express');
const app = express.Router();
const db = require('./db');
const uuid = require('uuid');

app.get('/plantsdata', (req, res, next) => {
    db.readJSON('db.json').then(data => res.send(data));
});

app.post('/plantsdata', async(req, res, next) => {
    console.log("hello");
    const { category, name, photo } = req.body;
    const data = await db.readJSON('db.json')
    data.unshift({
        category: category,
        name: name, 
        waterLevel: Math.round(Math.random() * 20),
        id: uuid.v1(),
        photo: photo
    });
    db.writeJSON('db.json', data)
});

module.exports = app;
