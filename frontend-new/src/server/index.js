const express = require('express');
const app = express();
const path = require('path');

app.use(express.json());

const staticFolder = path.join(__dirname, '..', '..', 'static')
const distFolder = path.join(__dirname, '..', '..', 'dist')
app.use(express.static(staticFolder))
app.use(express.static(distFolder))

app.use('/api/plants', require('./routes/plants'));
app.use('/api/requests', require('./routes/requests'));

app.get('/', (req, res, next) => {
  res.sendFile(path.join(staticFolder, 'index.html'))
});

app.use((err, req, res, next)=> {
  console.error(err);
  res.status(500).send({ message: err. message });
});


const port = process.env.PORT || 3000;

app.listen(port);
