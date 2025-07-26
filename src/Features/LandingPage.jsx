import './LandingPageCss.css';
import { useState,useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';



function LandingPage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  const handleLogout = () => {
   localStorage.removeItem("user");
    setUser(null);
    navigate("/login");
  }

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  return (
    <div className="home-container">
      <h1 className="home-title">Typing Mastry</h1>
      <p className="home-subtitle">Sharpen your typing skills with fun and effective modes!</p>

      <div className="menu-buttons">
        <Link to="/practice">
          <button className="menu-button">Practice</button>
        </Link>
        <Link to="/test">
          <button className="menu-button">Test</button>
        </Link>
        <Link to="/settings">
          <button className="menu-button">Settings</button>
        </Link>

          {!user ? (
          <>
            <Link to="/login">
              <button className="menu-button secondary">Log In</button>
            </Link>
            <Link to="/create_account">
              <button className="menu-button secondary">Sign Up</button>
            </Link>
          </>
        ) : (
          <>
            <div className="user-info">
              <p>Welcome, {user.name}</p>
              {user.profile_image && (
                <img
                  src={`http://localhost:5000/static/uploads/${user.profile_image}`}
                  alt="Profile"
                  width="60"
                  style={{ borderRadius: "50%", marginTop: "10px" }}
                />
              )}
            </div>
            <button onClick={handleLogout} className="menu-button secondary">Logout</button>
          </>
        )}
     
      </div>
      </div>
  );
}

export default LandingPage;
