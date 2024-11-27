import React, { useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import axios from 'axios';

function MediaAnalysis() {
  const [url, setUrl] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!url) {
      setError('Indtast venligst en URL');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/api/analyze', { url });
      setAnalysis(response.data);
    } catch (err) {
      setError('Der opstod en fejl under analysen. Prøv igen senere.');
      console.error('Analyse fejl:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Analysér Artikel
            </Typography>
            <Box sx={{ mt: 2 }}>
              <TextField
                fullWidth
                label="Artikel URL"
                variant="outlined"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                sx={{ mb: 2 }}
              />
              <Button
                variant="contained"
                onClick={handleAnalyze}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Analysér'}
              </Button>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}

            {analysis && (
              <Box sx={{ mt: 4 }}>
                <Typography variant="h6" gutterBottom>
                  Analyseresultater
                </Typography>
                
                <Grid container spacing={2}>
                  <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle1">Titel</Typography>
                      <Typography variant="body1">{analysis.title}</Typography>
                    </Paper>
                  </Grid>

                  <Grid item xs={12} sm={6}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle1">Sentiment Score</Typography>
                      <Typography variant="body1">
                        {analysis.sentiment.label}: {(analysis.sentiment.score * 100).toFixed(1)}%
                      </Typography>
                    </Paper>
                  </Grid>

                  <Grid item xs={12} sm={6}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle1">Antal Kilder</Typography>
                      <Typography variant="body1">{analysis.sources_count}</Typography>
                    </Paper>
                  </Grid>

                  <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle1">Nøgleord</Typography>
                      <Typography variant="body1">
                        {analysis.keywords.join(', ')}
                      </Typography>
                    </Paper>
                  </Grid>

                  <Grid item xs={12}>
                    <Paper sx={{ p: 2 }}>
                      <Typography variant="subtitle1">Sammenfatning</Typography>
                      <Typography variant="body1">{analysis.summary}</Typography>
                    </Paper>
                  </Grid>
                </Grid>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default MediaAnalysis;
