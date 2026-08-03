import { motion } from "framer-motion";
import {
    FiBook,
    FiFileText,
    FiHelpCircle,
    FiClipboard,
    FiZap
} from "react-icons/fi";

export default function EmptyState({

    onSuggestionClick,

    onUploadClick,

    onAskClick,

    onLearnClick

}) {

    const suggestions = [
        "Summarize Docs",
        "Generate Notes",
        "Generate Quiz",
        "Explain Concepts"
    ];

    return (

        <div className="flex flex-col items-center justify-center h-full px-6 text-center">

            <motion.div

                initial={{ scale: 0.9, opacity: 0 }}

                animate={{ scale: 1, opacity: 1 }}

                transition={{ duration: 0.4 }}

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

                {/* Logo */}

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
                        size={40}
                        className="text-blue-600"
                    />

                </div>

                {/* Title */}

                <h1 className="text-3xl font-bold text-gray-800">

                    Welcome to AI Study Assistant

                </h1>

                {/* Subtitle */}

                <p className="text-gray-500 mt-3 text-base leading-7">

                    Upload study materials and interact with them using AI.
                    Ask questions, generate summaries, notes,
                    quizzes, and explore concepts effortlessly.

                </p>

                {/* Suggestions */}

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">

                    {

                        suggestions.map((item) => (

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
                                    hover:shadow-md
                                    transition
                                "

                            >

                                <div className="flex items-center gap-3">

                                    <FiZap className="text-blue-600" />

                                    <span className="font-medium">

                                        {item}

                                    </span>

                                </div>

                            </button>

                        ))

                    }

                </div>

                {/* Bottom Features */}

                <div className="grid grid-cols-3 gap-4 mt-10">

                    <button

                        onClick={onUploadClick}

                        className="
                            flex
                            flex-col
                            items-center
                            p-4
                            rounded-xl
                            hover:bg-blue-50
                            transition
                        "

                    >

                        <FiFileText

                            size={28}

                            className="mb-2 text-blue-600"

                        />

                        <span className="text-sm font-medium text-gray-600">

                            Upload Materials

                        </span>

                    </button>

                    <button

                        onClick={onAskClick}

                        className="
                            flex
                            flex-col
                            items-center
                            p-4
                            rounded-xl
                            hover:bg-green-50
                            transition
                        "

                    >

                        <FiHelpCircle

                            size={28}

                            className="mb-2 text-green-600"

                        />

                        <span className="text-sm font-medium text-gray-600">

                            Ask Questions

                        </span>

                    </button>

                    <button

                        onClick={onLearnClick}

                        className="
                            flex
                            flex-col
                            items-center
                            p-4
                            rounded-xl
                            hover:bg-purple-50
                            transition
                        "

                    >

                        <FiClipboard

                            size={28}

                            className="mb-2 text-purple-600"

                        />

                        <span className="text-sm font-medium text-gray-600">

                            Learn Smarter

                        </span>

                    </button>

                </div>

            </motion.div>

        </div>

    );

}