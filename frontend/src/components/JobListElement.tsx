import { JobListElementDto } from "../types/types";

type JobListElementProps = {
    jobListElementDto: JobListElementDto,
    isLast: boolean
}

function JobListElement({jobListElementDto, isLast}: JobListElementProps) {

    return (
        <tr key={jobListElementDto.id} className="hover:bg-blue-100">
            <td className={`py-4 ${isLast ? "rounded-b-lg" : ""}`}>{jobListElementDto.id}</td>
            <td className="py-4">{jobListElementDto.state}</td>
            <td className={`py-4 ${isLast ? "rounded-b-lg" : ""}`}>
                {jobListElementDto.thumbnail_url ? <img className="w-40" alt="thumbnail" src={jobListElementDto.thumbnail_url} /> : <></>}
            </td>
        </tr>
    )
}

export default JobListElement;
