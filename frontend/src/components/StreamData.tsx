import { StreamMetadata } from "../types/types";

type StreamDataProps = {
    streamData: StreamMetadata,
    i: number,
    type: string
}

function StreamData({streamData, i, type}: StreamDataProps) {
    
    return (
        <div>
            <p className="pt-1">{`${type} stream no. ${i + 1}:`}</p>
            {Object.entries(streamData).map(([key, value]) => <p className="pl-5">{`${key}: ${value}`}</p>)}
        </div>
    )
}

export default StreamData;
