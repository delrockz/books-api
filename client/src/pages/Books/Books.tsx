import React, { useEffect, useState } from 'react'
import { Table, Typography, Button, Input, Empty, Tooltip } from 'antd'
import { useDispatch, useSelector } from 'react-redux'
import { deleteBooks, getBooks } from '../../store/actions'
import { AppState } from '../../store/reducers'
import IBook from '../../interfaces/IBook'
import CreateUpdateModal from './components/CreateUpdateModal'
import { EditOutlined, WarningOutlined } from '@ant-design/icons'
import AdjustStockModal from './components/AdjustStockModal'

const Books: React.FC = () => {
  const [searchBook, setSearchBook] = useState('')
  const [book, setBook] = useState({ gstTaxRate: 0, lowStockWarning: 0, gstInclusive: false } as IBook)
  const [showUpdateModal, setShowUpdateModal] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [lowStockWarningFilter, setLowStockWarningFilter] = useState(false)
  const [adjustStockModal, setAdjustStockModal] = useState(false)
  const [selectedRows, setSelectedRows] = useState([] as string[])
  const books = useSelector((state: AppState) => state.books)
  const dispatch = useDispatch()

  const rowSelection = {
    onChange: (selectedRowKeys: any[]) => {
      setSelectedRows(selectedRowKeys)
    },
  }

  const deleteRecords = () => {
    var bookIds = ''
    selectedRows.forEach(row => (bookIds += `${row},`))
    dispatch(deleteBooks(bookIds))
  }

  const columns = [
    {
      dataIndex: 'image',
      render: (image: string) => {
        return image ? (
          <img alt='' className='mx-auto' width={100} src={image} />
        ) : (
          <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description='' />
        )
      },
    },
    {
      dataIndex: 'bookCode',
      sorter: {
        compare: (a: IBook, b: IBook) => a.bookCode - b.bookCode,
      },
      title: 'Book Code',
    },
    {
      dataIndex: 'bookName',
      // sorter: (a: IBook, b: IBook) => a.bookName - b.bookName,
      title: 'Book Name',
      render: (bookName: string) => {
        return <Typography>{bookName ? bookName : ' - '}</Typography>
      },
    },
    {
      dataIndex: 'category',
      // sorter: (a: IBook, b: IBook) => a.bookName - b.bookName,
      title: 'Category',
    },
    {
      dataIndex: 'stock',
      sorter: (a: IBook, b: IBook) => a.stock - b.stock,
      title: 'Stock Quantity',
      render: (stock: number, data: IBook) => {
        return (
          <Typography className='my-0'>
            {data.stock <= data.lowStockWarning ? (
              <div className='flex items-center'>
                <Tooltip title='Low stock warning'>
                  <WarningOutlined className='mx-2 text-yellow-500' />
                </Tooltip>
                <Typography className='my-0'>{stock}</Typography>
              </div>
            ) : (
              <Typography className='my-0'>{stock}</Typography>
            )}
          </Typography>
        )
      },
    },
    {
      dataIndex: 'stock',
      title: 'Stock Value',
      sorter: (a: IBook, b: IBook) => a.stock * a.price - b.stock * b.price,
      render: (stock: number, data: IBook) => {
        return <Typography className='my-0'>&#8377;{stock * data.price}</Typography>
      },
    },
    {
      dataIndex: 'price',
      sorter: (a: IBook, b: IBook) => a.price - b.price,
      title: 'Price',
      render: (price: number, data: IBook) => {
        return (
          <Typography className='my-0'>
            &#8377;{data.gstInclusive ? price : price + (price * data.gstTaxRate) / 100}
          </Typography>
        )
      },
    },
    {
      dataIndex: '_id',
      title: 'Edit',
      render: (_id: string, data: IBook) => {
        return (
          <Button
            shape='circle'
            onClick={() => {
              setBook(data)
              setShowUpdateModal(true)
            }}
            icon={<EditOutlined />}
          />
        )
      },
    },
    {
      dataIndex: 'data',
      title: 'Actions',
      render: (_: any, data: IBook) => {
        return (
          <Button
            onClick={() => {
              setBook(data)
              setAdjustStockModal(true)
            }}
          >
            Adjust Stock
          </Button>
        )
      },
    },
  ]

  useEffect(() => {
    dispatch(getBooks({ name: searchBook, lowStockWarning: lowStockWarningFilter }))
  }, [dispatch, lowStockWarningFilter])

  return (
    <>
      <CreateUpdateModal
        type='create'
        book={book}
        setBook={setBook}
        open={showCreateModal}
        setOpen={setShowCreateModal}
      />
      <CreateUpdateModal
        type='edit'
        book={book}
        setBook={setBook}
        open={showUpdateModal}
        setOpen={setShowUpdateModal}
      />
      <AdjustStockModal open={adjustStockModal} setOpen={setAdjustStockModal} book={book} setBook={setBook} />
      <form
        onSubmit={(e: React.FormEvent) => {
          e.preventDefault()
          dispatch(getBooks({ name: searchBook, lowStockWarning: lowStockWarningFilter }))
        }}
        className='d-flex flex-row mt-4'
      >
        <Input
          placeholder='Search books by name'
          className='my-2 mr-2 w-1/2'
          value={searchBook}
          onChange={e => setSearchBook(e.target.value)}
        />
        <Button
          onClick={() => dispatch(getBooks({ name: searchBook, lowStockWarning: lowStockWarningFilter }))}
          className='mx-2'
          icon={<i className='fa fa-search mr-2' />}
        >
          Search
        </Button>
        <Button
          icon={lowStockWarningFilter ? <i className='fa fa-times mr-2' /> : <></>}
          onClick={() => setLowStockWarningFilter(!lowStockWarningFilter)}
          className='mx-2'
        >
          Show Low Stock
        </Button>
        <Button
          disabled={selectedRows.length === 0}
          onClick={() => deleteRecords()}
          type='default'
          className='mx-2'
          icon={<i className='fa fa-trash mr-2 text-red' />}
        >
          Delete Selected
        </Button>
        <Button
          type='primary'
          onClick={() => setShowCreateModal(true)}
          className='m-2'
          icon={<i className='fa fa-plus mr-2' />}
        >
          Add to Inventory
        </Button>
      </form>
      <div className='pb-5'>
        <Table
          rowSelection={{
            type: 'checkbox',
            ...rowSelection,
          }}
          style={{ overflowX: 'scroll' }}
          columns={columns}
          dataSource={books.data}
          loading={books.loading}
          size='large'
          footer={() => <div className='text-right'>{books.data?.length || 0} books</div>}
          pagination={{ position: ['bottomCenter'], pageSize: 5 }}
          rowKey='_id'
        />
      </div>
    </>
  )
}

export default Books
