import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; 
import { Box, Typography, Button } from '@mui/material';

import Layout from '../components/layout/Layout';
import MapView from '../pages/MapView'; 

// Home
const Home = () => (
  <Box 
    sx={{ 
      padding: { xs: 4, md: 8 }, 
      minHeight: 'calc(100vh - 200px)', 
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center', 
      justifyContent: 'center', 
      textAlign: 'center', 
      maxWidth: '1200px',
      margin: '0 auto' 
    }}
  >
    <Typography 
      variant="h2" 
      gutterBottom 
      sx={{ 
        color: '#0039a6', 
        fontWeight: 'bold',
        lineHeight: 1.2,
        mb: 3,
        textShadow: '1px 1px 2px rgba(0,0,0,0.1)' 
      }}
    >
      Welcome to NYC TRANSIT HUB
    </Typography>

    {/* Description Text */}
    <Typography 
      variant="body1" 
      color="text.secondary" 
      mb={6} 
      maxWidth="800px"
      sx={{ lineHeight: 1.6 }}
    >
      Real-time information platform for New York City subways and buses. Get route details, arrival times, and service status in one place.
    </Typography>

    {/* Buttons */}
    <Box 
      display="flex" 
      gap={{ xs: 2, md: 3 }} 
      flexWrap="wrap" 
      justifyContent="center" 
    >
      <Button 
        component={Link} 
        to="/map" 
        variant="contained" 
        size="large"
        sx={{ 
          bgcolor: '#0039a6', 
          '&:hover': { bgcolor: '#002d80' },
          padding: { xs: '12px 24px', md: '14px 28px' },
          fontSize: { xs: '0.9rem', md: '1rem' }
        }}
      >
        View Real-Time Map
      </Button>
      <Button 
        component={Link} 
        to="/arrivals" 
        variant="outlined" 
        size="large"
        sx={{ 
          borderColor: '#0039a6', 
          color: '#0039a6', 
          '&:hover': { borderColor: '#002d80' },
          padding: { xs: '12px 24px', md: '14px 28px' },
          fontSize: { xs: '0.9rem', md: '1rem' }
        }}
      >
        Check Arrival Times
      </Button>
      <Button 
        component={Link} 
        to="/status" 
        variant="outlined" 
        size="large"
        sx={{ 
          borderColor: '#0039a6', 
          color: '#0039a6', 
          '&:hover': { borderColor: '#002d80' },
          padding: { xs: '12px 24px', md: '14px 28px' },
          fontSize: { xs: '0.9rem', md: '1rem' }
        }}
      >
        Service Status
      </Button>
    </Box>

    {/* Decorative Element */}
    <Box 
      sx={{ 
        mt: 8,
        width: '100%',
        maxWidth: '600px',
        height: '8px',
        bgcolor: '#0039a6',
        borderRadius: '4px',
        opacity: 0.1
      }}
    />
  </Box>
);

// 到达时间页面（保留你的原始样式）
const ArrivalTimes = () => (
  <Box sx={{ padding: 4 }}>
    <Typography variant="h4" gutterBottom sx={{ color: '#0039a6' }}>
      Arrival Times
    </Typography>
    <Typography variant="body1" color="text.secondary" mb={4}>
      Search by station name or ID to get real-time arrival predictions and schedule information.
    </Typography>
    <Box sx={{ 
      bgcolor: '#f5faff', 
      padding: 4, 
      borderRadius: 2, 
      border: '1px solid #e3f2fd'
    }}>
      <Typography variant="h6" color="text.primary" mb={3}>
        Search for a Station
      </Typography>
      <Box sx={{ 
        display: 'flex', 
        gap: 2, 
        flexWrap: 'wrap',
        maxWidth: '600px'
      }}>
        <input
          type="text"
          placeholder="Enter station name or ID"
          style={{
            flex: 1,
            padding: '12px 16px',
            borderRadius: 4,
            border: '1px solid #ced4da',
            fontSize: '1rem'
          }}
        />
        <Button 
          variant="contained" 
          sx={{ bgcolor: '#0039a6', '&:hover': { bgcolor: '#002d80' } }}
        >
          Search
        </Button>
      </Box>
    </Box>
  </Box>
);

