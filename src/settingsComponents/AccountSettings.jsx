import { useState ,useEffect} from "react"
import styles from  "./AccountSettings.module.css"


const AccountSettings =()=>{

  const [name, setName] = useState("User 1.0");
  const [profile_image, setProfile] = useState("");
  const [userId, setUserId] = useState(null);
  const [email, setEmail] = useState("user1.0@gmail.com");
  const [preview, setPreview] = useState(null);
  const [image, setImage] = useState(null);

  const userData = JSON.parse(localStorage.getItem("user"));

  useEffect(() => {
    if (userData) {
      setName(userData.userName);
      setEmail(userData.email);
      setUserId(userData.user_id);
      if (userData.profile_image !== null && userData.profile_image !== "") {
        setProfile(userData.profile_image);
      }
    }
  }, []);

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSave = async () => {
    const formData = new FormData();
    formData.append("name", name);
    if (image) {
      formData.append("image", image);
    }

    const url = `http://127.0.0.1:5000/updates`;

    try {
      const response = await fetch(url, {
        method: "PATCH",
        body: formData,
      });

      // ✅ Safely parse JSON only if server says it's JSON
      const text = await response.text();
      let result;
      try {
        result = JSON.parse(text);
      } catch {
        console.error("Not JSON response:", text);
        alert("Server error: " + text);
        return;
      }

      if (result.messages) {
        result.messages.forEach((msg) => alert(msg));
      }
      let user = JSON.parse(localStorage.getItem("user"))

      if (result.name) {
        user.userName = result.name;
        setName(result.name)
    }
      if (result.profilePic) {
        user.profile_image = result.profilePic;
    setProfile(result.profilePic)}
      localStorage.setItem("user", JSON.stringify(user))
      //window.location.href = "/settings";

    } catch (e) {
      alert("Request failed: " + e.message);
    }
  };

    return(

        <div className={styles.accountContainer}>
            <h2>Account Settings</h2>

             {profile_image && (
                <label htmlFor="fileInput" style={{ width:"100px"}}>
                    <img
                      src={`${profile_image}`}
                      alt="Profile"
                      style={{borderRadius:"50%", height:"100px", width:"100px", cursor:"pointer"}}

                    />
                </label>
              )}
              <input type="file"   id="fileInput"  accept="image/*" onChange={e=>handleChange(e)}  style={profile_image ? {display: "none" }:{display: "flex"}}/>
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