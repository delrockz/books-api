export default interface INewBook {
  _id?: string
  bookName?: string
  description?: string
  category?: 'Fantasy' | 'Sci-Fi' | 'Mystery' | 'Thriller' | 'Romance'
  gstTaxRate?: string | number
  gstInclusive?: boolean
  image?: string
  bookCode?: number
  price?: number
  lowStockWarning?: number
  stock?: number
}
