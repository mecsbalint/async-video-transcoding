import { useEffect, useState } from "react"
import { getJobList } from "../services/jobService"
import { JobListElementDto } from "../types/types"
import JobListElement from "../components/JobListElement"

function JobListPage() {
    const [jobList, setJobList] = useState<JobListElementDto[]>([])

    useEffect(() => {
        getJobList().then(response => {
            if (response.status === 200) {
                setJobList(response.body as JobListElementDto[])
            }
        })
    }, [])

    return (
        <div className={"flex items-start"}>
            <table className="table table-zebra bg-base-300 h-auto">
                <thead className="tracking-wide">
                    <th></th>
                    <th>Id</th> 
                    <th>State</th> 
                    <th>Thumbnail</th> 
                </thead>
                <tbody>
                    {jobList.map((jobListElementDto, i) => <JobListElement jobListElementDto={jobListElementDto} isLast={jobList.length - 1 === i}/>)}
                </tbody>
            </table>
        </div>
    )
}

export default JobListPage