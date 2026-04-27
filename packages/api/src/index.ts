import axios from "axios";
import { io } from "socket.io-client";
import {
  Mentor,
  User,
  Booking,
  RecommendationResponse,
} from "@mentornet/types";

// Use environment variables with fallbacks for local development
const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const SOCKET_URL =
  process.env.NEXT_PUBLIC_SOCKET_URL || "http://localhost:8000";

export const API = axios.create({
  baseURL: API_URL,
});

// Request Interceptor for Auth
API.interceptors.request.use(async (config) => {
  let token = null;

  if (typeof window !== "undefined" && window.localStorage) {
    token = localStorage.getItem("token");
  }

  // If token is already set in headers (via setAuthToken), keep it
  if (token && !config.headers.Authorization) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export const setAuthToken = (token: string | null) => {
  if (typeof window !== "undefined" && window.localStorage) {
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  }

  if (token) {
    API.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete API.defaults.headers.common["Authorization"];
  }
};

// API Endpoints
export const getRecommendations = () =>
  API.get<RecommendationResponse>("/recommendations/feed");
export const getHybridSearch = (q: string) =>
  API.get<Mentor[]>(`/search/hybrid?q=${q}`);
export const getAnalytics = (id: string | number) =>
  API.get(`/analytics/mentor/${id}`);
export const getPublicProfile = (username: string) =>
  API.get(`/profiles/public/${username}`);
export const getReferralStats = () => API.get("/analytics/referrals");
export const getRoadmap = () => API.get("/roadmap");
export const completeMilestone = (milestoneId: string) =>
  API.post(`/roadmap/milestone/${milestoneId}`);

// Booking System
export const createBooking = (data: any) => API.post("/bookings", data);
export const setAvailability = (data: any) =>
  API.post("/bookings/availability", data);
export const getMyBookings = (params?: { is_mentor: boolean }) =>
  API.get("/bookings/my", { params });

// Session Management
export const getSessions = () => API.get("/sessions");
export const getSessionDetails = (id: string) => API.get(`/sessions/${id}`);
export const submitFeedback = (data: {
  session_id: string;
  rating: number;
  review?: string;
}) => API.post("/sessions/feedback", data);

// Authentication
export const login = (credentials: any) =>
  API.post<{ access_token: string }>("/auth/login", credentials);
export const signup = (data: any) =>
  API.post<{ access_token: string }>("/auth/signup", data);

// WebSocket Connection
export const socket = io(SOCKET_URL, {
  autoConnect: false,
  transports: ["websocket"], // Preferred for production
});
