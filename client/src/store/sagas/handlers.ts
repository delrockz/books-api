import { deleteBooksSuccess, getBooksSuccess, updateBookSuccess } from './../actions/index'
import { call, put } from 'redux-saga/effects'
import { SagaIterator } from 'redux-saga'
import { createBookSuccess } from '../actions'
import { createBookService, deleteBooksService, getBooksService, updateBookService } from './requests'
import { message } from 'antd'
import IResponse from '../../interfaces/IResponse'
import IAction from '../../interfaces/IAction'

export function* createBookHandle(action: IAction): SagaIterator {
  try {
    const response: IResponse = yield call(createBookService, action.payload)
    message.success({ content: `Created book '${response.data.data.bookName}'`, duration: 2 })
    yield put(createBookSuccess(response.data.data))
  } catch (e) {
    console.log(e)
  }
}

export function* updateBookHandle(action: IAction): SagaIterator {
  try {
    const response: IResponse = yield call(updateBookService, action.payload)
    message.success({ content: 'Updated book successfully', duration: 2 })
    yield put(updateBookSuccess(response.data.data))
  } catch (e) {
    console.log(e)
  }
}

export function* getBooksHandle(action: IAction): SagaIterator {
  try {
    const response: IResponse = yield call(getBooksService, action.payload)
    yield put(getBooksSuccess(response.data.data))
  } catch (e) {
    console.log(e)
  }
}

export function* deleteBooksHandle(action: IAction): SagaIterator {
  try {
    const response: IResponse = yield call(deleteBooksService, action.payload)
    message.success({ content: 'Deleted books successfully', duration: 2 })
    yield put(deleteBooksSuccess(action.payload))
  } catch (e) {
    console.log(e)
  }
}
