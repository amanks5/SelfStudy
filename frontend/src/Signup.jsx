import React, { useState } from "react";
import api from "./api";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");

    if(password !== passwordConfirm) {
        setError("Passwords do not match!");
        return;
    }

    try {
      const response = await api.post("/signup", {
        email,
        password,
      });
      const token = response.data.access_token;

      localStorage.setItem("token", token);
      setMessage("Signup successful! Token stored in localStorage.");
      window.location.href = "/";
    } catch (err) {
      // If signup fails error message 
      setError("Failed to signup");
    }
  };

  return (
    <div className="flex w-screen h-screen items-center">
      <div className="container grid mx-auto w-3/12 h-7/12 rounded-md border-4 border-dashed border-[#A62929] p-3">
        <h1 className="font-serif text-[#A62929] font-black text-center text-3xl">signup</h1>
        <form className="mx-auto w-11/12" onSubmit={handleSubmit}>
          <div className="my-2">
            <label className="font-serif text-[#A62929] font-semibold text-base">email:</label><br/>
            <input className="w-full rounded-sm bg-white font-serif text-base px-1 text-[#A62929] py-0.5" type="email" value={email} required onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="my-2">
            <label className="font-serif text-[#A62929] font-semibold text-base">password:</label><br/>
            <input className="w-full rounded-sm bg-white font-serif text-base px-1 text-[#A62929] py-0.5" type="password" value={password} required onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className="my-2">
            <label className="font-serif text-[#A62929] font-semibold text-base">confirm password:</label><br/>
            <input className="w-full rounded-sm bg-white font-serif text-base px-1 text-[#A62929] py-0.5" type="password" value={passwordConfirm} required onChange={(e) => setPasswordConfirm(e.target.value)} />
          </div><br/>
          <button className="w-full rounded-sm bg-[#A62929] font-serif font-bold text-[#F2DAC4] text-center py-1 cursor-pointer" type="submit">signup</button>
        </form>

        {error && <p style={{ color: "red" }}>{error}</p>}
        {message && <p style={{ color: "green" }}>{message}</p>}
      </div>
    </div>
  )
};

export default Signup;
