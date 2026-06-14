# Security: UXSS via window.open() via file:// pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40083844](https://issues.chromium.org/issues/40083844) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-03-13 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 51.0.2675.0 canary  

Operating System: windows 7

Actually I'm not sure about if this's a security issue because I can repro this just when I use the testcase from local (file:///) and when I try it from server ('http://') doesn't repro.

Please watch the video for the steps (steps.mp4)

## Attachments

- [steps.mp4](attachments/steps.mp4) (application/octet-stream, 215.8 KB)
- [testcase.html](attachments/testcase.html) (text/plain, 244 B)
- [result.png](attachments/result.png) (image/png, 62.5 KB)
- [testcase.html](attachments/testcase_53305419.html) (text/plain, 224 B)

## Timeline

### in...@chromium.org (2016-03-15)

This is just an alert box sticking on the screen due to navigation, but there is no cross origin data theft or leak of data. This is not an XSS since there is no script execution in that target window. Closing.

### ch...@gmail.com (2016-03-15)

Thanks - But I can make an alert box executing in the target window "google.com" as in the attached image results.png

### in...@chromium.org (2016-03-15)

Alert box is not useful, there is no user input that you can steal here.

### cr...@chromium.org (2016-03-15)

I can repro this, and it's definitely bad behavior.  Two dialogs are shown: one before the victim URL commits (showing blank), and one after, as shown in the screenshot.  The second dialog runs in the context of the new page, and it has access to the page (document.domain, document.cookie, etc).  That's a UXSS.

I'm not sure why it would be specific to file:// URLs, which is indeed a mitigating factor.  It also doesn't repro on M50, so it's probably a recent change.

@dcheng: Can you take a look?  I wonder if it's related to any of the UXSS fixes you've been doing.

### dc...@chromium.org (2016-03-15)

I took a quick look… and universal access is true?!

### dc...@chromium.org (2016-03-15)

OK, the problem is allowUniversalAccessFromFileURLs defaults to true in Blink.

In RenderViewImpl::Initialize , we create a new main frame (and its associated Document). At this point, Document::initSecurityContext sees that allowUniversalAccessFromFileURLs = true and grants universal access to the origin!

Of course, a few lines later in RenderViewImpl::Initialize, we apply the preferences [1], but it's already too late.

[1] https://code.google.com/p/chromium/codesearch#chromium/src/content/renderer/render_view_impl.cc&rcl=1457998259&l=743

### in...@chromium.org (2016-03-15)

Thanks Charlie and Daniel for correctly triaging this.

Assigning it medium severity based on the need of file:// url, still looks bad.

### in...@chromium.org (2016-03-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2016-03-15)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### dc...@chromium.org (2016-03-15)

OK, I have a preliminary fix prepared that changes it so we apply WebSettings as soon as possible: https://codereview.chromium.org/1799423003

I /think/ this should be safe (it doesn't crash locally), but it's somewhat of a large change.

I see two other possibilities for fixing it that would result in smaller but suboptimal patches.
- Default allowUniversalAccessFromFileURLs to false: this might break Android WebView (which I think depends on this setting) in the reverse way if a Document with file:// origin opens a new window.
- Just apply WebSettings related to security before creating the main frame. Kind of ugly, because it splits up the settings initializations into a special case.

[Monorail components: UI>Browser>Navigation]

### cl...@chromium.org (2016-03-15)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ch...@gmail.com (2016-03-15)

I can report this bug more easily without the first alert dialog:

<button onclick="fsBypass();">click Here</button>
<script>
function fsBypass() {
  var x = window.open("https://abc.xyz");
  setTimeout(function(){x.location = "javascript:alert(document.domain)";}, 1000)
}
</script>


### bu...@chromium.org (2016-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0ff94cfc829f6df331dd71df1eef201e06cca36c

commit 0ff94cfc829f6df331dd71df1eef201e06cca36c
Author: dcheng <dcheng@chromium.org>
Date: Tue Mar 15 21:50:51 2016

Apply WebSettings before initializing the main frame.

Some settings need to be applied before initializing the main frame,
since they affect the creation of the initial empty document.

BUG=594383
CQ_INCLUDE_TRYBOTS=tryserver.blink:linux_blink_rel

Review URL: https://codereview.chromium.org/1799423003

Cr-Commit-Position: refs/heads/master@{#381327}

[modify] https://crrev.com/0ff94cfc829f6df331dd71df1eef201e06cca36c/content/renderer/render_view_impl.cc
[add] https://crrev.com/0ff94cfc829f6df331dd71df1eef201e06cca36c/third_party/WebKit/LayoutTests/fast/dom/Window/file-origin-window-open-expected.txt
[add] https://crrev.com/0ff94cfc829f6df331dd71df1eef201e06cca36c/third_party/WebKit/LayoutTests/fast/dom/Window/file-origin-window-open.html
[add] https://crrev.com/0ff94cfc829f6df331dd71df1eef201e06cca36c/third_party/WebKit/LayoutTests/fast/dom/Window/resources/file-origin-window-open-frame.html


### dc...@chromium.org (2016-03-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-15)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-04-04)

[Comment Deleted]

### me...@chromium.org (2016-04-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-05-11)

[Comment Deleted]

### ch...@gmail.com (2016-06-02)

Any update on the reward?

### me...@chromium.org (2016-06-02)

+Tim from security :)

### ti...@google.com (2016-06-02)

Not yet - we're still working through a panel backlog. You should hear back in a few weeks.

### sh...@chromium.org (2016-06-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

OK - now we're through the reward panel backlog. Thanks for your patience.

$3,000 for this report - congrats! We'll add this to the next payment run.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/594383?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083844)*
