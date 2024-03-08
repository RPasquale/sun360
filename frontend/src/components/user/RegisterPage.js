// RegisterPage.js
import React, { useState, useContext } from "react"; // Import useContext

import "./RegisterPage.css"; // Import CSS file for register page styling
import SkinColorPalette from "../basic-ui/elements/SkinColorPalette";
import FamilyMemberCard from "./FamilyMemberCard";

function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [age, setAge] = useState(18);
  const [location, setLocation] = useState("");
  const [skinTone, setSkinTone] = useState(0);
  const [gender, setGender] = useState("");
  const [familyMembers, setFamilyMembers] = useState([]);
  const [error, setError] = useState(null);

  const handleFamilyMemberChange = (id, member) => {
    if (id === familyMembers.length + 1) {
      // New Member added
      setFamilyMembers([
        ...familyMembers,
        {
          id: familyMembers.length + 1,
          name: "",
          gender: "",
          age: 10,
          skinTone: 0,
        },
      ]);
    } else if (member === null) {
      // Current member removed
      const updatedMembers = familyMembers.filter((m) => m.id !== id);
      for (let i = 1; i <= updatedMembers.length; i += 1) {
        updatedMembers[i - 1].id = i;
      }
      console.log(updatedMembers);
      setFamilyMembers(updatedMembers);
    } else {
      // Current member value changed
      const updatedMembers = familyMembers.map((m) =>
        m.id === id ? member : m
      );
      setFamilyMembers(
        updatedMembers.filter((m) => m.name || m.gender || m.age || m.skinTone)
      );
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          email,
          password,
          location,
          skin_type: skinTone,
          gender,
        }),
      });

      console.log("Response:", response); // Log the entire response

      if (response.ok) {
        // 'if' statement on next line
        const userData = await response.json();
        // await register(name, password);
        window.location.href = "/";
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || "Registration failed");
      }
    } catch (error) {
      console.error("Registration Error:", error);
      setError("Registration failed. Please try again.");
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit} className="register-form">
        <div className="form-row">
          <label htmlFor="name" className="form-label">
            Name
          </label>
          <input
            type="text"
            name="name"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div className="form-row">
          <label htmlFor="email" className="form-label">
            Email
          </label>
          <input
            type="email"
            name="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="form-row">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            type="password"
            name="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="form-row">
          <label htmlFor="cpassword" className="form-label">
            Confirm Password
          </label>
          <input
            type="password"
            name="cpassword"
            id="cpassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        <div className="form-row">
          <label htmlFor="age" className="form-label">
            Age
          </label>
          <input
            type="number"
            name="age"
            id="age"
            value={age}
            onChange={(e) => setAge(e.target.value)}
          />
        </div>
        <div className="form-row">
          <label htmlFor="postcode" className="form-label">
            Postcode
          </label>
          <input
            type="text"
            name="postcode"
            id="postcode"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>
        <div className="form-row skin-tone">
          <label htmlFor="skintone" className="form-label">
            Skin Tone
          </label>
          <input
            type="range"
            name="skintone"
            id="skintone"
            min="0"
            max="9"
            value={skinTone}
            onChange={(e) => setSkinTone(parseInt(e.target.value))}
          />
          <SkinColorPalette />
        </div>
        <div className="form-row">
          <label htmlFor="gender" className="form-label">
            Gender
          </label>
          <select
            name="gender"
            id="gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
          >
            <option value="">Select...</option>
            <option value="M">Male</option>
            <option value="F">Female</option>
          </select>
        </div>
        <div className="form-row">
          {familyMembers.length > 0 && (
            <label htmlFor="familyMembers" className="form-label">
              Family Members
            </label>
          )}
          {familyMembers.map((member) => (
            <FamilyMemberCard
              key={member.id}
              member={member}
              onChange={handleFamilyMemberChange}
            />
          ))}
        </div>
        <button
          type="button"
          className="add-member"
          onClick={() =>
            handleFamilyMemberChange(familyMembers.length + 1, {
              id: familyMembers.length + 1,
              name: "",
              gender: "",
              age: 10,
              skinTone: 0,
            })
          }
        >
          Add Family Member
        </button>

        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default RegisterPage;
