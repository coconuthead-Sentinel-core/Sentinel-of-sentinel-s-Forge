import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type PropsWithChildren,
} from "react";
import { getProfile, type TokenResponse, type UserProfile } from "../lib/api";

type AuthState = {
  tokens: TokenResponse | null;
  profile: UserProfile | null;
  loading: boolean;
};

type AuthContextType = {
  tokens: TokenResponse | null;
  profile: UserProfile | null;
  isAuthenticated: boolean;
  loading: boolean;
  setSession: (tokens: TokenResponse) => Promise<void>;
  logout: () => void;
};

const STORAGE_KEY = "sf_tokens";

function loadTokens(): TokenResponse | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as TokenResponse) : null;
  } catch {
    return null;
  }
}

function saveTokens(tokens: TokenResponse | null) {
  if (tokens) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tokens));
  } else {
    localStorage.removeItem(STORAGE_KEY);
  }
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: PropsWithChildren) {
  const [state, setState] = useState<AuthState>({
    tokens: null,
    profile: null,
    loading: true,
  });

  // On mount, restore session from localStorage
  useEffect(() => {
    const stored = loadTokens();
    if (!stored?.access_token) {
      setState({ tokens: null, profile: null, loading: false });
      return;
    }
    getProfile(stored.access_token)
      .then((profile) => {
        setState({ tokens: stored, profile, loading: false });
      })
      .catch(() => {
        saveTokens(null);
        setState({ tokens: null, profile: null, loading: false });
      });
  }, []);

  const setSession = useCallback(async (tokens: TokenResponse) => {
    saveTokens(tokens);
    const profile = await getProfile(tokens.access_token);
    setState({ tokens, profile, loading: false });
  }, []);

  const logout = useCallback(() => {
    saveTokens(null);
    setState({ tokens: null, profile: null, loading: false });
  }, []);

  const value = useMemo<AuthContextType>(
    () => ({
      tokens: state.tokens,
      profile: state.profile,
      isAuthenticated: Boolean(state.tokens?.access_token),
      loading: state.loading,
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
