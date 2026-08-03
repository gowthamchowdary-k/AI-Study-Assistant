import { useState, useEffect } from "react";
import { Toaster } from "react-hot-toast";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import StudyBuddyPage from "./pages/StudyBuddyPage";
import { getCurrentUser } from "./services/api";

export default function App() {
    const [token, setToken] = useState(localStorage.getItem("token") || "");
    const [user, setUser] = useState(null);
    const [page, setPage] = useState("login"); // 'login' | 'register' | 'dashboard'
    const [checkingAuth, setCheckingAuth] = useState(true);

    useEffect(() => {
        async function verifyAuth() {
            const storedToken = localStorage.getItem("token");
            if (storedToken) {
                try {
                    const response = await getCurrentUser();
                    if (response.success && response.user) {
                        setToken(storedToken);
                        setUser(response.user);
                        setPage("dashboard");
                    } else {
                        handleLogout();
                    }
                } catch (err) {
                    console.error("Token verification failed:", err);
                    handleLogout();
                }
            } else {
                setPage("login");
            }
            setCheckingAuth(false);
        }
        
        verifyAuth();
    }, []);

    function handleLoginSuccess(newToken, authenticatedUser) {
        setToken(newToken);
        setUser(authenticatedUser);
        setPage("dashboard");
    }

    function handleLogout() {
        localStorage.removeItem("token");
        setToken("");
        setUser(null);
        setPage("login");
    }

    if (checkingAuth) {
        return (
            <div className="h-screen w-screen flex flex-col items-center justify-center bg-slate-950 text-white">
                <div className="w-10 h-10 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mb-4"></div>
                <p className="text-slate-400 text-sm font-medium">Verifying session...</p>
            </div>
        );
    }

    return (
        <>
            <Toaster position="top-right" reverseOrder={false} />
            {page === "login" && (
                <LoginPage
                    onLoginSuccess={handleLoginSuccess}
                    onNavigateToRegister={() => setPage("register")}
                />
            )}
            {page === "register" && (
                <RegisterPage
                    onRegisterSuccess={handleLoginSuccess}
                    onNavigateToLogin={() => setPage("login")}
                />
            )}
            {page === "dashboard" && (
                <StudyBuddyPage 
                    user={user} 
                    onLogout={handleLogout} 
                />
            )}
        </>
    );
}