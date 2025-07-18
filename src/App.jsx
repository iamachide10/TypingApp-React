import LandingPage from "./Features/LandingPage";
import TypingTestSelect from "./Features/TypingTestSelect";
import Settings from "./Features/Settings";
import PracticeLevels from "./Features/PracticeLevels";
import { Route,Routes } from "react-router-dom";
import PracticeLevelPage from "./Features/PracticeLevelPage";
import TypingTestPlay from "./Features/TypingTestPlay";
function App() {
  return (
    
      <Routes>
        <Route path="/" element ={<LandingPage/>} />
        <Route path="/test" element ={<TypingTestSelect/>} />
        <Route path="/practice" element ={<PracticeLevels/>} />
        <Route path="/game" element ={<Settings/>} />
        <Route path="/test/play" element ={<TypingTestPlay/>} />
        <Route path="/practice/:levelId" element ={<PracticeLevelPage/>} />

      </Routes>
    
  );
}

export default App;
