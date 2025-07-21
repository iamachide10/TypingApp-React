import { useState } from "react"
import styles from "./GeneralSettings.module.css"

const GeneralSettings =()=>{
    const [duration,setDuration]=useState("15")
    const [difficulty,setDifficulty]=useState("medium")
    const [mode,setMode]=useState("words")
    const [autoStart,setAutoStart]=useState(true)
    const [sound,setSound]=useState(true)

    const handleSave =()=>{
        const settings ={
            duration,
            difficulty,
            mode,
            autoStart,
            sound
        }
        console.log("These settings were saved",settings);
        alert("Settings saved succesfully")
        }

    return(
        <div className={styles.generalContainer}>
            <h2>General Preferences</h2>
            <div className={styles.settingGroup}>  
                <label >Default Duration:</label>
                <select value ={duration} onChange={(e)=>setDuration(e.target.value)}>
                    <option value="15">15 seconds</option>
                    <option value="30">30 seconds</option>
                    <option value="60">60 seconds</option>
                    <option value="120">120 seconds</option>
                </select>
            </div>

            <div className={styles.settingGroup}>
                <label >Dificulty:</label>
                <select  value={ difficulty }  onChange={(e)=>setDifficulty(e.target.value)}>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
                </select>
            </div>

            <div className={styles.settingGroup}>
                <label > Test Mode:</label>
                <select value={mode} onChange={(e)=>setMode(e.target.value)}>
                    <option value="words">Words</option>
                    <option value="setences">Sentences</option>
                    <option value="custom">Custom Passage</option>
                </select>
            </div>

            <div className={styles.settingGroupCheckbox}>
                <label > <input type="checkbox" checked={autoStart} onChange={()=>setAutoStart(!autoStart)} />
                Auto Start Test 
                </label>
            </div>

            <div className={styles.settingGroupCheckbox}>
                <label > <input type="checkbox" checked={sound} onChange={()=>setSound(!sound)} />
                Enable Sound Effect
                </label>
            </div>

            <button className={styles.saveBtn} onClick={handleSave}> Save settings</button>
        </div>
    )
}


export default GeneralSettings