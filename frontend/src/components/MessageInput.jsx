import { useState, useRef, useEffect } from "react";

export default function MessageInput({

    onSend,

    loading,

    inputFocusRef

}) {

    const [text, setText] = useState("");

    const textareaRef = useRef(null);

    useEffect(() => {

        if (inputFocusRef) {

            inputFocusRef.current = () => {

                textareaRef.current?.focus();

            };

        }

    }, [inputFocusRef]);

    function handleSubmit(e) {

        e.preventDefault();

        if (!text.trim()) return;

        onSend(text.trim());

        setText("");

        textareaRef.current?.focus();

    }

    return (

        <form

            onSubmit={handleSubmit}

            className="
                border-t
                bg-white
                p-3
                sm:p-4
                flex
                gap-3
                items-end
            "

        >

            <textarea

                ref={textareaRef}

                rows={1}

                className="
                    flex-1
                    border
                    border-gray-300
                    rounded-xl
                    px-4
                    py-3
                    resize-none
                    outline-none
                    focus:ring-2
                    focus:ring-blue-500
                    focus:border-blue-500
                    text-sm
                    sm:text-base
                "

                placeholder="Ask anything about your uploaded PDFs..."

                value={text}

                onChange={(e) => setText(e.target.value)}

                disabled={loading}

                onKeyDown={(e) => {

                    if (e.key === "Enter" && !e.shiftKey) {

                        e.preventDefault();

                        handleSubmit(e);

                    }

                }}

            />

            <button

                type="submit"

                disabled={loading || !text.trim()}

                className="
                    bg-blue-600
                    hover:bg-blue-700
                    disabled:bg-gray-400
                    disabled:cursor-not-allowed
                    transition
                    text-white
                    px-5
                    sm:px-6
                    py-3
                    rounded-xl
                    font-medium
                "

            >

                {loading ? "..." : "Send"}

            </button>

        </form>

    );

}