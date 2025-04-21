import React, { useState } from "react";
import api from "./api";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");

    try {
      const response = await api.post("/login", {
        email,
        password,
      });
      const token = response.data.access_token;

      localStorage.setItem("token", token);
      setMessage("Login successful! Token stored in localStorage.");
      window.location.href = "/";
    } catch (err) {
      // If login fails error message 
      setError("Invalid credentials");
    }
  };

  return (
    <div className="mx-auto flex h-screen justify-center items-center">
      <div className="grid grid-cols-2">
        <div className="mx-32 px-4 py-20 text-6xl font-serif font-bold text-[#A62929]">smart notes, smarter learning.</div>
        <div className="flex rounded-xl mx-32 px-12 items-center border-4 border-[#A62929] border-dashed">
          <form className="w-full px-6" onSubmit={handleSubmit}>
            <label className="font-serif text-lg text-[#A62929]">email:</label><br></br>
            <input className="bg-white w-full py-0.5 rounded-sm font-serif p-1.5" type="email" value={email} required onChange={(e) => setEmail(e.target.value)}/>
            <br></br>
            <label className="font-serif text-lg text-[#A62929]">password:</label><br></br>
            <input className="bg-white w-full py-0.5 rounded-sm font-serif p-1.5" type="password" value={password} required onChange={(e) => setPassword(e.target.value)} />
            <br></br><br></br>
            <div className="flex justify-center items-center">
            <button className="bg-[#A62929] hover:bg-[#F2DAC4] px-12 py-2 rounded-sm font-serif text-[#F2DAC4] hover:text-[#A62929] border-2 border-[#A62929] cursor-pointer" type="submit">login</button>
            </div>
          </form>
        </div>
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}
    </div>
  )
};

export default Login;
