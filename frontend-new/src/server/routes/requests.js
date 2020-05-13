const express = require('express');
const router = express.Router();
const axios = require('axios');


const API = 'http://backend-dev222222.us-east-1.elasticbeanstalk.com';


// mounted on /api/requests
router.get('/:id', async (req, res, next) => {
    try {
        const data = (await axios.get(`${API}/requests/all/${req.params.id}/0:00`)).data;
        res.status(201).json(data);
    } catch(err) {
        console.log(err);
    }
});

router.post('/insert', async (req, res, next) => {
    const { plant_id, category } = req.body;
    try {
        const plant = (await axios.post(`${API}/requests/insert`, { plant_id, category, timestamp: "" })).data;
        res.send(plant);
    } catch(err) {
        console.log(err);
    }
});

router.put('/edit', async(req, res, next) => {
    const { id, name, species, email, port, position, curr_photo, date_created, uri} = req.body;
    const light = parseInt(req.body.light);
    const water = parseInt(req.body.water);
    try {
        const plant = (await axios.put(`${API}/plants/update/${id}`, { water_threshold: water, plant_name: name, species, user_email: email, light_threshold: light, serial_port: port, position, curr_photo, date_created, uri })).data;
        res.status(201).json(plant);
    } catch(err) {
        console.log(err);
    }
});

module.exports = router;
