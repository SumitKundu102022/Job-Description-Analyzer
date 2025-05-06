import React from "react";
import ReactDOM from "react-dom/client";
import JobDescriptionAnalyzer from "./components/JobDescriptionAnalyzer"; // Adjust the import path as necessary
import "./index.css"; // You might need a basic index.css for global styles


const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <JobDescriptionAnalyzer/>
  </React.StrictMode>
);
