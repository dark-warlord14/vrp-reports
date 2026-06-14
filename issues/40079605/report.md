# Security: webgl draw buffers extension can expose unitialized video memory to webpage

| Field | Value |
|-------|-------|
| **Issue ID** | [40079605](https://issues.chromium.org/issues/40079605) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Reporter** | jm...@mozilla.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2014-05-23 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Using the webgl draw buffers extension you can drawBuffers([gl.NONE]). This prevents the usual implicit clear that happens before new draws. This unitialized surface can then be read from.

**VERSION**  

Chrome Version: 35.0.1916.114 stable  

Operating System: OS X 10.9

**REPRODUCTION CASE**  

I've attached a modified version of the EXT\_draw\_buffers conformance test suite that shows the problem. You may need to refresh the page a couple of times and perhaps resize the window. Eventually you'll see content that looks like text or scroll bars in the canvas area.

## Attachments

- [draw-buffers-leak.zip](attachments/draw-buffers-leak.zip) (application/zip, 24.7 KB)

## Timeline

### jl...@chromium.org (2014-05-23)

zmo: could you please take a look or help find an owner for this?

### zm...@chromium.org (2014-05-23)

I'll fix this.

Thanks for reporting it.

### cl...@chromium.org (2014-05-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-01)

zmo@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### zm...@chromium.org (2014-06-02)

if backbuffer's drawBuffers is set to GL_NONE, apparently we didn't set backbuffer to GL_COLOR_ATTACHMENT0 before clearing and then set to GL_NONE again.  However, there is some nastiness where drawBuffers() no longer has effects.  Still looking into why.

### bu...@chromium.org (2014-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ee7579229ff7e9e5ae28bf53aea069251499d7da

commit ee7579229ff7e9e5ae28bf53aea069251499d7da
Author: zmo@chromium.org <zmo@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Jun 06 05:21:42 2014

Framebuffer clear() needs to consider the situation some draw buffers are disabled.

This is when we expose DrawBuffers extension.

BUG=376951
TEST=the attached test case, webgl conformance
R=kbr@chromium.org,bajones@chromium.org

Review URL: https://codereview.chromium.org/315283002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@275338 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-06-06)

------------------------------------------------------------------
r275338 | zmo@chromium.org | 2014-06-06T05:21:42.465728Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/framebuffer_manager_unittest.cc?r1=275338&r2=275337&pathrev=275338
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/framebuffer_manager.cc?r1=275338&r2=275337&pathrev=275338
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/framebuffer_manager.h?r1=275338&r2=275337&pathrev=275338
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?r1=275338&r2=275337&pathrev=275338

Framebuffer clear() needs to consider the situation some draw buffers are disabled.

This is when we expose DrawBuffers extension.

BUG=376951
TEST=the attached test case, webgl conformance
R=kbr@chromium.org,bajones@chromium.org

Review URL: https://codereview.chromium.org/315283002
-----------------------------------------------------------------

### in...@chromium.org (2014-06-06)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-06-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-06-06)

[Empty comment from Monorail migration]

### jm...@mozilla.com (2014-06-07)

zmo: Can you upstream this test into the webgl conformance suite when appropriate?

### zm...@chromium.org (2014-06-09)

Will do, but probably after we merge the fix back to M36 before releasing this vulnerability to the public. 

### zm...@chromium.org (2014-06-10)

[Empty comment from Monorail migration]

### [Deleted User] (2014-06-11)

Can you provide a better justification as to why this change must go into 36?  I would prefer if we punt this over to 37 due to the size and severity of your change.

### ti...@chromium.org (2014-06-11)

FYI from a security perspective, we try to merge all medium-severity security fixes into Beta builds (and externally-reported Medium severity fixes into Stable builds).

If this merge is huge/hairy/scary and you want to punt it unless you get a justification on the severity of the issue, I'll leave it to those closer to the issue to comment. That said, I think it's reasonable to not take this fix into M36 without justification.

### aa...@google.com (2014-06-11)

There is lot of time for M-36 baking here. We can't punt a medium severity into M37 unless it is a complete code rewrite, large refactoring, etc.

### zm...@chromium.org (2014-06-12)

I think the security threat of this bug is low instead of medium.  Yes it does leak vram, but from what I see, it's garbage pixels from multisampled renderbuffers/textures.  It's very unlikely someone's able to exploit user info from this bug.

### [Deleted User] (2014-06-12)

Rejecting merge per https://crbug.com/chromium/376951#c18.

### in...@chromium.org (2014-06-17)

[Empty comment from Monorail migration]

### kb...@chromium.org (2014-07-09)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-14)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-14)

If we're not going to merge this to M36, it's already in M37 as that was cut at r278856. 

inferno@ - please let me know if you want to see this in a M36 patch or if we can let this roll into M37 due to comments above.

### in...@chromium.org (2014-07-14)

yes based on c#18, we can let it roll in m37.

### ti...@chromium.org (2014-07-14)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-08-22)

Thanks for the report! This qualifies for a $2000 reward. Someone should be reaching out to you soon with additional details.

How would you like to be credited when we mention this bug in our release notes?

### jm...@mozilla.com (2014-08-26)

Jeff Muizelaar <jmuizelaar@mozilla.com> is fine.

### zm...@chromium.org (2014-09-04)

Note that the test case is added in khronos webgl conformance suite:

https://github.com/KhronosGroup/WebGL/pull/685

### cl...@chromium.org (2014-09-12)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-09-18)

Jeff,

I passed your details over to the finance team - they'll contact you directly to get your details for payment. If you haven't heard from them by this time next week, please contact me directly (or update this bug).

Congrats on the reward!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### jr...@gmail.com (2014-09-30)

As far as I can see I've not received anything from the finance team.

### ti...@chromium.org (2014-10-10)

As discussed with Jeff via email, we doubling this reward to $4000 and donating it to a charity. Thanks Jeff!

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

This issue was migrated from crbug.com/chromium/376951?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079605)*
