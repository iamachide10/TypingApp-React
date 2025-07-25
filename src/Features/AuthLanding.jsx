const AuthLanding =({onSelect})=>{
    return(<div className="auth-container">
        <h2>Welcome TO Typing Mastry</h2>
        <p>Please choose an option:</p>
        <div className="auth-buttons">
            <button onClick={()=>onSelect("login")}>Login</button>
            <button onClick={()=>onSelect("signup")}>Create Account</button>
        </div>
    </div>)

}
export default AuthLanding  