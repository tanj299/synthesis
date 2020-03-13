const app = require('express').Router();
const path = require('path');

app.get("/plants", (req, res, next) => {
    res.sendFile(path.join(__dirname, "index.html"));
});

app.get("/addplant", (req, res, next) => {
    res.sendFile(path.join(__dirname, "addplant.html"));
});

module.exports = app;
