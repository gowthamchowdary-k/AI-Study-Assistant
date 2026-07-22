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

    return (

        <div className="h-screen flex flex-col bg-gray-100">

            <Header />

            <div className="flex flex-1 overflow-hidden">

                <Sidebar

                    documents={documents}
                    upload={upload}
                    remove={remove}

                />

                <main className="flex flex-col flex-1">

                    <div className="flex justify-end p-3 bg-white border-b">

                        <button

                            onClick={clearConversation}

                            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"

                        >
                            Clear Chat
                        </button>

                    </div>

                    {error && (

                        <div className="bg-red-100 text-red-700 p-3 text-center">

                            {error}

                        </div>

                    )}

                    <ChatWindow

                        messages={messages}
                        loading={loading}

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