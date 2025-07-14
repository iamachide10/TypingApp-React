import { useState } from "react";
import { useNavigate } from "react-router-dom";
import './TypingTestSelectCss.css';

const passages =[
    {
        id:'p1',
        title:'A simple story',
        text:'Once upon ar time there lived a cat who loved to nap under the sun.'
    },
    {
        id:'p2',
        title:'Tech Documentary',
        text:'React is JavaScript library used to build interactive user interfaces efficiently.'
    }
]


const TypingTestSelect =()=>{
    const navigate = useNavigate()
    const [customText, setCustomText ]=useState('')
    const [duration,setDuration]=useState(60)


    const handlePredefined =(passage)=>{
        if(duration){
            navigate("play", {
                state:{
                    passage:passage.text ,duration , title:passage.title
                }
            })
        }else{
            alert("Choose duration")
        }
    }


    const handleCustom =( )=>{
        if( !customText.trim()) return;

         navigate("play", {
            state:{
                passage:customText ,duration , title:"Custom passage"
            }
        })
    }


    return (
        <div className="typing-select-container">
            <h1>Typing Test</h1>
            <h2>Choose a Predefined Passage:</h2>
            <div className="passage-list">
                { passages.map((passage ) =>(
                    <div className="passage-card" key={passage.id}> 
                    <h3>{passage.title}</h3>
                    <p>{passage.text.slice(0,50)}...</p>
                    <button onClick={() =>handlePredefined(passage)}> Start</button>
                    </div>
                ))}
            </div>

            <h2>Or Paste your own:</h2>
            <textarea  placeholder="Paste your own paragraph here ..." value={customText} onChange={(e)=> setCustomText(e.target.value)}></textarea>
            <label>
                Duration: 
                <select value={ duration } onChange={(e) => setDuration(Number(e.target.value))}>
                    <option value={30}>30 seconds</option>
                    <option value={60}>60 seconds</option>
                    <option value={120}>120 seconds</option>
                    <option value={300}>300 seconds</option>
                    <option value={500}>500 seconds</option>
                </select>
            </label>
            <button onClick={handleCustom}>Start Custom test</button>

        </div>
    )
}


export default TypingTestSelect;