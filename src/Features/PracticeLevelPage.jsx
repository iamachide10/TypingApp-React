import { useState ,useEffect} from "react";

import { useParams } from "react-router-dom"
const levels = {
  level1: { name: "ASDF", keys: ["a", "s", "d", "f"] },
  level2: { name: "JKL;", keys: ["j", "k", "l", ";"] },
  level3: { name: "ERUI", keys: ["e", "r", "u", "i"] },
  level4: { name: "QWOP", keys: ["q", "w", "o", "p"] },
  level5: { name: "ZXCVBNM", keys: ["z", "x", "c", "v", "b", "n", "m"] },
  level6: { name: "Full Keyboard", keys: "abcdefghijklmnopqrstuvwxyz".split("") }
};




function PracticeLevelPage(){
    const [startTime,setStartTime]=useState(null)
    const [currentLetter,setCurrentLetter]=useState('')
    const [isFinished,setIsFinished] = useState(false)
    const [feedBack,setFeedBack]=useState('')
    const [correctCount,setCorrectCount]=useState(0)
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

   
  const handleKeyPress=(e)=>{
    if(isFinished) return ;

    if(!startTime){
        setStartTime(Date.now())
    }

    const keyPressed = e.key.toLowerCase();
    if(currentLetter.toLowerCase() === keyPressed){
        setFeedBack('Correct!!')
        setCorrectCount(prev=>prev +1)
    }else{
        setFeedBack('Incorrect!!')
        setIncorrectCount(prev=>prev +1)
    }

    if(correctCount + incorrectCount +1  >=20){
        setIsFinished(true)
    }else{
        setCurrentLetter(getCurrentLetter())
    }
    
  }
   
  
    useEffect(() => {
    window.addEventListener("keydown", handleKeyPress);
    
    return () => window.removeEventListener("keydown", handleKeyPress);
  });





return(
    <div>
        <h1>{currentLetter}</h1>
        <h2>{feedBack}</h2>
        <h2>Incorrects: {incorrectCount}</h2>
        <h2>Corrects: {correctCount}</h2>
        <>{startTime}</>
    </div>
)

}

export default PracticeLevelPage 