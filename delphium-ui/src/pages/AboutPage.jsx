import React from 'react';
import { Container, Typography, Box, Link as MuiLink } from '@mui/material';

export default function AboutPage() {
  return (
    <Container maxWidth="md" sx={{ py: 4, }}>
      <Typography variant="h4" gutterBottom>
        About Delphium
      </Typography>

      <Typography variant="body1" paragraph>
        Delphium is your personal chess‐analysis engine. It:
      </Typography>
      <Box component="ul" sx={{ pl: 2 }}>
        <li>Fetches your games from Chess.com</li>
        <li>Runs Stockfish to find tactical and strategic mistakes</li>
        <li>Uses GPT‐4 to generate human‐friendly summaries and training plans</li>
        <li>Caches per-user data for fast re-analysis</li>
        <li>Provides a clean React + MUI UI for browsing your progress</li>
      </Box>

      <Typography variant="body1" paragraph>
        Delphium was built with Python (Stockfish, FastAPI/Flask backend) and React/Material UI on the frontend.
      </Typography>

      <Typography variant="body1" paragraph>
        Feel free to browse your <MuiLink href="/">summaries</MuiLink> or <MuiLink href="/summary/abc123">view a specific report</MuiLink>.
      </Typography>

      <Typography variant="caption" display="block" sx={{ mt: 4 }}>
        © {new Date().getFullYear()} Delphium. All rights reserved.
      </Typography>
    </Container>
  );
}
