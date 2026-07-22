import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { FiCopy, FiCheck } from "react-icons/fi";
import { useState } from "react";
import CodeBlock from "./CodeBlock";

export default function Message({ message }) {

    const isUser = message.role === "user";

    const [copied, setCopied] = useState(false);

    async function copyMessage() {

        await navigator.clipboard.writeText(message.content);

        setCopied(true);

        setTimeout(() => {

            setCopied(false);

        }, 2000);

    }

    return (

        <div
            className={`flex ${
                isUser ? "justify-end" : "justify-start"
            } mb-6`}
        >

            <div
                className={`
                    relative
                    max-w-[95%]
                    sm:max-w-[90%]
                    md:max-w-[80%]
                    lg:max-w-[72%]
                    rounded-2xl
                    shadow-md
                    transition-all
                    duration-300
                    overflow-hidden

                    ${
                        isUser
                            ? "bg-blue-600 text-white rounded-br-md"
                            : "bg-white border border-gray-200 rounded-bl-md"
                    }
                `}
            >

                {!isUser && (

                    <button

                        onClick={copyMessage}

                        className="
                            absolute
                            top-3
                            right-3
                            flex
                            items-center
                            gap-1
                            text-gray-500
                            hover:text-blue-600
                            transition
                        "

                    >

                        {

                            copied

                                ?

                                <>

                                    <FiCheck size={16} />

                                    <span className="text-xs">

                                        Copied

                                    </span>

                                </>

                                :

                                <>

                                    <FiCopy size={16} />

                                    <span className="text-xs">

                                        Copy

                                    </span>

                                </>

                        }

                    </button>

                )}

                <div className="p-5">

                    {

                        isUser

                            ?

                            <p className="whitespace-pre-wrap leading-7 text-sm sm:text-base">

                                {message.content}

                            </p>

                            :

                            <ReactMarkdown

                                remarkPlugins={[remarkGfm]}

                                components={{

                                    code({

                                        inline,

                                        className,

                                        children,

                                        ...props

                                    }) {

                                        const match = /language-(\w+)/.exec(className || "");

                                        if (!inline && match) {

                                            return (

                                                <CodeBlock

                                                    language={match[1]}

                                                >

                                                    {String(children)}

                                                </CodeBlock>

                                            );

                                        }

                                        return (

                                            <code

                                                className="bg-gray-100 px-1 py-0.5 rounded text-red-600"

                                                {...props}

                                            >

                                                {children}

                                            </code>

                                        );

                                    },

                                    h1: ({ children }) => (

                                        <h1 className="text-3xl font-bold mt-4 mb-3">

                                            {children}

                                        </h1>

                                    ),

                                    h2: ({ children }) => (

                                        <h2 className="text-2xl font-semibold mt-4 mb-3">

                                            {children}

                                        </h2>

                                    ),

                                    h3: ({ children }) => (

                                        <h3 className="text-xl font-semibold mt-3 mb-2">

                                            {children}

                                        </h3>

                                    ),

                                    p: ({ children }) => (

                                        <p className="leading-8 mb-3 text-gray-800">

                                            {children}

                                        </p>

                                    ),

                                    ul: ({ children }) => (

                                        <ul className="list-disc pl-6 space-y-2">

                                            {children}

                                        </ul>

                                    ),

                                    ol: ({ children }) => (

                                        <ol className="list-decimal pl-6 space-y-2">

                                            {children}

                                        </ol>

                                    ),

                                    table: ({ children }) => (

                                        <div className="overflow-x-auto my-4">

                                            <table className="min-w-full border border-gray-300">

                                                {children}

                                            </table>

                                        </div>

                                    ),

                                    th: ({ children }) => (

                                        <th className="border bg-gray-100 px-4 py-2 text-left">

                                            {children}

                                        </th>

                                    ),

                                    td: ({ children }) => (

                                        <td className="border px-4 py-2">

                                            {children}

                                        </td>

                                    ),

                                    blockquote: ({ children }) => (

                                        <blockquote className="border-l-4 border-blue-500 bg-blue-50 px-4 py-2 italic my-4">

                                            {children}

                                        </blockquote>

                                    )

                                }}

                            >

                                {message.content}

                            </ReactMarkdown>

                    }

                    {

                        !isUser && message.sources?.length > 0 && (

                            <div className="mt-6 border-t pt-4">

                                <h4 className="font-semibold text-gray-500 uppercase text-xs mb-3">

                                    Sources

                                </h4>

                                <div className="grid gap-2">

                                    {

                                        message.sources.map((source, index) => (

                                            <div

                                                key={index}

                                                className="
                                                    bg-blue-50
                                                    border
                                                    border-blue-200
                                                    rounded-lg
                                                    px-3
                                                    py-2
                                                    text-sm
                                                    text-blue-700
                                                    break-all
                                                "

                                            >

                                                📄 {source}

                                            </div>

                                        ))

                                    }

                                </div>

                            </div>

                        )

                    }

                </div>

            </div>

        </div>

    );

}