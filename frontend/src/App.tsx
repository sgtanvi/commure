import { HelmetProvider } from 'react-helmet-async'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import './App.css'
import { AppHeader } from './components/organisms/app-header'
import SignIn from './components/organisms/sign-in'
import { useEffect, useState } from 'react'
import AllergiesPage from './components/organisms/allergies'
import ConditionsPage from './components/organisms/conditions'
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

  const [user, setUser] = useState<User | null>(() => {
    const savedUser = localStorage.getItem('user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  
  const [userId, setUserId] = useState<string | null>(() => {
    return localStorage.getItem('userId');
  });

  useEffect(() => {
    console.log('user changed', user);
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  }, [user]);

  useEffect(() => {
    if (userId) {
      localStorage.setItem('userId', userId);
    } else {
      localStorage.removeItem('userId');
    }
  }, [userId]);

  return (
    <HelmetProvider>
      <BrowserRouter>
        <Toaster />
        <div className='flex flex-col w-full min-h-screen'>
          <Routes>
            <Route path='/' element = {<AppHeader user={user} setUser={setUser} />}>
              <Route index element={<div>prescriptions</div>} />
              <Route path = "/conditions" element = {<ConditionsPage user={user} />}/>
              <Route path = "/allergies" element = {<AllergiesPage user={user} />}/>
            </Route>
            <Route path='/loginsignup' element={<SignIn setUser={setUser} setUserId={setUserId} />} />
          </Routes>
        </div>
      </BrowserRouter>
    </HelmetProvider>
  );
}

export default App
