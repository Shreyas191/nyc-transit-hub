// src/components/layout/Navbar.tsx
import React from 'react';
import { useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Box, IconButton } from '@mui/material';
import { Train, Map, Schedule, Warning, AccountCircle, Menu, Close } from '@mui/icons-material';

const Navbar: React.FC = () => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  // English Navigation Items
  const navItems = [
    { path: '/', label: 'HOME', icon: <Train /> },
    { path: '/map', label: 'MAP', icon: <Map /> },
    { path: '/arrivals', label: 'ARRIVALS', icon: <Schedule /> },
    { path: '/status', label: 'STATUS', icon: <Warning /> },
    { path: '/account', label: 'ACCOUNT', icon: <AccountCircle /> },
  ];

  return (
    <AppBar position="static" sx={{ bgcolor: '#0039a6', width: '100%' }}>
      <Toolbar sx={{ padding: '0 20px' }}>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
          NYC TRANSIT HUB
        </Typography>

        {/* Mobile Menu Button */}
        <IconButton
          color="inherit"
          aria-label="menu"
          sx={{ display: { xs: 'block', md: 'none' } }}
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <Close /> : <Menu />}
        </IconButton>

        {/* Desktop Navigation */}
        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 3 }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              component={Link}
              to={item.path}
              color="inherit"
              startIcon={item.icon}
              sx={{
                fontWeight: location.pathname === item.path ? 'bold' : 'normal',
                borderBottom: location.pathname === item.path ? '2px solid white' : 'none',
                textTransform: 'uppercase',
                padding: '0 16px'
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
      </Toolbar>

      {/* Mobile Navigation Menu */}
      {mobileMenuOpen && (
        <Box sx={{ display: { xs: 'flex', md: 'none' }, flexDirection: 'column' }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              component={Link}
              to={item.path}
              color="inherit"
              startIcon={item.icon}
              onClick={() => setMobileMenuOpen(false)}
              sx={{ 
                justifyContent: 'flex-start', 
                px: 4, 
                py: 2,
                borderBottom: '1px solid rgba(255,255,255,0.1)'
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
      )}
    </AppBar>
  );
};

export default Navbar;