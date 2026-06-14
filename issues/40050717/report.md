# Security: <portal>s with an autofocus element get focus

| Field | Value |
|-------|-------|
| **Issue ID** | [40050717](https://issues.chromium.org/issues/40050717) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Portals |
| **Platforms** | ChromeOS |
| **Reporter** | sm...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2019-11-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

If a page in a <portal> has an element with the "autofocus" attribute, then the page hosting the portal loses focus to that page. Keyboard shortcuts like Ctrl-T don't work, the reload key (on CrOS) doesn't work, etc. Since many websites have autofocused elements, and portals don't respect X-Frame-Options, this means that users can be tricked into interaction with pages via a portal. For example, since the Google OAuth authorization page has an autofocused element, you can trick people into authorizing your OAuth app if you can make them press the right keys in the right sequence.

**VERSION**  

Chrome Version: 78.0.3904.92 stable  

Operating System: Chrome OS

**REPRODUCTION CASE**  

Navigate to portal-test.html, and the input inside the portal when gain focus.

portal-test.html:  

<!doctype html>

<html>
<head></head>
<body>
<div>
This autofocused input will lose focus: <input type="text" autofocus>
</div>
<portal
src="portal-test-2.html"
style="width: 400px; height: 100px; border: 2px dashed black;"></portal>
</body>
</html>

portal-test-2.html:  

I'm in a portal!  

<input type="text" autofocus>

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Smitop

## Timeline

### do...@chromium.org (2019-11-17)

I'm not convinced this is a security issue given that tricking user input is required and there are probably easier ways of doing it. It may be a bug in portals though, so +that team to take a look.

[Monorail components: Blink>HTML>Portal]

### jb...@chromium.org (2019-11-17)

I believe Adithya is working on this. (I couldn't find an obvious existing bug, Adithya, bug dupe this if one exists.)

### me...@chromium.org (2019-11-19)

There is a similar but older bug about iframes stealing focus (https://crbug.com/chromium/622714). It was merged into https://crbug.com/chromium/954349 which is low severity. Given that precedent, I think we should treat this as a security bug.

smittycrbug: I wasn't able to repro on Linux with the PoC you attached. Is this specific to ChromeOS? (sounds unlikely?)

### ad...@chromium.org (2019-11-19)

This isn't chromeos specific. There are a few ways to repro, in fact just calling element.focus() on an input element inside the portal will allow the portal to steal focus.

### jb...@chromium.org (2019-11-19)

#3: This is an unshipped feature (it has to be enabled in chrome://flags to be available). This is the most likely reason why you can't reproduce, but I also think this significantly reduces the severity, since ordinary users should not have this feature enabled yet.

### sh...@chromium.org (2019-11-20)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lf...@chromium.org (2019-11-25)

Changing to Security_Impact-None since this is behind a flag.

### ad...@chromium.org (2019-12-04)

[Empty comment from Monorail migration]

### jb...@chromium.org (2020-01-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-17)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $500 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals]

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>Portal]

### is...@google.com (2020-10-12)

This issue was migrated from crbug.com/chromium/1025521?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1030838]
[Monorail blocking: crbug.com/chromium/1040212]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050717)*
