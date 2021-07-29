const mongoose = require('mongoose')

const BookSchema = mongoose.Schema({
  bookName: {
    type: String,
    required: true,
  },
  description: {
    type: String,
  },
  stock: {
    type: Number,
    required: true,
  },
  lowStockWarning: {
    type: Number,
    required: true,
    default: 0,
  },
  price: {
    type: Number,
    required: true,
  },
  bookCode: {
    type: Number,
    required: true,
  },
  image: {
    type: String,
  },
  gstInclusive: {
    type: Boolean,
    required: true,
  },
  category: {
    type: String,
    enum: ['Fantasy', 'Sci-Fi', 'Mystery', 'Thriller', 'Romance'],
    required: true,
  },
  gstTaxRate: {
    type: Number,
    enum: [0, 1, 0.25, 3, 5, 12],
  },
})

module.exports = mongoose.model('books', BookSchema)
