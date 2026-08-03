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

    // Silent refresh to update status badges in the background
    async function silentRefresh() {
        try {
            const response = await getDocuments();
            setDocuments(response.documents || []);
        } catch (err) {
            console.error("Background document refresh failed:", err);
        }
    }

    // ----------------------------
    // Upload File
    // ----------------------------
    async function upload(file) {
        if (!file) return;

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

        // Insert temporary uploading placeholder to make UI feel instantaneous
        const tempId = `temp-${Date.now()}`;
        const tempDoc = {
            filename: tempId,
            original_filename: file.name,
            status: "Uploading",
            created_at: new Date().toISOString()
        };
        setDocuments(prev => [tempDoc, ...prev]);

        try {
            setError("");
            await uploadPDF(file);
            
            // Re-fetch documents to show the database-registered document status (will show 'Indexing')
            const response = await getDocuments();
            setDocuments(response.documents || []);
            
            toast.success(`${file.name} uploaded successfully. Indexing started...`);
        }
        catch (err) {
            // Remove the temporary placeholder
            setDocuments(prev => prev.filter(doc => doc.filename !== tempId));
            
            const message = err.message || "Upload failed.";
            setError(message);
            toast.error(message);
            throw err;
        }
    }

    // ----------------------------
    // Delete Document
    // ----------------------------
    async function remove(filename) {
        try {
            setLoading(true);
            setError("");
            await deleteDocument(filename);
            setDocuments(prev => prev.filter(doc => (doc.filename || doc) !== filename));
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

    // Initial fetch on mount
    useEffect(() => {
        refreshDocuments();
    }, []);

    // Background polling effect to check for status transitions
    useEffect(() => {
        const isProcessing = documents.some(
            doc => doc.status === "Uploaded" || doc.status === "Indexing" || doc.status === "Uploading"
        );

        if (isProcessing) {
            const interval = setInterval(() => {
                silentRefresh();
            }, 3000);
            return () => clearInterval(interval);
        }
    }, [documents]);

    return {
        documents,
        loading,
        error,
        upload,
        remove,
        refreshDocuments
    };
}