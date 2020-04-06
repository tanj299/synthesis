const express = require('express');
const router = express.Router();
const axios = require('axios');

const API = 'http://127.0.0.1:5000/plant';

router.get('/plants', async (req, res, next) => {
    try {
        const data = (await axios.get(API)).data;
        res.status(201).json(data);
    } catch(err) {
        console.log(err);
    }
});

router.get('/plants/:id', async (req, res, next) => {
    try {
        const data = (await axios.get(`${API}/${req.params.id}`)).data;
        res.status(201).json(data);
    } catch(err) {
        console.log(err);
    }
});


module.exports = router;