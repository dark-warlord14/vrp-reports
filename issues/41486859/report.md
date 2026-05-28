# Security: container-overflow in FileSystemAccessManagerImpl::DidCleanupAccessHandleCapacityAllocation

| Field | Value |
|-------|-------|
| **Issue ID** | [41486859](https://issues.chromium.org/issues/41486859) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vu...@darknavy.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2023-12-26 |
| **Bounty** | $21,000.00 |

## Description

**VULNERABILITY DETAILS**  

When the renderer invokes the mojo call `FileSystemAccessAccessHandleHost.Close`, the browser ultimately processes it through multiple functions until it reaches `FileSystemAccessManagerImpl::DidCleanupAccessHandleCapacityAllocation`. The parameter `access_handle_host` of this function is a raw pointer. If the object is not found in `access_handle_host_receivers_`, the `find` function will return the end of the container, resulting in container-overflow at [0].

```
  auto iter = access_handle_host_receivers_.find(access_handle_host);  
  auto access_handle_host_receiver = std::move(\*iter); // [0]  
  access_handle_host_receivers_.erase(iter);  

```

To make the `find` fail, the renderer can call `FileSystemAccessAccessHandleHost.Close` twice, with the requirement being that the second call occurs before the destruction of `FileSystemAccessAccessHandleHostImpl`. This race is easy to win because there are multiple asynchronous calls from the `Close` to the vulnerable function.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_access_manager_impl.cc;drc=ec2f7a64dc4eced49c03001de4508c2e30d6a9c8;l=1756>

BISECT  

Introduced by <https://chromium.googlesource.com/chromium/src/+/15f458be5abf380d8778cf09df3a97ce391d4aa0>

**VERSION**  

Chrome Version: HEAD  

Operating System: All

SUGGESTED FIX:  

Prohibit two consecutive calls to `FileSystemAccessAccessHandleHost.Close`. Change the DCHECK at [0]

```
  DCHECK(!close_callback_); // [0]  

```

to

```
  if (close_callback_) {  
    // error handling  
  }  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_access_access_handle_host_impl.cc;drc=ec2f7a64dc4eced49c03001de4508c2e30d6a9c8;l=70>

**REPRODUCTION CASE**  

Host poc.html on an HTTP server.  

$ python -m http.server  

$ ./chrome --enable-blink-features=MojoJS '<http://localhost:8000/poc.html>'

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash log: see asan.txt

**CREDIT INFORMATION**  

Reporter credit: DarkNavy

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 995 B)
- [asan.txt](attachments/asan.txt) (text/plain, 23.1 KB)

## Timeline

### [Deleted User] (2023-12-26)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-12-26)

Repro'd on m122 and m121.  DNR on m120, which aligns with reporter's bisect.
As with most mojo.js examples, make the server root be out/Asan/gen to find the generated mojom files needed.
Provisionally setting all desktop OS, will need refinement later.

[Monorail components: Blink>Storage>FileSystem]

### ts...@chromium.org (2023-12-26)

Assigning to owner of suspect CL.

### [Deleted User] (2023-12-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2024-01-02)

cc-ing chrome storage team

### gi...@appspot.gserviceaccount.com (2024-01-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0dce112ae2bff6d21e73915185279a09ef21bc1d

commit 0dce112ae2bff6d21e73915185279a09ef21bc1d
Author: Nathan Memmott <memmott@chromium.org>
Date: Tue Jan 02 21:56:31 2024

FSA: Prevent repeated calls to FileSystemAccessAccessHandleHost.Close

In production code, a compromised renderer can call the mojo function
FileSystemAccessAccessHandleHost.Close multiple times on the same
access handle. This puts chrome in an invalid state. This fixes it by
killing the renderer if it attempts to do this.

Fixed: 1514301
Change-Id: I0b148fd908d5caeab223514efe0e9cd5eb0aa933
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5160388
Reviewed-by: Daseul Lee <dslee@chromium.org>
Commit-Queue: Daseul Lee <dslee@chromium.org>
Auto-Submit: Nathan Memmott <memmott@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1242153}

[modify] https://crrev.com/0dce112ae2bff6d21e73915185279a09ef21bc1d/content/browser/file_system_access/file_system_access_access_handle_host_impl.cc
[modify] https://crrev.com/0dce112ae2bff6d21e73915185279a09ef21bc1d/content/browser/file_system_access/file_system_access_manager_impl.cc


### me...@chromium.org (2024-01-02)

1. Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
This is a release blocker and an M121 regression. It is safe to merge.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://crrev.com/c/5160388

3. Have the changes been released and tested on canary?
No

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No

### [Deleted User] (2024-01-03)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-03)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-03)

Merge review required: M121 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-08)

M121 merge approved for https://crrev.com/c/5160388, please merge this fix to branch 6167 by EOD Tuesday 9 January so this fix can be included in the next M121 Beta update -- thank you

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### da...@google.com (2024-01-09)

https://chromium-review.googlesource.com/c/chromium/src/+/5181147

### [Deleted User] (2024-01-09)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-10)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M121, which branched on 2023-12-04 (Chromium branch: 6167, Chromium branch position: 1233107)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2024-01-10)

[Empty comment from Monorail migration]

### me...@chromium.org (2024-01-10)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-11)

Congratulations DarkNavy! The Chrome VRP Panel has decided to award you $20,000 for this report of browser process memory corruption + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- great work! 

### rz...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2024-01-11)

1. Just https://crrev.com/c/5190531
2. Low, only a simple conflict
3. 121
4. Yes

### am...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-22)

Removing the merge request as https://crrev.com/c/5081251 was introduced in 121 

### [Deleted User] (2024-01-22)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-22)

This issue was migrated from crbug.com/chromium/1514301?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### rz...@google.com (2024-02-12)

Marking as not applicable for 120 because the CL that introduced the issue landed on 121.

### pe...@google.com (2024-04-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41486859)*
