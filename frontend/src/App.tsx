import { HelmetProvider } from 'react-helmet-async'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import './App.css'
import { AppHeader } from './components/organisms/app-header'
import SignIn from './components/organisms/sign-in'
import { useEffect, useState } from 'react'

export interface User {
  firstname: string
  lastname: string
  email: string
  password: string
  conditions: string[]
  allergies: string[]
  family_members: string[]
  documents: string
}

function App() {

      {/**
      class UserData(BaseModel):
    user_id: str | None = None
    first_name: str
    last_name: str
    email: str
    password: str
    conditions: List[str] = []
    allergies: List[str] = []
    family_members: Optional[List[str]] = []
    #_id of the prescription document
    documents: str | None = None
 */}

  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    if (user) {
      console.log(user)
    }
  }, [user])

  return (
    <HelmetProvider>
      <BrowserRouter>
        <Toaster />
        <div className='flex flex-col w-full min-h-screen'>
          <Routes>
            <Route path='/' element = {<AppHeader user={user}/>}>
              <Route index element={<div>prescriptions</div>} />
              <Route path = "/conditions" element = {<div>conditions</div>}/>
              <Route path = "/allergies" element = {<div>allergies</div>}/>
            </Route>
            <Route path='/loginsignup' element={<SignIn setUser={setUser} />} />
          </Routes>
        </div>
      </BrowserRouter>
    </HelmetProvider>
  );
}

export default App
