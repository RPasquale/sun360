import React, { useState, useContext } from 'react'; // Import useContext
import UserContext from './UserContext';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [location, setLocation] = useState('');
  const [skinType, setSkinType] = useState('');
  const [gender, setGender] = useState('');
  const [error, setError] = useState(null);

  // Correctly using useContext at the component level
  const { register } = useContext(UserContext); // Update to new name 

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username,
          email,
          password,
          location,
          skin_type: skinType,
          gender,
        }),
      });
  
      console.log("Response:", response); // Log the entire response


      if (response.ok) { // 'if' statement on next line
        const userData = await response.json(); 
        await register(username, password);  
        window.location.href = '/'; 
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration Error:', error);
      setError('Registration failed. Please try again.'); 
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
            <label>Username</label>
            <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            </div>
            <div>
            <label>Email</label>
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            </div>
            <div>
            <label>Password</label>
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            </div>
            <div>
            <label>Confirm Password</label>
            <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
            />
            </div>
            <div>
            <label>Location</label>
            <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
            />
            </div>
            <div>
            <label>Skin Type</label>
            <select value={skinType} onChange={(e) => setSkinType(e.target.value)}>
                <option value="">Select...</option>
                <option value="Type I">Type I - Very fair</option>
                <option value="Type II">Type II - Fair</option>
                <option value="Type III">Type III - Medium</option>
                <option value="Type IV">Type IV - Olive</option>
                <option value="Type V">Type V - Brown</option>
                <option value="Type VI">Type VI - Very dark</option>
            </select>
            </div>
            <div>
            <label>Gender</label>
            <select value={gender} onChange={(e) => setGender(e.target.value)}>
                <option value="">Select...</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
                <option value="Prefer not to say">Prefer not to say</option>
            </select>
            </div>
                    <button type="submit">Register</button>
                </form>
                </div>
            );
}

export default RegisterPage;








   

