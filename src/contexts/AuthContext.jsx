import React, { createContext, useContext, useState, useEffect } from 'react';
import { http, setCsrf } from '../services/http';
const AuthContext = createContext(null);

export function AuthProvider({children}) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    let live = true;
    http.get('/auth/me').then(res => {
      if (!live) return;
      setCsrf(res.csrf); setUser(res.user);
    }).catch(() => { if (live) { setCsrf('');setUser(null); } }).finally(() => { if (live) setIsLoading(false); });
    return () => { live = false; };
  }, []);
  const login = async (email,password) => {
    const result = await http.post('/auth/login', {email,password});
    setCsrf(result.csrf); setUser(result.user);
    return {success:true, role:result.user.role};
  };
  const register = async (fullName,email,password) => {
    const result = await http.post('/auth/register', {full_name:fullName,email,password});
    setCsrf(result.csrf); setUser(result.user);
    return {success:true,role:result.user.role,requiresConfirmation:false};
  };
  const logout = async () => {
    try { await http.post('/auth/logout'); } finally { setCsrf('');setUser(null); }
  };
  const resetPassword = async () => { throw new Error('Email password recovery is not configured. Contact the administrator for account recovery.'); };
  const quickDemoLogin = () => { throw new Error('Demo bypass authentication has been removed. Sign in with a real account.'); };
  const updateProfile = async data => { const updated = await http.patch('/profile',data);setUser(updated);return updated; };
  return <AuthContext.Provider value={{user,role:user?.role || 'student',isAdmin:user?.role==='admin',isAuthenticated:!!user,isLoading,login,register,logout,resetPassword,quickDemoLogin,isSupabaseConnected:true,updateProfile}}>{children}</AuthContext.Provider>;
}
export function useAuth(){ const value=useContext(AuthContext);if(!value)throw new Error('Auth context missing');return value; }
