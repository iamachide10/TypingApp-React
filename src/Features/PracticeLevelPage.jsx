import { useState ,useEffect} from "react";
import './PracticeLevelPageCss.css';
import { useParams } from "react-router-dom"
import { Link } from "react-router-dom";

const levels = {
  level1: { name: "ASDF", keys: ["a", "s", "d", "f"] },
  level2: { name: "JKL;", keys: ["j", "k", "l", ";"] },
  level3: { name: "ERUI", keys: ["e", "r", "u", "i"] },
  level4: { name: "QWOP", keys: ["q", "w", "o", "p"] },
  level5: { name: "ZXCVBNM", keys: ["z", "x", "c", "v", "b", "n", "m"] },
  level6: { name: "Full Keyboard", keys: "abcdefghijklmnopqrstuvwxyz".split("") },
  level7: { name: "Numbers", keys: "123456".split("") }
};




function PracticeLevelPage(){
    const [pauseDuration,setPauseDuration] = useState(0)
    const [pausedStartime,setPausedStartime]=useState(null)
    const [startTime,setStartTime]=useState(null)
    const [currentLetter,setCurrentLetter]=useState('')
    const [isFinished,setIsFinished] = useState(false)
    const [isPaused,setIsPaused] = useState(false)
    const [feedBack,setFeedBack]=useState('')
    const [correctCount,setCorrectCount]=useState(0)
    const [className,setClassName]=useState('')
    const [incorrectCount,setIncorrectCount]=useState(0)
    const {levelId}=useParams()

    const level=levels[levelId]




  //This use effect set current letter the moment the level changes
    useEffect(() =>{
        if(level) {
            setCurrentLetter(getCurrentLetter())
        }   
    } ,[level])

    //function to get current letter 
    const getCurrentLetter=()=>{
        const keys=level.keys
         const index = Math.floor(Math.random() * keys.length) 
        const newLetter = keys[index]
        return newLetter
    }

//This is the logic use to controll the pause system
    const handlePause=()=>{
      if(!isPaused ){
        setPausedStartime(Date.now()) 
        
      }else{
        const pauseTime = Date.now() - pausedStartime;    
        setPauseDuration(prev => prev + pauseTime);
        setPausedStartime(null);        
      }
      setIsPaused(prev =>!prev)
    }
   
    //This is use to track the key pressed
  const handleKeyPress=(e)=>{
                 
    if(isFinished || isPaused) return ;

    if(!startTime){
        setStartTime(Date.now())
    }

  const keyPressed = e.key.toLowerCase();

  if(keyPressed!=='escape'){
    if(currentLetter.toLowerCase() === keyPressed){
        setFeedBack('Correct!!')
        setCorrectCount(prev=>prev +1)
        setClassName('correct')
    }else{
        setFeedBack('Incorrect!!')
        setClassName('incorrect')
        setIncorrectCount(prev=>prev +1)
    }
  }
    if(correctCount + incorrectCount +1  >=30){
        setIsFinished(true)
    }else{
        setCurrentLetter(getCurrentLetter())
    }
  }
   
//htis onw handles the key pressed for the paused button
  useEffect(() => {
    window.addEventListener("keydown", pause); 
    return () => window.removeEventListener("keydown", pause);
  });


//This useEffect handles the the key pressed 
  useEffect(() => {
    window.addEventListener("keydown", handleKeyPress); 
    return () => window.removeEventListener("keydown", handleKeyPress);
  });


//This handles the pause we press on escape
  const pause = (e) => {
    if (e.key === 'Escape' || e.keyCode === 27) {
      handlePause();
    }
  };

 
//This calculate the accuracy for us  
  const getAccuracy = () =>{
    const total = correctCount + incorrectCount;
    return total ===0? 0:Math.round((correctCount/total)*100)

  }


  //This calculate the WPM for us 
  const getWPM = ()=>{
    if(!startTime) return 0;
    const now= Date.now();

    const totalPaused = isPaused && pausedStartime ? pauseDuration + (now -pausedStartime) : pauseDuration;

    const activeTime = now -startTime-totalPaused;
    const timeElasped = activeTime/1000/60;
    return timeElasped ===0 ? 0: Math.round((correctCount/5)/timeElasped)
  }

  //This handles the restart button, sets everything to the start
  const restart=()=>{
    setCorrectCount(0)
    setIncorrectCount(0)
    setStartTime(null)
    setIsFinished(false)
    setFeedBack("")
    setCurrentLetter(getCurrentLetter())
    setIsPaused(false)
    setPauseDuration(0)
  }

//This place displays when the level you clicked is not found
  if(!level) return <p>Level not found!!</p>

//This displays everything to you

return (
  <div className="practice-play-container">


      {!isFinished ? (
        <>
        <h1>{level.name} Practice</h1>
        <div className="container_items">
        <button onClick={handlePause}>{isPaused ? "Continue" : "Pause"}</button>
        <p>Correct: {correctCount}</p>
        <p>Incorrect: {incorrectCount}</p>
        <p>Accuracy: {getAccuracy()}%</p>
        <p>WPM: {getWPM()}</p>        
        <p>Typed: {correctCount + incorrectCount}</p>

        <div className="pause_pop" style={{display: isPaused ? 'flex' :'none' }}>
         
          <button onClick={restart}>Restart</button>
        <button ><Link to="/practice" style={{color:'white'}}>Levels Page</Link></button>
        </div>
        </div>
        <div className="letter-box" style={{borderColor: feedBack==='Incorrect!!' ? 'red':'green'}} >{currentLetter}</div>
        <p className={className}>{feedBack}</p>

        </>
      ):(
        <div>
      <h2 className="test-results">Level Completed !</h2>
      <p>Final Accuracy: {getAccuracy()}%</p>
      <p>WPM: {getWPM()}</p>
      <button onClick={restart}>Restart Level</button>
        <button ><Link to="/practice" style={{color:'white'}}>Levels Page</Link></button>
      </div>)}

     </div>
  );
}


export default PracticeLevelPage ;
