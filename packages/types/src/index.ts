export interface User {
  id: string;
  name: string;
  email: string;
  role: "student" | "mentor" | "admin";
  created_at: string;
}

export interface Profile {
  id: string;
  user_id: string;
  full_name: string;
  headline: string;
  primary_field: string;
  bio: string;
  profile_score: number;
  tags: Tag[];
}

export interface Tag {
  id: string;
  name: string;
}

export interface Lab {
  id: string;
  name: string;
  pi_id: string;
  institution: string;
  description?: string;
  members?: User[];
}

export interface Badge {
  id: string;
  name: string;
  icon: string;
  description: string;
  rarity: "common" | "rare" | "elite";
}

export interface Notification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  type: "message" | "booking" | "ai_insight" | "system";
  is_read: boolean;
  created_at: string;
}

export interface Resume {
  id: string;
  user_id: string;
  file_path: string;
  analysis_results?: ResumeAnalysis;
  score: number;
}

export interface ResumeAnalysis {
  strengths: string[];
  weaknesses: string[];
  mentor_recommendation: string;
  score: number;
}

export interface Booking {
  id: string;
  student_id: string;
  mentor_id: string;
  start_time: string;
  end_time: string;
  status: "pending" | "confirmed" | "completed" | "cancelled";
  topic: string;
}
