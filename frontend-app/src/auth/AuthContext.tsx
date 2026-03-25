import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type PropsWithChildren,
} from "react";
import { getProfile, type TokenResponse, type UserProfile } from "../lib/api";

type AuthState = {
  tokens: TokenResponse | null;
  profile: UserProfile | null;
};

type AuthContextType = {
  tokens: TokenResponse | null;
  profile: UserProfile | null;
  isAuthenticated: boolean;
  setSession: (tokens: TokenResponse) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: PropsWithChildren) {
  const [state, setState] = useState<AuthState>({ tokens: null, profile: null });

  const setSession = useCallback(async (tokens: TokenResponse) => {
    // Runtime memory only: no localStorage/sessionStorage usage.
    const profile = await getProfile(tokens.access_token);
    setState({ tokens, profile });
  }, []);

  const logout = useCallback(() => {
    setState({ tokens: null, profile: null });
  }, []);

  const value = useMemo<AuthContextType>(
    () => ({
      tokens: state.tokens,
      profile: state.profile,
      isAuthenticated: Boolean(state.tokens?.access_token),
      setSession,
      logout,
    }),
    [state, setSession, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}