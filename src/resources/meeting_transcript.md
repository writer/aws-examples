# Meeting Transcript: AWS Lambda Latency Optimization

**Date:** July 22, 2025
**Time:** 10:00 AM - 11:00 AM
**Project:** Project Phoenix - API Performance
**Attendees:**
- **Sarah:** Engineering Manager
- **Tom:** Senior Backend Engineer
- **Maria:** DevOps Engineer
- **David:** Junior Developer

---

### Agenda:
1.  Review of current Lambda function performance metrics.
2.  Identify root causes of high latency in server responses.
3.  Brainstorm and prioritize solutions for optimization.
4.  Define action items and assign ownership.

---

**[10:02:15] Sarah:** Alright everyone, thanks for joining. Let's get straight to it. The main reason for this meeting is the increasing latency we're seeing in our primary user-facing API, which is served by a set of AWS Lambda functions. David, can you kick us off with a summary of what the monitoring dashboards are showing?

**[10:03:01] David:** Sure, Sarah. I've been looking at the CloudWatch metrics for the past two weeks. The p90 latency for the `process-user-request` function has crept up from an average of 800ms to over 2.5 seconds. The p99 is even worse, sometimes hitting 5 seconds. This is directly impacting user experience, and we've seen a 15% increase in client-side timeouts.

**[10:04:20] Tom:** Five seconds is completely unacceptable. That's an eternity in application time. A major part of that is almost certainly cold starts. I've noticed the invocation patterns are very spiky. We get bursts of traffic during business hours, then long periods of inactivity overnight. Every morning, the first users of the day are getting hit with the full cold start penalty.

**[10:05:15] Maria:** I agree with Tom. Cold starts are a huge factor, but I don't think it's the only one. I dug into the X-Ray traces, and the initialization phase (`Init`) for that function is taking up a significant chunk of time, even on warm invocations. The function package itself is over 100MB. What dependencies are we pulling in there?

**[10:06:05] David:** The function handles a lot. It connects to our Aurora PostgreSQL database, interacts with the S3 API, and uses the `pandas` library for a small data transformation step. I think `pandas` and its dependencies are the main contributors to the package size.

**[10:07:30] Tom:** There's our first smoking gun. Using `pandas` in a latency-sensitive Lambda function is an anti-pattern unless absolutely necessary. The library is massive and slow to import. David, can that transformation be rewritten using native Python code? Or, if it's a heavy operation, can we offload it to a separate, asynchronous process? The user shouldn't have to wait for it.

**[10:08:45] David:** I think we can rewrite it. It's mostly just creating a data frame to generate a CSV for S3. I can probably achieve the same result with Python's built-in `csv` module, which would be much lighter.

**[10:09:30] Sarah:** Excellent. That's our first action item. David, please lead the effort to refactor the `process-user-request` function to remove the `pandas` dependency. Now, let's talk about the cold starts. Maria, what are our options there?

**[10:10:15] Maria:** The most direct solution is Provisioned Concurrency. We can configure AWS to keep a certain number of execution environments warm and ready to respond instantly. Given our traffic spikes, we could set a provisioned concurrency level of, say, 50 during peak hours and scale it down to 5 or even 0 overnight. It costs more, but for a critical, user-facing API, it's often a necessary trade-off.

**[10:11:45] Tom:** Provisioned Concurrency is a great tool, but we should use it as a safety net, not a crutch. We should still optimize everything else first. What about our database connections? Are we opening a new connection on every invocation? That's a classic latency killer. The TLS handshake alone can add hundreds of milliseconds.

**[10:12:30] Maria:** According to the logs, yes, it looks like that's what's happening. We aren't using RDS Proxy or any form of connection pooling. Each invocation is setting up and tearing down its own connection. That's a massive performance bottleneck. I strongly recommend integrating RDS Proxy. It maintains a warm pool of connections to the database, so the Lambda function just has to make a quick, cheap connection to the proxy.

**[10:14:00] Sarah:** Okay, that sounds like a big win. Maria, can you take the lead on deploying an RDS Proxy for our Aurora cluster and helping the team integrate it into the Lambda functions?

**[10:14:30] Maria:** Absolutely. I'll start a proof-of-concept in our staging environment this afternoon.

**[10:15:10] Tom:** While we're on the topic of infrastructure, what about memory allocation? We have the function set to 512MB. Is that the right number? More memory means more vCPU, which can speed up compute-bound tasks and, more importantly, reduce initialization time. Have we done any performance tuning on this?

**[10:16:00] David:** I haven't, no. I just used the default setting from a template.

**[10:16:45] Maria:** We can use the AWS Lambda Power Tuning tool for that. It's an open-source state machine that runs your function with various memory settings and measures the performance and cost for each. It can help us find the optimal balance between speed and cost. I can run that against the function once David has refactored the `pandas` dependency. A smaller package size will change the performance profile, so we should test it after that change.

**[10:18:00] Tom:** Good point. Another thing to consider is caching. The function appears to fetch the same user configuration data from the database repeatedly. This data changes infrequently. We could introduce a caching layer with ElastiCache for Redis to store this data. A Redis lookup takes single-digit milliseconds, versus the tens or hundreds of milliseconds for a database query.

**[10:19:30] Sarah:** That's a great idea, Tom. Caching would take a significant load off the database and improve response times. Can you work with David to identify the best data to cache and implement the client-side logic?

**[10:20:00] Tom:** Will do.

**[10:20:45] Maria:** One last thing from my side. I noticed we're still on the Python 3.9 runtime. AWS has made significant performance improvements in newer runtimes, especially with Python 3.11, which has a faster startup time. Upgrading the runtime is a low-effort change that could give us a nice performance boost for free.

**[10:21:30] Sarah:** Fantastic. Let's add that to the list. Okay, this has been very productive. Let's recap the action items.

1.  **David:** Refactor the `process-user-request` function to remove the `pandas` dependency and use the native `csv` module.
2.  **Maria:** Deploy an RDS Proxy for the Aurora cluster and assist with integration.
3.  **Maria:** Once the refactoring is done, use the Lambda Power Tuning tool to find the optimal memory allocation.
4.  **Tom & David:** Implement a caching layer with ElastiCache for Redis to store frequently accessed, slow-changing data.
5.  **Maria:** Upgrade all our Python Lambda functions from the 3.9 to the 3.11 runtime.
6.  **Maria:** Set up a baseline Provisioned Concurrency configuration for the `process-user-request` function in staging for us to test.

**[10:23:00] Tom:** Sounds like a solid plan. We should tackle these in order. The refactoring is the highest priority, as it will impact the power tuning.

**[10:23:45] Sarah:** I agree. Let's aim to have the refactoring and RDS Proxy integration done in staging by the end of this week. We can then proceed with the other items next week. I'll schedule a follow-up for next Friday to review our progress. Thanks, everyone. Great work.

**[10:24:15] END OF MEETING**
