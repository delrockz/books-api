import { SagaIterator } from 'redux-saga'
import { takeLatest, all } from 'redux-saga/effects'
import { actions } from '../../statics/actions'
import { createBookHandle, deleteBooksHandle, getBooksHandle, updateBookHandle } from './handlers'

export function* watcherSaga(): SagaIterator {
  yield all([
    yield takeLatest(actions.CREATE_BOOK, createBookHandle),
    yield takeLatest(actions.GET_BOOKS, getBooksHandle),
    yield takeLatest(actions.UPDATE_BOOK, updateBookHandle),
    yield takeLatest(actions.DELETE_BOOKS, deleteBooksHandle),
  ])
}
