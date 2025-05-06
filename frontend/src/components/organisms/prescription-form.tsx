import React, { useState } from 'react';
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

interface Prescription {
  name: string;
  pres_strength: string;
  refills: number;
  date_prescribed: string;
  active: boolean;
}

const defaultPrescription: Prescription = {
  name: '',
  pres_strength: '',
  refills: 0,
  date_prescribed: '',
  active: true
};

export default function PrescriptionForm() {
  const [formData, setFormData] = useState<Prescription>(defaultPrescription);

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
  };

  return (
    <Box className="flex flex-col w-full min-h-screen p-4 bg-gradient-to-b from-white to-gray-100">
      <Card sx={{ maxWidth: 500, mx: 'auto', p: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Add Prescription
          </Typography>
          <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Medication Name"
              name="name"
              value={formData.name}
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
    </Box>
  );
}
