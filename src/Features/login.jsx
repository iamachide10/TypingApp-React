import React, { useState } from "react";
import "./loginCss.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit =async  (e) => {
    e.preventDefault();

    const credentials={
      email,
      password
    }

     const url="http://127.0.0.1:5000/login"
     const options={
      method: "POST",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify(credentials)
     }

     try{
      const response = await fetch(url, options)
      const data = await response.json();
      if (!response.ok) {
        throw new Error("Login failed. Please check your credentials.");
      }else{
        const message = data.message;
        alert(message);
        const credentials = data.credentials;
        localStorage.setItem("user", JSON.stringify(credentials));
        window.location.href = "/"; // Redirect to the landing page after successful login

      }
     }catch(error){
      alert(error)
     }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Log In</button>
      </form>
    </div>
  );
}

export default Login;
