import { HelmetProvider } from 'react-helmet-async'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import './App.css'
import { AppHeader } from './components/organisms/app-header'
import SignIn from './components/organisms/sign-in'
function App() {

  return (
    <HelmetProvider>
      <BrowserRouter>
        <Toaster />
        <div className='flex flex-col w-full min-h-screen'>
          <Routes>
            <Route path='/' element = {<AppHeader/>}>
              <Route index element={<div>landing page</div>} />
            </Route>
            <Route path='/loginsignup' element={<SignIn />} />
          </Routes>
        </div>
      </BrowserRouter>
    </HelmetProvider>
  );
}

export default App
