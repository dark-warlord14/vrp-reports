# Security: XSS Auditor behavior can cause leak of submitted form data because of about:blank redirection

| Field | Value |
|-------|-------|
| **Issue ID** | [40078608](https://issues.chromium.org/issues/40078608) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | ne...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2013-12-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When XSS Auditor detects XSS in form "action" attribute, it changes it to about:blank. Attacker can add bogus parameters to make sensitive information <<submitted>> to about:blank. After that, XSS Auditor under some conditions will allow to brute request body char-by-char by adding <script> with some content to that about:blank page and see if it is blocked.

More detailed:  

Assume there are two sites, attacker.com and victim.com. User agrees to send sensitive information to the victim.com but not to the attacker. Assume this information is user's password from his victim.com account. Attacker can perform following steps to get the password:

1. Assume user is browsing attacker.com. When user clicks on link "login using your victim.com account", attacker performs window.open. In the new window he makes POST request using form to the victim.com login page with bogus parameter which value is kind of "action='/login'" which is extracted from victim's source before attack and is victim.com login form action. If victim.com rejects POST at this page, attacker can use GET too, but it will be seen in location bar that there is strange url parameter.
2. User sees victim.com url at location bar and enters his password. What he doesn't see is that XSS Auditor filtered action of login form and set it to about:blank. When user submits form, info is "submited" to about:blank. Assume login form used POST.
3. Attacker can now access about:blank and run there his scripts. If he do so, XSS Auditor will use attacker's URL and request body sent by victim.com for initialization. If attacker add somethink like ?a=<script> to his own url before doing step 1, XSS Auditor will search every <script>'s content snippet if it is substring of request body. Another condition for this is that request body must contain at least one of < > ' " symbols. We'll discuss this below.
4. Now attacker starts to make <script> tags and see if they are filtered. Assume attacker has already got string s which is contained in request body. He can now create <script> tags using document write with such contents as sa, sb, sc, ..., sz. If s is followed by one of a..z in request body (and so in user's password) then one of this <script> will be filtered and others will not. So attacker knows new character of s in constant time without any network requests and he can brute the whole password or request body char-by-char.

Here is again list of preconditions is needed to attack:

1. victim.com is using POST for submitting login form, doesn't set X-XSS-Protection. Common case.
2. login form is submitted to some page different from page where it is shown, so that there is explicit action parameter in login form. Common case again.
3. one of ' " < > is contained in login request. That is the hardest precondition. The reason for it is that if none of that is contained in request body, XSS Auditor will completely ignore it. Well, if victim uses multipart/form-data there will be a lot of double quotes. I think that there could be come encoding issues also because XSS Auditor will use attacker's document encoding for decode request body.

**VERSION**  

Chrome Version: both stable and beta seems to be vulnerable  

Operating System: I used linux version to perform tests

**REPRODUCTION CASE**  

Attacker.html is example for attacker page located on attacker.com, and victim.html is example for victim's login form. I use multipart/form-data for demo, but there could be other ways to set up one of that ' " < > characters into the request body. You need to set up victim's url in attacker.html before you start reproduction, and you need to have attacker and victim in different origins.

I've tried really hard to make the PoC both minimal and showing full issue, and there are a lot of comments there, but attacker.html still has 65 lines. I don't think it is too hard to understand what it does, I think it could be minimal repro for such a complex attack.

## Attachments

- [attacker.html](attachments/attacker.html) (text/html, 3.8 KB)
- [victim.html](attachments/victim.html) (text/html, 293 B)
- [attacker_yahoo.html](attachments/attacker_yahoo.html) (text/html, 4.7 KB)

## Timeline

### mb...@chromium.org (2013-12-30)

Thanks for the report! This is an interesting attack.

Sorry that I keep assigning these XSS auditor bugs to you, Tom. Are there any other good contacts for these?

### ne...@gmail.com (2014-01-03)

I've found that there is other widely applicable way to include one of < > ' " in request body. Victim can use some kind of "page where redirect after login" parameter (and still properly escape it before sending to user!), so we can paste one of them here.

So, again, list of preconditions:
0. No XSS or other vulnerabilities is required on victim side
1. Victim has login form with explicit action argument, doesn't send X-XSS-Protection header and use POST request for login (if victim use ajax as login option, we can simply disable it using XSS Auditor by sending bogus parameters, but explicit "action" is required).
2. Attacker can make victim include one of < > ' " into request body. There could be some ways for doing that:
a) victim uses multipart/form-data so every parameter's name is in quotes
b) victim sends to login script a parameter which could be set by attacker, for example url of page to redirect after successful login
c) victim sends to login script some non-ASCII data so that attacker can set his own page charset in such way that one of ' < > " will appear after decoding.

