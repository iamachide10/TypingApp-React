import  { useState, useEffect } from "react";
import "./GoalsSettings.css";

const GoalsSettings =()=>{

  const [goals, setGoals] = useState(() => {
    const saved = localStorage.getItem("typingGoals");
    return saved ? JSON.parse(saved) : [];
  });
  const [newGoal, setNewGoal] = useState("");

  const addGoal = () => {
    if (newGoal.trim() !== "") {
      const updatedGoals = [...goals, newGoal.trim()];
      setGoals(updatedGoals);
      localStorage.setItem("typingGoals", JSON.stringify(updatedGoals));
      setNewGoal("");
    }
  };

  const deleteGoal = (index) => {
    const updatedGoals = goals.filter((_, i) => i !== index);
    setGoals(updatedGoals);
    localStorage.setItem("typingGoals", JSON.stringify(updatedGoals));
  };


  return (
    <div className="settings-container">
      <h2>Typing Goals</h2>
      <div className="goal-input">
        <input
          type="text"
          placeholder="Set a new goal..."
          value={newGoal}
          onChange={(e) => setNewGoal(e.target.value)}
        />
        <button onClick={addGoal}>Add Goal</button>
      </div>

      <ul className="goal-list">
        {goals.map((goal, index) => (
          <li key={index}>
            {goal}
            <button className="delete-button" onClick={() => deleteGoal(index)}>X</button>
          </li>
        ))}
      </ul>
    </div>
  );
}


export default GoalsSettings