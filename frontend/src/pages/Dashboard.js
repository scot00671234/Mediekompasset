import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Button,
  CircularProgress,
  Paper,
} from '@mui/material';
import MediaOverview from '../components/MediaOverview';

const Dashboard = () => {
  const [mediaStats, setMediaStats] = useState(null);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('Alle');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/stats');
        const data = await response.json();
        setMediaStats(data.media_stats);
        setCategories(['Alle', ...Object.keys(data.categories)]);
        setLoading(false);
      } catch (error) {
        console.error('Fejl ved hentning af statistik:', error);
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const filteredMediaStats = selectedCategory === 'Alle'
    ? mediaStats
    : Object.fromEntries(
        Object.entries(mediaStats || {}).filter(
          ([_, stats]) => stats.category === selectedCategory
        )
      );

  if (loading) {
    return (
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          minHeight: '80vh' 
        }}
      >
        <CircularProgress size={60} thickness={4} />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      <Paper 
        elevation={3} 
        sx={{ 
          p: 3,
          background: '#ffffff',
          borderRadius: 2,
        }}
      >
        <Box 
          sx={{ 
            mb: 4,
            display: 'flex',
            flexWrap: 'wrap',
            gap: 1.5,
            justifyContent: 'center'
          }}
        >
          {categories.map((category) => (
            <Button
              key={category}
              onClick={() => setSelectedCategory(category)}
              sx={{
                minWidth: 'auto',
                px: 3,
                py: 1,
                borderRadius: '25px',
                textTransform: 'none',
                fontSize: '0.95rem',
                fontWeight: selectedCategory === category ? 600 : 400,
                color: selectedCategory === category ? '#fff' : '#666',
                backgroundColor: selectedCategory === category 
                  ? 'primary.main'
                  : 'transparent',
                border: '1px solid',
                borderColor: selectedCategory === category 
                  ? 'primary.main'
                  : '#e0e0e0',
                boxShadow: selectedCategory === category 
                  ? '0 2px 8px rgba(25, 118, 210, 0.25)'
                  : 'none',
                transition: 'all 0.2s ease-in-out',
                '&:hover': {
                  backgroundColor: selectedCategory === category 
                    ? 'primary.dark'
                    : '#f5f5f5',
                  borderColor: selectedCategory === category 
                    ? 'primary.dark'
                    : '#bdbdbd',
                  transform: 'translateY(-1px)',
                  boxShadow: selectedCategory === category 
                    ? '0 4px 12px rgba(25, 118, 210, 0.35)'
                    : '0 2px 4px rgba(0,0,0,0.05)',
                }
              }}
            >
              {category}
            </Button>
          ))}
        </Box>

        <MediaOverview mediaStats={filteredMediaStats} />
      </Paper>
    </Container>
  );
};

export default Dashboard;
