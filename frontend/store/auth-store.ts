import { create } from "zustand";

type AuthState = {
  accessToken: string | null;
  setToken: (token: string | null) => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  setToken: (token) => set({ accessToken: token }),
}));
