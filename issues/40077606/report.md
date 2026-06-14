# Security: TLS Truncation attack on HTTP headers, including cookie flags

| Field | Value |
|-------|-------|
| **Issue ID** | [40077606](https://issues.chromium.org/issues/40077606) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>SSL |
| **CVE IDs** | CVE-2013-2853 |
| **Reporter** | an...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2013-05-27 |
| **Bounty** | $3,133.00 |

## Description

**VERSION**  

Chrome Version: 27.0.1453.94 stable  

Operating System: tested on Windows

**VULNERABILITY DETAILS**

Chrome, unlike Firefox, IE or Opera, attempts to defend against TLS truncation attacks by enforcing the Content-Length header to match the length of the query's response body length. However, like all other browsers, it doesn't implement the mandatory TLS closure alert enforcement from TLS 1.1 to prevent truncation attacks at the transport layer.

We discovered that in Chome, Safari and Opera, an HTTPS response truncated in the headers part was still processed by the browser, in particular, all Set-Cookie headers are parsed, even in the truncation occurs within a Set-Cookie line. This is a critical problem because a network attacker is able to cut the "secure" and "httpOnly" flags from a cookie and subsequently steal its value.

**REPRODUCTION CASE**

The following PHP script creates an HTTPS server that sends a truncated response to any query containing a single truncated cookie. The truncation occurs by TCP RSET. When the page is accessed at <https://localhost> (and the self-signed security warning is ignored) the cookie appears in the Resources tab of the Developer Tools.

<?
$serv = stream\_socket\_server("tls://0.0.0.0:88");
// Set to any self signed certificate with private key
stream\_context\_set\_option($serv, "ssl",
"local\_cert", "/etc/ssl/localhost.pem");
while ($conn = stream\_socket\_accept($serv))
{
for($b="";$r=fread($conn,1024) && trim($r););
fwrite($conn, "HTTP/1.1 200 OK\r\n"
."Set-Cookie: test=value"); // No line feed
stream\_socket\_shutdown($conn, STREAM\_SHUT\_RDWR);
}
THREAT MODEL
An active network attacker is required to exploit this attack by truncating the target TLS session.
EXAMPLE ATTACK
We were able to exploit this attack to steal Google Accounts sessions. Such sessions grant access to all Google services including GMail. The main difficulty in building an exploit is to get some plaintext or padding control in the response of the HTTP request to truncate, to be able to select the fragmentation point. Fortunately, there is a semi-open redirector in the Google Accounts login page (and in similar services) through the "continue" parameter containing an URL to redirect the user to after login, e.g. https://accounts.google.com/ServiceLogin?hl=en&continue=https://www.google.com/search%3Fhl%3Den%26q%3Dtest
Even though accounts.google.com is protected by HSTS, it is safe to assume that the continue parameter is under attacker control because many of the Google login buttons are sent over HTTP (for instance, on http://www.google.com, but also Youtube and others).
When the user submits valid credentials, the response is a redirect to https://accounts.google.com/CheckCookie?continue=[continue value] that includes many Set-Cookie headers for GAPS, NID, SID, LSID, HSID, SSID, APISID, SAPISID. Among those, only GAPS, LSID, SSID and SAPISID have the secure flag. Furthermore, only SSID is required to process login requests on accounts.google.com. Finally, these cookies all have a constant length, and they appear after the Location header containing the attacker-controlled padding.
The goal of the attacker is to chose the continue length such that fragmentation will occur immediately after:
Set-Cookie: SSID=xxx;Domain=.google.com;Path=/;Expires=yyy
This is generally easy because all Google servers use a constant fragment size of 1345 bytes. The network attacker injects a TCP FIN immediately after the target fragment, and because of the above bug, the SSID cookie will be saved without the secure flag set. Only APISID and SAPISID appear after SSID, and they are not necessary to the attacker.
Once the connection is truncated, the attacker either waits for or causes a request to http://www.google.com (e.g. by redirect-hijacking any other HTTP request from the user) to recover all non-secure cookies, including SID. This session can be used to log into the user's gmail account, among others.
As a side note, when Chrome is configured with allow-chrome-signin, the response also contains a "google-accounts-signin" header with the user's email address before the cookies. Thus, on Chrome, it may be necessary to guess the victim's account name length.
MITIGATIONS
The proper fix to this issue is to enforce closure alerts in accordance with the TLS 1.1 specification.
However, since this causes compatibility and performance issues, it is at least important to never accept cookies from a truncated request (i.e. missing a request body, even empty). Other browsers are affected in various degrees and will be notified.
Advisories will be sent to major vulnerable applications (such as Google) to mitigate the issue by setting all secure cookies at the very top of the response headers.

## Timeline

### ke...@chromium.org (2013-05-27)

[Empty comment from Monorail migration]

### ag...@chromium.org (2013-05-27)

This is a really fun attack, thanks!

Requiring close_notify isn't possible because so many sites don't send it, but you're correct that we shouldn't accept Cookies unless the request is complete. I'll do that on Tuesday unless someone beats me to it.

### sc...@gmail.com (2013-05-27)

Thanks Adam!
Fixing flags a bit. I'm not sure whether to go for severity medium or high.

### in...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-05-28)

Wouldn't a confidentiality bypass requiring an active network interception be medium, rather than high severity? At least, that's how we rated the CRIME attack.

### an...@gmail.com (2013-05-28)

Technically, a passive network attacker with dropping capability (i.e. tcpdump + iptables --reject-with tcp-reset) is enough for exploiting the secure flag truncation, which is much easier than CRIME. 

For the Google Accounts attack, it is possible to get the victim to access the login page for a given continue parameter by other means (e.g. sending link to a private google docs file with added junk parameters in the URL).

### sc...@gmail.com (2013-05-28)

Yeah, CRIME was Medium. I forget; didn't it require a large number of packets to practically mount a CRIME attack? That's the reason for my wavering.

### js...@chromium.org (2013-05-28)

We marked CRIME medium because it required some form of active connection manipulation (either via MitM or manipulating content in the site's origin). And forcing dropped packets is also clearly active connection manipulation. That's not to say this isn't a very technically interesting attack, just like CRIME. It's just that we have to look at it with respect to how we rate all vulnerabilities.

### in...@chromium.org (2013-05-28)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### ts...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### ag...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### ag...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### ag...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-29)

Adam, we are planning to close code 28 this week. Do you think the bug is fixable in this timeframe, we would really appreciate if you can.

### ag...@chromium.org (2013-05-29)

inferno: https://codereview.chromium.org/15688012/ - it's in the CQ.

It disables any processing of truncated headers for HTTPS. I believe that will address the problem. willchan suggested having someone else land it because I'm too linked with security fixes, but since the BUG= link is pointing at a restricted bug I figure we've already lost that battle anyway.

### in...@chromium.org (2013-05-29)

Adam, awesome, great to know it is in cq :) Don't worry about obfuscation, if we cared about it, then security team won't be landing any patches :) We believe in quickly fixing and release model :)

