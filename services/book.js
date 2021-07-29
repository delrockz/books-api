const Book = require('../models/Book')

module.exports = {
  async createBook(book) {
    return Book.create(book)
  },
  async deleteBook(bookIds) {
    for (var i in bookIds) {
      await Book.deleteOne({ _id: bookIds[i] })
    }
  },
  async updateBook(bookId, book) {
    await Book.updateOne({ _id: bookId }, book)
    return Book.findOne({ _id: bookId })
  },
  async getBooks(bookName, lowStockWarning) {
    if (bookName && lowStockWarning) return Book.find({ bookName }).$where('this.stock <= this.lowStockWarning')
    else if (bookName) return Book.find({ bookName })
    else if (lowStockWarning) return Book.find({ $expr: { $lte: ['$stock', '$lowStockWarning'] } })
    else return Book.find()
  },
}
