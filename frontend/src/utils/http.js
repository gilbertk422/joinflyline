import { userStorage } from "../store/user.js";
import axios from "axios";

const BASE_URL = process.env.VUE_APP_API_ENDPOINT || "http://127.0.0.1:9000";

export const api = axios.create({
  baseURL: `${BASE_URL}/api/`,
  headers: {
    Authorization: {
      toString() {
        if (!userStorage.token) return null;
        return `Token ${userStorage.token}`;
      }
    }
  }
});

api.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    if (error.response.status === 401) {
      localStorage.removeItem("authTokenExpiry");
      localStorage.removeItem("authToken");
      return Promise.reject(error);
    } else {
      return Promise.reject(error);
    }
  }
);

export default api;
