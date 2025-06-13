import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function HomePage() {
  return (
    <Container maxWidth="md">
      <Box sx={{ py: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Welcome to Delphium
        </Typography>
        <Typography variant="body1" paragraph>
          Delphium is your personal chess coach, analyzing your games to help you improve.
          Upload your games and get insights on recurring patterns and common mistakes.
        </Typography>
        <Typography variant="body1" paragraph>
          To get started, upload your games in PGN format. Delphium will analyze them and provide
          detailed summaries with actionable insights.
        </Typography>
        <Typography variant="body1" paragraph>
          Check out the <a href="/summary">summary page</a> to see your game analysis.
        </Typography>
        <Typography variant="body1" paragraph>
          For more information, visit our <a href="/about">about page</a>.
        </Typography> 
      </Box>
    </Container>
  );
}
