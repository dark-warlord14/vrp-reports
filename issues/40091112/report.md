# Consider blocking U+0307 after other i-like characters (e.g. U+1EC9)  

| Field | Value |
|-------|-------|
| **Issue ID** | [40091112](https://issues.chromium.org/issues/40091112) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | zx...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-04-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
http://xn--uncode-qyd1697c.org/

What is the expected behavior?

What went wrong?
Latin-extended from U+1EA0 not be blocked, it can lead to url spoof, for example, ỉ (U+1EC9) followed by a combining mark, just as https://crbug.com/chromium/750239 says: `U+0307 (dot above) after i, j, l, or U+0131 (dotless i) would be very hard to see if possible at all`, 

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: OS X 10.13.4
Flash Version: Shockwave Flash 29.0 r0

## Attachments

- [unicode.png](attachments/unicode.png) (image/png, 8.1 KB)
- [window_unicode.png](attachments/window_unicode.png) (image/png, 691 B)

## Timeline

### zx...@gmail.com (2018-04-15)

And on Windows, it seems more confused

### zx...@gmail.com (2018-04-15)

And anther payload: http://xn--googe-bgd9680c.com/
U+1ECB (ị) followed by U+0307 may confused with `l`

### ca...@chromium.org (2018-04-16)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### ca...@chromium.org (2018-04-16)

[Empty comment from Monorail migration]

### mg...@chromium.org (2018-04-17)

jshin deals with domain name spoofing.

### zx...@gmail.com (2018-04-17)

As `unicode.org` not in top domain list, so it can be spoofed simply by http://xn--uncode-xk8b.org/
anyway, as you block latin extended from U+1E00 to U+1E9F, so i think it's necessary to block latin extended from U+1EA0 as well

### zx...@gmail.com (2018-04-17)

And another interesting idn spoof cause by latin extened, https://xn--fabook-jhb.com/, U+0153/U+0152 (œ) shown like `ce` in address bar

### js...@chromium.org (2018-04-17)

As you mentioned in https://crbug.com/chromium/833138#c6. unỉ̇code.org with U+1EC9, U+0307) is not blocked because it's not in the top 10k list.

OTOH, gmaỉ̇l.com (http://xn--gmal-swc9473b.com/ ;gmail with U+1EC9 + U+0307) is blocked. 

We can't block U+1EA0 ~ U+1EFF blindly (it's used in Vietnamese). 

> U+0307 (dot above) after i, j, l, or U+0131 (dotless i)

Blocking U+0307 after other i-like characters can be considered. 



### zx...@gmail.com (2018-04-18)

[Comment Deleted]

### zx...@gmail.com (2018-04-19)

[Comment Deleted]

### sh...@chromium.org (2018-05-02)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2018-05-11)

From the set at https://goo.gl/2j6r18 ,  

\u00ec-\u00ef
\u0129 \u012b \u012d, \u012f, \u0135, \u013a, \u013c, \u013e, \u0142
\u01f0, \u0209, \u020b \u0211, \03af \0456-\u0458, ......

Hmm.... perhaps just banning all diacritics in U+03xx might be better (treating i/j like special does not seem to make a lot of sense) , but doing so will lose some language support.  

Alternatively, we can just do nothing. Top domains are protected anyway. 

Yet another alternative would be to wait for ICU to add an option for this group of characters. There's a work going on. 





### js...@chromium.org (2018-05-11)

See  http://bugs.icu-project.org/trac/ticket/13333  . There's a CL under review for this ICU ticket. 

I can cook up soemthing with 'soft-dotted char property', but I'd rather wait for ICU to deal with them. If necessary, we can cherry pick from the upstream. 


### js...@chromium.org (2018-05-11)

Hmm....
soft-dotted set (https://goo.gl/NRmgyA ) is a lot smaller than what I listed in https://crbug.com/chromium/833138#c12. 



### sh...@chromium.org (2018-05-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2018-05-14)

> This is a serious security regression.

It's not !

### sf...@google.com (2018-05-14)

I'm working on an ICU ticket to detect U+0307 following Soft_Dotted, dotless i, dotless j, 'l', and characters confusable with them:

http://bugs.icu-project.org/trac/ticket/13333

I based that set off of previous comments on this thread.  This is not yet in the Unicode specification.  If you would rather see more sequences forbidden than what I listed here, please comment within the next few days in order to get this into ICU 62.

### js...@chromium.org (2018-05-17)

Thanks, Shane. If the answer to my question at http://bugs.icu-project.org/trac/ticket/13333#comment:18 ) is positive, I think we're good. 



### me...@google.com (2018-07-26)

Looks like the fix for http://bugs.icu-project.org/trac/ticket/13333 is already in canary, and the payload in https://crbug.com/chromium/833138#c2 now displays punycode.

Can this be closed or is there remaining work?

### sf...@google.com (2018-08-03)

As far as I am concerned, from the ICU side, this issue is closed unless there is another compelling case that our solution does not address.

### me...@chromium.org (2018-08-03)

Thanks, let's close this as fixed.


### sh...@chromium.org (2018-08-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-13)

Thanks for the report! The VRP panel decided to award $500 - cheers!

### aw...@google.com (2018-08-13)

[Empty comment from Monorail migration]

### zx...@gmail.com (2018-08-13)

Wow, thanks a lot !

### zx...@gmail.com (2018-09-07)

And I want to know will this bug assigned a CVE ?

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-11-10)

This issue was migrated from crbug.com/chromium/833138?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091112)*
