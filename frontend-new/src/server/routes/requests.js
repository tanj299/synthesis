const express = require('express');
const router = express.Router();
const axios = require('axios');


const API = 'http://backend-dev222222.us-east-1.elasticbeanstalk.com/requests';


// mounted on /api/requests
router.get('/:id', async (req, res, next) => {
    try {
        const data = (await axios.get(`${API}/all/${req.params.id}/0:00`)).data;
        res.status(201).json(data);
    } catch(err) {
        console.log(err);
    }
});

router.post('/insert', async (req, res, next) => {
    const { plant_id, category } = req.body;
    try {
        const plant = (await axios.post(`${API}/insert`, { plant_id, category, timestamp: "" })).data;
        res.send(plant);
    } catch(err) {
        console.log(err);
    }
});

module.exports = router;
