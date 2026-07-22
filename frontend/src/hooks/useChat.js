import { useState, useEffect } from "react";

import {
    sendMessage,
    resetChat,
    getHistory
} from "../services/api";

export default function useChat() {

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    // ----------------------------
    // Load previous chat on startup
    // ----------------------------
    useEffect(() => {

        loadHistory();

    }, []);

    async function loadHistory() {

        try {

            const response = await getHistory();

            if (response.success) {

                setMessages(response.messages || []);

            }

        } catch (err) {

            console.error("Failed to load history:", err);

        }

    }

    // ----------------------------
    // Send Message
    // ----------------------------
    async function ask(question) {

        if (!question.trim()) return;

        setLoading(true);

        setError("");

        const userMessage = {

            role: "user",

            content: question

        };

        setMessages(prev => [

            ...prev,

            userMessage

        ]);

        try {

            const response = await sendMessage(question);

            setMessages(prev => [

                ...prev,

                {

                    role: "assistant",

                    content: response.answer,

                    sources: response.sources || []

                }

            ]);

        }

        catch (err) {

            setError(err.message);

        }

        finally {

            setLoading(false);

        }

    }

    // ----------------------------
    // Clear Conversation
    // ----------------------------
    async function clearConversation() {

        try {

            await resetChat();

            setMessages([]);

            setError("");

        }

        catch (err) {

            setError(err.message);

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