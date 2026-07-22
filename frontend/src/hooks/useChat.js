import { useState, useEffect } from "react";
import toast from "react-hot-toast";

import {
    sendMessage,
    resetChat,
    getHistory
} from "../services/api";

export default function useChat() {

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    useEffect(() => {

        loadHistory();

    }, []);

    async function loadHistory() {

        try {

            const response = await getHistory();

            if (response.success) {

                setMessages(response.messages || []);

            }

        }

        catch (err) {

            console.error(err);

            toast.error("Couldn't load previous chat.");

        }

    }

    async function ask(question) {

        const text = question.trim();

        if (!text || loading) return;

        setLoading(true);

        setError("");

        const userMessage = {

            role: "user",

            content: text

        };

        setMessages(prev => [

            ...prev,

            userMessage

        ]);

        try {

            const response = await sendMessage(text);

            const assistantMessage = {

                role: "assistant",

                content: response.answer || "No response received.",

                sources: response.sources || []

            };

            setMessages(prev => [

                ...prev,

                assistantMessage

            ]);

        }

        catch (err) {

            const message = err.message || "Something went wrong.";

            setError(message);

            toast.error(message);

        }

        finally {

            setLoading(false);

        }

    }

    async function clearConversation() {

        try {

            await resetChat();

            setMessages([]);

            setError("");

            toast.success("Conversation cleared.");

        }

        catch (err) {

            const message = err.message || "Unable to clear conversation.";

            setError(message);

            toast.error(message);

        }

    }

    return {

        messages,

        loading,

        error,

        ask,

        clearConversation

    };

}