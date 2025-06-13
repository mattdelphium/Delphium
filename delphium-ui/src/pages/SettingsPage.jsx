import React, { useContext } from 'react';
import { ColorModeContext } from '../ThemeProvider';
import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';

export default function SettingsPage() {
  const { mode, setMode } = useContext(ColorModeContext);

  return (
    <FormControl component="fieldset">
      <FormLabel component="legend">Theme</FormLabel>
      <RadioGroup
        row
        value={mode}
        onChange={e => setMode(e.target.value)}
        name="theme-mode"
      >
        <FormControlLabel value="light" control={<Radio />} label="Light" />
        <FormControlLabel value="dark" control={<Radio />} label="Dark" />
        <FormControlLabel value="system" control={<Radio />} label="System" />
      </RadioGroup>
    </FormControl>
  );
}