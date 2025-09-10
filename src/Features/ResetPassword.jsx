
import { useState } from "react";
import { useParams } from "react-router-dom";


export default function ResetPassaword(){
    const {token} =useParams();

    const [password,setPassword]=useState("")
    const [confirmPassword,setconfirmPassword]=useState("")
    const [message,setMessage]=useState("")

    const handleSubmit =async (e)=>{
        e.preventDefault();
        if(password ==confirmPassword){
            const url = `http://localhost:5000/reset-password?token=${token}`
            const options ={
                "method":"POST",
                headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({password})
            }
            try{
                const result = await fetch(url, options)
                const data = await result.json()
                setMessage(data.message)
                alert(data.message)
            }catch(e){
                setMessage(e)
            }
        }else{
            alert("Password doesnt match.")
        }

  
    };


    return(
        <div className="login-container">  
        <form onSubmit={handleSubmit} className="login-form" >
            <h2>Reset Password</h2>
            <p>Password: </p>
            <input type="password" placeholder="Enter new password " value={password}  onChange={e=>setPassword(e.target.value)}/>
            <p>Confirm Password: </p>
            <input type="password" placeholder="Confirm password " value={confirmPassword}  onChange={e=>setconfirmPassword(e.target.value)}/>

            <button type="submit">Update Password</button>
            <p>{message}</p>
        </form>
        </div>
    )

}