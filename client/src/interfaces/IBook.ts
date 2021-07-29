export default interface IBook {
  _id: string
  bookName: string
  description: string
  category: 'Fantasy' | 'Sci-Fi' | 'Mystery' | 'Thriller' | 'Romance'
  gstTaxRate: number
  gstInclusive: boolean
  image: string
  bookCode: number
  price: number
  lowStockWarning: number
  stock: number
}
