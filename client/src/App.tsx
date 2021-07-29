import React from 'react'
import Header from './components/Header'
import { Switch, Route } from 'react-router-dom'
import Books from './pages/Books/Books'
import { appRoutes } from './statics/appRoutes'
import TabLayout from './components/TabLayout'

function App() {
  return (
    <div className='App'>
      <Header />
      <TabLayout />
      <div className='container mx-auto'>
        <Switch>
          <Route path={appRoutes.booksPage} exact component={Books} />
        </Switch>
      </div>
    </div>
  )
}

export default App
