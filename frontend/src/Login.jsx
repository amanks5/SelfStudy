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
    } catch (err) {
      // If login fails error message 
      setError("Invalid credentials");
    }
  };


  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email: </label>
          <input 
            type="email" 
            value={email}
            required
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Password: </label>
          <input 
            type="password"
            value={password}
            required
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>


      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}
    </div>
  );
};

export default Login;
