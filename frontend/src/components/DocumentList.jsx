import { FiTrash2, FiFileText, FiImage } from "react-icons/fi";
import { motion } from "framer-motion";

function getDocTypeLabel(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    switch(ext) {
        case 'pdf': return 'PDF Document';
        case 'docx': return 'Word Document';
        case 'pptx': return 'PowerPoint';
        case 'txt': return 'Text Document';
        case 'png':
        case 'jpg':
        case 'jpeg':
        case 'webp':
            return 'Image (OCR)';
        default:
            return 'Document';
    }
}

function getStatusBadge(status, errorMessage) {
    switch (status) {
        case 'Uploading':
            return (
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-100 animate-pulse">
                    Uploading...
                </span>
            );
        case 'Uploaded':
            return (
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-gray-50 text-gray-700 border border-gray-100">
                    Uploaded
                </span>
            );
        case 'Indexing':
            return (
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-indigo-50 text-indigo-700 border border-indigo-100 animate-pulse">
                    <span className="w-1 h-1 bg-indigo-600 rounded-full animate-ping"></span>
                    Indexing...
                </span>
            );
        case 'Ready':
            return (
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-green-50 text-green-700 border border-green-100">
                    Ready
                </span>
            );
        case 'Failed':
            return (
                <span 
                    className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-red-50 text-red-700 border border-red-100 cursor-help"
                    title={errorMessage || "Indexing failed. Hover to see error."}
                >
                    Failed ⚠️
                </span>
            );
        default:
            return null;
    }
}

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
                    No study materials uploaded.
                </p>
                <p className="text-xs text-gray-400 mt-2">
                    Upload files to start studying.
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-3">
            {
                documents.map((doc) => {
                    const filename = doc.filename || doc;
                    const originalName = doc.original_filename || filename;
                    const status = doc.status || "Ready";
                    const errorMsg = doc.error_message || "";
                    
                    const ext = filename.split('.').pop().toLowerCase();
                    const isImg = ['png','jpg','jpeg','webp'].includes(ext);
                    
                    return (
                        <motion.div
                            key={filename}
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
                                        className={`
                                            p-2
                                            rounded-lg
                                            flex-shrink-0
                                            ${isImg ? 'bg-purple-100 text-purple-600' : 'bg-blue-100 text-blue-600'}
                                        `}
                                    >
                                        {isImg ? (
                                            <FiImage size={20} />
                                        ) : (
                                            <FiFileText size={20} />
                                        )}
                                    </div>
                                    
                                    <div className="min-w-0">
                                        <p
                                            className="
                                                text-sm
                                                font-medium
                                                text-gray-800
                                                truncate
                                            "
                                            title={originalName}
                                        >
                                            {originalName}
                                        </p>
                                        
                                        <div className="flex items-center gap-2 mt-0.5">
                                            <span className="text-xs text-gray-400">
                                                {getDocTypeLabel(filename)}
                                            </span>
                                            {getStatusBadge(status, errorMsg)}
                                        </div>
                                    </div>
                                </div>

                                <button
                                    onClick={() => onDelete(filename)}
                                    className="
                                        text-red-500
                                        hover:bg-red-100
                                        hover:text-red-700
                                        p-2
                                        rounded-lg
                                        transition
                                        flex-shrink-0
                                    "
                                    title="Delete Document"
                                >
                                    <FiTrash2 size={18} />
                                </button>
                            </div>
                        </motion.div>
                    );
                })
            }
        </div>
    );
}