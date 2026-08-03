import { FiInfo, FiLogOut, FiUser } from "react-icons/fi";

export default function Header({ onAbout, user, onLogout }) {

    return (

        <header className="bg-slate-900 border-b border-slate-800 text-white shadow-md">

            <div
                className="
                    max-w-full
                    mx-auto
                    px-4
                    sm:px-6
                    lg:px-8
                    py-4
                    flex
                    items-center
                    justify-between
                "
            >

                {/* Left Section */}

                <div>

                    <h1 className="text-xl sm:text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                        📚 AI Study Assistant
                    </h1>

                    <p className="mt-0.5 text-xs text-slate-400">
                        Upload study materials and chat with AI
                    </p>

                </div>

                {/* Right Section */}

                <div className="flex items-center gap-3">
                    
                    {/* User profile identifier */}
                    {user && (
                        <div className="hidden sm:flex items-center gap-2 bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700/60">
                            <FiUser className="text-blue-400" size={14} />
                            <span className="text-xs font-medium text-slate-200">{user.email}</span>
                        </div>
                    )}

                    <button

                        onClick={onAbout}

                        className="
                            flex
                            items-center
                            gap-1.5
                            bg-slate-800/80
                            hover:bg-slate-800
                            border
                            border-slate-700/50
                            transition-all
                            duration-200
                            px-3
                            py-2
                            rounded-lg
                            text-xs
                            font-medium
                            text-slate-300
                        "

                    >

                        <FiInfo size={15} />

                        About

                    </button>

                    {onLogout && (
                        <button
                            onClick={onLogout}
                            className="
                                flex
                                items-center
                                gap-1.5
                                bg-red-950/40
                                hover:bg-red-950/80
                                border
                                border-red-900/40
                                hover:border-red-900/60
                                text-red-400
                                transition-all
                                duration-200
                                px-3
                                py-2
                                rounded-lg
                                text-xs
                                font-medium
                            "
                            title="Log Out"
                        >
                            <FiLogOut size={15} />
                            <span className="hidden xs:inline">Logout</span>
                        </button>
                    )}

                </div>

            </div>

        </header>

    );

}