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
  level6: { name: "Full Keyboard", keys: "abcdefghijklmnopqrstuvwxyz".split("") }
};




function PracticeLevelPage(){
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





    useEffect(() =>{
        if(level) {
            setCurrentLetter(getCurrentLetter())
        }   
    } ,[level])


    const getCurrentLetter=()=>{
        const keys=level.keys
         const index = Math.floor(Math.random() * keys.length) 
        const newLetter = keys[index]
        return newLetter
    }


    const handlePause=()=>{
      setIsPaused(true)
    }
   
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
   
  
  useEffect(() => {
    window.addEventListener("keydown", pause);
    
    return () => window.removeEventListener("keydown", pause);
  });
  useEffect(() => {
    window.addEventListener("keydown", handleKeyPress);
    
    return () => window.removeEventListener("keydown", handleKeyPress);
  });

  const pause =(e)=>{
    if(e.key==='Escape' || e.keyCode ===27){
      if(isPaused){
        setIsPaused(false)
      }else{

        handlePause()
      }
    }
  }

 


  
  const getAccuracy = () =>{
    const total = correctCount + incorrectCount;
    return total ===0? 0:Math.round((correctCount/total)*100)

  }

  const getWPM = ()=>{
    const timeElapsed =(Date.now() - startTime)/1000/60;
    return timeElapsed ===0 ? 0 : Math.round((correctCount/5)/timeElapsed)

  }

  const restart=()=>{
    setCorrectCount(0)
    setIncorrectCount(0)
    setStartTime(null)
    setIsFinished(false)
    setFeedBack("")
    setCurrentLetter(getCurrentLetter())
    setIsPaused(false)
  }
  if(!level) return <p>Level not found!!</p>



return (
  <div className="practice-play-container">

    <h1>{level.name} Practice</h1>
    <div>{startTime}</div>
      {!isFinished ? (
        <>
        <div className="container_items">
        <button onClick={handlePause}>Pause</button>
        <p>Correct: {correctCount}</p>
        <p>Incorrect: {incorrectCount}</p>
        <p>Accuracy: {getAccuracy()}%</p>
        <p>WPM: {getWPM()}</p>        
        <p>Typed: {correctCount + incorrectCount}</p>

        <div className="pause_pop" style={{display: isPaused ? 'flex' :'none' }}>
          <button onClick={()=>setIsPaused(false)}>Continue</button>
          <button onClick={restart}>Restart</button>
        <button ><Link to="/practice" style={{color:'white'}}>Levels Page</Link></button>
        </div>
        </div>
        <div className="letter-box" style={{borderColor: feedBack==='Incorrect!!' ? 'red':'green'}} >{currentLetter}</div>
        <p className={className}>{feedBack}</p>

        </>
      ):(
        <>
      <h2>Level Completed !</h2>
      <p>Final Accuracy: {getAccuracy()}</p>
      <p>WPM: {getWPM()}</p>
      <button onClick={restart}>Restart Level</button>
        <button ><Link to="/practice" style={{color:'white'}}>Levels Page</Link></button>
      </>)}

     </div>
  );
}




export default PracticeLevelPage 
