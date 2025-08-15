import { useState } from "react";
import { useParams } from "react-router-dom";


export default function ResetPassaword(){
    const {token} =useParams();

    const [password,setPassword]=useState("")
    const [confirmPassword,setconfirmPassword]=useState("")
    const [message,setMessage]=useState("")

    const handleSubmit =async (e)=>{
        e.preventDefault();
    };


    return(
        <div className="login-container">

        <form onSubmit={handleSubmit} className="login-form" >
            <h2>Reset Password</h2>
            <p>Password: </p>
            <input type="password" placeholder="Enter new password " value={password}  onChange={e=>setPassword(e.target.value)}/>
            <p>Confirm Password: </p>
            <input type="password" placeholder="Confirm password " value={password}  onChange={e=>setPassword(e.target.value)}/>

            <button type="submit">Update Password</button>
            <p>{message}</p>
        </form>
        </div>
    )

}