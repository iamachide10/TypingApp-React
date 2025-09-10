import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function VerifyEmail() {
  const { token } = useParams();
  const [message, setMessage] = useState("Verifying...");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verifyUser = async () => {
      try {
        const API_URL = process.env.REACT_APP_API_URL;
        const response= await fetch(`${API_URL}/verify-email?token=${token}`);
        const data = await response.json();
        setMessage(data.Message || data.message);
      } catch (error) {
        setMessage("Something went wrong while verifying your email.");
      } finally {
        setLoading(false);
      }
    };
    verifyUser();
  }, [token]);


  return (
    <div className="verify-container">
      {loading ? <p>Checking verification link...</p> : <h2>{message}</h2>}
    </div>
  );
}



