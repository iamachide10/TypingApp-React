import { useState,useEffect, use } from "react"
import TypingBox from "./TypingBox";
import TypingInput from "./TypingInput";
import { useLocation ,useNavigate} from "react-router-dom"
import './TypingTestPlayCss.css';


const TypingTestPlay = () =>{

    const [startTime,setStartTime] =useState(null)
    const [isFinished,setIsFinished] =useState(false)
    const [timeLeft , setTimeLeft] =useState(null)
    const [wpm, setWPM]=useState(0)
    const [accuracy,setAccuracy]=useState(0)
    const [pauseDuration,setPauseDuration]=useState(0)
    const [pausedStartTime,setPausedStartTime] = useState()
    const [textTyped,setTextTyped]=useState("")
    const [isPaused , setIsPaused] = useState(false)
    const [finalStats,setFinalStats]=useState(null)
    const {state} =useLocation()
    const navigate = useNavigate();
    const {passage, duration , title} = state || {}



    const handlePause =()=>{

        if(!isPaused){
            setPausedStartTime(Date.now())
        }else{
            const duration = Date.now()-pausedStartTime
            setPauseDuration(prev =>prev+duration)
            setPausedStartTime(null)
        }
        setIsPaused(prev=>!prev )   
    }



    useEffect(() => {
        if(startTime ) return ;

        const handleStart=()=>{
            setStartTime(Date.now())
        }
        window.addEventListener( "keydown" ,handleStart ,{once:true})
        return ()=> window.removeEventListener("keydown" ,handleStart)
    }, [startTime])
    

    useEffect(() => {
        if (isFinished) {
            const finalWPM = getWPM();
            const finalAccuracy = getAccuracy();
            setFinalStats({ wpm: finalWPM, accuracy: finalAccuracy }); 
            setAccuracy(finalAccuracy)
            setWPM(finalWPM)
            // keep them frozen}
    } },[isFinished])



    useEffect(() =>{
        if(!startTime|| isFinished ) return;

        const interval =setInterval(()=>{
            if(isPaused) return;
            const totalPaused = isPaused && pausedStartTime ? pauseDuration +(Date.now() - pausedStartTime):pauseDuration;

            const timeElasped=Math.floor((Date.now() - startTime-totalPaused)/1000)
            const timeLefts = duration - timeElasped
            setTimeLeft(timeLefts)

            if(timeLefts <=0 ){
                clearInterval(interval)
                setIsFinished(true)
            }  
        },1000)
        
        return ()=> clearInterval(interval)
        } , [isFinished,startTime,duration])




        useEffect(()=>{
            if(textTyped.trim() === passage.trim()){
                setIsFinished(true)
            }
        },[textTyped,passage])


        const user= localStorage.getItem("user")


        useEffect(()=>{ 
            const saveResult = async()=>{
            
            if(isFinished && user && finalStats){
                const userData = JSON.parse(user)
                const userId = userData.user_id
                console.log(wpm,accuracy)
                const API_URL = process.env.REACT_APP_API_URL;
                const url=  `${API_URL}/history`
                const options ={
                    method: "POST",
                    headers: {
                    "Content-Type":"application/json",
                    },
                    body: JSON.stringify({
                    wpm,
                    accuracy,   
                    score: Math.round(wpm * (accuracy)),
                    }),    
                }
                const response = await fetch (url, options)
                const result = await response.json();
                if(response.ok){
                    console.log("Result saved:", result);
                }
                else {
                    alert("Error: " + result.message);
                }   
            }
        }
        saveResult()
    },[finalStats])




        const getWPM =()=>{
            const now =Date.now()
            const totalPaused=isPaused && pausedStartTime ? pauseDuration +(now - pausedStartTime):pauseDuration
            const timeElasped = (now-startTime -totalPaused)/1000/60 
           const wordCount = textTyped.trim().split(/\s+/).length;
            return timeElasped ===0? 0 : Math.round(wordCount/timeElasped)||0
        }


        const getAccuracy=()=>{
            let correct = 0
            for(let i=0; i <textTyped.length; i++  ) {
                if(textTyped[i]===passage[i]) {
                 correct+=1  
                }
            }
            const totalTyped=textTyped.length
            return totalTyped ===0? 0: Math.round((correct/totalTyped) * 100)
        }

const handleRestart = () => {
  setStartTime(null);
  setIsFinished(false);
  setTimeLeft(null);
  setPauseDuration(0);
  setPausedStartTime(null);
  setTextTyped("");
  setIsPaused(false);
  setFinalStats(null)
};





return (<>
    <div className="typing-play-container">
    {!isFinished ? (
        <div>
        <TypingBox text={passage} userInput={textTyped} />
          <TypingInput userInput={textTyped} setUserInput={setTextTyped} />
        </div>
    ):
    (<div className="test-results">
        <h3>Test Completed</h3>
       <p>
        WPM: <strong>{wpm}</strong>
        </p> 
        <p>Accuracy : <strong>{accuracy}</strong></p>
        <button onClick={()=>handleRestart()} >Try Again </button>
    </div>
    )}
    </div>
    </>)
}

 export default TypingTestPlay;