import React, { useState } from "react";
import axios from "axios";

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
      const response = await axios.post("http://localhost:8000/signup", {
        email,
        password,
      });
      const token = response.data.access_token;

      localStorage.setItem("token", token);
      setMessage("Signup successful! Token stored in localStorage.");
    } catch (err) {
      // If signup fails error message 
      setError("Failed to signup");
    }
  };


  return (
    <div>
      <h2>Signup</h2>
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
        <div>
          <label>Confirm Password: </label>
          <input 
            type="password"
            value={passwordConfirm}
            required
            onChange={(e) => setPasswordConfirm(e.target.value)}
          />
        </div>
        <button type="submit">Signup</button>
      </form>


      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}
    </div>
  );
};

export default Signup;
