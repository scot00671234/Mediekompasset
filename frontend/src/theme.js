import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#007AFF', 
      light: '#47a1ff',
      dark: '#0055b3',
    },
    secondary: {
      main: '#8E8E93', 
      light: '#AEAEB2',
      dark: '#636366',
    },
    background: {
      default: '#FBFBFD', 
      paper: '#ffffff',
    },
    text: {
      primary: '#1D1D1F', 
      secondary: '#86868B', 
    },
  },
  typography: {
    fontFamily: '"SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    h1: {
      fontWeight: 600,
      letterSpacing: '-0.025em',
    },
    h2: {
      fontWeight: 600,
      letterSpacing: '-0.02em',
    },
    h3: {
      fontWeight: 500,
      letterSpacing: '-0.015em',
    },
    body1: {
      letterSpacing: '-0.01em',
    },
    button: {
      textTransform: 'none',
      letterSpacing: '-0.01em',
    },
  },
  shape: {
    borderRadius: 10,
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          backdropFilter: 'blur(20px) saturate(180%)',
          borderBottom: '1px solid rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          padding: '6px 16px',
          transition: 'all 0.2s ease-out',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '16px',
          border: '1px solid rgba(0, 0, 0, 0.05)',
          boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.04)',
        },
      },
    },
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#FBFBFD',
          backgroundImage: 'radial-gradient(circle at 50% 0%, rgba(0, 122, 255, 0.03), transparent 40%)',
          backgroundAttachment: 'fixed',
        },
      },
    },
  },
});

export default theme;
