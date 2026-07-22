import { useRef } from "react";
import DocumentList from "./DocumentList";

export default function Sidebar({

    documents,

    upload,

    remove

}) {

    const fileInput = useRef();

    function chooseFile() {
        fileInput.current.click();
    }

    async function handleFile(event) {

        const file = event.target.files[0];

        if (!file) return;

        await upload(file);

        event.target.value = "";

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
            "
        >

            <h2 className="text-lg md:text-xl font-semibold mb-4">
                📄 Documents
            </h2>

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

                type="file"

                accept=".pdf"

                ref={fileInput}

                onChange={handleFile}

                hidden

            />

            <div className="mt-5 max-h-[55vh] overflow-y-auto">

                <DocumentList

                    documents={documents}

                    onDelete={remove}

                />

            </div>

        </aside>

    );

}