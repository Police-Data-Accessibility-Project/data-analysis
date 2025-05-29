To optimize processing, construct "check queries" that check to see whether URLs are missing a given job.

There are two levels of check queries:
1. Global check queries: Check to see if ANY URL is missing a given job. These are used to determine whether to run local (set) checks.
2. Local check queries: Check to see if a given URL is missing a given job. 