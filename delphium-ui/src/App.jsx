import { Routes, Route } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import SummaryPage from './pages/SummaryPage';

function App() {
  return (
    <>
      <CssBaseline />
      <Header />
      <Box sx={{ pt: 8 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/summary/:hash" element={<SummaryPage />} />
        </Routes>
      </Box>
    </>
  );
}

export default App;
