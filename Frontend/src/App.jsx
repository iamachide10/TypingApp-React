import LandingPage from "./Features/LandingPage";
import TypingTestSelect from "./Features/TypingTestSelect";
import PracticeLevels from "./Features/PracticeLevels";
import { Route,Routes } from "react-router-dom";
import PracticeLevelPage from "./Features/PracticeLevelPage";
import TypingTestPlay from "./Features/TypingTestPlay";
import Settings from "./settingsComponents/Settings";
import CreateAccount from "./Features/CreateAccount";
import Login from "./Features/login";
import RequestReset from "./Features/RequestReset";
import VerifyEmail from "./Features/verifyEmail";
import ResetPassaword from "./Features/ResetPassword";

function App() {
  return (
      <Routes>
        <Route path="/verify-email/:token" element={<VerifyEmail />} />
        <Route path="/" element ={<LandingPage/>} />
        <Route path="/request-reset" element ={<RequestReset/>} />
        <Route path="/reset-password" element ={<ResetPassaword/>} />
        <Route path="/test" element ={<TypingTestSelect/>} />
        <Route path="/practice" element ={<PracticeLevels/>} />
        <Route path="/settings" element ={<Settings/>} />
        <Route path="/test/play" element ={<TypingTestPlay/>} />
        <Route path="/practice/:levelId" element ={<PracticeLevelPage/>} />
        <Route path="/login" element ={<Login/>} />
        <Route path="/create_account" element ={<CreateAccount/>} />
        <Route path="/reset-password/:token" element ={<ResetPassaword/>} />
        
      </Routes>
  );
}


export default App;
