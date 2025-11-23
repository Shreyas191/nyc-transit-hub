// src/components/layout/Footer.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Box, Typography, Container, Link as MuiLink } from '@mui/material';

const Footer: React.FC = () => {
  return (
    
    <Box component="footer" sx={{ bgcolor: '#f5f5f5', py: 4, mt: 'auto' }}>
      <Container maxWidth="lg">
        {/* Flexbox Layout  */}
        <Box 
          sx={{ 
            display: 'flex', 
            flexDirection: { xs: 'column', md: 'row' }, // Vertical mobile devices, horizontal desktop devices
            gap: 6, 
            mb: 4 
          }}
        >
          {/* Project Information */}
          <Box sx={{ flex: 1 }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#0039a6' }}>
              NYC TRANSIT HUB
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Real-time New York City Transit Information Platform, offering route lookup, arrival alerts, service status updates, and more.
            </Typography>
          </Box>

          {/* Quick Links */}
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle1" gutterBottom>
              Quick Links
            </Typography>
            <Box display="flex" flexDirection="column" gap={1}>
              <MuiLink component={Link} to="/" color="text.secondary" underline="hover">
                Home
              </MuiLink>
              <MuiLink component={Link} to="/map" color="text.secondary" underline="hover">
                Real-time Map
              </MuiLink>
              <MuiLink component={Link} to="/arrivals" color="text.secondary" underline="hover">
                Arrival time
              </MuiLink>
              <MuiLink component={Link} to="/status" color="text.secondary" underline="hover">
                Service Status
              </MuiLink>
              <MuiLink component={Link} to="/account" color="text.secondary" underline="hover">
                User Account
              </MuiLink>
            </Box>
          </Box>

          {/* Data Source*/}
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle1" gutterBottom>
              Data Source
            </Typography>
            <MuiLink 
              href="https://api.mta.info" 
              target="_blank" 
              rel="noopener noreferrer" 
              color="text.secondary" 
              underline="hover"
            >
              MTA Developer API
            </MuiLink>
          </Box>
        </Box>

        {/* Bottom Copyright Information */}
        <Box 
          sx={{ 
            pt: 3, 
            borderTop: '1px solid #e0e0e0', 
            textAlign: 'center' 
          }}
        >
          <Typography variant="body2" color="text.secondary">
            © {new Date().getFullYear()} NYC TRANSIT HUB. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;