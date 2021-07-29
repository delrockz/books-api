const express = require('express')
const router = express.Router()
const BooksController = require('./controllers/BookController')
const { upload } = require('./utils/multer')
router.post('/books', upload, BooksController.createBookController)
router.get('/books', BooksController.getBooksController)
router.put('/books/:id', upload, BooksController.updateBookController)
router.delete('/books', BooksController.deleteBookController)

module.exports = router
