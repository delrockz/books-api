import axios from 'axios'
import IBook from '../../interfaces/IBook'
import { links } from '../../statics/links'

export const createBookService = (book: IBook) => {
  return axios.post(`${links.books}`, book)
}
export const deleteBooksService = (bookIds: string) => {
  return axios.delete(`${links.books}?bookIds=${bookIds}`)
}
export const getBooksService = ({ name, lowStockWarning }: { name: string; lowStockWarning: boolean }) => {
  return axios.get(`${links.books}?name=${name}&showLowStock=${lowStockWarning}`)
}
export const updateBookService = ({ bookId, book }: { bookId: string; book: IBook }) => {
  return axios.put(`${links.books}/${bookId}`, book)
}
