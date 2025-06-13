import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import CircularProgress from '@mui/material/CircularProgress';

const USER = import.meta.env.VITE_USERNAME || 'your_username';

export default function SummaryPage() {
  const { hash } = useParams();
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    axios
      .get(`/summaries/${USER}/${hash}.json`)
      .then(res => setSummary(res.data))
      .catch(() => console.error('Could not load summary'));
  }, [hash]);

  if (!summary)
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Box>
    );

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        Summary for Game {hash}
      </Typography>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          🎯 Recurring Patterns
        </Typography>
        <List>
          {summary.recurring_patterns?.map((p, i) => (
            <ListItem key={i} sx={{ pl: 0 }}>
              <Typography variant="body1">{p}</Typography>
            </ListItem>
          ))}
        </List>
      </Box>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          🗝️ Most Common Mistake Types
        </Typography>
        <List>
          {summary.mistake_types?.map((m, i) => (
            <ListItem key={i} sx={{ pl: 0 }}>
              <Typography variant="body1">{m}</Typography>
            </ListItem>
          ))}
        </List>
      </Box>

      {/* Continue rendering other sections: examples, openings, recommendations, training plan */}
    </Container>
  );
}
