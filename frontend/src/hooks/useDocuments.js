import { useEffect, useState } from "react";

import {
    getDocuments,
    uploadPDF,
    deleteDocument
} from "../services/api";

export default function useDocuments() {

    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    async function refreshDocuments() {

        try {

            setLoading(true);

            const response = await getDocuments();

            setDocuments(response.documents || []);

        } catch (err) {

            setError(err.message);

        } finally {

            setLoading(false);

        }

    }

    async function upload(file) {

        try {

            setLoading(true);

            await uploadPDF(file);

            await refreshDocuments();

        } catch (err) {

            setError(err.message);

            throw err;

        } finally {

            setLoading(false);

        }

    }

    async function remove(filename) {

        try {

            setLoading(true);

            await deleteDocument(filename);

            await refreshDocuments();

        } catch (err) {

            setError(err.message);

        } finally {

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