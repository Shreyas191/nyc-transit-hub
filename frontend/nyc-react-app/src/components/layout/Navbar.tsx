// src/components/layout/Navbar.tsx
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Box, IconButton } from '@mui/material';
import { Train, Map, Schedule, Warning, AccountCircle, Menu, Close } from '@mui/icons-material';

const Navbar: React.FC = () => {
  const location = useLocation(); 
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false); // Mobile Menu Toggle

  // Path, Icon, Display Text
  const navItems = [
    { path: '/', label: 'Home', icon: <Train /> },
    { path: '/map', label: 'Map', icon: <Map /> },
    { path: '/arrivals', label: 'Arrivals', icon: <Schedule /> },
    { path: '/status', label: 'Status', icon: <Warning /> },
    { path: '/account', label: 'Account', icon: <AccountCircle /> },
  ];

  return (
    <AppBar position="static" sx={{ bgcolor: '#0039a6' }}> {/* NYC地铁蓝配色 */}
      <Toolbar>
        {/* Website Title + Desktop Navigation */}
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, display: { xs: 'none', md: 'block' } }}>
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

        {/* Desktop navigation buttons */}
        <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
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
              sx={{ justifyContent: 'flex-start', px: 3 }}
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