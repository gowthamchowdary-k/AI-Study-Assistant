import { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { FiCopy, FiCheck } from "react-icons/fi";

export default function CodeBlock({
    language,
    children
}) {

    const [copied, setCopied] = useState(false);

    const code = String(children).replace(/\n$/, "");

    async function copyCode() {
        await navigator.clipboard.writeText(code);
        setCopied(true);

        setTimeout(() => {
            setCopied(false);
        }, 2000);
    }

    return (

        <div className="relative my-4 rounded-xl overflow-hidden border border-gray-700 shadow-lg">

            <div className="flex items-center justify-between bg-gray-900 px-4 py-2">

                <span className="text-xs uppercase tracking-wide text-gray-300">

                    {language || "text"}

                </span>

                <button
                    onClick={copyCode}
                    className="flex items-center gap-2 text-xs text-white hover:text-green-400 transition"
                >

                    {copied ? <FiCheck size={16} /> : <FiCopy size={16} />}

                    {copied ? "Copied" : "Copy"}

                </button>

            </div>

            <div className="overflow-x-auto">

                <SyntaxHighlighter
                    language={language}
                    style={oneDark}
                    customStyle={{
                        margin: 0,
                        borderRadius: 0,
                        fontSize: "14px",
                        padding: "16px",
                        minWidth: "100%"
                    }}
                    wrapLongLines={false}
                >
                    {code}
                </SyntaxHighlighter>

            </div>

        </div>

    );

}