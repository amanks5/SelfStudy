import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Signup from "./Signup";

function Header() {
  return <div className="fixed flex content-center w-full bg-[#A62929] py-3">
    <h1 className="mx-auto align-middle font-serif text-3xl text-[#F2DAC4]">[ self study. ]</h1>
  </div>
}

function Footer() {
  return <div className="fixed bottom-0 w-full content-left px-2 bg-[#A62929] py-1.5">
    <p className="font-serif text-sm text-[#F2DAC4]">Created by Aman Shaan, Brandon Sibbitt, Joshua Kitaigorod, and William Hamon for CEN 3031</p>
  </div>
}

function App() {
  return (
    <body className="bg-[#F2DAC4]">
    <Header />
    <Router>
      <Routes>
        <Route path="/" element={<h1 class="underline">Hello, Worldd!</h1>} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
    <Footer />
    </body>
  );
}

export default App;
