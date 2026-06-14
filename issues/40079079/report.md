# sandbox::CodeGen::MergeTails (seccomp-bpf) is unsound for single-successor basic blocks

| Field | Value |
|-------|-------|
| **Issue ID** | [40079079](https://issues.chromium.org/issues/40079079) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox |
| **Platforms** | Linux |
| **Reporter** | [Deleted User] |
| **Assignee** | jl...@chromium.org |
| **Created** | 2014-03-10 |
| **Bounty** | $500.00 |

## Description

*No description available.*

## Timeline

### pa...@chromium.org (2014-03-10)

Assigning to jln to determine whether this impacts Chromium, and if so how severe the problem is.

### jl...@chromium.org (2014-03-11)

Thanks a lot for the detailed report and the patch!
Definitely something we want to fix. FYI, your patch does pass the tests.

Markus: if you have a moment to take a look, this would save me a lot of context-switch and time.

Otherwise I'll take a look, but it'll wait until next week.

### pa...@chromium.org (2014-03-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-03-11)

@jln - I can't work out what the actual impact is here. Could you please add the appropriate labels?

### jl...@chromium.org (2014-03-11)

The bug is a compiler bug for our BPF programs.

I don't think there is any direct impact to users with our current BPF policies.

I also did a quick check on x86_64 that this case does not happen by adding NOTREACHED() to this particular condition. It didn't trigger, at least not for the main process types.

I'll do a more thorough check later and update.

However, this bug has the potential for high impact security issues and we'll want to look at it very carefully.

### js...@chromium.org (2014-03-11)

Okay, reflagging it as not a vulnerability for now.

### jl...@chromium.org (2014-03-26)

This is a pretty bad bug in our core BPF compiler. As far as I can tell, none of the existing BPF programs do hit it, but it is hard to truly verify since our BPF programs are generated dynamically and depend on the architecture.

I'm marking this as Medium, taking into consideration the potential devastating effects of a compiler bug.

I'm marking this bug as potentially eligible for a reward and I would like to mention how great the bug report is: it comes not only with a full patch to fix the issue, but also with a full reproducer.

### cl...@chromium.org (2014-03-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-03-28)

------------------------------------------------------------------
r260157 | jln@chromium.org | 2014-03-28T16:26:30.852467Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf/codegen_unittest.cc?r1=260157&r2=260156&pathrev=260157
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/linux/seccomp-bpf/codegen.cc?r1=260157&r2=260156&pathrev=260157

Linux Sandbox: fix BPF compiler bug

The code responsible for detecting similar blocks and merging
them didn't check for the next blocks if the last instruction was
not a JMP or a RET.

The patch to fix this bug (in codegen.cc) is based on a patch by
jld@panix.com, attached to the bug report.

Additional unittests are from jln@chromium.org

BUG=351103

Review URL: https://codereview.chromium.org/215173002
-----------------------------------------------------------------

### jl...@chromium.org (2014-04-01)

This is now on Dev channel, let's wait a few days and merge.

### jl...@chromium.org (2014-04-01)

Actually, I'll let the TPMs tell me when to merge to M34.

### cl...@chromium.org (2014-04-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-01)

[Empty comment from Monorail migration]

### ka...@google.com (2014-04-01)

this is already in m35 so if you need to merge it must be 34.

### jl...@chromium.org (2014-04-01)

Yes, I clearly put the merge request for M34. When should I merge this?

Ideally I would let it another day or so on Dev channel.

### in...@chromium.org (2014-04-01)

m34 is going to be cut today at 3 pm. then this code change will be taken up in next m34 patch. this can wait.

### jl...@chromium.org (2014-04-01)

Yeah, that's fine with me.

### dx...@chromium.org (2014-04-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-09)

------------------------------------------------------------------
r262837 | jln@chromium.org | 2014-04-09T22:18:12.457706Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/sandbox/linux/seccomp-bpf/codegen_unittest.cc?r1=262837&r2=262836&pathrev=262837
   M http://src.chromium.org/viewvc/chrome/branches/1847/src/sandbox/linux/seccomp-bpf/codegen.cc?r1=262837&r2=262836&pathrev=262837

Merge 260157 "Linux Sandbox: fix BPF compiler bug"

> Linux Sandbox: fix BPF compiler bug
> 
> The code responsible for detecting similar blocks and merging
> them didn't check for the next blocks if the last instruction was
> not a JMP or a RET.
> 
> The patch to fix this bug (in codegen.cc) is based on a patch by
> jld@panix.com, attached to the bug report.
> 
> Additional unittests are from jln@chromium.org
> 
> BUG=351103
> 
> Review URL: https://codereview.chromium.org/215173002

TBR=jln@chromium.org

Review URL: https://codereview.chromium.org/231783003
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-26)

Congrats - $500 for the patch here.

### cl...@chromium.org (2014-07-08)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-26)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/351103?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox, Security]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079079)*
