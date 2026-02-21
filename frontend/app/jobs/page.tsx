"use client";
import { JobFilters } from "@/components/jobs/JobFilters";
import { JobCard } from "@/components/jobs/JobCard";
import { useJobs } from "@/hooks/useJobs";

export default function JobsPage() {
  const { data } = useJobs();
  return <div className="p-3 text-sm"><JobFilters />{data?.results?.map((job: any) => <JobCard key={job.id} job={job} />)}</div>;
}
