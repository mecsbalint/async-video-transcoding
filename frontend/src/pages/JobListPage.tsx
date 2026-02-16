import { useEffect, useRef, useState } from "react"
import { getJobList } from "../services/jobService"
import { JobListElementDto } from "../types/types"
import JobListElement from "../components/JobListElement"

function JobListPage() {
    const [jobList, setJobList] = useState<JobListElementDto[]>([]);
    const isPolling = useRef<boolean>(false);

    useEffect(() => {
        const interval = setInterval(async () => {
            if (isPolling.current) return;
            isPolling.current = true;
            try {
                const response = await getJobList();
                if (response.status === 200) {
                    setJobList(response.body as JobListElementDto[]);
                }
            } finally {
                isPolling.current = false;
            }
        }, 2000);
        return () => clearInterval(interval);
    }, []);

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