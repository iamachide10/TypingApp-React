import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./loginCss.css";


function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
  e.preventDefault();

  const credentials = {
    email,
    password,
  };

  const url = "http://127.0.0.1:5000/login";
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  };

  try {
    const response = await fetch(url, options);
    const data = await response.json();

    const message = data.message;
    alert(message);

    if (response.ok) {
      const userData = data.credentials;
      localStorage.setItem("user", JSON.stringify(userData));
   


      const generalSettingsRes = await fetch(`http://127.0.0.1:5000/general-settings/${userData.user_id}`);
      const generalSettingsData = await generalSettingsRes.json();
      if (generalSettingsRes.ok) {
        localStorage.setItem("generalSettings",JSON.stringify(generalSettingsData ));
      } else {
        console.warn("No general settings found:", generalSettingsData);
      }


      const themeSettingsRes = await fetch(`http://127.0.0.1:5000/theme-settings/${userData.user_id}`)
      const themeSettingsData =await themeSettingsRes.json()
      if(generalSettingsData.ok){
        localStorage.setItem("themeSettings" , JSON.stringify(themeSettingsData))
      }else{
        console.log(themeSettingsData)
      }

      
      const accountSettingsRes = await fetch(`http://127.0.0.1:5000/account-settings/${userData.user_id}`)
      const accountSettingsData =await accountSettingsRes.json()
      if(accountSettingsData.ok){
        localStorage.setItem("accountSettings" , JSON.stringify(accountSettingsData))
      }else{
        console.log(accountSettingsData)
      }


      // 🔹 Redirect after everything is saved
      window.location.href = "/";
    }
  } catch (error) {
    alert(error);
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
        <p><Link to="/request-reset">forgot password </Link></p>
      </form>
    </div>
  );
}

export default Login;
