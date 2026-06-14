# Security: Flash Cross Domain Policy Bypass by Using File Upload and Redirection - only in Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40080687](https://issues.chromium.org/issues/40080687) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2015-0337 |
| **Reporter** | so...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-10-20 |
| **Bounty** | $2,000.00 |

## Description

==VULNERABILITY DETAILS==
It is possible to bypass Flash Cross Domain policy in Google Chrome to read other websites' contents after a user uploads a file to a destination that redirects the user to the target website. It is also possible to send a file upload request to a target website without checking the cross domain policy by using an open redirect with status code of 307 (or 308).
This attack works as follows:
1- The "FileReference" class provides a means to upload file to a target server in ActionScript.
2- It accepts a URL as the destination for the file upload process.
3- It also has access to the target website's contents via the "UPLOAD_COMPLETE_DATA" event. This event is dispatched after data is received from the server after a successful upload.
4- If the target website redirects the user to another website, Flash in Google Chrome follows the redirection and discloses the destination content via the "UPLOAD_COMPLETE_DATA" event (first security issue). Moreover, if the target website redirects the user with status code of 307 (or 308), Google Chrome send the same file upload request to the final destination without checking the cross domain policy (second security issue).

Note: in other browsers such as IE or Mozilla Firefox, Adobe Flash returns an error code when the first response status code is anything other than 200.


==VERSION==
Chrome Version: 38.0.2125.104 stable
Operating System: Windows 7 SP1 64b


==REPRODUCTION CASE==
A SWF PoC file and its ActionScript source has been attached.
This SWF file can be hosted on any website to target other websites.
http://attacker.com/chromeFileUploadCrossDomain.swf?url=redirect.php?input=https://plus.google.com/u/0/

"redirect.php" is just a simple open redirect to the target URL. An example is as follows:
http://attacker.com/chromeFileUploadCrossDomain.swf?url=http://0me.me/demo/openredirect/redirect.php?target=https://plus.google.com/u/0/%26status=301
Note: "0me.me" has an open cross domain policy and that's why we did not need to host it on "attacker.com".

An image has been attached that shows the result of exploiting this vulnerability. Source code of the "redirect.php" file has also been attached just for information.


## Attachments

- [chromeFileUploadCrossDomain.as](attachments/chromeFileUploadCrossDomain.as) (application/octet-stream, 2.7 KB)
- [PoC.png](attachments/PoC.png) (image/png, 45.4 KB)
- [redirect.php.txt](attachments/redirect.php.txt) (text/plain, 437 B)
- [chromeFileUploadCrossDomain.swf](attachments/chromeFileUploadCrossDomain.swf) (application/octet-stream, 1.7 KB)

## Timeline

### jw...@chromium.org (2014-10-22)

Assigning this to cpu@ since it is my understanding that he's taking a look at these issues while jschuh@ is out. cpu@, please feel free to assign as necessary. Thanks!

### la...@chromium.org (2014-10-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-01)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-11-03)

cevans, can you triage this one as well when you get in on Monday. Thanks

### cl...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-14)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-17)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### so...@gmail.com (2014-11-17)

The credit for this issue goes to "Soroush Dalili from NCC Group" please.

Also please can you confirm if any bug bounty can be assigned to this issue?

Thanks

### mb...@chromium.org (2014-11-17)

Once the issue is fixed, the reward panel will determine whether or not it qualifies for a bounty. If we mention this in our release notes, we'll be sure to credit you appropriately.

### cl...@chromium.org (2014-11-25)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### sc...@gmail.com (2014-11-26)

Unassigning self; realistically I'm not going to get a chance to look into this before 2015.

Also, this issue represents an interesting cross-origin interaction but I am rusty in this area. cc:ing Joel who is strong in the cross-origin area and might know who would be the best to try reproducing and triaging this.

### ke...@chromium.org (2014-11-28)

Assigning Joel because finding owners is hard during Thanksgiving week and I want to make sure this doesn't get dropped.

### cl...@chromium.org (2014-12-06)

jww@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-13)

jww@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### so...@gmail.com (2014-12-17)

Any update on this please? it is an SOP bypass.

### cl...@chromium.org (2014-12-18)

jww@: Uh oh! This issue is still open and hasn't been updated in the last 57 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

jww@: Uh oh! This issue is still open and hasn't been updated in the last 57 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### so...@gmail.com (2015-01-06)

Any update on this please?

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-09)

jww@: Uh oh! This issue is still open and hasn't been updated in the last 79 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2015-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2015-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2015-01-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-05)

jww@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### [Deleted User] (2015-02-05)

We're testing a fix presently.  Barring any crazy fallout, it should land in our Octavia release.

### jw...@chromium.org (2015-02-07)

Thanks for the update!

### jw...@chromium.org (2015-02-07)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-02-24)

What's the timeline for the Octavia release? Could we consider this as fixed now?

### [Deleted User] (2015-02-24)

Octavia ships on March 10th

### me...@chromium.org (2015-02-24)

Thanks!

### so...@gmail.com (2015-03-12)

This issue has been patched by Adobe now (CVE-2015-0337): https://helpx.adobe.com/security/products/flash-player/apsb15-05.html


### mb...@chromium.org (2015-04-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-30)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-17)

soroush.dalili - Congratulations - $2,000 for this report. We'll be in contact to collect payment details. If you don't hear from someone within a week, please contact me directly at timwillis@.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-23)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/425280?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080687)*
