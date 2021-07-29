import { Button, Input, message, Modal, Radio, RadioChangeEvent, Typography } from 'antd'
import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import IBook from '../../../interfaces/IBook'
import { updateBook } from '../../../store/actions'

interface PropTypes {
  open: boolean
  setOpen: Function
  book: IBook
  setBook: Function
}
const AdjustStockModal: React.FC<PropTypes> = ({ open, setOpen, book, setBook }) => {
  const dispatch = useDispatch()
  const [adjustedStock, setAdjustedStock] = useState(0)
  const [addStock, setAddStock] = useState(true)
  const clearModal = () => {
    setAdjustedStock(0)
    setAddStock(true)
    setBook({ gstTaxRate: 0, lowStockWarning: 0, gstInclusive: false } as IBook)
    setOpen(false)
  }
  return (
    <Modal
      title='Adjust Stock Quantity'
      visible={open}
      onCancel={() => setOpen(false)}
      destroyOnClose={true}
      onOk={() => setOpen(false)}
      footer={
        <>
          <Button type='dashed' onClick={() => clearModal()}>
            Cancel
          </Button>
          <Button
            type='primary'
            onClick={() => {
              var finalStock = addStock ? ((book.stock + adjustedStock) as any) : ((book.stock - adjustedStock) as any)
              if (finalStock < 0) {
                message.error({ content: "You don't have enough stock", duration: 2 })
                return
              }
              const formData = new FormData()
              formData.append('stock', finalStock)
              dispatch(
                updateBook({
                  bookId: book._id,
                  book: formData,
                })
              )
              clearModal()
            }}
          >
            Save
          </Button>
        </>
      }
    >
      <div className='flex flex-col justify-center items-start'>
        <div className='grid items-center grid-cols-2 gap-4'>
          <Typography className='col-span-1 font-semibold'>Book Name:</Typography>
          <Typography className='col-span-1'>{book.bookName}</Typography>
          <Typography className='col-span-1 font-semibold'>Current Stock:</Typography>
          <Typography className='col-span-1'>{book.stock}</Typography>
        </div>
        <Typography className='text-gray-400 my-4'>Add or Reduce stock</Typography>
        <Radio.Group
          onChange={(e: RadioChangeEvent) => {
            setAddStock(e.target.value)
          }}
          value={addStock}
        >
          <Radio value={true}>Add (+)</Radio>
          <Radio value={false}>Reduce (+)</Radio>
        </Radio.Group>
        <Input
          className='my-4'
          placeholder='Adjust stock'
          value={adjustedStock}
          type='number'
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setAdjustedStock(parseInt(e.target.value))}
        />
        <div className='grid items-center grid-cols-2 gap-4'>
          <Typography className='font-semibold col-span-1'>Final Stock:</Typography>
          <Typography className='col-span-1'>
            {!Number.isInteger(adjustedStock)
              ? book.stock
              : addStock
              ? book.stock + adjustedStock
              : book.stock - adjustedStock}
          </Typography>
        </div>
      </div>
    </Modal>
  )
}

export default AdjustStockModal
