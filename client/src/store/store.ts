import { applyMiddleware, compose, createStore } from 'redux'
import createSagaMiddleware from 'redux-saga'
import { watcherSaga } from './sagas'
import allReducers from '../store/reducers'

declare global {
  interface Window {
    __REDUX_DEVTOOLS_EXTENSION_COMPOSE__?: typeof compose | any
  }
}

const sagaMiddleware = createSagaMiddleware()

const composeEnhancers =
  typeof window === 'object' && window['__REDUX_DEVTOOLS_EXTENSION_COMPOSE__']
    ? window['__REDUX_DEVTOOLS_EXTENSION_COMPOSE__']({})
    : compose

const enhancer = composeEnhancers(applyMiddleware(sagaMiddleware))

const store = createStore(allReducers, enhancer)

sagaMiddleware.run(watcherSaga)

export default store
