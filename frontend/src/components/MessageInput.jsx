import { useState } from "react";

export default function MessageInput({

    onSend,

    loading

}) {

    const [text, setText] = useState("");

    function handleSubmit(e) {

        e.preventDefault();

        if (!text.trim()) return;

        onSend(text);

        setText("");

    }

    return (

        <form

            onSubmit={handleSubmit}

            className="border-t bg-white p-4 flex gap-3"

        >

            <input

                className="flex-1 border rounded-lg px-4 py-2"

                placeholder="Ask anything..."

                value={text}

                onChange={(e) => setText(e.target.value)}

                disabled={loading}

            />

            <button

                className="bg-blue-600 text-white px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400"

                disabled={loading}

            >

                Send

            </button>

        </form>

    );

}