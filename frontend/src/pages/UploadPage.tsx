import { useState } from "react";
import { uploadVideo } from "../services/videoService";
import { useNavigate } from "react-router-dom";

function UploadPage() {
    const [file, setFile] = useState<File | null>(null);
    const navigate = useNavigate();

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();

        uploadVideo(file as File).then(response => {
            if (response.status === 201) {
                navigate("/joblist");
            }
            setFile(null);
        });
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2>Upload video</h2>
            <input type="file" onChange={event => {
                if (event.target.files !== null) {
                    setFile(event.target.files[0]);
                }
                }} />
            <button type="submit" disabled={file === null}>
                Upload video
            </button>
        </form>
    )
}

export default UploadPage;
