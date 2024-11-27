import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Methodology from './pages/Methodology';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/metode" element={<Methodology />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
