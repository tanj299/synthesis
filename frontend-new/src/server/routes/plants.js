const express = require('express');
const router = express.Router();
const axios = require('axios');


const API = 'http://backend-dev222222.us-east-1.elasticbeanstalk.com/plants';


// mounted on /api/plants
router.get('/all/:email', async (req, res, next) => {
    try {
        const data = (await axios.get(`${API}/all/${req.params.email}`)).data;
        res.status(201).json(data);
    } catch(err) {
        console.log(err);
    }
});

router.post('/', async(req, res, next) => {
    const { plant_name, species, email, serial_port, position } = req.body;
    try {
        const newPlant = (await axios.post(`${API}/insert`, { plant_name, species, uri: '', curr_photo: '', position, user_email: email, serial_port, water_threshold: 25, light_threshold: 25, headers: {"content-type": "application/json"}})).data;
        res.status(201).json(newPlant);
    } catch(err) {
        console.log(err);
    }
});

router.get('/:id', async (req, res, next) => {
    try {
        const data = (await axios.get(`${API}/plant/${req.params.id}`)).data;
        res.status(201).json(data);
    } catch(err) {
        console.log(err);
    }
});

router.delete('/:id', async (req, res, next) => {
    try {
        await axios.delete(`${API}/plant/${req.params.id}`);
        res.status(201);
    } catch(err) {
        console.log(err);
    }
});

module.exports = router;
