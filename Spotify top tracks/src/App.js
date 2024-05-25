import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [artistName, setArtistName] = useState('');
  const [artistInfo, setArtistInfo] = useState(null);
  const [tracks, setTracks] = useState([]);

  const searchArtist = async () => {
    try {
      const response = await axios.get('http://localhost:5000/search_artist', {
        params: { artist_name: artistName }
      });
      setArtistInfo(response.data);

      const tracksResponse = await axios.get('http://localhost:5000/top_tracks', {
        params: { artist_id: response.data.id }
      });
      setTracks(tracksResponse.data);
    } catch (error) {
      console.error('Error fetching artist info or tracks:', error);
    }
  };

  return (
    <div className="App">
      <h1>Spotify Top Tracks</h1>
      <div className="search-box">
        <input
          type="text"
          value={artistName}
          onChange={(e) => setArtistName(e.target.value)}
          placeholder="Enter artist name"
        />
        <button className="green-button" onClick={searchArtist}>Get Top Tracks</button>
      </div>

      {artistInfo && (
        <div className="artist-info">
          <h2><strong>{artistInfo.name}</strong></h2>
          {artistInfo.image_url && <img src={artistInfo.image_url} alt={artistInfo.name} />}
        </div>
      )}

      <div className="song-list">
        <h2>Top Tracks</h2>
        <ul>
          {tracks.map((track, index) => (
            <li key={index}>
              <a href={track.url} target="_blank" rel="noopener noreferrer">{track.name}</a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
