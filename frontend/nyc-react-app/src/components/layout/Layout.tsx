// src/components/layout/Layout.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Box } from '@mui/material';
import Navbar from './Navbar';
import Footer from './Footer';

const Layout: React.FC = () => {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh', 
      width: '100vw', 
      margin: 0, 
      padding: 0,
      overflowX: 'hidden',
      backgroundColor: '#ffffff'
    }}>
      <Navbar />

      {/* Main Content Area */}
      <Box component="main" sx={{ 
        flexGrow: 1, 
        padding: { xs: 2, md: 4 },
        width: '100%',
        maxWidth: '100vw',
        margin: '0 auto'
      }}>
        <Outlet />
      </Box>

      <Footer />
    </Box>
  );
};

export default Layout;