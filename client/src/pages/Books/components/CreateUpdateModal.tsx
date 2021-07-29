import { Button, Card, DatePicker, Input, message, Modal, Select, Switch, Typography } from 'antd'
import React, { useEffect, useRef, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import IBook from '../../../interfaces/IBook'
import { categories, gstTaxRates } from '../../../statics'
import { createBook, updateBook } from '../../../store/actions'
import moment from 'moment'
import { AppState } from '../../../store/reducers'
const { Option } = Select

interface PropTypes {
  book: IBook
  setBook: Function
  open: boolean
  setOpen: Function
  type: 'edit' | 'create'
}

const CreateUpdateModal: React.FC<PropTypes> = ({ open, setOpen, setBook, book, type }) => {
  const imgRef = useRef<HTMLImageElement>(null)
  const imgUploaderRef = useRef<HTMLInputElement>(null)
  const dispatch = useDispatch()
  const [lowStockWarning, setLowStockWarning] = useState(false)
  const books = useSelector((state: AppState) => state.books)
  const [file, setFile] = useState<any>()
  const [fileName, setFileName] = useState('')
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0])
      setFileName(event.target.files[0].name)
      var reader = new FileReader()
      reader.onload = function (e) {
        if (imgRef.current && e.target) {
          imgRef.current.src = e.target.result as string
        }
      }
      reader.readAsDataURL(event.target.files[0])
    }
  }

  const validateRequest = () => {
    if (lowStockWarning && !book.lowStockWarning) {
      message.error({ content: 'Please enter low stock units', duration: 2 })
      return false
    } else if (type === 'create' && book.lowStockWarning > book.stock) {
      message.error({ content: 'Low stock warning cannot be higher than stock', duration: 2 })
      return false
    } else if (!book.stock) {
      message.error({ content: 'Please enter opening stock', duration: 2 })
      return false
    } else if (book.stock <= 0) {
      message.error({ content: 'Opening stock has to be more than 0', duration: 2 })
      return false
    } else if (!book.price) {
      message.error({ content: 'Please enter price', duration: 2 })
      return false
    } else if (book.price <= 0) {
      message.error({ content: 'Price has to be more than 0', duration: 2 })
      return false
    } else if (!book.bookName) {
      message.error({ content: 'Please enter book name', duration: 2 })
      return false
    } else if (!book.bookCode) {
      message.error({ content: 'Please enter book code', duration: 2 })
      return false
    } else if (!book.category) {
      message.error({ content: 'Please enter book category', duration: 2 })
      return false
    }
    return true
  }

  const createBookHandle = () => {
    if (!validateRequest()) return
    const formData = new FormData()
    if (file) formData.append('file', file)
    Object.entries(book).forEach(book => {
      var [key, value] = book
      formData.append(key, value)
    })
    dispatch(createBook(formData))
    clearModal()
  }
  const updateBookHandle = () => {
    if (!validateRequest()) return
    const formData = new FormData()
    if (file) formData.append('file', file)
    Object.entries(book).forEach(book => {
      var [key, value] = book
      formData.append(key, value)
    })
    dispatch(updateBook({ bookId: book._id ? book._id : '', book: formData }))
    clearModal()
  }

  useEffect(() => {
    if (type === 'edit' && book.lowStockWarning) setLowStockWarning(true)
  }, [book, type])

  const clearModal = () => {
    resetVariables()
    setOpen(false)
  }

  const resetVariables = () => {
    setBook({ gstTaxRate: 0, lowStockWarning: 0, gstInclusive: false } as IBook)
    setLowStockWarning(false)
    setFile(null)
    setFileName('')
    if (imgRef.current) imgRef.current.src = ''
  }

  const resetBook = () => {
    var bookData = books.data.filter((obj: IBook) => obj._id === book._id)[0]
    setBook(bookData)
  }

  return (
    <Modal
      width={1080}
      destroyOnClose={true}
      title={type === 'edit' ? `Edit book ${book.bookName}` : 'Create Book'}
      onCancel={() => clearModal()}
      onOk={() => clearModal()}
      visible={open}
      footer={
        <>
          <Button
            type='primary'
            onClick={() => {
              if (type === 'edit') updateBookHandle()
              else createBookHandle()
            }}
          >
            Save
          </Button>
          <Button
            type='dashed'
            onClick={() => {
              if (type === 'create') resetVariables()
              else resetBook()
            }}
          >
            Reset
          </Button>
        </>
      }
    >
      <div className='h-116 sm:h-112 lg:h-104 w-full grid grid-cols-1 lg:grid-cols-2'>
        <Card className='m-2' title='General details'>
          <Typography className='mx-2 text-gray-400'>Upload Book Image:</Typography>
          <img
            alt=''
            className='m-2 w-48 h-48'
            ref={imgRef}
            src={book.image && type === 'edit' ? book.image : ''}
            style={{ display: book.image || file ? 'block' : 'none' }}
          />
          <input
            ref={imgUploaderRef}
            onChange={handleImageUpload}
            type='file'
            accept='image/*'
            style={{ display: 'none' }}
          />
          {fileName && <Typography className='m-2'>{fileName}</Typography>}
          <Button className='m-2' onClick={() => imgUploaderRef.current?.click()}>
            Upload Image
          </Button>
          <div className='grid items-center grid-cols-3'>
            <Typography className='m-2 col-span-3 sm:col-span-1'>Book Name:</Typography>
            <Input
              className='m-2 col-span-2'
              placeholder='Book name'
              value={book.bookName}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setBook((prev: IBook) => {
                  return { ...prev, bookName: e.target.value }
                })
              }
            />
            <Typography className='m-2 col-span-3 sm:col-span-1'>Book Code:</Typography>
            <Input
              className='m-2 col-span-2'
              placeholder='Book code'
              type='number'
              value={book.bookCode}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setBook((prev: IBook) => {
                  return { ...prev, bookCode: parseInt(e.target.value) }
                })
              }
            />
            <Typography className='m-2 col-span-3 sm:col-span-1'>Book Description:</Typography>
            <Input
              className='m-2 col-span-2'
              placeholder='Book description'
              value={book.description}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setBook((prev: IBook) => {
                  return { ...prev, description: e.target.value }
                })
              }
            />
            <Typography className='m-2 col-span-3 sm:col-span-1'>Book Category:</Typography>
            <Select
              className='m-2 col-span-2'
              style={{ width: 200 }}
              placeholder='Category'
              value={book.category}
              onChange={(value: any) => {
                setBook((prev: IBook) => {
                  return { ...prev, category: value }
                })
              }}
            >
              {categories.map(category => (
                <Option value={category}>{category}</Option>
              ))}
            </Select>
          </div>
        </Card>
        <div>
          <Card className='m-2' title='Stock details'>
            <div className='grid items-center grid-cols-3'>
              <Typography className='m-2 col-span-3 sm:col-span-1'>Opening stock:</Typography>
              <Input
                required
                className='m-2 col-span-2'
                placeholder='Quantity'
                type='number'
                value={book.stock}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setBook((prev: IBook) => {
                    return { ...prev, stock: parseInt(e.target.value) }
                  })
                }
              />
              <Typography className='m-2 col-span-3 sm:col-span-1'>As of date:</Typography>
              <DatePicker className='m-2 col-span-2' value={moment()} format='MM/DD/YYYY' placeholder='As of Date' />
              <Typography className='m-2 col-span-3 sm:col-span-1'>Low stock warning:</Typography>
              <div className='col-span-2'>
                <Switch
                  className='m-2'
                  checked={book.lowStockWarning > 0 ? true : lowStockWarning}
                  title='Enable low stock warning'
                  onChange={(value: boolean) => {
                    setLowStockWarning(value)
                    if (!value)
                      setBook((prev: IBook) => {
                        return { ...prev, lowStockWarning: 0 }
                      })
                  }}
                />
              </div>
              {lowStockWarning && (
                <>
                  <Typography className='m-2 col-span-3 sm:col-span-1 align-baseline'>Low stock units:</Typography>
                  <Input
                    className='m-2 col-span-2'
                    placeholder='Low stock units'
                    type='number'
                    value={book.lowStockWarning}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                      setBook((prev: IBook) => {
                        return { ...prev, lowStockWarning: parseInt(e.target.value) }
                      })
                    }}
                  />
                </>
              )}
            </div>
          </Card>
          <Card className='m-2' title='Pricing details'>
            <div className='grid items-center grid-cols-3'>
              <Typography className='m-2 col-span-3 sm:col-span-1'>Purchase price:</Typography>
              <Input
                className='m-2 col-span-2'
                prefix={<span>&#8377;</span>}
                placeholder='Price'
                type='number'
                value={book.price}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setBook((prev: IBook) => {
                    return { ...prev, price: parseInt(e.target.value) }
                  })
                }
              />
              <Typography className='mx-2 col-span-3 sm:col-span-1'>Inclusive of tax:</Typography>
              <div className='col-span-2'>
                <Switch
                  className='m-2'
                  checked={book.gstInclusive}
                  title='Inclusive of tax'
                  onChange={(value: boolean) =>
                    setBook((prev: IBook) => {
                      return { ...prev, gstInclusive: value }
                    })
                  }
                />
              </div>
              <Typography className='mx-2 col-span-3 sm:col-span-1'>GST tax rate (%):</Typography>
              <Select
                className='m-2 col-span-2'
                value={book.gstTaxRate != null ? `GST @ ${book.gstTaxRate}%` : ''}
                placeholder='GST tax rate (%)'
                onChange={(value: string) =>
                  setBook((prev: IBook) => {
                    return { ...prev, gstTaxRate: value }
                  })
                }
              >
                {gstTaxRates.map(taxRate => (
                  <Option value={taxRate}>{taxRate === 0 ? 'None' : `GST @ ${taxRate}%`}</Option>
                ))}
              </Select>
            </div>
          </Card>
        </div>
      </div>
    </Modal>
  )
}

export default CreateUpdateModal
