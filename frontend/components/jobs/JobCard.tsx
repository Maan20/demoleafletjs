export function JobCard({ job }: { job: any }) {
  return <div className="border rounded p-3 my-2 text-xs"><div className="font-semibold text-sm">{job.title}</div><div>{job.company_name}</div></div>;
}
