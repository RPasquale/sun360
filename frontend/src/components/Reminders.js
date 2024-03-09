import React, { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import ReminderSettings from './ssusage/ReminderSettings';
import SunscreenTracker from './ssusage/SunscreenTracker';
import './Reminders.css';


function Reminders() {
  //   const userId = user ? user.id : null;
  //   const [reminder, setReminder] = useState({
  //   date: '',
  //   time: '',
  //   title: '',
  //   notes: '',
  //   color: '#ffffff',
  //   severity: '',
  //   daysOfWeek: [], // for weekly reminders
  // });

  // const handleChange = (e) => {
  //   const { name, value } = e.target;
  //   setReminder({ ...reminder, [name]: value });
  // };

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   console.log(reminder); // Implement the logic for submitting the reminder
  // };

  // return (
  //   <div className="reminders-page">
  //     <Link to="/reminders">Set Reminder</Link>
  //     <form onSubmit={handleSubmit} className="reminder-form">
  //       {/* Form inputs for setting a reminder */}
  //       <input type="date" name="date" value={reminder.date} onChange={handleChange} />
  //       <input type="time" name="time" value={reminder.time} onChange={handleChange} />
  //       {/* Add additional fields here */}
  //       <button type="submit">Set Reminder</button>
  //     </form>
  //     <ReminderSettings userId={userId} />
  //     <SunscreenTracker userId={userId} />

  //   </div>
  // );
}

export default Reminders;