// Service Status Page
const ServiceStatus = () => (
  <Box sx={{ padding: 4 }}>
    <Typography variant="h4" gutterBottom sx={{ color: '#0039a6' }}>
      Service Status
    </Typography>
    <Typography variant="body1" color="text.secondary" mb={4}>
      Check current service conditions, delays, and planned maintenance for all MTA routes.
    </Typography>
    <Box sx={{ 
      bgcolor: '#f5faff', 
      padding: 4, 
      borderRadius: 2, 
      border: '1px solid #e3f2fd'
    }}>
      <Typography variant="h6" color="text.primary" mb={3}>
        MTA Service Updates
      </Typography>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Box sx={{ padding: 2, bgcolor: 'white', borderRadius: 1, borderLeft: '3px solid #4caf50' }}>
          <Typography variant="subtitle1" color="text.primary">
            1/2/3 Lines - Normal Service
          </Typography>
          <Typography variant="body2" color="text.secondary">
            No delays or disruptions reported
          </Typography>
        </Box>
        <Box sx={{ padding: 2, bgcolor: 'white', borderRadius: 1, borderLeft: '3px solid #ff9800' }}>
          <Typography variant="subtitle1" color="text.primary">
            A/C/E Lines - Minor Delays
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Delays due to signal maintenance at 59th Street
          </Typography>
        </Box>
        <Box sx={{ padding: 2, bgcolor: 'white', borderRadius: 1, borderLeft: '3px solid #f44336' }}>
          <Typography variant="subtitle1" color="text.primary">
            F Line - Planned Service Change
          </Typography>
          <Typography variant="body2" color="text.secondary">
            No service between Jay Street and Church Avenue (weekend maintenance)
          </Typography>
        </Box>
      </Box>
    </Box>
  </Box>
);

// User Account Page
const UserAccount = () => (
  <Box sx={{ padding: 4 }}>
    <Typography variant="h4" gutterBottom sx={{ color: '#0039a6' }}>
      User Account
    </Typography>
    <Typography variant="body1" color="text.secondary" mb={4}>
      Manage your transit preferences, saved stations, and MetroCard balance.
    </Typography>
    <Box sx={{ 
      bgcolor: '#f5faff', 
      padding: 4, 
      borderRadius: 2, 
      textAlign: 'center',
      border: '1px solid #e3f2fd'
    }}>
      <Typography variant="h6" color="text.primary" mb={3}>
        Account Features Coming Soon
      </Typography>
      <Button 
        variant="contained" 
        sx={{ bgcolor: '#0039a6', '&:hover': { bgcolor: '#002d80' } }}
      >
        Sign In / Register
      </Button>
    </Box>
  </Box>
);

// 404
const NotFound = () => (
  <Box sx={{ 
    padding: 4, 
    textAlign: 'center', 
    minHeight: 'calc(100vh - 200px)', 
    display: 'flex', 
    flexDirection: 'column', 
    justifyContent: 'center' 
  }}>
    <Typography variant="h1" sx={{ color: '#0039a6', mb: 2, fontWeight: 'bold' }}>
      404
    </Typography>
    <Typography variant="h4" gutterBottom>
      Page Not Found
    </Typography>
    <Typography variant="body1" color="text.secondary" mb={4} maxWidth="md" margin="0 auto">
      The page you're looking for doesn't exist or has been moved. Please check the URL or return to the homepage.
    </Typography>
    <Button 
      component={Link} 
      to="/" 
      variant="contained" 
      sx={{ 
        bgcolor: '#0039a6', 
        '&:hover': { bgcolor: '#002d80' },
        width: '180px', 
        margin: '0 auto',
        padding: '10px 0'
      }}
    >
      Return to Homepage
    </Button>
  </Box>
);

// Route Configuration
const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <NotFound />,
    children: [
      { path: '/', element: <Home /> },
      { path: 'map', element: <MapView /> }, // 现在指向 src/pages/MapView.tsx 真地图
      { path: 'arrivals', element: <ArrivalTimes /> },
      { path: 'status', element: <ServiceStatus /> },
      { path: 'account', element: <UserAccount /> },
    ],
  },
  { path: '*', element: <Navigate to="/" replace /> },
]);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}