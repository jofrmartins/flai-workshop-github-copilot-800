import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';
import GetStarted from './components/GetStarted';
import logo from './octofitapp-small.png';

function App() {
  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            <img src={logo} alt="OctoFit Logo" className="navbar-logo" />
            OctoFit Tracker
          </Link>
          <button 
            className="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav"
            aria-controls="navbarNav" 
            aria-expanded="false" 
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link" to="/users">Users</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/teams">Teams</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/activities">Activities</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/workouts">Workouts</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={
          <div className="container mt-5">
            <div className="text-center mb-5">
              <h1 className="display-4 fw-bold">Welcome to OctoFit Tracker</h1>
              <p className="lead text-muted">Track your fitness activities and compete with your team!</p>
            </div>
            
            <div className="row g-4">
              <div className="col-md-6 col-lg-4">
                <div className="card h-100">
                  <div className="card-body text-center">
                    <div className="display-4 mb-3">👥</div>
                    <h5 className="card-title">Users</h5>
                    <p className="card-text">View all registered users and their profiles.</p>
                    <Link to="/users" className="btn btn-primary">View Users</Link>
                  </div>
                </div>
              </div>
              
              <div className="col-md-6 col-lg-4">
                <div className="card h-100">
                  <div className="card-body text-center">
                    <div className="display-4 mb-3">🤝</div>
                    <h5 className="card-title">Teams</h5>
                    <p className="card-text">Browse all teams and their members.</p>
                    <Link to="/teams" className="btn btn-primary">View Teams</Link>
                  </div>
                </div>
              </div>
              
              <div className="col-md-6 col-lg-4">
                <div className="card h-100">
                  <div className="card-body text-center">
                    <div className="display-4 mb-3">🏃</div>
                    <h5 className="card-title">Activities</h5>
                    <p className="card-text">See recent fitness activities logged by users.</p>
                    <Link to="/activities" className="btn btn-primary">View Activities</Link>
                  </div>
                </div>
              </div>
              
              <div className="col-md-6 col-lg-4">
                <div className="card h-100">
                  <div className="card-body text-center">
                    <div className="display-4 mb-3">🏆</div>
                    <h5 className="card-title">Leaderboard</h5>
                    <p className="card-text">Check out the competitive rankings.</p>
                    <Link to="/leaderboard" className="btn btn-primary">View Leaderboard</Link>
                  </div>
                </div>
              </div>
              
              <div className="col-md-6 col-lg-4">
                <div className="card h-100">
                  <div className="card-body text-center">
                    <div className="display-4 mb-3">💪</div>
                    <h5 className="card-title">Workouts</h5>
                    <p className="card-text">Get personalized workout suggestions.</p>
                    <Link to="/workouts" className="btn btn-primary">View Workouts</Link>
                  </div>
                </div>
              </div>
              
              <div className="col-md-6 col-lg-4">
                <div className="card h-100">
                  <div className="card-body text-center">
                    <div className="display-4 mb-3">✨</div>
                    <h5 className="card-title">Get Started</h5>
                    <p className="card-text">Join a team and start tracking your fitness journey today!</p>
                    <Link to="/get-started" className="btn btn-success">Get Started</Link>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="row mt-5">
              <div className="col-12">
                <div className="alert alert-info" role="alert">
                  <h4 className="alert-heading">🎯 About OctoFit Tracker</h4>
                  <p>
                    OctoFit Tracker is your comprehensive fitness companion designed to help you stay motivated and achieve your health goals.
                    Track activities, join teams, compete on leaderboards, and get personalized workout recommendations.
                  </p>
                  <hr/>
                  <p className="mb-0">
                    <strong>Features:</strong> User Profiles • Team Management • Activity Logging • Competitive Leaderboards • Workout Suggestions
                  </p>
                </div>
              </div>
            </div>
          </div>
        } />
        <Route path="/users" element={<Users />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/activities" element={<Activities />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/workouts" element={<Workouts />} />
        <Route path="/get-started" element={<GetStarted />} />
      </Routes>
    </div>
  );
}

export default App;
