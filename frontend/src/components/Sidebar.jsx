import { useRef, useEffect } from "react";
import DocumentList from "./DocumentList";

export default function Sidebar({

    documents,

    upload,

    remove,

    uploadTrigger

}) {

    const fileInput = useRef(null);

    function chooseFile() {

        fileInput.current?.click();

    }

    useEffect(() => {

        if (uploadTrigger) {

            uploadTrigger.current = chooseFile;

        }

    }, [uploadTrigger]);

    async function handleFile(event) {

        const file = event.target.files[0];

        if (!file) return;

        try {

            await upload(file);

        }

        finally {

            event.target.value = "";

        }

    }

    return (

        <aside
            className="
                w-full
                md:w-80
                bg-white
                border-b
                md:border-b-0
                md:border-r
                p-4
                md:p-5
                shadow-sm
                flex
                flex-col
                h-full
            "
        >

            {/* Sidebar Title */}

            <h2 className="text-lg md:text-xl font-semibold mb-4">
                📄 Document
            </h2>

            {/* Upload Button */}

            <button

                onClick={chooseFile}

                className="
                    w-full
                    bg-blue-600
                    hover:bg-blue-700
                    transition
                    text-white
                    py-2.5
                    rounded-lg
                    font-medium
                "

            >
                Upload PDF
            </button>

            <input

                ref={fileInput}

                type="file"

                accept=".pdf"

                hidden

                onChange={handleFile}

            />

            {/* Document List */}

            <div className="mt-5 flex-1 overflow-y-auto">

                <DocumentList

                    documents={documents}

                    onDelete={remove}

                />

            </div>

            {/* Footer */}

            <div className="mt-6 pt-4 border-t text-center">

    <p className="text-xs text-gray-500 mb-2">
        Developed by
    </p>

    <p className="text-x text-gray-700 leading-6">
        Kunta Gowtham Chowdary
        <br />
        &
        <br />
        Nukavarapu Eswar Chowdary
    </p>

    <p className="text-[11px] text-gray-400 mt-3">
        AI Study Assistant v1.0
    </p>

</div>

        </aside>

    );

}