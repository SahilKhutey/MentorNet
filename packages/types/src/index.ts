export type UserRole = "mentor" | "student" | "admin";

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  avatar?: string;
  bio?: string;
}

export interface Mentor extends User {
  expertise: string[];
  field: string;
  rating: number;
  reviewCount: number;
  availability: AvailabilitySlot[];
  hourlyRate?: number;
}

export interface AvailabilitySlot {
  day: string; // e.g., "Monday"
  slots: string[]; // e.g., ["10:00", "14:00"]
}

export interface Booking {
  id: string;
  mentorId: string;
  studentId: string;
  status: "pending" | "confirmed" | "cancelled" | "completed";
  time: string;
  duration: number; // in minutes
  topic?: string;
}

export interface Message {
  id: string;
  senderId: string;
  receiverId: string;
  content: string;
  timestamp: string;
  isRead: boolean;
}

export interface RecommendationResponse {
  data: Mentor[];
  metadata: {
    total: number;
    latency: number;
  };
}
