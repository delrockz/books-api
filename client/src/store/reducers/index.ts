import { actions } from '../../statics/actions'
import { combineReducers } from 'redux'
import IBooks from '../../interfaces/IBooks'
import IBook from '../../interfaces/IBook'
import IAction from '../../interfaces/IAction'

const books = (state: IBooks = { loading: false, data: [] }, action: IAction) => {
  switch (action.type) {
    case actions.GET_BOOKS:
      return { ...state, loading: true }
    case actions.GET_BOOKS_SUCCESS:
      return { ...state, data: action.payload, loading: false }
    case actions.CREATE_BOOK:
      return { ...state, loading: true }
    case actions.CREATE_BOOK_SUCCESS:
      return { ...state, data: [...state.data, action.payload], loading: false }
    case actions.UPDATE_BOOK:
      return { ...state, loading: true }
    case actions.UPDATE_BOOK_SUCCESS:
      var bookId: string = action.payload._id
      var updatedBook: IBook = action.payload
      return {
        ...state,
        data: state.data.map(book => (book._id === bookId ? (book = updatedBook) : book)),
        loading: false,
      }
    case actions.DELETE_BOOKS:
      return { ...state, loading: true }
    case actions.DELETE_BOOKS_SUCCESS:
      var bookIds = action.payload.split(',').filter((bookId: string) => bookId !== '')
      for (var i in bookIds) {
        state = { ...state, data: state.data.filter(book => book._id !== bookIds[i]), loading: false }
      }
      return state
    default:
      return state
  }
}

const allReducers = combineReducers({
  books,
})

export default allReducers

export type AppState = ReturnType<typeof allReducers>
