import { Action } from 'redux'

export default interface IAction extends Action {
  payload?: any
}
