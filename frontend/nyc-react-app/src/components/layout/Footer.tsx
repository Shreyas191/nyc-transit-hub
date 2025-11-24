// src/components/layout/Footer.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Box, Typography, Link as MuiLink } from '@mui/material';

const Footer: React.FC = () => {
  return (
    <Box component="footer" sx={{ 
      bgcolor: '#f5f5f5', 
      py: 4, 
      mt: 'auto',
      width: '100%',
      borderTop: '1px solid #e0e0e0'
    }}>
      <Box sx={{ 
        display: 'flex', 
        flexDirection: { xs: 'column', md: 'row' },
        gap: 6,
        padding: '0 40px',
        maxWidth: '100%',
        margin: '0 auto'
      }}>
        {/* Left: About */}
        <Box sx={{ flex: 1 }}>
          <Typography variant="h6" gutterBottom sx={{ color: '#0039a6', fontWeight: 'bold' }}>
            NYC TRANSIT HUB
          </Typography>
          <Typography variant="body2" color="text.secondary">
            A comprehensive platform for real-time NYC transit information. 
            Track subways, buses, and get accurate arrival predictions.
          </Typography>
        </Box>

        {/* Middle: Quick Links (English) */}
        <Box sx={{ flex: 1 }}>
          <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'medium' }}>
            Quick Links
          </Typography>
          <Box display="flex" flexDirection="column" gap={1}>
            <MuiLink component={Link} to="/" color="text.secondary" underline="hover">
              Home
            </MuiLink>
            <MuiLink component={Link} to="/map" color="text.secondary" underline="hover">
              Real-Time Map
            </MuiLink>
            <MuiLink component={Link} to="/arrivals" color="text.secondary" underline="hover">
              Arrival Times
            </MuiLink>
            <MuiLink component={Link} to="/status" color="text.secondary" underline="hover">
              Service Status
            </MuiLink>
            <MuiLink component={Link} to="/account" color="text.secondary" underline="hover">
              User Account
            </MuiLink>
          </Box>
        </Box>

        {/* Right: Data Source (English) */}
        <Box sx={{ flex: 1 }}>
          <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'medium' }}>
            Data Source
          </Typography>
          <MuiLink 
            href="https://api.mta.info" 
            target="_blank" 
            rel="noopener noreferrer" 
            color="text.secondary" 
            underline="hover"
            sx={{ display: 'block', mb: 2 }}
          >
            MTA Developer API
          </MuiLink>
          <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'medium', mt: 2 }}>
            Contact Us
          </Typography>
          <Typography variant="body2" color="text.secondary">
            feedback@nyctransithub.com
          </Typography>
        </Box>
      </Box>

      {/* Copyright (English) */}
      <Box mt={4} textAlign="center" sx={{ padding: '0 40px', borderTop: '1px solid #e0e0e0', pt: 3 }}>
        <Typography variant="body2" color="text.secondary">
          © {new Date().getFullYear()} NYC TRANSIT HUB. All rights reserved.
        </Typography>
      </Box>
    </Box>
  );
};

export default Footer;