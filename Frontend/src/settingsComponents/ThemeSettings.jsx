import { useState ,useEffect} from "react"
import styles from "./ThemeSettings.module.css"


const ThemeSettings=()=>{
    const [theme,setTheme]=useState("light")
    const [accentColor,setAccentColor]=useState("red")
    const [textSize,setTextSize]=useState("medium")
    const [font,setFont]=useState("sans-serif")
    const [userId,setUserId] = useState(null)


    const userData = JSON.parse(localStorage.getItem("user"));

    useEffect(()=>{
        if(userData){  
            setUserId(userData.user_id)
            const themeSettingsData= localStorage.getItem("themeSettings")
            if(themeSettingsData){
                const themeSettings = JSON.parse(themeSettingsData)
                setTheme(themeSettings.theme || "light")
                setAccentColor(themeSettings.accentColor || "red")
                setTextSize(themeSettings.textSize || "medium")
                setFont(themeSettings.font || "sans-serif")
            } 
        }
    }, [])


    

 
    const handleSave= async()=>{
        if(userId){
            try{
            const API_URL = process.env.REACT_APP_API_URL;
             const url =` ${API_URL}/theme-settings`
             const options ={
                method: "POST",
                headers: {
                "Content-Type":"application/json",
                body: JSON.stringify({
                generalSettings: {
                theme,
                accentColor,
                textSize,
                font
                },
              }),
              },
            }
    
          const response = await fetch (url, options)
            
          const result = await response.json();
          if(response.ok){
    
            localStorage.setItem(
              "themeSettings",
              JSON.stringify(result.settings)
            );
            
          }else {
            alert("Error: " + result.Message);
          }
            }catch(e){
                console.log("Erro: " + {e})
            }
        }
        else{
            alert("Log in or sign up first.")
        }
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
            <select onChange={(e)=>setFont(e.target.value)}>
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