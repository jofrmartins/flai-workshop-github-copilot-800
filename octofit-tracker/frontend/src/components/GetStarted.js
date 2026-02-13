import React from 'react';
import CombinaBanner from './CombinaBanner';

function GetStarted() {
  return (
    <div className="container mt-4">
      {/* COMBINA Advertisement Banner */}
      <CombinaBanner />
      
      <h1>🚀 Get Started with OctoFit Tracker</h1>
      <p className="text-muted mb-4">Everything you need to know to begin your fitness journey!</p>

      <div className="row g-4">
        <div className="col-12">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title">📋 Quick Start Guide</h2>
              <p className="card-text">Follow these simple steps to get started:</p>
              
              <div className="mt-4">
                <h5>1️⃣ Create Your Profile</h5>
                <p>Visit the <a href="/users">Users</a> page to view user profiles and see how the system works.</p>
                
                <h5>2️⃣ Join a Team</h5>
                <p>Check out the <a href="/teams">Teams</a> page to see available teams and their members.</p>
                
                <h5>3️⃣ Log Your Activities</h5>
                <p>Start tracking your fitness journey by logging activities on the <a href="/activities">Activities</a> page.</p>
                
                <h5>4️⃣ Compete & Track Progress</h5>
                <p>View your ranking on the <a href="/leaderboard">Leaderboard</a> and see how you compare with others.</p>
                
                <h5>5️⃣ Get Workout Suggestions</h5>
                <p>Explore personalized <a href="/workouts">Workouts</a> tailored to your fitness level and goals.</p>
              </div>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card h-100">
            <div className="card-body">
              <h3 className="card-title">🎯 Key Features</h3>
              <ul>
                <li><strong>User Management:</strong> Track multiple users and their fitness profiles</li>
                <li><strong>Team Collaboration:</strong> Join teams and work together toward goals</li>
                <li><strong>Activity Tracking:</strong> Log runs, cycling, swimming, and more</li>
                <li><strong>Leaderboards:</strong> Competitive rankings to keep you motivated</li>
                <li><strong>Workout Plans:</strong> Personalized recommendations based on your progress</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card h-100">
            <div className="card-body">
              <h3 className="card-title">💡 Tips for Success</h3>
              <ul>
                <li>Log your activities consistently for better tracking</li>
                <li>Set realistic goals and celebrate small wins</li>
                <li>Engage with your team members for motivation</li>
                <li>Try different workout types to stay interested</li>
                <li>Monitor your progress on the leaderboard</li>
                <li>Follow the suggested workout plans</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="col-12">
          <div className="card bg-light">
            <div className="card-body">
              <h3 className="card-title">❓ Need Help?</h3>
              <p>
                If you have any questions or need assistance, explore each section using the navigation menu above.
                Each page provides detailed information about its specific functionality.
              </p>
              <p className="mb-0">
                <strong>Ready to start?</strong> Choose an option from the navigation menu or the home page cards!
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GetStarted;
