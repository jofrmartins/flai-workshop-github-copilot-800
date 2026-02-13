import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Workouts - Fetching from:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts - Processed data:', workoutsData);
        setWorkouts(workoutsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts - Error fetching data:', error);
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
          <p className="mt-3 text-muted">Loading workouts...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error Loading Workouts</h4>
          <p className="mb-0">{error}</p>
        </div>
      </div>
    );
  }

  const getDifficultyBadge = (difficulty) => {
    const difficultyLower = difficulty?.toLowerCase() || '';
    let badgeClass = 'bg-secondary';
    let icon = '';
    
    if (difficultyLower === 'easy') {
      badgeClass = 'bg-success';
      icon = '✓';
    } else if (difficultyLower === 'medium') {
      badgeClass = 'bg-warning text-dark';
      icon = '⦿';
    } else if (difficultyLower === 'hard') {
      badgeClass = 'bg-danger';
      icon = '⚠';
    }
    
    return (
      <span className={`badge ${badgeClass}`}>
        {icon} {difficulty}
      </span>
    );
  };

  return (
    <div className="container mt-4">
      <div className="mb-4">
        <h2>Workout Suggestions</h2>
        <p className="text-muted">
          Personalized workout recommendations to help you reach your fitness goals
        </p>
      </div>
      
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Duration (min)</th>
              <th>Difficulty</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {workouts.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center text-muted py-4">
                  No workout suggestions available
                </td>
              </tr>
            ) : (
              workouts.map((workout, index) => (
                <tr key={workout.id || index}>
                  <td><strong>{workout.name}</strong></td>
                  <td>
                    <span className="badge bg-info text-dark">
                      {workout.workout_type || workout.type}
                    </span>
                  </td>
                  <td>
                    <span className="badge bg-primary">
                      {workout.duration} min
                    </span>
                  </td>
                  <td>{getDifficultyBadge(workout.difficulty)}</td>
                  <td>{workout.description}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Workouts;
