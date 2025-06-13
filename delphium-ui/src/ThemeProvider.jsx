import React, { createContext, useMemo, useState, useEffect } from 'react';
import { ThemeProvider as MuiThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

export const ColorModeContext = createContext({
  mode: 'system',
  setMode: () => {},
});

const getSystemTheme = () =>
  window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

export default function ThemeProvider({ children }) {
  const [mode, setMode] = useState(() => localStorage.getItem('themeMode') || 'system');
  const [resolvedMode, setResolvedMode] = useState(mode === 'system' ? getSystemTheme() : mode);

  useEffect(() => {
    if (mode === 'system') {
      const listener = (e) => setResolvedMode(e.matches ? 'dark' : 'light');
      const mql = window.matchMedia('(prefers-color-scheme: dark)');
      mql.addEventListener('change', listener);
      setResolvedMode(getSystemTheme());
      return () => mql.removeEventListener('change', listener);
    } else {
      setResolvedMode(mode);
    }
  }, [mode]);

  useEffect(() => {
    localStorage.setItem('themeMode', mode);
  }, [mode]);

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: resolvedMode,
        },
      }),
    [resolvedMode]
  );

  return (
    <ColorModeContext.Provider value={{ mode, setMode }}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ColorModeContext.Provider>
  );
}