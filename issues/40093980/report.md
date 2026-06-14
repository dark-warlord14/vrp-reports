# Stale node in StyleSheetCandidateListHashSet

| Field | Value |
|-------|-------|
| **Issue ID** | [40093980](https://issues.chromium.org/issues/40093980) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ax...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-08-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Tab is crashing when modifying SVG file.

I had two different crash places with this test case, probably they are due to one one bug. First crash place is shown in attachment dbg-1.tar.gz. and is related to 15.0.849.0 dev-m (unfortunately, I don't have minimized test case - I have only huge one). Second crash looks more dangerous, for that test case is attached here, with debug info dbg-2.tar.gz, reproduced on 14.0.835.35 beta-m.

One note about test case - if to change font size in test case, then register eax value changes too.

**VERSION**  

Windows XP SP3: 15.0.849.0 dev-m, 14.0.835.35 beta-m

**REPRODUCTION CASE**  

See attachment.

## Attachments

- [test-case-2.tar.gz](attachments/test-case-2.tar.gz) (application/x-gzip; charset=binary, 1.0 KB)
- [dbg-1.tar.gz](attachments/dbg-1.tar.gz) (application/x-gzip; charset=binary, 13.4 KB)
- [dbg-2.tar.gz](attachments/dbg-2.tar.gz) (application/x-gzip; charset=binary, 14.7 KB)
- [test-case-1.tar.gz](attachments/test-case-1.tar.gz) (application/x-gzip; charset=binary, 3.6 KB)

## Timeline

### ax...@gmail.com (2011-08-15)

Attaching test-case-1. Sorry for such a fat SVG file, I'm in hurry and won't be soon near my workstation. This test-case is related to dbg-1.tar.gz.

### in...@chromium.org (2011-08-16)

Thank you for the nice bug.

In the future, can you please attach the testcase and stacktrace directly to the bug without zipping it. In fact, smaller testcases and stack, you can paste directly in the comments.

test-case-2 reproduces perfectly, but it is not fully reproduced. Also, i don't think you need 2 files. If you can fully reduce the testcase and have a clear repro, you will qualify for the higher reward. Want to give it a shot ?

### in...@chromium.org (2011-08-16)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=66335

### ax...@gmail.com (2011-08-17)

Ok, will do so.

I will try to reduce testcase, albeit I can't promise to do that fast - unfortunately, currently I am quite limited to internet. Hope to provide reduced testcase in a couple of days.

Also, how do you mean "not fully reproduced" - it works not always or file is just too bloated? On dev and beta under windows it worked always for me.

And do you need smaller repro for test-case-1?


### in...@chromium.org (2011-08-17)

They are the same bug, isn't it. So, we need reduction for only one. For now, i reduced it, this will serve as an example for your future reports. By reduced, we mean smaller and cleaner testcase

<!DOCTYPE html>
<html>
<script>
function runTest() {
    svgdoc = document.getElementById('root').contentDocument;
    var style = document.createElement('style');
    var test1 = svgdoc.getElementById('test1');
    test1.appendChild(style);
    svgdoc.getElementById('test2').setAttribute('xlink:href', 0);
    svgdoc.getElementById('test').setAttribute('stroke', 0);

}
</script>
<object data="animate-elem-77-t.svg" id="root" onload="runTest();" type="image/svg+xml"></object>
</html>

----animate-elem-77-t.svg----
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<g id="test">
<text id="test1">PASS</text>
</g>
<use id="test2" xlink:href="#test"/>
<use xlink:href="#test"/>
<set attributeName="font-style" to="italic"/>
</svg>


### in...@chromium.org (2011-08-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-08-17)

http://trac.webkit.org/changeset/93227

### ax...@gmail.com (2011-08-17)

Great, thanks a lot, inferno!

### in...@chromium.org (2011-08-17)

Ax330d, the pleasure is all ours, keep your fuzzers rocking!!

### sc...@gmail.com (2011-08-20)

@Ax330d: thanks for this report, and it's my pleasure to offer you a $1000 Chromium Security Reward -- congrats!

It's always good to see new researchers, so I hope you have more research planned ;-)

We reward at the higher $1000 level for good quality reports. To be sure of getting the higher reward amount in the future, please make sure to strip any unneeded constructs out of the repro files, and keep them as small and tidy as possible.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ax...@gmail.com (2011-08-20)

Nice, pleasure to work with you :)

### sc...@gmail.com (2011-08-22)

Merged to M14: http://trac.webkit.org/changeset/93497

### sc...@gmail.com (2011-08-22)

@Ax330d: with what name would you like to be credited?

### ax...@gmail.com (2011-08-22)

@scarybeasts, you can use my real name - Arthur Gerkis.

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-30)

Payment is in system.

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/92959?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093980)*
