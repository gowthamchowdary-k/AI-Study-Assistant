export default function Message({ message }) {

    const isUser = message.role === "user";

    return (

        <div
            className={`flex ${
                isUser ? "justify-end" : "justify-start"
            } mb-4`}
        >

            <div
                className={`max-w-[75%] rounded-xl px-4 py-3 shadow

                ${
                    isUser
                        ? "bg-blue-600 text-white"
                        : "bg-white border"
                }`}
            >

                <p className="whitespace-pre-wrap">
                    {message.content}
                </p>

            </div>

        </div>

    );

}