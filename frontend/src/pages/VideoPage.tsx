import { useEffect, useState } from "react";
import { VideoData } from "../types/types";
import { getVideoData } from "../services/jobService";
import { useNavigate, useParams } from "react-router-dom";
import StreamData from "../components/StreamData";

function VideoPage() {
    const [video, setVideo] = useState<VideoData | null>(null);
    const {id} = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        if (typeof id === "undefined") {
            navigate("/");
        } else {
            const idNum = parseInt(id)
            if (!Number.isNaN(idNum)) {
                getVideoData(idNum).then(response => setVideo(response.body));
            } else {
                navigate("/");
            }
        }
    }, []);

    return video ? (
        <div className="card shadow-md bg-base-100">
            <div>
                <h2 className="text-center font-bold">Preview</h2>
                <video controls width="250">
                    <source src={video.preview_url} type="video/mp4"/>
                <a className="btn btn-secondary btn-xs" href={video.original_url}>Download</a>
                </video>
            </div>
            <div className="card-body">
                {video.video_streams_metadata.length > 0 ? (
                    <div>
                        <p className="text-center pt-5 font-bold">Video Streams</p>
                        {video.video_streams_metadata.map((streamData, i) => <StreamData streamData={streamData} i={i} type="Video" />)}
                    </div>
                ) : (
                    <></>
                )}
                {video.audio_streams_metadata.length > 0 ? (
                    <div>
                        <p className="text-center pt-5 font-bold">Audio Streams</p>
                        {video.audio_streams_metadata.map((streamData, i) => <StreamData streamData={streamData} i={i} type="Audio" />)}
                    </div>
                ) : (
                    <></>
                )}
                {video.subtitles_streams_metadata.length > 0 ? (
                    <div>
                        <p className="text-center pt-5 font-bold">Subtitles Streams</p>
                        {video.subtitles_streams_metadata.map((streamData, i) => <StreamData streamData={streamData} i={i} type="Subtitles" />)}
                    </div>
                ) : (
                    <></>
                )}
            </div>
        </div>
    ) : (
        <div>
            Video data not found
        </div>
    );
}

export default VideoPage;