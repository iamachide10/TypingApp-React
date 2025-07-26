import LandingPage from "./Features/LandingPage";
import TypingTestSelect from "./Features/TypingTestSelect";
import PracticeLevels from "./Features/PracticeLevels";
import { Route,Routes } from "react-router-dom";
import PracticeLevelPage from "./Features/PracticeLevelPage";
import TypingTestPlay from "./Features/TypingTestPlay";
import Settings from "./settingsComponents/Settings";
import CreateAccount from "./Features/CreateAccount";
import Login from "./Features/login";
function App() {
  return (
      <Routes>
        <Route path="/" element ={<LandingPage/>} />
        <Route path="/test" element ={<TypingTestSelect/>} />
        <Route path="/practice" element ={<PracticeLevels/>} />
        <Route path="/settings" element ={<Settings/>} />
        <Route path="/test/play" element ={<TypingTestPlay/>} />
        <Route path="/practice/:levelId" element ={<PracticeLevelPage/>} />
        <Route path="/login" element ={<Login/>} />
        <Route path="/create_account" element ={<CreateAccount/>} />
      </Routes>
  );
}

export default App;
