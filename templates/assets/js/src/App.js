import React from "react";
import "./App.css";
import Navbar from "./components/Navbar";
// import { Outlet } from "react-router-dom";
import Footer from "./pages/Footer";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Home from "./pages/Home";
import Exam from "./pages/Exam";
import { useLocation, useParams } from "react-router-dom";
import OmrScan from "./pages/OmrScan";
import OmrResults from "./pages/OmrResults";

function App() {
  console.log(window.location.href);
  const location = useLocation();
  console.log("pathname", location.pathname);
  const handleRoter = () => {
    switch (location.pathname.toLowerCase()) {
      case "/":
        return <Home />;
      case "/exam/":
        return <Exam />;
      case "/scan/":
        return <OmrScan />;
      case "/results/":
        return <OmrResults />;

      default:
        break;
    }
  };
  return (
    <div className="App">
      <ToastContainer theme="dark" />
      <Navbar />
      <div className="min-h-screen">{handleRoter()}</div>
      <Footer />
    </div>
  );
}

export default App;
