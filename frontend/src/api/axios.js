import axios from "axios";

// Axios server handle for simpler requests (login and signup)
export default axios.create({
  baseURL: "http://localhost:9000",
});

// Axios server handle for protected requests (search and logout)
export const axiosPrivate = axios.create({
  baseURL: "http://localhost:9000",
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
});
