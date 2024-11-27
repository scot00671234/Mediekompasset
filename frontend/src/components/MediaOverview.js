import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  Chip,
  LinearProgress,
  Tooltip
} from '@mui/material';

const TopicBar = ({ topic, percentage }) => (
  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
    <Typography variant="body2" sx={{ minWidth: 100 }}>
      {topic}
    </Typography>
    <Box sx={{ width: '100%', ml: 1 }}>
      <LinearProgress
        variant="determinate"
        value={percentage * 100}
        sx={{
          height: 10,
          borderRadius: 5,
          backgroundColor: '#e0e0e0',
          '& .MuiLinearProgress-bar': {
            backgroundColor: '#1976d2',
            borderRadius: 5,
          },
        }}
      />
    </Box>
    <Typography variant="body2" sx={{ minWidth: 50, ml: 1 }}>
      {Math.round(percentage * 100)}%
    </Typography>
  </Box>
);

const PoliticalBiasBar = ({ bias }) => {
  // Position af markøren (konverterer fra [-1,1] til [0,100])
  const position = ((bias + 1) / 2) * 100;

  return (
    <Box sx={{ position: 'relative', mb: 2 }}>
      {/* Gradient bar */}
      <Box
        sx={{
          height: 20,
          width: '100%',
          borderRadius: 1,
          background: 'linear-gradient(to right, #f44336, #f5f5f5, #2196f3)',
          position: 'relative',
        }}
      />
      
      {/* Markør */}
      <Box
        sx={{
          position: 'absolute',
          top: -5,
          left: `${position}%`,
          transform: 'translateX(-50%)',
          width: 4,
          height: 30,
          backgroundColor: 'black',
          borderRadius: 1,
        }}
      />
      
      {/* Labels */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        mt: 1,
        color: 'text.secondary',
        fontSize: '0.75rem'
      }}>
        <span>Venstreorienteret</span>
        <span>Neutral</span>
        <span>Højreorienteret</span>
      </Box>
      
      {/* Numerisk værdi */}
      <Typography 
        variant="caption" 
        sx={{ 
          position: 'absolute',
          top: -20,
          left: `${position}%`,
          transform: 'translateX(-50%)',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          padding: '2px 4px',
          borderRadius: 1,
        }}
      >
        {bias.toFixed(2)}
      </Typography>
    </Box>
  );
};

const MediaCard = ({ media, stats }) => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {media}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {stats.description}
        </Typography>

        <Box sx={{ mt: 2, mb: 2 }}>
          <Chip
            label={stats.category}
            size="small"
            sx={{ mr: 1, mb: 1 }}
          />
        </Box>

        <Typography variant="subtitle2" gutterBottom>
          Politisk orientering
        </Typography>
        <PoliticalBiasBar bias={stats.political_bias} />

        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            <Typography variant="subtitle2" gutterBottom>
              Pålidelighed
            </Typography>
            <Typography variant="h6">
              {Math.round(stats.reliability_score * 100)}%
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="subtitle2" gutterBottom>
              Kildediversitet
            </Typography>
            <Typography variant="h6">
              {Math.round(stats.source_diversity * 100)}%
            </Typography>
          </Grid>
        </Grid>

        <Typography variant="subtitle2" gutterBottom>
          Emnefordeling
        </Typography>
        {Object.entries(stats.topic_coverage).map(([topic, percentage]) => (
          <TopicBar key={topic} topic={topic} percentage={percentage} />
        ))}
      </CardContent>
    </Card>
  );
};

const MediaOverview = ({ mediaStats }) => {
  return (
    <Grid container spacing={3}>
      {Object.entries(mediaStats).map(([media, stats]) => (
        <Grid item xs={12} sm={6} md={4} key={media}>
          <MediaCard media={media} stats={stats} />
        </Grid>
      ))}
    </Grid>
  );
};

export default MediaOverview;
