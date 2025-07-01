import './LandingPageCss.css'; // if the component is in the same folder

function LandingPage(){


    return(
        <div className="home-container">
            <h1 className="home-title">Typing Mastry</h1>
            <p className="home-subtitle">Sharpen your typing skills with fun and effective modes!</p>
          
           <div className="menu-buttons">
            <button className="btn">Practice</button>
            <button className="btn">Test</button>
            <button className="btn">Game</button>
           </div>

        </div>

    )
}

export default LandingPage;