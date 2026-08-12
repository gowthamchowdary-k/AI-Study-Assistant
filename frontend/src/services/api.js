// =======================
// API Configuration
// =======================

const API_BASE =
    import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

const REQUEST_TIMEOUT = 120000;

// =======================
// Generic Request Helper
// =======================

async function request(endpoint, options = {}) {

    const controller = new AbortController();

    const timeout = setTimeout(() => {

        controller.abort();

    }, REQUEST_TIMEOUT);

    // Automatically inject JWT token from localStorage
    const token = localStorage.getItem("token");
    const headers = {
        ...options.headers,
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    try {

        const response = await fetch(

            `${API_BASE}${endpoint}`,

            {

                ...options,
                headers,
                signal: controller.signal

            }

        );

        clearTimeout(timeout);

        let data = {};

        try {

            data = await response.json();

        }

        catch {

            // Ignore empty body

        }

        if (!response.ok) {

            throw new Error(

                data.error ||

                `Request failed (${response.status})`

            );

        }

        return data;

    }

    catch (err) {

        clearTimeout(timeout);

        if (err.name === "AbortError") {

            throw new Error(

                "Request timed out. Please try again."

            );

        }

        throw err;

    }

}

// =======================
// Auth Services
// =======================

export async function loginUser(email, password) {

    return request("/auth/login", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({ email, password })

    });

}

export async function registerUser(email, password) {

    return request("/auth/register", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({ email, password })

    });

}

export async function getCurrentUser() {

    return request("/auth/me");

}

// =======================
// Chat
// =======================

export async function sendMessage(question, actionId = null) {

    return request("/chat", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            question,
            action_id: actionId

        })

    });

}

// =======================
// Chat History
// =======================

export async function getHistory() {

    return request("/history");

}

// =======================
// Upload PDF
// =======================

export async function uploadPDF(file) {

    const formData = new FormData();

    formData.append("file", file);

    return request("/upload", {

        method: "POST",

        body: formData

    });

}

// =======================
// Documents
// =======================

export async function getDocuments() {

    return request("/documents");

}

export async function deleteDocument(filename) {

    return request(

        `/documents/${encodeURIComponent(filename)}`,

        {

            method: "DELETE"

        }

    );

}

// =======================
// Reset Conversation
// =======================

export async function resetChat() {

    return request("/reset", {

        method: "POST"

    });

}

// =======================
// Health Check
// =======================

export async function healthCheck() {

    return request("/health");

}