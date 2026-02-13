import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
    console.log('Leaderboard - Fetching from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard - Processed data:', leaderboardData);
        setLeaderboard(leaderboardData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-container">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3 text-muted">Loading leaderboard...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error Loading Leaderboard</h4>
          <p className="mb-0">{error}</p>
        </div>
      </div>
    );
  }

  const getRankBadge = (rank) => {
    if (rank === 1) return <span className="rank-badge rank-1">🥇</span>;
    if (rank === 2) return <span className="rank-badge rank-2">🥈</span>;
    if (rank === 3) return <span className="rank-badge rank-3">🥉</span>;
    return <span className="badge bg-secondary">{rank}</span>;
  };

  return (
    <div className="container mt-4">
      <div className="mb-4">
        <h2>Leaderboard</h2>
        <p className="text-muted">
          Rankings based on total points
        </p>
      </div>
      
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th style={{width: '100px'}}>Rank</th>
              <th>User</th>
              <th>Total Points</th>
              <th>Activities</th>
              <th>Team</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center text-muted py-4">
                  No leaderboard data found
                </td>
              </tr>
            ) : (
              leaderboard.map((entry, index) => {
                const rank = index + 1;
                return (
                  <tr key={entry.id || index} className={rank <= 3 ? 'table-active' : ''}>
                    <td className="text-center">{getRankBadge(rank)}</td>
                    <td><strong>{entry.user_name || entry.user || 'N/A'}</strong></td>
                    <td>
                      <span className="badge bg-primary" style={{fontSize: '1rem'}}>
                        {entry.total_points} pts
                      </span>
                    </td>
                    <td>
                      <span className="badge bg-info text-dark">
                        {entry.total_activities || 0} activities
                      </span>
                    </td>
                    <td>{entry.team_name || entry.team || 'N/A'}</td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
