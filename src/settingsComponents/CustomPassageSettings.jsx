import { useState } from "react"
import styles from "./CustomPassageSettingsCss.module.css"

const CustomPassageSettings =()=>{
const [CustomPassage,setCustomPassage]=useState({
    title:"",
    content:""
})


const handlePassageChange=(e)=>{
    const {name,value} = e.target;

    setCustomPassage(prev=>({
        ...prev,
        [name]:value
    }))

}

const handleSave =async()=>{
    console.log(CustomPassage)

    const url ="http://127.0.0.1:5000/login"
    const options={
        method:"POSt",
        body:CustomPassage
    }
    try{
        const response=await  fetch(url,options)
    }catch(error){
        alert(error)
    }

}


return(
    <div className={styles.section}>
        <h3 className={styles.subheader}> Custom Passage</h3>

        <label className={styles.label}> Passage Title:</label>
        <input  type="text" name="title" value={CustomPassage.title} onChange={handlePassageChange} className={styles.title} placeholder="e.g. Motivational Story" />
        <label style={styles.label}> Passage Content:</label>
        <textarea   type="text" name="content" value={CustomPassage.content} onChange={handlePassageChange} className={styles.content} placeholder="Paste or type your custom passage here ..." />

        <button onClick={handleSave} >Save settings</button>


    </div>
)
}


export default CustomPassageSettings