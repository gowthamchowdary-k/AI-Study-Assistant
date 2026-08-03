import { useEffect, useState } from "react";
import toast from "react-hot-toast";

import {
    getDocuments,
    uploadPDF,
    deleteDocument
} from "../services/api";

export default function useDocuments() {

    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    // ----------------------------
    // Fetch Documents
    // ----------------------------

    async function refreshDocuments() {

        try {

            setLoading(true);

            setError("");

            const response = await getDocuments();

            setDocuments(response.documents || []);

        }

        catch (err) {

            const message = err.message || "Failed to load documents.";

            setError(message);

            toast.error(message);

        }

        finally {

            setLoading(false);

        }

    }

    // ----------------------------
    // Upload PDF
    // ----------------------------

    async function upload(file) {

        if (!file) return;

        if (loading) return;

        // Validate file extension
        const allowedExtensions = [".pdf", ".docx", ".pptx", ".txt", ".png", ".jpg", ".jpeg", ".webp"];
        const ext = "." + file.name.split('.').pop().toLowerCase();
        if (!allowedExtensions.includes(ext)) {

            toast.error("Unsupported format. Please upload PDF, DOCX, PPTX, TXT, or Image (PNG, JPG, JPEG, WEBP).");

            return;

        }

        // 20 MB limit
        if (file.size > 20 * 1024 * 1024) {

            toast.error("Maximum file size is 20 MB.");

            return;

        }

        try {

            setLoading(true);

            setError("");

            await uploadPDF(file);

            await refreshDocuments();

            toast.success(`${file.name} uploaded successfully.`);

        }

        catch (err) {

            const message = err.message || "Upload failed.";

            setError(message);

            toast.error(message);

            throw err;

        }

        finally {

            setLoading(false);

        }

    }

    // ----------------------------
    // Delete PDF
    // ----------------------------

    async function remove(filename) {

        if (loading) return;

        try {

            setLoading(true);

            setError("");

            await deleteDocument(filename);

            setDocuments(prev => prev.filter(doc => doc !== filename));

            toast.success("Document deleted.");

        }

        catch (err) {

            const message = err.message || "Delete failed.";

            setError(message);

            toast.error(message);

        }

        finally {

            setLoading(false);

        }

    }

    useEffect(() => {

        refreshDocuments();

    }, []);

    return {

        documents,

        loading,

        error,

        upload,

        remove,

        refreshDocuments

    };

}