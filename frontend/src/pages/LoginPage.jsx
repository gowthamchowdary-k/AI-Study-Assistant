import { useState } from "react";
import { motion } from "framer-motion";
import { loginUser } from "../services/api";
import toast from "react-hot-toast";
import { FiMail, FiLock, FiBookOpen } from "react-icons/fi";

export default function LoginPage({ onLoginSuccess, onNavigateToRegister }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e) {
        e.preventDefault();
        
        const cleanEmail = email.trim();
        if (!cleanEmail || !password) {
            toast.error("Please fill in all fields.");
            return;
        }

        try {
            setLoading(true);
            const response = await loginUser(cleanEmail, password);
            if (response.success && response.token) {
                localStorage.setItem("token", response.token);
                toast.success("Welcome back! 👋");
                onLoginSuccess(response.token, response.user);
            } else {
                toast.error(response.error || "Login failed. Check your credentials.");
            }
        } catch (err) {
            console.error(err);
            toast.error(err.message || "Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-950 relative overflow-hidden px-4">
            {/* Animated background highlights */}
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-[100px] animate-pulse"></div>
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[100px] animate-pulse delay-1000"></div>

            <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-md"
            >
                <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800 rounded-3xl p-8 shadow-2xl">
                    
                    {/* Header */}
                    <div className="flex flex-col items-center mb-8">
                        <div className="w-14 h-14 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/20 mb-4">
                            <FiBookOpen size={28} className="text-white" />
                        </div>
                        <h2 className="text-2xl font-bold text-white tracking-tight">AI Study Assistant</h2>
                        <p className="text-slate-400 text-sm mt-1">Sign in to your learning dashboard</p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-6">
                        
                        {/* Email */}
                        <div>
                            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                                Email Address
                            </label>
                            <div className="relative">
                                <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400 pointer-events-none">
                                    <FiMail size={18} />
                                </span>
                                <input
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    placeholder="you@example.com"
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-11 pr-4 text-white text-sm placeholder-slate-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition duration-200 outline-none"
                                />
                            </div>
                        </div>

                        {/* Password */}
                        <div>
                            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                                Password
                            </label>
                            <div className="relative">
                                <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400 pointer-events-none">
                                    <FiLock size={18} />
                                </span>
                                <input
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    placeholder="••••••••"
                                    className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-11 pr-4 text-white text-sm placeholder-slate-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition duration-200 outline-none"
                                />
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 active:scale-[0.98] text-white py-3.5 rounded-xl font-medium shadow-lg shadow-blue-500/20 transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center text-sm"
                        >
                            {loading ? (
                                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                            ) : (
                                "Sign In"
                            )}
                        </button>
                    </form>

                    {/* Footer Links */}
                    <div className="mt-8 text-center border-t border-slate-800/60 pt-6">
                        <p className="text-slate-400 text-sm">
                            Don't have an account?{" "}
                            <button
                                onClick={onNavigateToRegister}
                                className="text-blue-500 hover:text-blue-400 font-semibold transition"
                            >
                                Sign Up
                            </button>
                        </p>
                    </div>

                </div>
            </motion.div>
        </div>
    );
}
