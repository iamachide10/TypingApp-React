import { useNavigate } from "react-router-dom";
import './PracticeLevelsCss.css';
import { Link } from "react-router-dom";

function PracticeLevels() {
  const navigate = useNavigate()
const levels = [
  { id: "level1", title: "Level 1", keys: "ASDF", description: "Left-hand home row" },
  { id: "level2", title: "Level 2", keys: "JKL;", description: "Right-hand home row" },
  { id: "level3", title: "Level 3", keys: "E R U I", description: "Index finger stretch" },
  { id: "level4", title: "Level 4", keys: "Q W O P", description: "Outer keys" },
  { id: "level5", title: "Level 5", keys: "Z X C V B N M", description: "Bottom row" },
  { id: "level6", title: "Level 6", keys: "Full Keyboard", description: "All fingers practice" },
  { id: "level7", title: "Level 7", keys: "Numbers", description: "Number practice " },
];  
  
  return (
    <div className="levels-container">
      <h1 className="levels-title">   <button style={{marginRight:'10em'}} ><Link to="/" style={{color:'white'}}>Home</Link></button> Select a Practice Level</h1>
      <div className="levels-grid">
        {levels.map((level) => (
          <div key={level.id} className="level-card">
            <h2>{level.title}</h2>
            <p><strong>Keys:</strong> {level.keys}</p>
            <p>{level.description}</p>
            <button onClick={() => navigate(`/practice/${level.id}`)}>Start</button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default  PracticeLevels