import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const backendTarget = "http://127.0.0.1:5000";

function backendProxy(path) {
  return {
    target: backendTarget,
    changeOrigin: true,
    configure: (proxy) => {
      proxy.on("error", (error, req, res) => {
        if (res.headersSent) return;

        res.writeHead(503, { "Content-Type": "application/json" });
        res.end(JSON.stringify({
          error: "Backend is offline. Start the Flask server on port 5000, then try again.",
        }));
      });
    },
  };
}

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/chat": backendProxy("/chat"),
      "/health": backendProxy("/health"),
      "/reset": backendProxy("/reset"),
    },
  },
});
