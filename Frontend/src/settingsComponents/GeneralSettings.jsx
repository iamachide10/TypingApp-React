import { useState, useEffect } from "react";
import styles from "./GeneralSettings.module.css";

const GeneralSettings = () => {
  const [user, setUser] = useState(null);
  const [duration, setDuration] = useState("15");
  const [difficulty, setDifficulty] = useState("medium");
  const [test_mode, setTest_mode] = useState("words");
  const [autoStart, setAutoStart] = useState(true);
  const [sound, setSound] = useState(true);

  // 🔹 Load user from localStorage
  const userData = localStorage.getItem("user");
useEffect(() => {
  if (userData) {
    const parsed = JSON.parse(userData);
    setUser(parsed);

    // 🔹 Instead of fetching from backend, just read from localStorage
    const storedSettings = localStorage.getItem("generalSettings");
    if (storedSettings) {
      const data = JSON.parse(storedSettings);
      console.log(data)
      setDuration(data.duration || "15");
      setDifficulty(data.difficulty || "medium");
      setTest_mode(data.test_mode || "words");
      setAutoStart(
          data.auto_start_text !== undefined
          ? data.auto_start_text
          : true
      );
      setSound(
        data.enable_sound_effect !== undefined
          ? data.enable_sound_effect
          : true
      );
    } else {
      console.warn("No settings found in localStorage, using defaults.");
    }
  }
}, []);

  const userId = user ? user.user_id : null;

  const handleSave = async () => {
    if(userData){

      try {
        const response = await fetch(
          `http://127.0.0.1:5000/general-settings`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              generalSettings: {
                duration,
                difficulty,
                auto_stat_text: autoStart,
                enable_sound_effect: sound,
                test_mode,
              },
            }),
          }
        );
  
        const result = await response.json();
        alert(result.message)
        if (response.ok) {
          // update localStorage too
          localStorage.setItem(
            "generalSettings",
            JSON.stringify(result.settings)
          );
        } else {
          alert("Error: " + result.Message);
        }
      } catch (error) {
        console.error("Request failed: " + error);
      }
    }
    else{
      alert("Please Log in")
    }
  };

  return (
    <div className={styles.generalContainer}>
      <h2>General Preferences</h2>

      <div className={styles.settingGroup}>
        <label>Default Duration:</label>
        <select
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
        >
          <option value="15">15 seconds</option>
          <option value="30">30 seconds</option>
          <option value="60">60 seconds</option>
          <option value="120">120 seconds</option>
        </select>
      </div>

      <div className={styles.settingGroup}>
        <label>Difficulty:</label>
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      <div className={styles.settingGroup}>
        <label>Test Mode:</label>
        <select
          value={test_mode}
          onChange={(e) => setTest_mode(e.target.value)}
        >
          <option value="words">Words</option>
          <option value="sentences">Sentences</option>
          <option value="custom">Custom Passage</option>
        </select>
      </div>

      <div className={styles.settingGroupCheckbox}>
        <label>
          <input
            type="checkbox"
            checked={autoStart}
            onChange={() => setAutoStart(!autoStart)}
          />
          Auto Start Test
        </label>
      </div>

      <div className={styles.settingGroupCheckbox}>
        <label>
          <input
            type="checkbox"
            checked={sound}
            onChange={() => setSound(!sound)}
          />
          Enable Sound Effect
        </label>
      </div>

      <button className={styles.saveBtn} onClick={handleSave}>
        Save settings
      </button>
    </div>
  );
};

export default GeneralSettings;
