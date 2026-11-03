import React from 'react';
import {Link} from 'react-router-dom';
import {Card} from '../../components/common/Card';
import {KeyRound} from 'lucide-react';
export const ForgotPasswordPage = () => <div className="min-h-[70vh] flex items-center justify-center px-4"><Card className="p-8 max-w-md text-center space-y-4"><KeyRound className="text-brand-600 w-10 h-10 mx-auto"/><h1 className="text-xl font-black">Account recovery</h1><p className="text-sm text-slate-600">Self-service recovery email is not configured for this deployment. Ask your LingoBridge administrator to reset your password securely. No reset email has been sent.</p><Link to="/login" className="block text-brand-600 text-sm font-semibold">Return to sign in →</Link></Card></div>;
