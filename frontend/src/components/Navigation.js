import React from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Button,
  Box,
  Container,
  SvgIcon,
} from '@mui/material';

// Minimalist compass logo
const LogoIcon = (props) => (
  <SvgIcon {...props} viewBox="0 0 24 24">
    <path
      fill="currentColor"
      d="M12,2L9.1,9.1L2,12L9.1,14.9L12,22L14.9,14.9L22,12L14.9,9.1L12,2M12,7L13.5,11L17,12.5L13.5,14L12,18L10.5,14L7,12.5L10.5,11L12,7Z"
    />
  </SvgIcon>
);

const Navigation = () => {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <AppBar 
      position="sticky" 
      elevation={0}
    >
      <Container maxWidth="lg">
        <Toolbar 
          sx={{ 
            justifyContent: 'space-between',
            minHeight: '64px',
            px: { xs: 2, sm: 4 },
          }}
        >
          <Button
            component={RouterLink}
            to="/"
            sx={{
              color: 'primary.main',
              fontSize: { xs: '1.25rem', sm: '1.375rem' },
              textTransform: 'none',
              fontWeight: 500,
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
              letterSpacing: '-0.02em',
              fontFamily: '"SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
              '&:hover': {
                backgroundColor: 'transparent',
                color: 'primary.light',
              },
              transition: 'color 0.2s ease-out',
            }}
          >
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                position: 'relative',
              }}
            >
              <LogoIcon 
                sx={{ 
                  fontSize: { xs: '1.75rem', sm: '2rem' },
                  color: 'primary.main',
                  transition: 'color 0.2s ease-out',
                }} 
              />
            </Box>
            <Box 
              component="span"
              sx={{
                color: 'text.secondary',
                fontWeight: 400,
                letterSpacing: '-0.025em',
                '&:hover': {
                  color: 'text.primary',
                },
                transition: 'color 0.2s ease-out',
              }}
            >
              Mediekompasset
            </Box>
          </Button>

          <Box 
            sx={{ 
              display: 'flex', 
              gap: 2,
            }}
          >
            {[
              { path: '/', label: 'Oversigt' },
              { path: '/metode', label: 'Metode' },
            ].map(({ path, label }) => (
              <Button
                key={path}
                component={RouterLink}
                to={path}
                sx={{
                  color: isActive(path) ? 'primary.main' : 'text.secondary',
                  fontSize: '0.9375rem',
                  fontWeight: 400,
                  px: 2,
                  py: 0.75,
                  borderRadius: '6px',
                  letterSpacing: '-0.01em',
                  '&:hover': {
                    backgroundColor: 'rgba(0, 122, 255, 0.04)',
                    color: 'primary.main',
                  },
                  ...(isActive(path) && {
                    backgroundColor: 'rgba(0, 122, 255, 0.08)',
                  }),
                  transition: 'all 0.2s ease-out',
                }}
              >
                {label}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navigation;
