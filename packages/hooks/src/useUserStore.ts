import { create } from "zustand";

interface UserState {
  user: any;
  token: string | null;
  setUser: (user: any) => void;
  setToken: (token: string) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  token: null,
  setUser: (user) => set({ user }),
  setToken: (token) => set({ token }),
  logout: () => set({ user: null, token: null }),
}));
