import { FiInfo } from "react-icons/fi";

export default function Header({ onAbout }) {

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

            </div>

        </header>

    );

}