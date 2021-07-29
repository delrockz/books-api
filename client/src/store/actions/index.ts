import IBook from '../../interfaces/IBook'
import { actions } from '../../statics/actions'

export const createBook = (book: FormData) => {
  return {
    type: actions.CREATE_BOOK,
    payload: book,
  }
}

export const createBookSuccess = (book: IBook) => {
  return {
    type: actions.CREATE_BOOK_SUCCESS,
    payload: book,
  }
}

export const getBooks = ({ name, lowStockWarning }: { name: string; lowStockWarning: boolean }) => {
  return {
    type: actions.GET_BOOKS,
    payload: { name, lowStockWarning },
  }
}

export const getBooksSuccess = (books: Array<IBook>) => {
  return {
    type: actions.GET_BOOKS_SUCCESS,
    payload: books,
  }
}

export const updateBook = ({ bookId, book }: { bookId: string; book: FormData }) => {
  return {
    type: actions.UPDATE_BOOK,
    payload: { bookId, book },
  }
}

export const updateBookSuccess = (book: IBook) => {
  return {
    type: actions.UPDATE_BOOK_SUCCESS,
    payload: book,
  }
}

export const deleteBooks = (bookIds: string) => {
  return {
    type: actions.DELETE_BOOKS,
    payload: bookIds,
  }
}
export const deleteBooksSuccess = (bookId: string) => {
  return {
    type: actions.DELETE_BOOKS_SUCCESS,
    payload: bookId,
  }
}
