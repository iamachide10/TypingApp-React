import { useState } from "react";
import AccountSettings from "./AccountSettings";
import GeneralSettings from "./GeneralSettings";
import ThemeSettings from "./ThemeSettings";
import CustomPassageSettings from "./CustomPassageSettings";
import styles from "./Settings.module.css"

function Settings() {
  const [activeTab,setActiveTab]=useState("General")

  const tabs=[
    "General",
    "Theme and display",
    "Custom Passages",
    "Account",
  ]

  const renderContent =()=>{
    switch(activeTab){
      case "General":
        return <GeneralSettings />
      case "Theme and display":
        return <ThemeSettings/>
      case "Custom Passages":
        return <CustomPassageSettings/>
      case  "Account":
        return <AccountSettings/>
    }
  }


  return (  
      <div className={styles.container}> 
      <h1 className={styles.header}> Settings</h1>
      <div className={styles.tabList}>
        {tabs.map(tab=>(
          <button key={tab} onClick={()=>setActiveTab(tab)} className={` ${styles.tabButton}  ${activeTab === tab ? styles.activeTab: "" }`}>{tab}</button>
        ))}
      </div>
      <div className={styles.tabContent}>{renderContent()}</div>
      </div>
    
  );
}

export default Settings;