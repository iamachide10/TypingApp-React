import LandingPage from "./Features/LandingPage";
import Test from "./Features/Test";
import Game from "./Features/Game";
import PracticeLevels from "./Features/PracticeLevels";
import { Route,Routes } from "react-router-dom";
import PracticeLevelPage from "./Features/PracticeLevelPage";
function App() {
  return (
    
      <Routes>
        <Route path="/" element ={<LandingPage/>} />
        <Route path="/test" element ={<Test/>} />
        <Route path="/practice" element ={<PracticeLevels/>} />
        <Route path="/game" element ={<Game/>} />
        <Route path="/practice/:levelId" element ={<PracticeLevelPage/>} />

      </Routes>
    
  );
}

export default App;
