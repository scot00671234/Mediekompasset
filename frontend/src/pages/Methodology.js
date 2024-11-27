import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Grid,
  Card,
  CardContent,
  Divider,
} from '@mui/material';
import DatasetIcon from '@mui/icons-material/Dataset';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import SourceIcon from '@mui/icons-material/Source';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import CodeIcon from '@mui/icons-material/Code';
import WarningIcon from '@mui/icons-material/Warning';

const MethodSection = ({ icon, title, children }) => (
  <Card 
    elevation={3}
    sx={{
      height: '100%',
      transition: 'transform 0.2s',
      '&:hover': {
        transform: 'translateY(-4px)',
      }
    }}
  >
    <CardContent>
      <Box display="flex" alignItems="center" mb={2}>
        {React.cloneElement(icon, { 
          sx: { 
            fontSize: 40,
            color: '#1976d2'
          }
        })}
        <Typography variant="h6" ml={2} color="primary">
          {title}
        </Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />
      {children}
    </CardContent>
  </Card>
);

const Methodology = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 8 }}>
      <Typography 
        variant="h4" 
        gutterBottom 
        align="center"
        sx={{ 
          fontWeight: 700,
          mb: 6,
          color: '#1976d2'
        }}
      >
        Metode og dataindsamling
      </Typography>

      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <MethodSection 
            icon={<DatasetIcon />}
            title="Dataindsamling"
          >
            <Typography variant="body1" paragraph>
              Mediekompasset indsamler automatisk artikler fra de største danske nyhedsmedier gennem deres 
              offentligt tilgængelige websider. Vi benytter avancerede web scraping-teknikker, der 
              respekterer mediernes robots.txt-filer og god praksis for datahøstning.
            </Typography>
          </MethodSection>
        </Grid>

        <Grid item xs={12} md={6}>
          <MethodSection 
            icon={<AnalyticsIcon />}
            title="Politisk analyse"
          >
            <Typography variant="body1" paragraph>
              Den politiske analyse baseres på en kombination af maskinlæringsmodeller trænet på dansk 
              politisk tekst. Vi analyserer ordvalg, temaer og vinklinger i artiklerne for at placere 
              dem på en politisk højre-venstre skala.
            </Typography>
          </MethodSection>
        </Grid>

        <Grid item xs={12} md={6}>
          <MethodSection 
            icon={<SourceIcon />}
            title="Kildeanalyse"
          >
            <Typography variant="body1" paragraph>
              Vi identificerer og analyserer kilder gennem Natural Language Processing (NLP). 
              Dette omfatter genkendelse af citater, ekspertudtalelser og referencer. Vi vurderer 
              diversiteten af kilder og deres baggrund.
            </Typography>
          </MethodSection>
        </Grid>

        <Grid item xs={12} md={6}>
          <MethodSection 
            icon={<VerifiedUserIcon />}
            title="Pålidelighedsvurdering"
          >
            <Typography variant="body1" paragraph>
              Pålidelighedsscoren beregnes ud fra flere faktorer:
            </Typography>
            <Box component="ul" sx={{ pl: 2, mt: 0 }}>
              <li>Antal og diversitet af kilder</li>
              <li>Brug af faktuelle påstande og deres verificerbarhed</li>
              <li>Adskillelse af fakta og holdninger</li>
              <li>Transparens omkring metoder og datagrundlag</li>
            </Box>
          </MethodSection>
        </Grid>

        <Grid item xs={12} md={6}>
          <MethodSection 
            icon={<CodeIcon />}
            title="Tekniske detaljer"
          >
            <Typography variant="body1" paragraph>
              Vi anvender state-of-the-art danske sprogmodeller, specifikt den danske BERT-model, 
              til tekstanalyse. Vores sentiment-analyse er baseret på DaCy, en dansk 
              sprogmodel specialiseret i følelsesanalyse.
            </Typography>
          </MethodSection>
        </Grid>

        <Grid item xs={12} md={6}>
          <MethodSection 
            icon={<WarningIcon />}
            title="Begrænsninger"
          >
            <Typography variant="body1" paragraph>
              Det er vigtigt at bemærke, at automatiseret medieanalyse har sine begrænsninger. 
              Vores system kan ikke fange alle nuancer i journalistisk arbejde, og der kan 
              forekomme fejlvurderinger.
            </Typography>
          </MethodSection>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Methodology;