### in...@chromium.org (2013-05-29)

https://src.chromium.org/viewvc/chrome?view=rev&revision=202927

### sc...@gmail.com (2013-05-29)

@google@bouchon.org: this is a very clever attack.

How would you like to be credited in our releases notes (name, affiliation etc.)?

Are there any particular embargo deadlines? i.e. we usually patch faster than other browsers so should we avoid accidentally revealing too much in our release notes?

### an...@gmail.com (2013-05-29)

Thank you agl for fixing this so quickly. If you plan to attend Usenix or CCS and meet members from Prosecco, INRIA please come say hi since we've been discussing some security aspects of SPDY and TLS that might interest you.

If possible, can a CVE number be assigned for academic citation?
Credit goes to Antoine Delignat-Lavaud and Karthikeyan Bhargavan from Prosecco at INRIA Paris. As you suspected, other browsers aren't as swift but keeping release notes vague and restricting access to this bug for a while is likely the best course of action since someone smart and determined enough could always figure out the problem in the commit logs.

### sc...@gmail.com (2013-05-29)

My pleasure to assign you CVE-2013-2853

### [Deleted User] (2013-05-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-07)

M28: r204972

We can consider if for M27 if there's another patch; marking merged for now.

### sc...@gmail.com (2013-06-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-11)

Oops, my first merge was reverted due to compile failure of the unit test.

A better merge to M28 is landed at r205382

### pa...@chromium.org (2013-06-27)

$3133.7 for this one :)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### jo...@chromium.org (2013-07-02)

[Empty comment from Monorail migration]

### an...@gmail.com (2013-07-05)

Status of other browsers:
- Problem is fixed in current chromium-based Opera 15
- A member of Apple's product security team confirmed the issue would be investigated in Safari but current version appears to still be vulnerable

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### an...@gmail.com (2013-10-08)

Two things:
1. +reward-paid :)
2. since this bug is not fixed in Safari even though we reported it to Apple several months ago, we notified Apple that we would discuss the bug in a submitted paper that may appear next year. They commented that they did not object to the disclosure (but did not say whether they had any intention of patching).

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/244260?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077606)*
