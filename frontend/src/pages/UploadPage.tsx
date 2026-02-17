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
            <h1 className="text-2xl mb-5">Upload video</h1>
            <input type="file" className="file-input" onChange={event => {
                if (event.target.files !== null) {
                    setFile(event.target.files[0]);
                }
                }} />
            <button type="submit" className="btn btn-primary mt-2" disabled={file === null}>
                Upload video
            </button>
        </form>
    )
}

export default UploadPage;
