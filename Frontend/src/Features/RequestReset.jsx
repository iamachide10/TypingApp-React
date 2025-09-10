import { useState } from "react";
import { Link } from "react-router-dom";
import { useParams } from "react-router-dom";

const RequestReset=()=>{
    const [email,setEmail]=useState("")
    const [message, setMessage]=useState("")
    const {token} = useParams();


    const handleSubmit=async(e)=>{
        e.preventDefault()
        const API_URL = process.env.REACT_APP_API_URL;

        const url = `${API_URL}/forgot-password`;
        const options={
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({email})
        }
        try{
            const response = await fetch(url,options)
            const data =await response.json();
            setMessage(data.message)
        }catch(error){
            alert(error)
        }
    }

    return(<div className="login-container">
        <form onSubmit={handleSubmit} className="login-form">
            <h2>Forgot Password:</h2>
            <input type="email" placeholder="Enter your email " value={email} onChange={e=>setEmail(e.target.value)}  required/>
            <button type="submit" >Send Reset Link</button>
            <p>{message}</p>
        </form>
    </div>);
}

export default RequestReset;