import { useState ,useEffect} from "react"
import styles from  "./AccountSettings.module.css"


const AccountSettings =()=>{
    const [name,setName]=useState("User 1.0")
    const [email,setEmail]=useState("User 1.0@gmail.com")
    const [profile_image,setProfile]=useState("")

    const userData =JSON.parse(localStorage.getItem("user")) 
    useEffect(()=>{
        if(userData){
            setName(userData.userName)
            setEmail(userData.email)
            if(userData.profile_image==!null || userData.profile_image){
                setProfile(userData.profile_image)
            }
        }

    },[])

    const handleSave=()=>{
        const settins={
            name,
            email
        }
        alert("Account settings saved succefully.")
    }



    return(

        <div className={styles.accountContainer}>
            <h2>Account Settings</h2>

             {profile_image && (
                <img
                  src={`${profile_image}`}
                  alt="Profile"
                />
              )}
            <div className={styles.settingGroup}>
                <label > Display Name: </label>
                <input type="text" value={name}  onChange={(e)=>setName(e.target.value)}/>
            </div>

            <div className={styles.settingGroup}>
                <label > Email:</label>
                <input type="text" value={email}  onChange={(e)=>setEmail(e.target.value)}/>
            </div>
            <button onClick={handleSave} > Save Settings</button>
        </div>

    )

}


export default AccountSettings