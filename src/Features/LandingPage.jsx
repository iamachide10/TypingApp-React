import './LandingPageCss.css';
import { Link } from 'react-router-dom';


function LandingPage(){
    


    return(
        <div className="home-container">
            <h1 className="home-title">Typing Mastry</h1>
            <p className="home-subtitle">Sharpen your typing skills with fun and effective modes!</p>
          
           <div className="menu-buttons">
            <Link to="/practice" >
            <button  >Practice</button>
            </Link>
            
            <Link to="/test" >
            <button >Test</button>
            </Link>
            
            <Link to="/settings" >
            <button >Settings</button>
            </Link>
            
            <Link to="/login" >
            <button >Log In</button>
            </Link>
            
            <Link to="/create_account" >
            <button >Sing Up</button>
            </Link>
           </div>

        </div>

    )
}

export default LandingPage;