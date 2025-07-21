import { useState } from "react"
import styles from  "./AccountSettings.module.css"

const AccountSettings =()=>{
    const [name,setName]=useState("User 1.0")
    const [email,setEmail]=useState("User 1.0@gmail.com")
    const [password,setPassword]=useState("1234567")

    const handleSave=()=>{
        const settins={
            name,
            password,
            email
        }

        alert("Account settings saved succefully.")
    }


    return(
        <div className={styles.accountContainer}>
            <h2>Account Settings</h2>
            <div className={styles.settingGroup}>
                <label > Display Name: </label>
                <input type="text" value={name}  onChange={(e)=>setName(e.target.value)}/>
            </div>

            <div className={styles.settingGroup}>
                <label > Email:</label>
                <input type="text" value={email}  onChange={(e)=>setEmail(e.target.value)}/>
            </div>

            <div className={styles.settingGroup}>
                <label > New Password:</label>
                <input type="password" value={password}  placeholder=" Leave blank to keep the old one."onChange={(e)=>setPassword(e.target.value)}/>
            </div>

            <button onClick={handleSave} > Save Settings</button>

        </div>
    )

}


export default AccountSettings