import LandingPage from "./Features/LandingPage";
import Test from "./Features/Test";
import Game from "./Features/Game";
import Practice from "./Features/Practice";
import { Route,Routes } from "react-router-dom";

function App() {
  return (
    
      <Routes>
        <Route path="/" element ={<LandingPage/>} />
        <Route path="/test" element ={<Test/>} />
        <Route path="/practice" element ={<Practice/>} />
        <Route path="/game" element ={<Game/>} />
      </Routes>
    
  );
}

export default App