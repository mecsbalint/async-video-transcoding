import { Link } from "react-router-dom";

function HomePage() {

    return (
        <div className={"grid grid-cols-1 h-50 justify-center gap-1"}>
            <Link to="/upload" className="btn btn-primary">Upload video</Link>
            <Link to="/joblist" className="btn btn-primary">Jobs</Link>
        </div>
    )
}

export default HomePage;
