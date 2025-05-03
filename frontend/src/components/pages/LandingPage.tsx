import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  Typography,
  Box,
  CircularProgress,
} from '@mui/material'

interface Prescription {
  pres_name: string
  pres_strength: string
  refills: number
  date_prescribed: string
  date_uploaded: string
}

export default function LandingPage() {
  const [prescriptions, setPrescriptions] = useState<Prescription[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get('http://localhost:8000/prescriptions/abc')
        setPrescriptions(res.data.active_prescriptions || [])
      } catch (err) {
        console.error('Failed to fetch prescriptions:', err)
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
              sx={{
                width: '300px',
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
    </Box>
  )
}
