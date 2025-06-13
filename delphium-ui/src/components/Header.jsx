import React, { useContext } from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';

const Header = () => {
  const theme = useTheme();
  // You need two logo variants: delphium-logo-black.png and delphium-logo-white.png
  const logoSrc =
    theme.palette.mode === 'dark' ? '/delphium-logo-white.png' : '/delphium-logo-black.png';

  return (
    <AppBar position="fixed" sx={{ backgroundColor: 'transparent', width: '100%', color: 'black' }}>
      <Toolbar disableGutters sx={{ px: 2, py: 1 }}>
        <Box
          component="img"
          src={logoSrc}
          alt="Delphium Logo"
          sx={{ height: 40, width: 'auto', mr: 2 }}
        />
        <Typography variant="h5" color="inherit" noWrap>
          Delphium
        </Typography>
        <Box sx={{ flexGrow: 1 }} />
        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 2 }}>
          <Typography variant="body1" component="a" href="/" color="inherit">
            Home
          </Typography>
          <Typography variant="body1" component="a" href="/summary" color="inherit">
            Summary
          </Typography>
          <Typography variant="body1" component="a" href="/about" color="inherit">
            About
          </Typography>
          <Typography variant="body1" component="a" href="/settings" color="inherit">
            Settings
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
