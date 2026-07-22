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

        <aside className="w-80 bg-white border-r p-5">

            <h2 className="text-xl font-semibold mb-4">
                Documents
            </h2>

            <button

                onClick={chooseFile}

                className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700"

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

            <div className="mt-5">

                <DocumentList

                    documents={documents}

                    onDelete={remove}

                />

            </div>

        </aside>

    );

}