const { createBook, deleteBook, getBooks, updateBook } = require('../services/book')
const { createResponse } = require('../utils/response')
const _promise = require('../utils/simpleAsync')
const AWS = require('aws-sdk')
require('dotenv').config()

AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY,
  secretAccessKey: process.env.AWS_SECRET_KEY,
  region: process.env.AWS_REGION,
})
var s3 = new AWS.S3()

module.exports = {
  async createBookController(req, res, next) {
    if (req.file) {
      var params = {
        Bucket: process.env.AWS_S3_BUCKET,
        Body: req.file.buffer,
        Key: `books/${req.file.originalname}`,
      }
      s3.upload(params, async (error, data) => {
        if (error) return res.json(createResponse(false, null, error))
        req.body.image = data.Location
        const [err, book] = await _promise(createBook(req.body))
        if (err) return res.json(createResponse(false, null, err.message))
        return res.json(createResponse(true, book, null))
      })
    } else {
      const [err, book] = await _promise(createBook(req.body))
      if (err) return res.json(createResponse(false, null, err.message))
      return res.json(createResponse(true, book, null))
    }
  },

  async deleteBookController(req, res, next) {
    var bookIds = req.query.bookIds.split(',').filter(bookId => bookId != '')
    const [err, _] = await _promise(deleteBook(bookIds))
    if (err) return res.json(createResponse(false, null, err.message))
    return res.json(createResponse(true, 'Deleted book', null))
  },

  async getBooksController(req, res, next) {
    const [err, books] = await _promise(getBooks(req.query.name, req.query.showLowStock === 'true'))
    if (err) return res.json(createResponse(false, null, err.message))
    return res.json(createResponse(true, books, null))
  },

  async updateBookController(req, res, next) {
    if (req.file) {
      var params = {
        Bucket: process.env.AWS_S3_BUCKET,
        Body: req.file.buffer,
        Key: `books/${req.file.originalname}`,
      }
      s3.upload(params, async (error, data) => {
        if (error) return res.json(createResponse(false, null, error))
        req.body.image = data.Location
        const [err, updatedBook] = await _promise(updateBook(req.params.id, req.body))
        if (err) return res.json(createResponse(false, null, err.message))
        return res.json(createResponse(true, updatedBook, null))
      })
    } else {
      const [err, updatedBook] = await _promise(updateBook(req.params.id, req.body))
      if (err) return res.json(createResponse(false, null, err.message))
      return res.json(createResponse(true, updatedBook, null))
    }
  },
}
