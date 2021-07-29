import Title from 'antd/lib/typography/Title'
import React from 'react'

const Header: React.FC = () => {
  return (
    <>
      <header className='sticky top-0 z-50 bg-blue-300 h-16 flex items-center'>
        <Title level={4} className='mx-8 '>
          Book Inventory
        </Title>
      </header>
    </>
  )
}

export default Header
