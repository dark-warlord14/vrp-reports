# Security: manipulating the cvs data 

| Field | Value |
|-------|-------|
| **Issue ID** | [40071635](https://issues.chromium.org/issues/40071635) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Tools |
| **Reporter** | an...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2023-09-07 |
| **Bounty** | $500.00 |

## Description

hello team,

I found a bucket hosting cvs data inside a python script was available for takeover.

# Step to Reproduce:

1) go to https://github.com/search?q=org%3Achromium++%22chrome-health-tvdata%22++NOT+is%3Aarchived+++language%3Apython&type=code

2)Its been use to for the health data purpose.

#POC
https://storage.googleapis.com/chrome-health-tvdata/index.html

# Impact

An attacker can manipulate data and also upload malicious data in the bucket.

thanks
AnupamAS01



## Timeline

### [Deleted User] (2023-09-07)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-09-07)

Thanks for the report.

I can't see anywhere where `CLOUD_PATH` is used, so those links might be unused, but even if so this isn't good to have in the code.

sullivan@: Are you the right person to look at this, or do you know who is? Can these links just be deleted?

[Monorail components: Tools]

### su...@chromium.org (2023-09-07)

I don't think I have access to the code, but soundwave was a project by perezju@ who left the team several years ago and the code can be deleted.

### ke...@chromium.org (2023-09-07)

Is the code not just /tools/perf/soundwave? (And tools/perf/cli_tools/soundwave)

### jo...@chromium.org (2023-09-08)

I'll submit a CL to delete soundwave. However, I don't have access to gs://chrome-health-tvdata.

@kenrb: Could you help finding owner of gs://chrome-health-tvdata?

### ke...@chromium.org (2023-09-08)

johnchen@: I don't understand the question. It looks like it has no owner, since the reporter of this bug claimed it?

We shouldn't have URLs in the code that reference things we don't control.

### ke...@chromium.org (2023-09-08)

And thanks for volunteering to delete that!

### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f300dd680dc5508785d068b2b5891f71ba941bc1

commit f300dd680dc5508785d068b2b5891f71ba941bc1
Author: John Chen <johnchen@chromium.org>
Date: Fri Sep 08 20:16:59 2023

Remove soundwave tool

It's deprecated, and may have security issues.

Bug: 1480000
Change-Id: Ie5369dd0569e4d9266c70736f7975590f99f9ba2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4851006
Reviewed-by: Wenbin Zhang <wenbinzhang@google.com>
Commit-Queue: John Chen <johnchen@chromium.org>
Auto-Submit: John Chen <johnchen@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1194282}

[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/tables/bugs_test.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/tables/timeseries.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/__init__.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/studies/__init__.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/pandas_sqlite_test.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/tables/__init__.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/studies/v8_study.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/tables/alerts.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/studies/health_study.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/worker_pool.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/soundwave
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/examples/soundwave/startup_timeseries.json
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/tables/alerts_test.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/worker_pool_test.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/commands.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/tables/timeseries_test.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/tables/bugs.py
[delete] https://crrev.com/c01671ba32f8644a60ea2b885c9acc2935b7fd94/tools/perf/cli_tools/soundwave/pandas_sqlite.py


### ke...@chromium.org (2023-09-08)

[Empty comment from Monorail migration]

### an...@gmail.com (2023-09-09)

hello team,

Should i realease the bucket ?

do chromium have HOF or monitory reward?

thanks
AnupamAS01

### [Deleted User] (2023-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-09)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-09-11)

re https://crbug.com/chromium/1480000#c10: Releasing the bucket is fine. It doesn't appear this was being used, so there is no immediate risk to users.

This report will be considered by the VRP panel for reward eligibility.

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Thank you for this report, AnupamAS01. While this issue did not impact a part of Chrome infra that we use, it serves of a good reminder for us to maintain good infra hygiene. As a show of appreciation, the Chrome VRP would like to extend to you a $500 thank you award. Thanks again for taking the time to find and report this issue to us! 

### an...@gmail.com (2023-09-22)

Hi team,

Thank you so much for the bounty!

Regards,
AnupamAS01

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-16)

This issue was migrated from crbug.com/chromium/1480000?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-02-27)

Project: chromium/src
Branch: main

commit 617bba1e12bb2d07f14e85c6bdace682fcd89350
Author: Camillo Bruni <cbruni@chromium.org>
Date:   Tue Feb 27 21:29:21 2024

    [tools][perf] Remove soundwave reference and deprecated code
    
    - README.md was still referring to old and deprecated dashboards
    - tools/perf/experimental/story_clustering depended on the prevously
      removed soundwave tool
    
    Bug: 40626151, 40071635
    
    Change-Id: I023d8d02cef8541933c1e06d37163b2ef7efc12b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5317151
    Commit-Queue: Camillo Bruni <cbruni@chromium.org>
    Reviewed-by: Wenbin Zhang <wenbinzhang@google.com>
    Cr-Commit-Position: refs/heads/main@{#1266069}

M       tools/perf/README.md
D       tools/perf/experimental/story_clustering/OWNERS
D       tools/perf/experimental/story_clustering/README.md
D       tools/perf/experimental/story_clustering/__init__.py
D       tools/perf/experimental/story_clustering/cluster_stories.py
D       tools/perf/experimental/story_clustering/create_soundwave_input.py
D       tools/perf/experimental/story_clustering/gather_historical_records_and_cluster_stories.py
D       tools/perf/experimental/story_clustering/similarity_calculator.py
D       tools/perf/export_csv

https://chromium-review.googlesource.com/5317151


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071635)*
