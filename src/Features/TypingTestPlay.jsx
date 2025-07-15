import { useState,useEffect } from "react"
import { useLocation ,useNavigate} from "react-router-dom"
import './TypingTestPlavyCss.css';


const TypingTestPlay = () =>{
    const [startTime,setStartTime] =useState(null)
    const [isFinished,setIsFinished] =useState(false)
    const [timeLeft , setTimeLeft] =useState(null)
    const [textTyped,setTextTyped]=useState("")
    const {state} =useLocation()
    const {navigate} =useNavigate()
    const {passage, duration , titel} = state || {}

    useEffect(() => {
        if(startTime ) return ;
        const handleStart=()=>{
            setStartTime(Date.now())
        }
        window.addEventListener( "keydown" ,handleStart ,{once:true})
        return window.removeEventListener("keydown" ,handleStart)
    }, [startTime])


    useEffect(() =>{
        if(!startTime|| isFinished ) return ;

        const interval =setInterval(()=>{
            const timeElasped=Math.floor((Date.now() - startTime)/1000)
            const timeLefts = duration - timeElasped
            setTimeLeft(timeLefts)

            if(timeLefts <=0){
                clearInterval(interval)
                setIsFinished(true)
            }
        },1000)
        
        return clearInterval(interval)
        },[isFinished,startTime,duration])



        const getWPM =()=>{
            const timeElasped =( Date.now() - startTime)/1000/60
            const wordCount =textTyped.trim().split(/ \s+ /).length
            return Math.round(wordCount/timeElasped)||0
        }

        
    return (<>
    </>)
}