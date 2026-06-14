# Security: XSS Auditor info disclosure using iframe length from different domains

| Field | Value |
|-------|-------|
| **Issue ID** | [40082252](https://issues.chromium.org/issues/40082252) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Reporter** | ga...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2015-06-10 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**  

Using contentWindow.length and when the filter uses block mode you can detect if the filter has blocked the page provided there is an existing iframe on the site. You can inject fake XSS payloads and use this detection technique to see if the content has been matched. If a script block contains an user id or an email address you can inject a string that matches the script block e.g.

<script>
uid = 123;
</script>

somepage.php?fakeinjection=<script>%0auid = 123;%0a

This will be blocked as an XSS injection, the uid can be bruteforced by injecting different combinations it is pretty slow but the next attack below is more effective as it can check if the string partially matches.

Eduardo Vela suggested I pad using existing param inside a form block. I then produced a PoC that can read a 32 character hash (token\_example.html) thanks Sirdarckcat! The token example works by trying every character from 1-f I exclude 0 because this character is ignored by XSS auditor. If no match occurs for each of the characters I assume that the character is 0. If this sequence is repeated and no matches occur I then assume 2 0's exist. This enables me to steal a hash even if it contains zeros.

**VERSION**  

Chrome Version: 44.0.2403.30 beta-m  

Operating System: Windows 7 SP1

**REPRODUCTION CASE**  

This one uses iframes onload bruteforces the value 123  

<http://www.businessinfo.co.uk/labs/chrome_xss_filter_bruteforce/bruteforce_uid.html>

This works using windows and checks if the email was blocked  

<http://www.businessinfo.co.uk/labs/chrome_xss_filter_bruteforce/check_if_email_matches.html>

This one is pretty slow but shows how to do it x-domain even if a site has x-frame-options:  

<http://www.businessinfo.co.uk/labs/chrome_xss_filter_bruteforce/slow_bruteforce_using_windows.php>

Steal token example using existing filtered param and an existing form:  

<http://www.businessinfo.co.uk/labs/chrome_xss_filter_bruteforce/token_example.html>

## Attachments

- [check_if_email_matches.html](attachments/check_if_email_matches.html) (text/html, 550 B)
- [token_example.html](attachments/token_example.html) (text/html, 2.3 KB)
- [test.php](attachments/test.php) (text/plain, 126 B)
- [form.php](attachments/form.php) (text/plain, 350 B)
- [slow_bruteforce_using_windows.php](attachments/slow_bruteforce_using_windows.php) (text/plain, 639 B)
- [test2.php](attachments/test2.php) (text/plain, 140 B)
- [bruteforce_uid.html](attachments/bruteforce_uid.html) (text/html, 936 B)

## Timeline

### ts...@chromium.org (2015-06-10)

This is related to https://code.google.com/p/chromium/issues/detail?id=396544.  What this bug cleverly proves is that the issue in 396544 isn't fixed, nor is it likely to ever be *fixable* in the general case given the design of the web.  Which means if you can guess tokens, you can verify them, under the following conditions:

1. The site must supply an 'x-xss-protection mode=block' header.
2. The site must place sensitive information in an attribute filtered by XSSAuditor.
3. The sensitive information must occur within the first 100 characters of the attribute.
4. The attacker must fully control all of attribute value string prior to the point at which the server appends the sensitive information. This may be rare.
5. The site must not block you after making repeated requests for the same page rapidly in a loop (i.e. no DOS protection).

So the best we can do is ensure that we don't provide efficient ways of guessing secrets.  The PoC shows this is currently possible to guess a token in linear time in one case.  There's a patch at https://codereview.chromium.org/1179633002/ that should break these cases.




### ts...@chromium.org (2015-06-10)

+mkwst@ cc'd.

### ev...@google.com (2015-06-11)

About (4) - we are highly likely to have products in Google vulnerable to this.

Appending CSRF tokens in action is easier than creating a new input@type=hidden. Search for action=.*PageAction to see some vulnerable apps.

### ev...@google.com (2015-06-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2015-06-11)

Re #3: Good to know.  Sounds like a bad practice.

### ke...@chromium.org (2015-06-11)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-06-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2015-06-11)

See https://src.chromium.org/viewvc/blink?view=rev&revision=196971

### ts...@chromium.org (2015-06-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-06-11)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196971

------------------------------------------------------------------
r196971 | tsepez@chromium.org | 2015-06-11T20:25:33.798312Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/resources/echo-form-action.pl?r1=196971&r2=196970&pathrev=196971
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/form-action-token-fragment.html?r1=196971&r2=196970&pathrev=196971
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/parser/XSSAuditor.cpp?r1=196971&r2=196970&pathrev=196971
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/form-action-token-fragment-expected.txt?r1=196971&r2=196970&pathrev=196971

Prevent linear-time forcing of tokens by inducing XSSAuditor page blocks.

The page itself must control where the fragment to match ends,
otherwise leading-substring matches may be induced.  The pre-conditions
required for this are expected to be uncommon.

BUG=498982

Review URL: https://codereview.chromium.org/1179633002
-----------------------------------------------------------------

### cl...@chromium.org (2015-06-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-06-15)

Merge requested to M44 (branch 2403)

### pe...@google.com (2015-06-15)

Approved for M44 (branch: 2403)

### ts...@chromium.org (2015-06-16)

https://src.chromium.org/viewvc/blink?view=rev&revision=197177

### bu...@chromium.org (2015-06-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=197177

------------------------------------------------------------------
r197177 | tsepez@chromium.org | 2015-06-16T16:22:08.310231Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/security/xssAuditor/form-action-token-fragment.html?r1=197177&r2=197176&pathrev=197177
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/core/html/parser/XSSAuditor.cpp?r1=197177&r2=197176&pathrev=197177
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/security/xssAuditor/form-action-token-fragment-expected.txt?r1=197177&r2=197176&pathrev=197177
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/security/xssAuditor/resources/echo-form-action.pl?r1=197177&r2=197176&pathrev=197177

Prevent linear-time forcing of tokens by inducing XSSAuditor page blocks.

The page itself must control where the fragment to match ends,
otherwise leading-substring matches may be induced.  The pre-conditions
required for this are expected to be uncommon.

BUG=498982

Review URL: https://codereview.chromium.org/1179633002

(cherry picked from commit 52e2a37cc5f36890d6015db7852ead73eac5c36c)

Review URL: https://codereview.chromium.org/1190433008.
-----------------------------------------------------------------

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ga...@gmail.com (2015-07-28)

Hello, am I ok to publish a blog post about this issue now? Thanks

### ts...@chromium.org (2015-07-28)

+timwillis - release is out, but no action from panel yet. Not sure what the rules apply here ...  thanks.

### ti...@google.com (2015-08-17)

@gazhayes: We decided to pay $1,337 for this report. We'll be in touch to collect details for payment, though please contact me at timwillis@ if you haven't heard from our finance area in a week.

Panel notes: $1000 for the infoleak, bumped up to $1337 because it was leet.

As M44 has been out for 3+ weeks, no issue with you blogging on the issue. Let me know if you want me to open up public access to this bug ahead of schedule if you want to link to this issue from your blogpost.

### ti...@google.com (2015-08-28)

In process: waiting on enrollment details.

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-09-18)

Bulk update: removing view restriction from closed bugs.

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

### el...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-27)

This issue was migrated from crbug.com/chromium/498982?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/836123]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082252)*
