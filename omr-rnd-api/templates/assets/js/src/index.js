import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter as Router } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  // <React.StrictMode>
  <Router>
    <App />
  </Router>
  // </React.StrictMode>
);
// const app = ReactDOM.createRoot(document.getElementById("app"));

// if (document.getElementById("root")) {
//   console.log("root is already");
//   ReactDOM.createRoot(document.getElementById("root")).render(
//     <React.StrictMode>
//       <App />
//     </React.StrictMode>
//   );
// } else if (document.getElementById("app")) {
//   console.log("app is already");
//   ReactDOM.createRoot(document.getElementById("app")).render(
//     <React.StrictMode>
//       <h1>hellow app</h1>
//     </React.StrictMode>
//   );
// }

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
