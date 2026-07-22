// Backend URL
const API_BASE = "http://127.0.0.1:5000";

async function request(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, options);

    let data = {};

    try {
        data = await response.json();
    } catch (e) {
        // Ignore empty response body
    }

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
    }

    return data;
}

// =======================
// Chat
// =======================

export async function sendMessage(question) {
    return request("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            question,
        }),
    });
}

// NEW
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
        body: formData,
    });
}

// =======================
// Documents
// =======================

export async function getDocuments() {
    return request("/documents");
}

export async function deleteDocument(filename) {
    return request(`/documents/${encodeURIComponent(filename)}`, {
        method: "DELETE",
    });
}

// =======================
// Reset Chat
// =======================

export async function resetChat() {
    return request("/reset", {
        method: "POST",
    });
}

// =======================
// Health Check
// =======================

export async function healthCheck() {
    return request("/health");
}