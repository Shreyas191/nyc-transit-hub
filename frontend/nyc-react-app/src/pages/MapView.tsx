import React, { useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';

declare global {
  interface Window {
    L: any; // 全局 L 对象
  }
}

// Simulated data
const mockStations = [
  { id: '1', name: 'Times Square - 42nd St', lat: 40.7559, lng: -73.9862, line: '1/2/3', status: 'normal' },
  { id: '2', name: 'Grand Central - 42nd St', lat: 40.7527, lng: -73.9772, line: '4/5/6', status: 'normal' },
  { id: '3', name: 'Penn Station - 34th St', lat: 40.7505, lng: -73.9934, line: 'A/C/E', status: 'delayed' },
  { id: '4', name: 'Brooklyn Bridge - City Hall', lat: 40.7124, lng: -74.0060, line: '4/5/6', status: 'normal' },
  { id: '5', name: 'Union Square', lat: 40.7359, lng: -73.9910, line: 'N/Q/R/4/5/6', status: 'normal' },
  { id: '6', name: 'Central Park - 59th St', lat: 40.7658, lng: -73.9763, line: 'N/Q/R', status: 'normal' },
  { id: '7', name: 'Wall St', lat: 40.7075, lng: -74.0083, line: '2/3', status: 'delayed' },
];

// Simulated train data
const mockTrains = [
  { id: 't1', lat: 40.7565, lng: -73.9870, line: '1', direction: 'Downtown', speed: '30 mph' },
  { id: 't2', lat: 40.7520, lng: -73.9780, line: '6', direction: 'Uptown', speed: '25 mph' },
  { id: 't3', lat: 40.7490, lng: -73.9940, line: 'A', direction: 'Brooklyn', speed: '28 mph' },
  { id: 't4', lat: 40.7365, lng: -73.9920, line: 'R', direction: 'Queens', speed: '32 mph' },
];

// Subway Colors
const lineColors = {
  '1': '#ff3333',
  '2': '#ff3333',
  '3': '#ff3333',
  '4': '#009933',
  '5': '#009933',
  '6': '#009933',
  'A': '#0066cc',
  'C': '#0066cc',
  'E': '#0066cc',
  'N': '#ffcc00',
  'Q': '#ffcc00',
  'R': '#ffcc00',
};

const MapView: React.FC = () => {
  
  const nycCenter: [number, number] = [40.730610, -73.986623];

  useEffect(() => {
    if (window.L) {
      delete window.L.Icon.Default.prototype._getIconUrl;
      window.L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      });
    }
  }, []);

  // Generate site location
  const getStationPosition = (lat: number, lng: number): [number, number] => {
    return [lat, lng];
  };

  // Generate train position
  const getTrainPosition = (lat: number, lng: number): [number, number] => {
    return [lat, lng];
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ padding: { xs: 2, md: 4 }, textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom sx={{ color: '#0039a6', fontWeight: 'bold' }}>
          NYC Transit Real-Time Map
        </Typography>
        <Typography variant="body1" color="text.secondary" maxWidth="1000px" margin="0 auto">
          Track live locations of subways and buses. Click on markers for detailed information.
        </Typography>
      </Box>
      <Box sx={{ height: 'calc(100vh - 250px)', width: '100%', border: '1px solid #e0e0e0', borderRadius: 2 }}>
        <MapContainer
          center={nycCenter}
          zoom={13}
          style={{ width: '100%', height: '100%' }}
          scrollWheelZoom={true}
          attributionControl={true}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />

          {/* Subway Station Marker */}
          {mockStations.map((station) => (
            <Marker
              key={station.id}
              position={getStationPosition(station.lat, station.lng)} 
              icon={window.L.divIcon({
                className: 'custom-station-icon',
                html: `<div style="width: 14px; height: 14px; background: ${station.status === 'delayed' ? '#f44336' : '#0039a6'}; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
                iconSize: [14, 14],
                iconAnchor: [7, 7],
              })}
              title={station.name}
            >
              <Popup maxWidth={300}>
                <Box sx={{ padding: 1 }}>
                  <Typography variant="h6" sx={{ color: '#0039a6', mb: 1, fontSize: '1rem' }}>
                    {station.name}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    <strong>Lines:</strong> {station.line.split('/').map(line => (
                      <span key={line} style={{ color: lineColors[line as keyof typeof lineColors] || '#0039a6', fontWeight: 'bold', margin: '0 2px' }}>
                        {line}
                      </span>
                    ))}
                  </Typography>
                  <Typography 
                    variant="body2" 
                    color={station.status === 'delayed' ? 'error.main' : 'success.main'}
                  >
                    <strong>Status:</strong> {station.status === 'delayed' ? 'Delayed' : 'Normal Service'}
                  </Typography>
                </Box>
              </Popup>
            </Marker>
          ))}

          {/* Render real-time train markers*/}
          {mockTrains.map((train) => (
            <Marker
              key={train.id}
              position={getTrainPosition(train.lat, train.lng)} 
              icon={window.L.divIcon({
                className: 'custom-train-icon',
                html: `<div style="width: 18px; height: 18px; background: ${lineColors[train.line as keyof typeof lineColors] || '#f44336'}; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.5);"></div>`,
                iconSize: [18, 18],
                iconAnchor: [9, 9],
              })}
              title={`Train ${train.id} (Line ${train.line})`}
            >
              <Popup maxWidth={300}>
                <Box sx={{ padding: 1 }}>
                  <Typography variant="h6" sx={{ color: lineColors[train.line as keyof typeof lineColors] || '#f44336', mb: 1, fontSize: '1rem' }}>
                    Train {train.id} - Line {train.line}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    <strong>Direction:</strong> {train.direction}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    <strong>Speed:</strong> {train.speed}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Last updated: {new Date().toLocaleTimeString()}
                  </Typography>
                </Box>
              </Popup>
            </Marker>
          ))}

          {/* Simulated Circuit 1 */}
          <Circle
            center={[40.7559, -73.9862] as [number, number]} 
            radius={1500}
            color="#ff3333"
            fillColor="#ff3333"
            fillOpacity={0.1}
            weight={2}
          />

          {/* Simulated Circuit A  */}
          <Circle
            center={[40.7505, -73.9934] as [number, number]} 
            radius={1200}
            color="#0066cc"
            fillColor="#0066cc"
            fillOpacity={0.1}
            weight={2}
          />
        </MapContainer>
      </Box>

      {/* Map Legend */}
      <Box sx={{ padding: 2, textAlign: 'center', bgcolor: '#f5f5f5', borderRadius: 1, margin: { xs: 2, md: 4 }, mt: 2 }}>
        <Typography variant="body2" color="text.secondary">
          <span style={{ display: 'inline-block', width: 12, height: 12, backgroundColor: '#0039a6', borderRadius: 50, marginRight: 8 }}></span>
          Subway Station • 
          <span style={{ display: 'inline-block', width: 12, height: 12, backgroundColor: '#f44336', borderRadius: 50, margin: '0 8px' }}></span>
          Delayed Station • 
          <span style={{ display: 'inline-block', width: 12, height: 12, backgroundColor: '#ff3333', borderRadius: 50, margin: '0 8px' }}></span>
          Live Train
        </Typography>
      </Box>
    </Box>
  );
};

export default MapView;