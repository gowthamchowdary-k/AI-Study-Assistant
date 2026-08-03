import { FiInfo, FiLogOut, FiUser } from "react-icons/fi";

export default function Header({ onAbout, user, onLogout }) {

    return (

        <header className="bg-blue-600 text-white shadow-md">

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

                    <h1 className="text-xl sm:text-2xl md:text-3xl font-bold break-words">
                        💬 MY AI Study Assistant
                    </h1>

                    <p className="mt-1 text-xs sm:text-sm md:text-base text-blue-100">
                        Ask questions from your uploaded PDF
                    </p>

                </div>

                {/* Right Section */}

                <div className="flex items-center gap-3">
                    
                    {/* User profile identity */}
                    {user && (
                        <div className="hidden sm:flex items-center gap-2 bg-white/10 px-3 py-1.5 rounded-lg border border-white/10">
                            <FiUser className="text-blue-200" size={14} />
                            <span className="text-xs font-medium text-blue-50">{user.email}</span>
                        </div>
                    )}

                    <button

                        onClick={onAbout}

                        className="
                            flex
                            items-center
                            gap-2
                            bg-white/15
                            hover:bg-white/25
                            transition-all
                            duration-200
                            px-4
                            py-2
                            rounded-lg
                            text-sm
                            font-medium
                            border
                            border-white/20
                        "

                    >

                        <FiInfo size={18} />

                        About

                    </button>

                    {onLogout && (
                        <button
                            onClick={onLogout}
                            className="
                                flex
                                items-center
                                gap-1.5
                                bg-red-600
                                hover:bg-red-700
                                transition-all
                                duration-200
                                px-4
                                py-2
                                rounded-lg
                                text-sm
                                font-medium
                                border
                                border-red-500/20
                            "
                            title="Log Out"
                        >
                            <FiLogOut size={16} />
                            <span>Logout</span>
                        </button>
                    )}

                </div>

            </div>

        </header>

    );

}