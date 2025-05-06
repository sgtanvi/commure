import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  Typography,
  Box,
  CircularProgress,
} from '@mui/material'
import {User} from "../../App"

interface LandingPageProps {
  user: User | null
}

interface Prescription {
  pres_name: string
  pres_strength: string
  refills: number
  date_prescribed: string
  date_uploaded: string
}

export default function LandingPage({ user }: LandingPageProps) {
  const [prescriptions, setPrescriptions] = useState<Prescription[]>([])
  const [summaries, setSummaries] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get('http://localhost:8000/prescriptions/abc')
        const active = res.data.active_prescriptions || []
        setPrescriptions(active)

        if (active.length > 0) {
          const medDefs = active.map((p: { pres_name: any; pres_strength: any }) => ({
            name: p.pres_name,
            definition: `${p.pres_name} ${p.pres_strength}`,
          }))

          const payload = {
            medications: medDefs,
            profile: {
              firstName: 'Jane',
              lastName: 'Doe',
              email: 'jane@example.com',
              password: 'abc123',
              age: 65,
              conditions: [],
              allergies: [],
              prescriptions: [],
            },
          }

          const geminiRes = await axios.post('http://localhost:8000/generate_plan', payload)
          setSummaries(geminiRes.data.html || '')
        }
      } catch (err) {
        console.error('Failed to fetch prescriptions or summary:', err)
        setPrescriptions([])
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <Box sx={{ p: 4, backgroundColor: '#121212', minHeight: '100vh', color: '#fff' }}>
      <Typography variant="h4" align="center" gutterBottom>
        Welcome {user?.firstname}
      </Typography>
      <Typography variant="h6" align="center" gutterBottom>
        Your Active Prescriptions
      </Typography>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
          <CircularProgress />
        </Box>
      ) : prescriptions.length === 0 ? (
        <Typography align="center">No active prescriptions found.</Typography>
      ) : (
        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            gap: 3,
            mt: 2,
          }}
        >
          {prescriptions.map((prescription, index) => (
            <Box
              key={index}
              onMouseEnter={() => setHoveredIndex(index)}
              onMouseLeave={() => setHoveredIndex(null)}
              sx={{
                width: hoveredIndex === index ? '360px' : '300px',
                transition: 'all 0.3s ease',
                backgroundColor: '#1e1e1e',
                color: '#fff',
                borderRadius: 2,
                p: 2,
                boxShadow: 3,
              }}
            >
              <Typography variant="h6" gutterBottom>
                {prescription.pres_name}
              </Typography>
              <Typography variant="body2">Strength: {prescription.pres_strength}</Typography>
              <Typography variant="body2">Refills: {prescription.refills}</Typography>
              <Typography variant="body2">Prescribed: {prescription.date_prescribed}</Typography>
              <Typography variant="caption" color="gray">
                Uploaded: {new Date(prescription.date_uploaded).toLocaleDateString()}
              </Typography>
            </Box>
          ))}
        </Box>
      )}

      {summaries && (
        <Box
          sx={{
            mt: 4,
            px: 2,
            py: 3,
            backgroundColor: '#181818',
            borderRadius: 2,
            color: '#eee',
            fontSize: '1rem',
            lineHeight: 1.7,
          }}
          dangerouslySetInnerHTML={{ __html: summaries }}
        />
      )}
    </Box>
  )
}
