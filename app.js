const express = require('express')
const app = express()
const path = require('path')
const routes = require('./routes')
const mongoose = require('mongoose')
require('dotenv').config()
app.use(express.static(path.join(__dirname, 'client/build')))
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use('/api', routes)
app.use('/*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/build', 'index.html'))
})
mongoose.connect(process.env.DB_PATH, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
app.listen(5000)
