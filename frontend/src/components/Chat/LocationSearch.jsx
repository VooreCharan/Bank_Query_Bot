import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaMapMarkerAlt, FaSearch, FaCrosshairs, FaTimes } from 'react-icons/fa';
import axios from 'axios';
import { toast } from 'react-toastify';
import '../../styles/LocationSearch.css';

const LocationSearch = ({ onClose, onLocationSelect }) => {
  const [location, setLocation] = useState('');
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState([]);
  const [gettingLocation, setGettingLocation] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  const handleSearch = async () => {
    if (!location.trim()) {
      toast.error('Please enter a location');
      return;
    }

    setSearching(true);
    
    try {
      const token = localStorage.getItem('auth_token');
      
      console.log('='.repeat(60));
      console.log('LOCATION SEARCH REQUEST');
      console.log('='.repeat(60));
      console.log('Location:', location);
      console.log('Token:', token ? 'Present' : 'Missing');
      console.log('API URL:', `${API_URL}/location/search`);
      
      const requestData = { 
        location: location.trim(),
        limit: 10 
      };
      
      console.log('Request data:', requestData);
      
      const response = await axios.post(
        `${API_URL}/location/search`,
        requestData,
        { 
          headers: { 
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
          } 
        }
      );

      console.log('Response received:', response.data);
      console.log('='.repeat(60));

      if (response.data.success) {
        setResults(response.data.results);
        if (response.data.count > 0) {
          toast.success(`Found ${response.data.count} location${response.data.count > 1 ? 's' : ''}`);
        } else {
          toast.info(response.data.error || 'No locations found in this area');
        }
      } else {
        toast.error(response.data.error || 'No results found');
        setResults([]);
      }
    } catch (error) {
      console.error('='.repeat(60));
      console.error('LOCATION SEARCH ERROR');
      console.error('='.repeat(60));
      console.error('Error:', error);
      
      if (error.response) {
        console.error('Status:', error.response.status);
        console.error('Data:', error.response.data);
        console.error('Headers:', error.response.headers);
        
        const errorMsg = error.response.data?.error || 
                        error.response.data?.message || 
                        `Error ${error.response.status}`;
        toast.error(errorMsg);
      } else if (error.request) {
        console.error('No response received');
        console.error('Request:', error.request);
        toast.error('No response from server. Please check your connection.');
      } else {
        console.error('Request setup error:', error.message);
        toast.error('Failed to make request: ' + error.message);
      }
      console.error('='.repeat(60));
      setResults([]);
    } finally {
      setSearching(false);
    }
  };

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      toast.error('Geolocation is not supported by your browser');
      return;
    }

    setGettingLocation(true);
    toast.info('Getting your location...');

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        const coordString = `${latitude.toFixed(6)}, ${longitude.toFixed(6)}`;
        setLocation(coordString);
        toast.success('Location detected!');
        setGettingLocation(false);
        
        // Auto-search with current location
        await handleSearchWithCoords(latitude, longitude);
      },
      (error) => {
        console.error('Geolocation error:', error);
        let errorMessage = 'Failed to get your location';
        
        switch(error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location permission denied. Please enable location access.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information unavailable';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timed out';
            break;
          default:
            errorMessage = 'An unknown error occurred';
        }
        
        toast.error(errorMessage);
        setGettingLocation(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  };

  const handleSearchWithCoords = async (lat, lon) => {
    setSearching(true);
    
    try {
      const token = localStorage.getItem('auth_token');
      const coordLocation = `${lat.toFixed(6)}, ${lon.toFixed(6)}`;
      
      console.log('Searching with coordinates:', coordLocation);
      
      const response = await axios.post(
        `${API_URL}/location/search`,
        { location: coordLocation, limit: 10 },
        { 
          headers: { 
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
          } 
        }
      );

      console.log('Coordinates search response:', response.data);

      if (response.data.success && response.data.results) {
        setResults(response.data.results);
        if (response.data.count > 0) {
          toast.success(`Found ${response.data.count} nearby location${response.data.count > 1 ? 's' : ''}`);
        } else {
          toast.info('No banks or ATMs found within 5km');
        }
      } else {
        toast.warning(response.data.error || 'No results found nearby');
        setResults([]);
      }
    } catch (error) {
      console.error('Coordinate search error:', error);
      toast.error('Failed to search nearby locations');
      setResults([]);
    } finally {
      setSearching(false);
    }
  };

  const handleSelectLocation = (bank) => {
    console.log('Location selected:', bank);
    if (onLocationSelect) {
      onLocationSelect(bank);
    }
    // Don't close modal automatically - let parent handle it
  };

  return (
    <motion.div
      className="location-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="location-modal"
        initial={{ scale: 0.9, y: 50 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.9, y: 50 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="location-header">
          <h2><FaMapMarkerAlt /> Find Banks & ATMs</h2>
          <button className="close-btn" onClick={onClose} title="Close">
            <FaTimes />
          </button>
        </div>

        <div className="location-search-bar">
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter city, area, or address..."
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            disabled={searching || gettingLocation}
          />
          <motion.button
            className="current-location-btn"
            onClick={getCurrentLocation}
            disabled={gettingLocation || searching}
            whileHover={{ scale: gettingLocation ? 1 : 1.05 }}
            whileTap={{ scale: gettingLocation ? 1 : 0.95 }}
            title="Use your current location"
          >
            <FaCrosshairs /> {gettingLocation ? 'Getting...' : 'Current Location'}
          </motion.button>
          <motion.button
            className="search-btn"
            onClick={handleSearch}
            disabled={searching || gettingLocation || !location.trim()}
            whileHover={{ scale: searching ? 1 : 1.05 }}
            whileTap={{ scale: searching ? 1 : 0.95 }}
            title="Search for banks and ATMs"
          >
            <FaSearch /> {searching ? 'Searching...' : 'Search'}
          </motion.button>
        </div>

        <div className="location-results">
          {searching ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Searching for nearby banks and ATMs...</p>
            </div>
          ) : results.length > 0 ? (
            <AnimatePresence>
              {results.map((bank, index) => (
                <motion.div
                  key={`${bank.lat}-${bank.lon}-${index}`}
                  className="location-card"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => handleSelectLocation(bank)}
                >
                  <div className="location-icon">
                    {bank.type === 'BANK' ? '🏦' : '🏧'}
                  </div>
                  <div className="location-info">
                    <h3>{bank.name}</h3>
                    <p className="location-type">
                      {bank.type}
                      {bank.brand && ` • ${bank.brand}`}
                    </p>
                    <p className="location-address">{bank.address}</p>
                    <div className="location-meta">
                      <span className="distance">📍 {bank.distance_km} km away</span>
                      {bank.phone && <span className="phone">📞 {bank.phone}</span>}
                    </div>
                    {bank.opening_hours && (
                      <p className="opening-hours">⏰ {bank.opening_hours}</p>
                    )}
                  </div>
                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${bank.lat},${bank.lon}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="map-link"
                    onClick={(e) => e.stopPropagation()}
                    title="Open in Google Maps"
                  >
                    View on Map →
                  </a>
                </motion.div>
              ))}
            </AnimatePresence>
          ) : (
            <div className="no-results">
              <FaMapMarkerAlt size={48} />
              <p>Enter a location to find nearby banks and ATMs</p>
              <small>Try: "Mumbai", "Bangalore MG Road", or use your current location</small>
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

export default LocationSearch;
