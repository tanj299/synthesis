const express = require('express');
const router = express.Router();
const axios = require('axios');


const API = 'http://backend-dev222222.us-east-1.elasticbeanstalk.com';


// mounted on /api/requests
router.get('/requests/:id', async (req, res, next) => {
    try {
        const data = (await axios.get(`${API}/all/${req.params.id}/0:00`)).data;
        res.status(201).json(data);
    } catch(err) {
        console.log(err);
    }
});

router.post('/insert', async (req, res, next) => {
    const { plant_id, category, waterthreshold, lightthreshold } = req.body;
    try {
        if(waterthreshold) {
            await axios.put(`${API}/update/${plant_id}`, { water_threshold: waterthreshold })
        } else if(lightthreshold) {
            await axios.put(`${API}/update/${plant_id}`, { light_threshold: lightthreshold })
        }
        const plant = (await axios.post(`${API}/requests/insert`, { plant_id, category, timestamp: "" })).data;
        res.send(plant);
    } catch(err) {
        console.log(err);
    }
});



module.exports = router;
