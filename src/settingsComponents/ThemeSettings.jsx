import { useState } from "react"
import styles from "./ThemeSettings.module.css"
/*
theme
accent red blue green
font sytel mono space,sans-serif,serif
text soze small , medium , large
save theme button
 */

const ThemeSettings=()=>{
    const [theme,setTheme]=useState("light")
    const [accentColor,setAccentColor]=useState("red")
    const [textSize,setTextSize]=useState("medium")
    const [font,setFont]=useState("sans-serif")

    const handleSave=()=>{
        const settings ={
            theme,
            accentColor,
            textSize,
            font
        }
        console.log("These theme settings were saved",settings ); 
        alert("Settings save successfully.")
    }

    return(
    <div className={styles.themeContainer}>
        <div className={styles.settingGroup}>
            <label >Theme Mode:</label>
            <select onChange={(e)=>setTheme(e.target.value)}>
                <option value="dark">Dark</option>
                <option value="light">Light</option>
                <option value="system">System Default</option>
            </select>
        </div>

         <div className={styles.settingGroup}>
            <label >Accent Color:</label>
            <select onChange={(e)=>setAccentColor(e.target.value)}>
                <option value="blue">Blue</option>
                <option value="red">Red</option>
                <option value="green">Green</option>
            </select>
        </div>

         <div className={styles.settingGroup}>
            <label >Text Size:</label>
            <select onChange={(e)=>setTextSize(e.target.value)}>
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
            </select>
        </div>

         <div className={styles.settingGroup}>
            <label >Font Style:</label>
            <select onChange={(e)=>setTextSize(e.target.value)}>
                <option value="monospace">Monospace</option>
                <option value="sans-serif">Sans-serif</option>
                <option value="Serif">Serif</option>
            </select>
        </div>

        <button className={styles.saveBtn} onClick={handleSave}> Save Theme Settings</button>
    </div>
    )
}


export default ThemeSettings