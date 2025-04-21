import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Signup from "./Signup";
import NoteEditor from "./NoteEditor";

function Header() {
  return <div className="fixed flex content-center w-full bg-[#A62929] h-1/12 items-center">
    <a href="/" className="mx-auto font-serif text-3xl text-[#F2DAC4]">[ self study. ]</a>
  </div>
}

function Footer() {
  return <div className="fixed bottom-0 w-full content-left px-2 bg-[#A62929] h-1/12 align-middle">
    <p className="font-serif text-sm text-[#F2DAC4]">Created by Aman Shaan, Brandon Sibbitt, Joshua Kitaigorod, and William Hamon for CEN 3031</p>
  </div>
}

function App() {
  return (
    <div>
    <Header />
    <Router>
      <Routes>
        <Route path="/" element={<h1 class="underline">Hello, Worldd!</h1>} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/write" element={<NoteEditor />} />
      </Routes>
    </Router>
    <Footer />
    </div>
  );
}

export default App;
