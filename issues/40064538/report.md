# Security: Chrome German capital sharp s "ẞ"

| Field | Value |
|-------|-------|
| **Issue ID** | [40064538](https://issues.chromium.org/issues/40064538) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Network, Internals>Network, UI>Security (Use Subcomponent)>UrlFormatting |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | he...@googlemail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2023-05-12 |
| **Bounty** | $2,000.00 |

## Description

Good evening together,

For some time now Chrome(OS) is obviously supporting domain names, which are containing the German letter "ß" (aka Eszett aka Scharfes S, English sharp s). The letter "ß" is no longer translated to "ss".

Really great, as the owner of such a domain! It was a long lasting time since 2008. ;o)

Unfortunately, there is a security issue in this regard.

In German, for a few years now you can capitalize the "ß" to "ẞ": https://de.wikipedia.org/wiki/Gro%C3%9Fes_%C3%9F
Also, it is not uncommon to write domainnames capitalized.

Thus, both the small and the capital "ß" are the same.

Exactly that is the crux of the matter: Whilst "ß" is correctly kept when opening an URL, the capital sharp s "ẞ" is still translated to "ss", thus leading to a wrong domain, which the user has not requested.

That behaviour could be used for bad things, as publicly known, like phishing and/or spreading wrong informations about something on the corresponding ss-domain (like WWW[.]DUMMY-ẞANK[.]DE or an ss-domain, which the ß-owner does not have).

You may think "who's using ß-domains ... absolutely seldom!" Probably yes, but no: In my sight the reason is (was) cleary based on the fact that major browers, like Chrome, were not supporting such domains properly in my experiences. Due to the last change the wind will change.

Hint regarding spoofing: In German a "ß" logically CANNOT be
• at the beginning of a WORD ("ßommer", "warmer-ßommer")
and/or
• only at the second position from the beginning (ißt)
• and/or second last postion end of a word (buße)
• both when the first/last letter is an Umlaut (a/e/i/o/u) or the and a "t" (like "paßt"), the remaining positions: everywhere inbetween. 
• That does not hinder people from registering valid domains like "ßßßßßßß"
• I am wondering whether ß-domains are only valid in .DE context or not ... I am suspecting yes. => fußball[.].com should be invalid

I do not know where the cause is lying, whether in a common String function of the used programming language or within Chrome-code itself. Insofer other areas in Chrome/OS/Android/Google/Web might be also affected. Or not.

Thank you in advance for checking and fixing.

Enjoy your weekend.

With best regards


P.S.:
In connection with the support of "ß"-domains, my ticket from 03/2019, namely https://crbug.com/chromium/129558305, is sadly quite acute now, as it is actually really inconsistent. :( Checked again today. :/

## Attachments

- [german-sharp-s-in-address-bar.png](attachments/german-sharp-s-in-address-bar.png) (image/png, 195.2 KB)

## Timeline

### [Deleted User] (2023-05-12)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-05-12)

Thanks for the report. I think I was able to reproduce this on Linux and on Windows. If you type it in, the omnibox will change "ẞ" to "ss". The URL also gets rewritten if you click on a link. For example:

```
$ echo http://ßẞ
http://ßẞ
```

If you run that in your terminal, and click the link, Chrome will navigate to "http://ßss".

I'll give this a severity of medium for now because it seems to be URL spoofing and assign to meacer@ for further confirmation.



[Monorail components: Blink>Network Internals>Network UI>Security>UrlFormatting]

### me...@chromium.org (2023-05-13)

Thanks for the report! There is an argument to be made here to normalize capital sharp ẞ to lowercase. http://www.unicode.org/L2/L2007/07108-n3227.pdf seems to agree:
```
Asis the case with all pairs of uppercase-/lowercase pairs, capital $ and lowercase ß must be equivalent. Following the IDN-rules, the lowercase ß is equivalent to the string “ss”. That implies that a
capital $ in a domain-name is equivalent to the string “ss”.
```

(The second sentence is no longer valid in IDNA 2008 but the document is from 2007)

