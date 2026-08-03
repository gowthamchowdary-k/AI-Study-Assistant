import {
    FiX,
    FiCode,
    FiBookOpen
} from "react-icons/fi";

export default function AboutModal({ open, onClose }) {

    if (!open) return null;

    return (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4">

            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-7 relative">

                {/* Close Button */}

                <button
                    onClick={onClose}
                    className="absolute right-5 top-5 text-gray-500 hover:text-red-500 transition"
                >
                    <FiX size={22} />
                </button>

                {/* Logo */}

                <div className="flex justify-center">

                    <div className="w-20 h-20 rounded-full bg-blue-100 flex items-center justify-center">

                        <FiBookOpen
                            size={38}
                            className="text-blue-600"
                        />

                    </div>

                </div>

                {/* Title */}

                <h2 className="text-3xl font-bold text-center mt-5 text-gray-800">

                    AI Study Assistant

                </h2>

                {/* Version Badge */}

                <div className="flex justify-center mt-3">

                    <span className="bg-blue-100 text-blue-700 px-4 py-1 rounded-full text-sm font-semibold">

                        Version 1.0

                    </span>

                </div>

                {/* Description */}

                <p className="mt-6 text-center text-gray-600 leading-8">

    An AI-powered study companion that helps students
    learn from PDF documents using
    <span className="font-semibold"> Retrieval-Augmented Generation (RAG)</span>,
    semantic search, and
    <span className="font-semibold"> Large Language Models (LLMs)</span>.

</p>

                {/* Developers */}

               <div className="mt-8 text-center">

    <h3 className="text-lg font-semibold text-gray-800 mb-4">

        Developed By

    </h3>

    <p className="text-lg font-semibold text-gray-900">

        Kunta Gowtham Chowdary

    </p>

    <p className="text-lg font-semibold text-gray-900 mt-2">

        Nukavarapu Eswar Chowdary

    </p>

    <p className="text-gray-500 mt-4">

        KL University

    </p>

</div>
                {/* Technology Stack */}

                <div className="mt-8">

                    <h3 className="font-semibold text-lg flex items-center gap-2 text-gray-800">

                        <FiCode />

                        Technology Stack

                    </h3>

                    <div className="grid grid-cols-2 gap-3 mt-4">

                        <div className="bg-blue-50 text-blue-700 rounded-lg px-3 py-2 text-sm font-medium">
                            React
                        </div>

                        <div className="bg-green-50 text-green-700 rounded-lg px-3 py-2 text-sm font-medium">
                            Flask
                        </div>

                        <div className="bg-purple-50 text-purple-700 rounded-lg px-3 py-2 text-sm font-medium">
                            Google Gemini
                        </div>

                        <div className="bg-orange-50 text-orange-700 rounded-lg px-3 py-2 text-sm font-medium">
                            FAISS
                        </div>

                        <div className="bg-indigo-50 text-indigo-700 rounded-lg px-3 py-2 text-sm font-medium">
                            Sentence Transformers
                        </div>

                        <div className="bg-cyan-50 text-cyan-700 rounded-lg px-3 py-2 text-sm font-medium">
                            Tailwind CSS
                        </div>

                        <div className="bg-red-50 text-red-700 rounded-lg px-3 py-2 text-sm font-medium">
                            Python
                        </div>

                        <div className="bg-gray-100 text-gray-700 rounded-lg px-3 py-2 text-sm font-medium">
                            PyPDF
                        </div>

                    </div>

                </div>

                {/* Footer */}

                <p className="text-center text-xs text-gray-400 mt-8">

                    Version 1.0 • © 2026 AI Study Assistant

                </p>

            </div>

        </div>

    );

}