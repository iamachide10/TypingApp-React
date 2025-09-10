import { use, useState } from "react";
import styles from  "./createAccountCss.module.css"
import { useNavigate } from "react-router-dom";


function CreateAccount(){
    const [preview,setPreview]=useState("")
    const [name,setName]=useState("")
    const [email,setEmail]=useState("")
    const [password,setPassword]=useState("")
    const [confirmPassword,setconfirmPassword]=useState("")
    const [profilePic ,setProfilePic]=useState(null)

    const  navigate =   useNavigate();
    const handleSubmit = async(e)=>{
      e.preventDefault()

      if(password !==confirmPassword){
        alert("Password doesnt match.")
        return
      }

      const dataContainer= new FormData();
      dataContainer.append("email",email)
      dataContainer.append("name",name)
      dataContainer.append("password",password)
      if(profilePic){
        dataContainer.append("profile_image", profilePic)
      }
      try{
        const API_URL = process.env.REACT_APP_API_URL;
        const url = `${API_URL}/sign_in`;

        const options = {
        method: "POST",
        body: dataContainer
        };
        
        const response=await  fetch(url,options)
        const data=await response.json()
        const m= data.message
        alert(m)
         window.location.href = "/login";
      }catch(error){
        alert(error)
      } 
    
    //  navigate("/login");
    }

    const handleImageChange =(e)=>{
        const file=e.target.files[0]
        if(file){
            setProfilePic(file)
            setPreview(URL.createObjectURL(file))
        }
    }

    return(
        <div className={styles.login_container}>
            <h2 >Create Account </h2>
            <form onSubmit={handleSubmit}>
                <div className={styles.imageSection}>
                    {preview && <img src={preview} alt="Preview" className={styles.preview} />}
                    <input type="file" accept="image/*"  onChange={handleImageChange}/>
                </div>

                <div className={styles.inputGroup}>
                    <label> Full Name</label>
                    <input type="text" required value={name}  onChange={(e)=>setName(e.target.value)}/>
                </div>
                
                <div className={styles.inputGroup}>
                    <label >Email</label>
                    <input type="email" required value={email} onChange={e=>setEmail(e.target.value)} />
                </div>

                <div className={styles.inputGroup}>
                    <label >Password</label>
                    <input type="password" required value={password} onChange={e=>setPassword(e.target.value)} />
                </div>

                <div className={styles.inputGroup}>
                    <label >Confirm Password</label>
                    <input type="password" required value={confirmPassword} onChange={e=>setconfirmPassword(e.target.value)} />
                </div>

                <button type="submit" className={styles.submitBtn}>Create Account</button>
            </form>
        </div>
    )
}


export default CreateAccount