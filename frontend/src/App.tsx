import { HelmetProvider } from 'react-helmet-async'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import './App.css'
import { AppHeader } from './components/organisms/app-header'
import { useEffect, useState } from 'react'
import LandingPage from './components/pages/LandingPage'

export interface Prescription {
  pres_name: string;
  pres_strength: string;
  refills: number;
  date_prescribed: string;
  active: boolean;
}

export interface PrescriptionDocument {
  user_id: string;
  prescriptions: Prescription[];
  date_uploaded: string;
}

export interface User {
  firstname: string;
  lastname: string;
  email: string;
  password: string;
  conditions: string[];
  allergies: string[];
  family_members: string[];
  documents: PrescriptionDocument[];  // <-- now allows objects
}

function App() {
  const [user, setUser] = useState<User | null>(null)


  useEffect(() => {
    setUser({
      firstname: 'Alfred',
      lastname: 'Doe',
      email: 'jane@example.com',
      password: 'abc123',
      conditions: ['hypertension'],
      allergies: ['penicillin'],
      family_members: ['dad456', 'mom789'],
      documents: [ 
        {
          user_id: 'jane123',
          prescriptions: [],
          date_uploaded: new Date().toISOString(),
        }
      ],
    })
    

  }, [])


  return (
    <HelmetProvider>
      <BrowserRouter>
        <Toaster />
        <div className="flex flex-col w-full min-h-screen">
          <Routes>
            <Route
              path="/"
              element={<AppHeader user={user} setUser={setUser} />}
            >
              <Route index element={<LandingPage user={user} />} />
              <Route path="/conditions" element={<div>conditions</div>} />
              <Route path="/allergies" element={<div>allergies</div>} />
            </Route>
          </Routes>
        </div>
      </BrowserRouter>
    </HelmetProvider>
  )
}

export default App
