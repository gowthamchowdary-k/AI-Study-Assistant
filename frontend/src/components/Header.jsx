export default function Header() {
    return (
        <header className="bg-blue-600 text-white shadow-md">
            <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-4">

                <h1 className="text-xl sm:text-2xl md:text-3xl font-bold break-words">
                    💬 MY AI Study Assistant
                </h1>

                <p className="mt-1 text-xs sm:text-sm md:text-base text-blue-100">
                    Ask questions from your uploaded PDFs
                </p>

            </div>
        </header>
    );
}