Example in attachment steals yahoo login and password using 2b (only 4 lines defining constants have been changed, so I'm proud of my poc ;-) ). Google, Facebook and Twitter would have been vulnerable too if there had been no X-XSS-Protection header.


### ts...@chromium.org (2014-01-06)

Patch at https://codereview.chromium.org/124973004/

### bu...@chromium.org (2014-01-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=164538

------------------------------------------------------------------------
r164538 | tsepez@chromium.org | 2014-01-07T01:09:29.188549Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/form-action-expected.txt?r1=164538&r2=164537&pathrev=164538
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/formaction-on-button-expected.txt?r1=164538&r2=164537&pathrev=164538
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/parser/XSSAuditor.cpp?r1=164538&r2=164537&pathrev=164538
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/formaction-on-input-expected.txt?r1=164538&r2=164537&pathrev=164538

Use data:, rather than about:blank as a substitute form action so the resulting blank page will have an unique origin.

This is similar to the work we did in XSSAuditorDelegate for the mode=block
case, where we used the SecurityOrigin::urlWithUniqueOrign constant.  We can't
use that here due to threading.

Testing is covered by rebasing the existing test cases.
BUG=331060
R=abarth@chromium.org

Review URL: https://codereview.chromium.org/124973004
------------------------------------------------------------------------

### ts...@chromium.org (2014-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-01-08)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-16)

Requesting merge for M32 and M33.

### ts...@chromium.org (2014-01-17)

We'll let this bake and release in m33.

### la...@google.com (2014-01-18)

Approved for M33 (1750).

### bu...@chromium.org (2014-01-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=165545

------------------------------------------------------------------------
r165545 | tsepez@chromium.org | 2014-01-22T20:09:14.756817Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/http/tests/security/xssAuditor/formaction-on-input-expected.txt?r1=165545&r2=165544&pathrev=165545
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/http/tests/security/xssAuditor/form-action-expected.txt?r1=165545&r2=165544&pathrev=165545
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/http/tests/security/xssAuditor/formaction-on-button-expected.txt?r1=165545&r2=165544&pathrev=165545
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/html/parser/XSSAuditor.cpp?r1=165545&r2=165544&pathrev=165545

Merge 164538 "Use data:, rather than about:blank as a substitute..."

> Use data:, rather than about:blank as a substitute form action so the resulting blank page will have an unique origin.
> 
> This is similar to the work we did in XSSAuditorDelegate for the mode=block
> case, where we used the SecurityOrigin::urlWithUniqueOrign constant.  We can't
> use that here due to threading.
> 
> Testing is covered by rebasing the existing test cases.
> BUG=331060
> R=abarth@chromium.org
> 
> Review URL: https://codereview.chromium.org/124973004

TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/144093014
------------------------------------------------------------------------

### dh...@chromium.org (2014-02-11)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $1000 reward. While there were a number of mitigating factors here, your samples did a good job of demonstrating the exploitability of the issue.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-15)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-09-17)

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

This issue was migrated from crbug.com/chromium/331060?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078608)*
