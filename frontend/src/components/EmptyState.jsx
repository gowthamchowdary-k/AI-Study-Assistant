import { motion } from "framer-motion";
import {
    FiBook,
    FiFileText,
    FiHelpCircle,
    FiClipboard,
    FiZap
} from "react-icons/fi";

export default function EmptyState({ onSuggestionClick }) {

    const suggestions = [
        "Summarize this PDF",
        "Generate 10 MCQs",
        "Explain this chapter",
        "List important topics"
    ];

    return (

        <div className="flex flex-col items-center justify-center h-full px-6 text-center">

            <motion.div

                initial={{ scale: 0.8, opacity: 0 }}

                animate={{ scale: 1, opacity: 1 }}

                transition={{ duration: 0.5 }}

                className="
                    bg-white
                    rounded-3xl
                    shadow-lg
                    border
                    border-gray-200
                    p-8
                    w-full
                    max-w-3xl
                "

            >

                <div
                    className="
                        mx-auto
                        w-20
                        h-20
                        rounded-full
                        bg-blue-100
                        flex
                        items-center
                        justify-center
                        mb-6
                    "
                >

                    <FiBook
                        size={42}
                        className="text-blue-600"
                    />

                </div>

                <h1 className="text-3xl font-bold text-gray-800">

                    Welcome to MY AI Study Assistant

                </h1>

                <p className="text-gray-500 mt-3 text-base">

                    Upload one or more PDFs and ask questions,
                    generate notes, quizzes, summaries, and much more.

                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">

                    {suggestions.map((item) => (

                        <button

                            key={item}

                            onClick={() => onSuggestionClick?.(item)}

                            className="
                                border
                                rounded-xl
                                px-5
                                py-4
                                text-left
                                hover:bg-blue-50
                                hover:border-blue-300
                                transition
                                shadow-sm
                            "

                        >

                            <div className="flex items-center gap-3">

                                <FiZap className="text-blue-600" />

                                <span className="font-medium">

                                    {item}

                                </span>

                            </div>

                        </button>

                    ))}

                </div>

                <div className="grid grid-cols-3 gap-4 mt-10 text-gray-500">

                    <div className="flex flex-col items-center">

                        <FiFileText
                            size={26}
                            className="mb-2 text-blue-600"
                        />

                        <span className="text-sm">

                            Upload PDFs

                        </span>

                    </div>

                    <div className="flex flex-col items-center">

                        <FiHelpCircle
                            size={26}
                            className="mb-2 text-green-600"
                        />

                        <span className="text-sm">

                            Ask Questions

                        </span>

                    </div>

                    <div className="flex flex-col items-center">

                        <FiClipboard
                            size={26}
                            className="mb-2 text-purple-600"
                        />

                        <span className="text-sm">

                            Learn Faster

                        </span>

                    </div>

                </div>

            </motion.div>

        </div>

    );

}