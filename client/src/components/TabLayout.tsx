import { Tabs } from 'antd'
import React from 'react'
import { RouteComponentProps, withRouter } from 'react-router-dom'
import { appRoutes } from '../statics/appRoutes'
const { TabPane } = Tabs

const TabLayout: React.FC<RouteComponentProps> = props => {
  const handleTabClick = (key: string) => {
    props.history.push(key)
  }
  return (
    <Tabs defaultActiveKey={window.location.pathname} centered onChange={handleTabClick}>
      <TabPane tab='Home' key='/'></TabPane>
      <TabPane tab='Books' key={appRoutes.booksPage}></TabPane>
      <TabPane tab='Expenses' disabled key='3'></TabPane>
    </Tabs>
  )
}

export default withRouter(TabLayout)
