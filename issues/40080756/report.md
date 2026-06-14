# Security: Use after free in Flash (StageVideoAvailabilityEvent) can make bad things happen

| Field | Value |
|-------|-------|
| **Issue ID** | [40080756](https://issues.chromium.org/issues/40080756) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-10-31 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Use after free during the StageVideoAvailabilityEvent event can be abused to execute arbitrary code.  

An attacker can register this event and have the movie reloaded at the same time with LoadMovie (JavaScript call) (see notes.txt).

**VERSION**  

Chrome Version: [38.0.2125.111] stable  

Operating System: [Win 7 x64 SP1]

**REPRODUCTION CASE**  

Load loadStageMain.html in Chrome with the --no-sandbox flag and pray for calc.

## Attachments

- [StageVideo.zip](attachments/StageVideo.zip) (application/zip, 21.5 KB)
- [StageLoader.as](attachments/StageLoader.as) (application/octet-stream, 575 B)
- [StageLoader.swf](attachments/StageLoader.swf) (application/octet-stream, 735 B)
- [loadMovieUAF.html](attachments/loadMovieUAF.html) (text/html, 989 B)

## Timeline

### in...@chromium.org (2014-10-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-11-02)

Thanks for assigning to me @aarya.
I will triage it on Monday.

### wf...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-11-05)

I confirm the exploit. I prayed to the gods of calc and lo! i was granted the ability to perform simple math.

Another great piece of work.

I'll defang the exploit and send it along to Adobe. Quick couple of notes / questions for @biloulehibou:

1) I'll do it this time, but next time, is it also possible get a PoC separate from the exploit? A PoC should be as simple as possible whilst still exhibiting the crash :)

2) I'm really intrigued by the StageLoader.LoadMovie call from the HTML file. I didn't even know that was possible :) Does the same attack work (or can it be made to work?) purely within the SWF file? What if the SWF file tries to call loadMovie on itself inside the actual callback function?

### sc...@gmail.com (2014-11-05)

Attaching de-fanged PoC :)

### sc...@gmail.com (2014-11-05)

Adobe tracking id: PSIRT-3130

### bi...@gmail.com (2014-11-06)

[Comment Deleted]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-07)

Fixed in the Flash included here: http://googlechromereleases.blogspot.com/2015/02/stable-channel-update.html

https://helpx.adobe.com/security/products/flash-player/apsb15-04.html

### cl...@chromium.org (2015-02-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Merge not required - see #11.

### ti...@google.com (2015-04-09)

Congrats - $7500 for this one.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-16)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/429276?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080756)*
