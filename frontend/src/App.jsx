import { Toaster } from "react-hot-toast";
import StudyBuddyPage from "./pages/StudyBuddyPage";

export default function App() {
    return (
        <>
            <Toaster position="top-right" reverseOrder={false} />

            <StudyBuddyPage
                user={null}
                onLogout={() => {}}
            />
        </>
    );
}