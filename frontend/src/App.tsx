import { HelmetProvider } from 'react-helmet-async'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import './App.css'
import { AppHeader } from './components/organisms/app-header'
import SignIn from './components/organisms/sign-in'
import { useEffect, useState } from 'react'
import AllergiesPage from './components/organisms/allergies'
import ConditionsPage from './components/organisms/conditions'
import PrescriptionForm from './components/organisms/prescription-form'
export interface User {
  firstname: string
  lastname: string
  email: string
  password: string
  conditions: string[]
  allergies: string[]
  family_members: string[]
  documents: PrescriptionDocument 
}

export interface Prescription {
  pres_name: string
  pres_strength: string
  refills: number
  date_prescribed: string
  active: boolean
}

export interface PrescriptionDocument {
  user_id: string
  prescriptions: Prescription[]
  date_uploaded: string
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



    class Prescription(BaseModel):
    pres_name: str
    pres_strength: str
    refills: int
    date_prescribed: str
    active: bool

class PrescriptionDocument(BaseModel):
    user_id: str
    prescriptions: List[Prescription]
    date_uploaded: datetime
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
              <Route index element={<PrescriptionForm user={user} setUser={setUser} />} />
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
