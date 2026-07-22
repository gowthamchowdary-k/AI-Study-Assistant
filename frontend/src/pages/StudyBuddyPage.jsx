import { useState } from "react";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import MessageInput from "../components/MessageInput";

import useChat from "../hooks/useChat";
import useDocuments from "../hooks/useDocuments";

export default function StudyBuddyPage() {

    const {

        messages,
        loading,
        error,
        ask,
        clearConversation

    } = useChat();

    const {

        documents,
        upload,
        remove

    } = useDocuments();

    const [showSidebar, setShowSidebar] = useState(false);

    // Called when a suggestion card is clicked
    const handleSuggestionClick = (prompt) => {
        ask(prompt);
    };

    return (

        <div className="h-screen flex flex-col bg-gray-100">

            <Header />

            {/* Mobile Top Bar */}

            <div className="md:hidden flex items-center justify-between bg-white border-b px-4 py-3">

                <button
                    onClick={() => setShowSidebar(!showSidebar)}
                    className="text-2xl"
                >
                    ☰
                </button>

                <button
                    onClick={clearConversation}
                    className="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-lg text-sm transition"
                >
                    Clear Chat
                </button>

            </div>

            <div className="flex flex-1 overflow-hidden">

                {/* Desktop Sidebar */}

                <div className="hidden md:block">

                    <Sidebar
                        documents={documents}
                        upload={upload}
                        remove={remove}
                    />

                </div>

                {/* Mobile Sidebar */}

                {

                    showSidebar && (

                        <div
                            className="fixed inset-0 z-50 bg-black/40 md:hidden"
                            onClick={() => setShowSidebar(false)}
                        >

                            <div
                                className="w-72 h-full bg-white"
                                onClick={(e) => e.stopPropagation()}
                            >

                                <Sidebar
                                    documents={documents}
                                    upload={upload}
                                    remove={remove}
                                />

                            </div>

                        </div>

                    )

                }

                <main className="flex flex-col flex-1">

                    {/* Desktop Clear Chat */}

                    <div className="hidden md:flex justify-end p-3 bg-white border-b">

                        <button
                            onClick={clearConversation}
                            className="
                                bg-red-500
                                hover:bg-red-600
                                transition
                                text-white
                                px-4
                                py-2
                                rounded-lg
                            "
                        >
                            Clear Chat
                        </button>

                    </div>

                    {

                        error && (

                            <div className="bg-red-100 text-red-700 p-3 text-center">

                                {error}

                            </div>

                        )

                    }

                    <ChatWindow
                        messages={messages}
                        loading={loading}
                        onSuggestionClick={handleSuggestionClick}
                    />

                    <MessageInput
                        onSend={ask}
                        loading={loading}
                    />

                </main>

            </div>

        </div>

    );

}