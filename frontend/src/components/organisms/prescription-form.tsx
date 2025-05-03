import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  Stack,
  Card,
  CardContent,
  FormControlLabel,
  Checkbox
} from '@mui/material';
import { User } from '../../App';
import { useNavigate } from 'react-router-dom';
import { Prescription } from '../../App';
const defaultPrescription: Prescription = {
  pres_name: "",
  pres_strength: "",
  refills: 0,
  date_prescribed: "",
  active: false
};

interface PrescriptionProps {
  user: User | null,
  setUser: (user: User) => void
}

export default function PrescriptionForm({ user, setUser }: PrescriptionProps) {
  const [formData, setFormData] = useState<Prescription>(defaultPrescription);
  const [prescriptions, setPrescriptions] = useState<Prescription[]>([]);

  const [response, setResponse] = useState<string>(" ehllo");


  const navigate = useNavigate();
  useEffect(() => {
      console.log('in prescription form');
      if (user === null) {
          console.log('navigating to login/signup');
          navigate("/loginsignup");
      }
      setPrescriptions(user?.documents.prescriptions || []);
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Submitted Prescription:', formData);
    // TODO: send data to backend or store in parent component
    if (user) {
      user.documents.prescriptions.push(formData);
      setUser(user);
    }
    setPrescriptions([...prescriptions, formData]);
  };

  return (
    <div className='flex flex-row w-full min-h-screen p-4 bg-gradient-to-b from-white to-gray-100'>
    <Box className="flex flex-col w-full min-h-screen p-4 bg-gradient-to-b from-white to-gray-100">
      <Card sx={{ maxWidth: 500, mx: 'auto', p: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Add Prescription
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Medication Name"
              name="pres_name"
              value={formData.pres_name}
              onChange={handleChange}
              required
            />
            <TextField
              label="Strength"
              name="pres_strength"
              value={formData.pres_strength}
              onChange={handleChange}
              required
            />
            <TextField
              label="Refills"
              name="refills"
              type="number"
              value={formData.refills}
              onChange={handleChange}
              required
            />
            <TextField
              label="Date Prescribed"
              name="date_prescribed"
              type="date"
              InputLabelProps={{ shrink: true }}
              value={formData.date_prescribed}
              onChange={handleChange}
              required
            />
            <FormControlLabel
              control={
                <Checkbox
                  name="active"
                  checked={formData.active}
                  onChange={handleChange}
                />
              }
              label="Currently Active"
            />
            <Button type="submit" variant="contained">
              Submit Prescription
            </Button>
          </Box>
        </CardContent>
      </Card>
      <Stack direction="column" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5" gutterBottom>Prescriptions</Typography>
        <ul className='overflow-y-auto h-full'>
          {prescriptions.map((prescription) => (
            <li key={prescription.pres_name}>{prescription.pres_name} {prescription.pres_strength} {prescription.refills} {prescription.date_prescribed} {prescription.active ? "Active" : "Inactive"}</li>
          ))}
        </ul>
      </Stack>
    </Box>
    <div className='border-red-500'>
    <Button>
      Query Medication
    </Button>
    <div
      dangerouslySetInnerHTML={{ __html: response }}
    >

    </div>
    </div>
    </div>
  );
}