That said, both Safari and Firefox also convert http://ßẞ to http://ßss. If we were to make any changes, we should keep compatibility with other browsers in mind.

sffc@, curious if you have any thoughts?

### ad...@google.com (2023-05-13)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-05-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-27)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2023-06-05)

(security secondary shepherd) I reproduced on M114. Adding FoundIn label.

### [Deleted User] (2023-06-05)

[Empty comment from Monorail migration]

### sf...@chromium.org (2023-06-05)

Copying Markus to advise on IDNA. Also Robin who has been working on the Unicode specs for security.

### ms...@google.com (2023-06-06)

This data comes from Unicode (UTS #46), and has been like this from the beginning, but has been masked while "transitional mappings" were used for ß and a few other characters.
I will report it upstream.
The next time that the Unicode Technical Committee meets to make formal decisions is in late July.
If Unicode decides to change this mapping, then it could go into Unicode 15.1 in September, and from there eventually into implementations.
I expect that there will be some discussion about implications for backward compatibility.

### [Deleted User] (2023-06-06)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-10)

meacer: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@google.com (2023-06-12)

I suggest we lower the priority. This issue has been around for any user of nontransitional processing in UTS #46 since about 2010, and if Unicode agrees to make a change, it won't go into products before 2023-nov or so.

### he...@googlemail.com (2023-06-12)

Wherby the sharp-s was introduced in Chrome just a few months ago, thus in my sight the issue is not existing "in-the-wild" since about 2010, but 2022/2023.

Before, it was quasi irrelevant, but due to the implementation of the lowercase ß it got relevant.

Just for putting into scale.

### vi...@google.com (2023-07-04)

As per comments https://crbug.com/chromium/1445238#c3 and https://crbug.com/chromium/1445238#c10, this issue requires industry alignment before implementation. I suggest making status as "ExternalDependency" and lowering the priority in our queue until this is resolved and implementation can start.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### vi...@google.com (2023-09-08)

[Empty comment from Monorail migration]

### ms...@google.com (2023-09-08)

The Unicode 15.1 version of UTS #46, will map U+1E9E capital sharp s to U+00DF small sharp s in nontransitional processing (instead of to ss which remains in transitional processing).
Unicode 15.1 is scheduled to be released next Tuesday, sep12.
This is going into ICU 74, to be released at the end of October.
ICU 74 will go into Chromium probably in November.
I don't know the schedule for when Safari and Firefox upgrade to ICU 74. Could be similar.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-15)

[security shepherd] Yes, we can't make changes like this unilaterally as this would be going against industry standards and could cause breakages for Chrome users. I concur with https://crbug.com/chromium/1445238#c15 in updating this issue as in External Dependency status. Thank you for all hte information about the next ICU updates here. 
Adding a next action of 30 November to trigger a follow-up on this issue. 

### ms...@google.com (2023-11-15)

Industry alignment is in place via the change in Unicode 15.1. See my https://crbug.com/chromium/1445238#c18.

### [Deleted User] (2023-11-15)

[Empty comment from Monorail migration]

### me...@google.com (2023-11-30)

mscherer: Thank you for following up on this!

The current ICU version in HEAD is 73: https://source.chromium.org/chromium/chromium/src/+/main:third_party/icu/version.json

Can we bumpt it to 74?

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1445238?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Network, Internals>Network, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

### ms...@google.com (2024-08-22)

Why is this still open? Has Chromium not yet moved to ICU 74 which was released 9.5 months ago?

### pe...@google.com (2024-10-26)

meacer: Uh oh! This issue still open and hasn't been updated in the last 532 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### me...@google.com (2024-11-01)

mscherer: Thanks for the heads up!

This now navigates to [http://ßß](http://%C3%9F%C3%9F) in Chrome, as expected:

```
$ echo http://ßẞ
http://ßẞ

```

Marking as fixed.

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower-impact security UI spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Congratulations Andy! Thank you for your efforts and reporting this issue to us -- nice work!

### pe...@google.com (2025-02-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064538)*
