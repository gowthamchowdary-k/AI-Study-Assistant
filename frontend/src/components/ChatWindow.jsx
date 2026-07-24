import { useEffect, useRef } from "react";

import Message from "./Message";
import TypingIndicator from "./TypingIndicator";
import EmptyState from "./EmptyState";

export default function ChatWindow({

    messages = [],

    loading = false,

    onSuggestionClick,

    onUploadClick,

    onAskClick,

    onLearnClick

}) {

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({

            behavior: "smooth"

        });

    }, [messages, loading]);

    return (

        <section
            className="
                flex-1
                overflow-y-auto
                bg-gray-50
                px-3
                sm:px-5
                md:px-8
                py-4
            "
        >

            {

                messages.length === 0 ? (

                    <EmptyState

                        onSuggestionClick={onSuggestionClick}

                        onUploadClick={onUploadClick}

                        onAskClick={onAskClick}

                        onLearnClick={onLearnClick}

                    />

                ) : (

                    <div className="space-y-4">

                        {

                            messages.map((message, index) => (

                                <Message

                                    key={`${message.role}-${index}`}

                                    message={message}

                                />

                            ))

                        }

                        {

                            loading && (

                                <TypingIndicator />

                            )

                        }

                        <div ref={bottomRef}></div>

                    </div>

                )

            }

        </section>

    );

}