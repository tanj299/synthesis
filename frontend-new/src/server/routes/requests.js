const express = require('express');
const router = express.Router();
const axios = require('axios');


const API = 'http://127.0.0.1:5000/requests';


// mounted on /api/requests
router.get('/:id', async (req, res, next) => {
    try {
        const data = (await axios.get(`${API}/${req.params.id}`)).data;
        res.status(201).json(data);
    } catch(err) {
        console.log(err);
    }
});

router.post('/insert/category', async (req, res, next) => {
    try {
        console.log(req.body);
    } catch(err) {
        console.log(err);
    }
});

module.exports = router;
