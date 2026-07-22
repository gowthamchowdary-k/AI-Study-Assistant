import { FiTrash2, FiFileText } from "react-icons/fi";
import { motion } from "framer-motion";

export default function DocumentList({

    documents,

    onDelete

}) {

    if (documents.length === 0) {

        return (

            <div className="text-center py-10">

                <FiFileText
                    className="mx-auto text-gray-400 mb-3"
                    size={40}
                />

                <p className="text-gray-500 text-sm">

                    No PDFs uploaded yet.

                </p>

                <p className="text-xs text-gray-400 mt-2">

                    Upload a PDF to start chatting.

                </p>

            </div>

        );

    }

    return (

        <div className="space-y-3">

            {

                documents.map((doc) => (

                    <motion.div

                        key={doc}

                        whileHover={{
                            scale: 1.02
                        }}

                        whileTap={{
                            scale: 0.98
                        }}

                        className="
                            bg-white
                            border
                            border-gray-200
                            rounded-xl
                            shadow-sm
                            hover:shadow-md
                            transition-all
                            duration-200
                            p-3
                        "

                    >

                        <div className="flex items-center justify-between gap-3">

                            <div className="flex items-center gap-3 flex-1 min-w-0">

                                <div
                                    className="
                                        bg-blue-100
                                        p-2
                                        rounded-lg
                                        flex-shrink-0
                                    "
                                >

                                    <FiFileText
                                        className="text-blue-600"
                                        size={20}
                                    />

                                </div>

                                <div className="min-w-0">

                                    <p
                                        className="
                                            text-sm
                                            font-medium
                                            text-gray-800
                                            truncate
                                        "
                                        title={doc}
                                    >
                                        {doc}
                                    </p>

                                    <p className="text-xs text-gray-400">

                                        PDF Document

                                    </p>

                                </div>

                            </div>

                            <button

                                onClick={() => onDelete(doc)}

                                className="
                                    text-red-500
                                    hover:bg-red-100
                                    hover:text-red-700
                                    p-2
                                    rounded-lg
                                    transition
                                    flex-shrink-0
                                "

                                title="Delete PDF"

                            >

                                <FiTrash2 size={18} />

                            </button>

                        </div>

                    </motion.div>

                ))

            }

        </div>

    );

}