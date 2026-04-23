import axios from "axios";
import { io } from "socket.io-client";

export const API = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

export const setAuthToken = (token: string) => {
  API.defaults.headers.common["Authorization"] = `Bearer ${token}`;
};

export const getRecommendations = () => API.get("/recommendations/feed");
export const getHybridSearch = (q: string) => API.get(`/search/hybrid?q=${q}`);
export const getAnalytics = (id: string | number) => API.get(`/analytics/mentor/${id}`);

export const socket = io("http://localhost:8000", {
  autoConnect: false,
});
