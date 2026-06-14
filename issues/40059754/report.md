# Security: PageSpeed Insights: DDOS via Blind XSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40059754](https://issues.chromium.org/issues/40059754) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Headless |
| **Reporter** | [Deleted User] |
| **Assignee** | am...@chromium.org |
| **Created** | 2022-05-25 |
| **Bounty** | $500.00 |

## Description

(I'm the TL of PageSpeed Insights, a Google service run by a team within Chrome. The vulnerability is not strictly within Chrome, but in the configuration of our service. I'm not reporting a bug here, but moreso using this issue to ask questions to Chrome VRP folks. In short: I'm curious if there's any opportunity for reward.)

**VULNERABILITY DETAILS**

details: <https://github.com/GoogleChrome/web.dev/issues/7971> reported by <https://github.com/Zweizack>  

video: <https://www.youtube.com/watch?v=VIlul4zVG7s>

In essence:

1. Create a webpage that makes thousands of XHRs repeatedly to a target. Put it online.
2. Have <https://pagespeed.web.dev/> analyze that page. Now, Google IPs are making these requests.
3. Not part of the report, but step 2 could be scripted with our public API, making the scale of the DOS quite sizable.

Since the bug was reported, we (the PageSpeed Insights team) have implemented a fix. Internal bug: <http://b/233650292>  

We consider this bug to be resolved now.

I don't think this bug falls within scope of Google or Chrome VRP, as it's mostly an issue of our service's configuration.  

However I'd ideally like to show our appreciation to the reporter. I saw he does have a <https://www.buymeacoffee.com/Zweizack> page.

Questions:  

\* Is it reasonable for our team to provide a reward?  

\* Is using the buymeacoffee.com service fine? (I imagine it's not preferred, but I don't want to spend much time here :)  

\* And if those are both yes's, then how much is reasonable?

## Timeline

### dr...@chromium.org (2022-05-26)

I don't think this is within the Chrome VRP guidelines, which has its rules listed here: https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules. We're really only interested in vulnerabilities in Chrome/ChromeOS itself. There is an internal Google VRP, though, which definitely covers Google-run websites better. I'm not too familiar with their rules, so I can't say for sure if this qualifies for them. The internal reporting link is http://shortn/_N4cfFtU2XO, I'd reach out there.

### am...@chromium.org (2022-05-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-27)

Hi Paul -- thanks for this question and your desire to reward some folks that reported a valuable issue. I will reach out to you over email about this! 

### am...@chromium.org (2022-05-27)

as per paulirish@ - this issue was fixed https://github.com/GoogleChrome/web.dev/security/advisories/GHSA-pcw2-w2rg-784g
setting reward-topanel label; need a reward-to email address for researcher 

### am...@chromium.org (2022-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-27)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-05-28)

arbitrary component (headless, since LightSpeed > PageSpeed Insights is not a core Chrome browser component and does not have a monorail component and impact Chrome headless) 
foundIn-100 and severity set completely arbitrarily since this does not impact general Chrome build and release cycles and severity low since this does not impact Chrome browser directly but need to quell the bot 

[Monorail components: Internals>Headless]

### am...@chromium.org (2022-05-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-28)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-28)

dear friendly neighborhood bot, I would sincerely appreciate it if you would kindly refrain from reopening this ticket. sincerely, your friendly neighborhood security bug wrangler 

### am...@chromium.org (2022-05-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-29)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-29)

[Empty comment from Monorail migration]

### pa...@chromium.org (2022-05-31)

[Description Changed]

### pa...@chromium.org (2022-05-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-31)

[Empty comment from Monorail migration]

### pa...@chromium.org (2022-06-02)

+cc zweizack's gmail, for bug visibility

### [Deleted User] (2022-06-02)

Hi,

Actually, I also reported the vulnerability that I reported to you to the "google bug bounty" system, but I contacted you directly on github as I did not receive any response. I also wrote the report in more detail, and there was one more thing I learned later on the subject. I will transfer what is written in the report I reported from the google system in the same way!

1. Summary: I can attack systems using your "Google PageSpeed Tool". I was also able to perform the same attack on "googleapis" today. You need to set a limit to it. I can understand that you have a tool that tests the speed of websites, but it is not a pleasant situation as it will be a useful tool for black hat and your ip addresses will be blocked from the attacked systems. I was able to even crash my own website using your tool yesterday. Even if you are not going to set a limit, you can ensure that only people with api keys can do this. This is my solution suggestion.

(other thing i want to talk about)
2. Summary: I did not show it in the video, but you can attack instantly using the url below.

URL: https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://zweizack.github.io?uid=RANDOMMMMMM&strategy=mobile

Attack scenario:
They can make ddos attacks on other websites or servers using your systems. In addition, your IP addresses can be blocked by counter systems because they become aggressive.

(Google buganizer-system - issue_id - 233792120)

### am...@chromium.org (2022-06-02)

Hi OR (original reporter :)), thank you for the background. I don't have access to the buganizer ticket and it's marked as a "customer issue" with a status of "won't fix/ working as intended" and was assigned to the Intel Collection Trust and Safety team. This means it like would have not made it to the Google VRP (Vulnerability Rewards Program/bug bounty) for review/a response. 

While this does not meet the eligibility requirements for Chrome VRP, since the fix did help a team within Chrome, we (the Chrome VRP) would like to consider it for a potential reward at a future VRP Panel. As this issue does have a reward-topanel label, it will ensure it makes it to our list of bugs to consider for rewards in the near future. Any update will be added directly here for your visibility. 


### [Deleted User] (2022-06-02)

Hi amyressler :) , Thank you very much for your interest in the matter.

Also, Paul, thank you very much indeed. You've devoted a lot of time and interest to the subject. I hope I have done something useful.

thanks :)





### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations, Zweizack! The PageSpeed Insights team greatly appreciate your report and your efforts in reporting this issue to them. While this issue is not technically eligible for the Chrome VRP, after conferring with Paul, the Chrome VRP would like to extend a $500 thank you reward to show our appreciation for your efforts. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-23)

Thank you, amyressler!

Thank you to Paul and the entire google team for their efforts. I was happy to receive the reward :)

### [Deleted User] (2022-09-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-09-07)

This issue was migrated from crbug.com/chromium/1329298?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pg...@google.com (2024-02-29)

Updating the reporter field to the gmail account of the actual reporter

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059754)*
