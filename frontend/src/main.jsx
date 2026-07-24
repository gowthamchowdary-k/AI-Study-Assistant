import React from "react";
import ReactDOM from "react-dom/client";
import { Toaster } from "react-hot-toast";

import App from "./App";

import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(

    <React.StrictMode>

        <App />

        <Toaster
            position="top-right"
            reverseOrder={false}
            toastOptions={{
                duration: 3000,
                style: {
                    borderRadius: "10px",
                    background: "#333",
                    color: "#fff",
                    fontSize: "14px"
                },
                success: {
                    iconTheme: {
                        primary: "#22c55e",
                        secondary: "#fff"
                    }
                },
                error: {
                    iconTheme: {
                        primary: "#ef4444",
                        secondary: "#fff"
                    }
                }
            }}
        />

    </React.StrictMode>

);