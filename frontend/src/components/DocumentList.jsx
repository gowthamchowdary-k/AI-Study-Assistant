export default function DocumentList({
    documents,
    onDelete
}) {

    if (documents.length === 0) {

        return (
            <p className="text-gray-500 text-sm">
                No PDFs uploaded.
            </p>
        );

    }

    return (

        <div className="space-y-2">

            {documents.map((doc) => (

                <div
                    key={doc}
                    className="flex justify-between items-center bg-gray-100 rounded-lg px-3 py-2"
                >

                    <span
                        className="truncate text-sm"
                    >
                        📄 {doc}
                    </span>

                    <button

                        onClick={() => onDelete(doc)}

                        className="text-red-600 hover:text-red-800"

                    >
                        Delete
                    </button>

                </div>

            ))}

        </div>

    );

}