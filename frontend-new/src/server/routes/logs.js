const express = require('express');
const router = express.Router();
const axios = require('axios');


const API = 'http://backend-dev222222.us-east-1.elasticbeanstalk.com/logs';


// mounted on /api/logs
router.get('/:id', async (req, res, next) => {
    try {
        const logs = (await axios.get(`${API}/all/${req.params.id}`)).data;
        res.json(logs);
    } catch(err) {  
        console.log(err);
    }
});

module.exports = router;
