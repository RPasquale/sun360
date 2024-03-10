import React, { useState } from "react";
import "./ReminderMiniCard.css";

function convertTo12HourFormat(time24) {
  const [hour, minute] = time24.split(":").map(Number);
  const amOrPm = hour < 12 ? "am" : "pm";
  const hour12 = hour % 12 || 12;
  const time12 = `${hour12.toString().padStart(2, "0")}:${minute
    .toString()
    .padStart(2, "0")}${amOrPm}`;
  return time12;
}

function isCurrentDate(dateString) {
  // Create a new Date object for the current date
  const currentDate = new Date();

  // Extract year, month, and day from the current date
  const currentYear = currentDate.getFullYear();
  const currentMonth = String(currentDate.getMonth() + 1).padStart(2, "0");
  const currentDay = String(currentDate.getDate()).padStart(2, "0");

  // Construct the current date string in the format "YYYY-MM-DD"
  const currentDateString = `${currentYear}-${currentMonth}-${currentDay}`;

  // Compare the input date string with the current date string
  return dateString === currentDateString;
}

function isTomorrowDate(dateString) {
  // Create a new Date object for the current date
  const currentDate = new Date();

  // Add one day to the current date
  const tomorrowDate = new Date(currentDate);
  tomorrowDate.setDate(currentDate.getDate() + 1);

  // Extract year, month, and day from tomorrow's date
  const tomorrowYear = tomorrowDate.getFullYear();
  const tomorrowMonth = String(tomorrowDate.getMonth() + 1).padStart(2, "0");
  const tomorrowDay = String(tomorrowDate.getDate()).padStart(2, "0");

  // Construct tomorrow's date string in the format "YYYY-MM-DD"
  const tomorrowDateString = `${tomorrowYear}-${tomorrowMonth}-${tomorrowDay}`;

  // Compare the input date string with tomorrow's date string
  return dateString === tomorrowDateString;
}

function formatDateToDDMMMYYYY(dateString) {
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  const [year, month, day] = dateString.split("-");
  const monthIndex = parseInt(month, 10) - 1; // Months in JavaScript are zero-based

  // Format the date to "DD MMM YYYY"
  const formattedDate = `${parseInt(day, 10)} ${months[monthIndex]} ${year}`;

  return formattedDate;
}

function getFullWeekdayName(initials) {
  switch (initials) {
    case "SU":
      return "Sunday";
    case "MO":
      return "Monday";
    case "TU":
      return "Tuesday";
    case "WE":
      return "Wednesday";
    case "TH":
      return "Thursday";
    case "FR":
      return "Friday";
    case "SA":
      return "Saturday";
    default:
      return "Invalid Initials";
  }
}

function getCurrentWeekday() {
  const weekdays = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const currentDate = new Date();
  const currentWeekdayIndex = currentDate.getDay(); // Returns a number from 0 (Sunday) to 6 (Saturday)
  const currentWeekday = weekdays[currentWeekdayIndex];
  return currentWeekday;
}

function isCurrentWeekday(day) {
  const currentWeekday = getCurrentWeekday();
  return day === currentWeekday;
}

function isTomorrowWeekday(day) {
  const weekdays = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const firstIndex = weekdays.indexOf(getCurrentWeekday());
  const secondIndex = weekdays.indexOf(day);
  return secondIndex > firstIndex;
}

function ReminderMiniCard(props) {
  let color = "red";

  switch (props.color) {
    case "R":
      color = "red";
      break;
    case "Y":
      color = "yellow";
      break;
    case "G":
      color = "green";
      break;
    default:
      color = "red";
  }

  let frequency = "";
  let day = "";
  switch (props.frequency) {
    case "O":
      frequency = "(Once)";
      day = props.date;
      if (isCurrentDate(day)) {
        day = "Today";
      } else if (isTomorrowDate(day)) {
        day = "Tomorrow";
      } else {
        day = formatDateToDDMMMYYYY(day);
      }
      break;
    case "D":
      frequency = "(Daily)";
      day = "Today";
      break;
    case "W":
      frequency = "(Weekly)";
      day = getFullWeekdayName(props.weekday);
      if (isCurrentWeekday(day)) {
        day = "Today";
      } else if (isTomorrowWeekday(day)) {
        day = "Tomorrow";
      }
      break;
    default:
      frequency = "";
  }

  const time12 = convertTo12HourFormat(props.time.slice(0, -3));

  return (
    <div className={`mini-card ${color}`}>
      <div className="time">{time12}</div>
      <div className="user">{props.user}</div>
      <div className="last">
        <div className="day">{day}</div>
        <div className="frequency"> {frequency}</div>
      </div>
    </div>
  );
}

export default ReminderMiniCard;
