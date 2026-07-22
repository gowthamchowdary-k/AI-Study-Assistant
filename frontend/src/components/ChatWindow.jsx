import Message from "./Message";
import TypingIndicator from "./TypingIndicator";

export default function ChatWindow({ messages = [], loading = false }) {
    return (
        <section className="flex-1 overflow-y-auto bg-gray-50 p-4">
            {messages.length === 0 ? (
                <div className="flex h-full items-center justify-center text-center text-gray-500">
                    Ask a question to start your study session.
                </div>
            ) : (
                messages.map((message, index) => (
                    <Message
                        key={`${message.role}-${index}`}
                        message={message}
                    />
                ))
            )}

            {loading && <TypingIndicator />}
        </section>
    );
}
