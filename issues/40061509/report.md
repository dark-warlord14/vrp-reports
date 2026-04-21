# Incorrect handle of url scheme lead to rce+sbx escape

| Field | Value |
|-------|-------|
| **Issue ID** | [40061509](https://issues.chromium.org/issues/40061509) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2021-1810, CVE-2021-30657, CVE-2022-22616, CVE-2022-32910 |
| **Reporter** | su...@gmail.com |
| **Assignee** | rs...@chromium.org |
| **Created** | 2022-10-28 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

1、Browse poc.html in any version chrome.  

2、git clone <https://github.com/koocola/test_app.git>  

3、open the click\_me button or wait 30s then you will see calculator open

**Problem Description:**  

mailto, news, snews are three external url scheme which will be handled by default[1] without asking user for permission in chrome[1][2].  

It's ok in windows or linux and it can be regarded as a feature. However, it can result in critical security impact in macos.

[1]

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/external_protocol/external_protocol_handler.cc;l=338;drc=50d8da971873550eb909b9c177cf6188e81ff4c3?q=ExternalProtocolHandler::GetBlockState&ss=chromium%2Fchromium%2Fsrc>

[2]  

constexpr const char\* kAllowedSchemes[] = {  

"mailto", "news", "snews",  

};

In macos, most user don’t have an application to handle “news” and “snews” url scheme. And if an application was download from network. Macos system will \*\*automatically\*\* register the application’s url scheme from its info.plist. Turns out if a malicious application with “news” and “snews” url scheme mentioned in there info.plist. Then chrome can use “snews://xxx” or “news://xxx” to open it. Lead to arbitrary code execution.

However, macos has there own security mechanism called gatekeeper to detect user open the application from network directly. If user download an application from network directly. Then the file will be set a flag “com.apple.quarantine”. The first open of an application with this flag will ask user whether they really want to open this application which is from network.

There are two possibly attack situation through my research:

1、Using git or curl(eg..).

If an application is downloaded from git or curl. It will not set the flag “com.apple.quarantine”. It means the application can be opened without any warning message. So bypass the gatekeeper.

So there has a attack situation.

User visit attacker’s website. Attacker could guide user to use git to clone a malicious github or gitlab repo which include a malicious application has “news” and “snews” url scheme mentioned in there info.plist. Once git clone success. the “news” and “snews” url scheme will be registered to mac. Then the website in chrome can use “news” or “snews” url scheme to open the malicious app.

\*\*In this attack situation. The only thing user should do is to git clone a repo. User will not realize this operation has any security impact. And then rce and sbx escape will be achieved.\*\*

2、 With a gatekeeper bypass bug in mac.

Although user may upgrade chrome to the newest version. there operation system may not upgrade to the newest. And the version of user’s operation system information will be sent to attacker by the first get requests user requests the website. If a user’s operation system is lower then 15.1( user don’t upgrade there system after july, 2022). User can use cve-2022-32910(See <https://www.jamf.com/blog/jamf-threat-labs-macos-archive-utility-vulnerability/>) to bypass gatekeeper.

So there has a attack situation.

A user don’t upgrade there operation system from july,2022. A user visit attacker's website. Attacker’s website automatically download a zip file. User curiously click the zip file then macos will automatically unzip it. Then a malicious application will be released to user’s computer and “news”,snews url scheme is registered. After that , the website can open this malicious application without user's permission with the url scheme being registered.

\*\*In this attack situation. The only thing user should do is to unzip a zip file download from chrome.\*\*

**Additional Comments:**  

Report credit: koocola and Guang Gong of 360 Vulnerability Research Institute

\*\*Chrome version: \*\* 106.0.0.0 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [poc1.mp4](attachments/poc1.mp4) (video/mp4, 171.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 766 B)
- [exp.html](attachments/exp.html) (text/plain, 787 B)
- [test.app.zip](attachments/test.app.zip) (application/octet-stream, 74.1 KB)
- [exp_zip.mp4](attachments/exp_zip.mp4) (video/mp4, 242.0 KB)

## Timeline

### su...@gmail.com (2022-10-28)

Steps to reproduce the problem:
1、Browse poc.html in any version chrome.
2、git clone https://github.com/koocola/test_app.git
3、click the click_me button or wait 30s then you will see calculator open



### [Deleted User] (2022-10-28)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-10-28)

Thank you for the detailed report.

As you pointed, this requires a malicious app on the user's disk, which in turn requires the user to run commands on the terminal. That's significant friction for a feasible attack, but I'm also surprised that macOS simply uses the plist from an app that hasn't run yet.

ellyjones, could you please take a look and reassign as appropriate? Thanks.

[Monorail components: UI>Browser>Navigation]

### [Deleted User] (2022-10-28)

[Empty comment from Monorail migration]

### su...@gmail.com (2022-10-28)

Hello，thanks for your assign. Run commands on the command is just one of attack way. 
Another attack way i mentioned just need user click a zip file to unclick it.
Is it eligible for a highly severity level？ Thanks！
I will provide the poc next week.

### su...@gmail.com (2022-10-28)

Another attack way i mentioned just need user click a zip file to unzip it.

### [Deleted User] (2022-10-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-29)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2022-10-31)

Here is the second attack way which need a gatekeeper bug in mac. Is it eligible for a higher security severity leavel?

Although user may upgrade chrome to the newest version. there operation system may not upgrade to the newest. And the version of user’s operation system information will be sent to attacker by the first get requests when user requests the website. If a user’s operation system is lower then 12.5.1( user don’t upgrade there system after july, 2022).  attacker can use CVE-2022-32910 to attack just with one click.


Steps to reproduce the problem:
1、Download the attachment and run a simple python server in a macbook which system version<12.5.1 (July, 2022)
2、Browser exp.html
3、Click the download zip file.
4、Wait around 30s then calculator open.(or you can the click_me button to immediately open the calculator)

And attacker can also discover a 0day gatekeeper bug. There are a lot of Gatekeeper bug in mac nowaday. Such as ( CVE-2022-32910,CVE-2022-22616,CVE-2021-30657,CVE-2021-1810, eg......).

### su...@gmail.com (2022-10-31)

And In the first situation. For example, when the user visit  the attacker's webpage, the attacker can describe the source code leak of the xxx product. The code is on GitHub and can be downloaded by execute the git clone command while the attacker can disguise the github repository as a source code leak repo and put the malicious app in a hidden subfolder, once the user downloads this repository to see the source code. Attacker can execute arbitrary commands.

As far as I known, many people use git clone to download repo.

### el...@chromium.org (2022-10-31)

That's pretty unexpected. Maybe this is more of a macOS bug? I'm not sure either way; -> rsesek@ for Mac security.

### rs...@chromium.org (2022-10-31)

I don’t think exploiting a known and patched vulnerability in an unpatched OS version increases the severity of this report.

Ultimately the issue is that news:// and snews:// are default-allowed despite not having any default protocol handler on macOS, which means LaunchServices will find another app that does. I think simply removing news: and snews: as default-allowed schemes and forcing them to go through the external protocol dialog is a sufficient mitigation here. We should check to see if any OS has a default handler for news: and snews: to see if we should `#if` them out on certain OSes, or if they can be removed entirely.

I checked to see when/why news: and snews: were added to the allowlist, and they date back to initial.commit: https://chromium.googlesource.com/chromium/src/+/09911bf300f1a419907a9412154760efd0b7abc3/chrome/browser/external_protocol_handler.cc#77. I also spelunked the chrome-history repo and mailto:, news:, and snews: were added to the allowlist in b2ba6a56aa87bd721a73b8125fc9a69ee8c77686, though there are references to them in the code all the way back to the first check in of //net in 927d88e41ce979708210b67aae5538f12ea86338.

[Monorail components: -UI>Browser>Navigation UI>Browser>Permissions>Prompts]

### do...@chromium.org (2022-10-31)

news:// and snews:// appear to be usenet protocols.

I'm struggling to understand why this needs mitigation in Chrome, so perhaps I'm missing something here. For instance, mailto is also unrestricted, and the user could download a malicious app that takes over that protocol just as outlined here. Or the default mail app could itself have a known RCE within it. Those situations don't seem any more or less likely than the scenarios outlined in this bug.

And let's say in the future that something like Apple News takes over the news:// protocol by default. Does that change our posture here?

### su...@gmail.com (2022-10-31)

Hello, I think we should do this on macos is because mac **automatically** register the app’s protocol to system without asking user for permission and without run the application and nomatter whereever they are. while in other operation system register the external protocol to the system will need user do some special operation. 
Thus result in user only need to git clone a repo could result in arbitrary code excecution.
I notice safari also has some external-protocol that don’t have the default handled application by default in Mac. But safari check the digital signature to figure out whether this application is from apple.

### rs...@chromium.org (2022-11-01)

>  For instance, mailto is also unrestricted, and the user could download a malicious app that takes over that protocol just as outlined here.

An app cannot take over an existing protocol handler without either direct user selection or already being executed. The system-installed Apple Mail will be the default for mailto:, but there is no default for news: or snews:.

>  Or the default mail app could itself have a known RCE within it. 

While possible, I think this is not very likely with mailto:.

> Those situations don't seem any more or less likely than the scenarios outlined in this bug.

I agree that this is not a super likely scenario, but the way macOS auto-discovers applications and associates handlers does make this at least Sev-Low IMO.

I think a different question would be: why have *any* default-allowed schemes and instead just always show the external protocol handler dialog?

### do...@chromium.org (2022-11-01)

> An app cannot take over an existing protocol handler without either direct user selection or already being executed. The system-installed Apple Mail will be the default for mailto:, but there is no default for news: or snews:.

Hmm, I see. I'm still struggling to square "user downloaded malicious executable code onto their machine, then clicked a specific protocol link that ended up running that malicious code" as being a particularly viable threat vector.

I think I can accept this being Sev-Low, based on "Low severity vulnerabilities are usually bugs that would normally be a higher severity, but which have extreme mitigating factors or highly limited scope." If you're comfortable, I'll make that change and drop this to a P2.

> I think a different question would be: why have *any* default-allowed schemes and instead just always show the external protocol handler dialog?

This well predates all of us, so it's hard to tell what the underlying reasons are. I can see why mailto: is default-allowed. I can only imagine that the same reason applied to the Usenet protocols at the time this was first put together.

### rs...@chromium.org (2022-11-02)

+1 to Sev-Low Pri-2

> This well predates all of us, so it's hard to tell what the underlying reasons are. I can see why mailto: is default-allowed. I can only imagine that the same reason applied to the Usenet protocols at the time this was first put together.

Yeah, the rationale is definitely lost to time. IIRC, the original external protocol dialog did not have the option for remembering the user’s choice, either. Personally I would just remove the concept of default-allowed schemes. Maybe just conditionalize that behind a Finch flag to deprecate it and make sure nothing breaks?

### do...@chromium.org (2022-11-02)

Adjusting priority and severity per the last couple of comments, thanks.

> Yeah, the rationale is definitely lost to time. IIRC, the original external protocol dialog did not have the option for remembering the user’s choice, either. Personally I would just remove the concept of default-allowed schemes. Maybe just conditionalize that behind a Finch flag to deprecate it and make sure nothing breaks?

I suspect removing the mailto default allow is going to cause some grief due to the pervasiveness of mailto and since the choice remembering is tied to the origin + app pair. I feel less strongly about news/snews, but since we don't have a good understanding of why these were default-allowed in the first place, I worry we'll have something that comes up that causes us to have to reverse the stance.

### su...@gmail.com (2022-11-02)

[Comment Deleted]

### su...@gmail.com (2022-11-02)

[Comment Deleted]

### su...@gmail.com (2022-11-03)

[Comment Deleted]

### su...@gmail.com (2022-11-03)

[Comment Deleted]

### su...@gmail.com (2022-11-11)

[Comment Deleted]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-06-20)

[Empty comment from Monorail migration]

### su...@gmail.com (2023-06-22)

deleted

### am...@chromium.org (2023-06-27)

hello OP, thanks for this additional information and the information you provided in https://crbug.com/chromium/1456315. 
In https://crbug.com/chromium/1456315 you conveyed that you have reported the Gatekeeper bypass issue to Apple. Can you please provide the Radar case number from that report here so we can check in with Apple regarding the status? This will be important when this issue is resolved, to ensure we do not publicly disclose and n-day Apple in the process.   

While the basis for this to occur provided by the MacOS bug and is not an issue in Chrome, the demonstration and impact of RCE to allow for a sandbox escape through Chrome which is enabled by Chrome, based on the way that Chrome handles the URL scheme. 

I concur this issue here -- alone -- would be a low-severity issue; however, as what is achievable through the MacOS gatekeeper bypass and demonstrated in the POC / exploit in https://crbug.com/chromium/1456315, I believe it is warranted to adjust this issue to Medium severity. We should raise the priority of the proposed mitigation in https://crbug.com/chromium/1379358#c18, especially since we are unsure as to the status of Apple's fix for the gatekeeper bypass and we should work to ensure our users can be protected from this potential exploitation scenario sooner than later. 

Please let me know if there are any issues or dissenting thoughts here. 

OP, thanks for reaching out and to provide context and information on these issues here. And thank you for your work here to help better demonstrate the potential impact and exploitability of this issue. 

### su...@gmail.com (2023-06-28)

deleted

### [Deleted User] (2023-06-28)

dominickn: Uh oh! This issue still open and hasn't been updated in the last 238 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-06-28)

hi there -- re: https://crbug.com/chromium/1379358#c30, we aren't negating this as eligible for a Chrome VRP reward. Once this issue is resolved, this issue will be assessed for a Chrome VRP reward. 
The general Chrome VRP reward eligibility is different and separate than the Chrome Full Chain Exploit Bonus. 

We still very much care about user security, which is why we care about full chains in other platforms and will do everything we can to support a quick resolution and mitigation of a particular issue and reward that through the Chrome VRP, regardless of the platform as mentioned in the Q&A. But those bugs are eligible for the standard VRP reward amounts. The Q&A applies to the Chrome VRP, however, the Full Chain Exploit Bonus is not the general Chrome VRP. This is a specific, time-bound opportunity with specific requirements and eligibility criteria. This is why its has it's own Rules and Conditions section specific to and within the Full Chain Exploit Bonus section. 

We have different goals we seek to achieve through this bonus opportunity and we are only interested in a Chrome full chain for this bonus opportunity, in which each bug in the chain is a vulnerability in Chrome code that results in sandbox escape and RCE / attacker control demonstrated outside the sandbox via vulnerabilities in Chrome. 



### su...@gmail.com (2023-06-29)

Get it, thanks for the reply!

### su...@gmail.com (2023-07-11)

Friendly ping, is there any update? Thanks!

### rs...@chromium.org (2023-07-12)

I think we should move news/snews off default-allowed and make them like any other external protocol, and put that behind a Finch kill-switch.

WIP: https://chromium-review.googlesource.com/c/chromium/src/+/4678089

### do...@chromium.org (2023-07-12)

Thanks for picking this up Robert - I had just about freed up some time to look at this, but I really appreciate you taking it on. :)

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6e4fc226f4699296ea833520771db9b61ed9a24e

commit 6e4fc226f4699296ea833520771db9b61ed9a24e
Author: Robert Sesek <rsesek@chromium.org>
Date: Mon Jul 17 14:01:59 2023

Add the PromptForExternalNewsSchemes feature

This enabled-by-default feature changes the external protocol handling
to not treat news: and snews: schemes as default-allowed. If a handler
is present, the user will be prompted to open the application, as with
other arbitrary app schemes. With this feature enabled, only mailto:
remains default-allowed.

Bug: 1379358
Change-Id: Ic136e19728c69599ccbba9172679388cbcb855c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4678089
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Ravjit Uppal <ravjit@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1171162}

[modify] https://crrev.com/6e4fc226f4699296ea833520771db9b61ed9a24e/chrome/browser/external_protocol/external_protocol_handler.h
[modify] https://crrev.com/6e4fc226f4699296ea833520771db9b61ed9a24e/chrome/browser/external_protocol/external_protocol_handler.cc
[modify] https://crrev.com/6e4fc226f4699296ea833520771db9b61ed9a24e/chrome/browser/external_protocol/external_protocol_handler_unittest.cc
[modify] https://crrev.com/6e4fc226f4699296ea833520771db9b61ed9a24e/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/6e4fc226f4699296ea833520771db9b61ed9a24e/tools/metrics/histograms/metadata/permissions/histograms.xml


### rs...@chromium.org (2023-08-11)

Update: because this change has compat risk, it is rolling out as part of M117. So far metrics look fine, but we will need to wait for stable data.

### rs...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-09-19)

Data from M117 stable look clear. Usage of news/snews is 0.00%.

### [Deleted User] (2023-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Thank you for the report. The Chrome VRP Panel has decided to award you $1,000 for this report. We do appreciate that you allowed us to make a security relevant change in Chrome, however, the main vector of exploitation of this issue requires exploiting a known and patched vulnerability in MacOS. As such, the reward is reflective of the specific issue and impact in Chrome at the time of this report. Thank you for your efforts and reporting this issue to us. 

### su...@gmail.com (2023-09-29)

Hello, This bug don't need a known and patched vulnerability in MacOS at the time of this report. The 0 day gatekeeper bypass bug I discover in https://bugs.chromium.org/p/chromium/issues/detail?id=1456315  exists more than 2 years. Apple hasn't fixed it until now. Thus this chain mentioned in https://bugs.chromium.org/p/chromium/issues/detail?id=1456315 is still exploitable at the time of this report. 
***And I update the information before the bug was fixed. ***

Is there something wrong for the following rules?

Q: What about full-chain exploits on platforms other than Chrome OS?
A: We are interested in full-chain exploits against Chrome running on other platforms. For example and referring to the table above, a high-quality full-chain exploit that escapes the sandbox on non-Chrome OS platforms would likely receive at least $40,000 ($30,000 for the sandbox escape portion, $10,000 for the code execution in the renderer).***** In addition, any other bugs in the operating system that can manifest through Chrome are likely to be rewarded as well.****

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-10-05)

Marking Restrict-View-SecurityEmbargo to keep this from being opened automatically and disclosing unfixed Gatekeeper bugs. Adding a NextAction date in 6 months so we know when to review if we can open this up.

### am...@chromium.org (2023-10-05)

Thanks for reaching out. I'm sorry that you are disappointed by this reward amount. There are a number of comments from both security / VRP and the security engineers who owned and resolved this issue, so I feel like we have fully communicated our assessment of this issue from both a severity and impact as well as VRP standpoints. We did review your email and have once again reviewed this issue and have decided the reward amount is sufficient for the Chrome issue presented here. 

>>>Q: What about full-chain exploits on platforms other than Chrome OS?
A: We are interested in full-chain exploits against Chrome running on other platforms...

Once again, it is important to note that we are interested in full-chain exploits against Chrome running on other platforms, yes. This means that the chains should predominantly consist of vulnerabilities in Chrome that can be exploited to result of a Chrome sandbox escape and code execution in another platform/OS. In this case, however, the predominant vulnerability here is not an issue in or having to do with Chrome, but the Gatekeeper bypass bug in MacOS. This is a bug inherent to MacOS and has nothing to do with Chrome. Chrome was a very small part of this chain, and the impact of the Chrome url scheme has been thoroughly assessed here to be of very low severity and impact on its own. 

We consider this issued fully assessed and the reward decision to be final at this time. 

### pg...@google.com (2023-10-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c48764eed5f8a3b0ef3a4513d67aac2db5c05efb

commit c48764eed5f8a3b0ef3a4513d67aac2db5c05efb
Author: Robert Sesek <rsesek@chromium.org>
Date: Wed Oct 25 13:28:23 2023

Remove the PromptForExternalNewsSchemes feature and do associated cleanup

The news and snews schemes are now treated as normal external protocols
are no longer are default-allowed to open.

The feature was a kill-switch that did not need to be used. Remove it
and the code it was guarding.

Bug: 1379358
Change-Id: I20d41e88b3cfb4301bed188e8047357715a88052
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4968321
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1214804}

[modify] https://crrev.com/c48764eed5f8a3b0ef3a4513d67aac2db5c05efb/chrome/browser/external_protocol/external_protocol_handler.h
[modify] https://crrev.com/c48764eed5f8a3b0ef3a4513d67aac2db5c05efb/chrome/browser/external_protocol/external_protocol_handler.cc
[modify] https://crrev.com/c48764eed5f8a3b0ef3a4513d67aac2db5c05efb/chrome/browser/external_protocol/external_protocol_handler_unittest.cc


### pg...@google.com (2023-11-07)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1379358?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1456315]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### pe...@google.com (2024-04-04)

The NextAction date has arrived: 2024-04-04 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### dr...@chromium.org (2024-06-25)

Per <https://crbug.com/40066093#comment19>, all Gatekeeper bypasses here have been fixed by Apple. Removing security embargo.

### pe...@google.com (2024-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### me...@google.com (2024-10-31)

A variant of this bug was previously reported by [bug 40054004](https://issues.chromium.org/issues/40054004) (November 2020) and [bug 40059768](https://issues.chromium.org/issues/40059768) (May 2022). Both were triaged as low severity, but this issue had a more complete proof of concept.

+cc amyressler: I merged the two low severity bugs into this bug. Wanted to let you know in case this has vrp implications, thanks.

### de...@gmail.com (2024-12-30)

hello，can i get the vrp also？
---- Replied Message ----
From buganizer-system@google.com Date 11/01/2024 06:26 To b-system+191468661@google.com Cc dearmyload@gmail.com Subject Re: Issue 40061509: Incorrect handle of url scheme lead to rce+sbx escape 
Replying to this email means your email address will be shared with the team that works on this product.
https://issues.chromium.org/issues/40061509
Changed
me...@google.com added comment #59:
A variant of this bug was previously reported by bug 40054004 (November 2020) and bug 40059768 (May 2022). Both were triaged as low severity, but this issue had a more complete proof of concept.
+cc amyressler: I merged the two low severity bugs into this bug. Wanted to let you know in case this has vrp implications, thanks.
_______________________________
Reference Info: 40061509 Incorrect handle of url scheme lead to rce+sbx escape
component: Public Trackers > 1362134 > Chromium > UI > Browser > Permissions > Prompts
status: Fixed
reporter: su...@gmail.com
assignee: rs...@chromium.org
cc: am...@chromium.org, do...@chromium.org, dr...@chromium.org, and 4 more
collaborators: se...@chromium.org
type: Vulnerability
access level: Default access
priority: P1
severity: S2
duplicate: 40066093, 40059768, 40054004
found in: 106
hotlist: CVE_description-submitted, external_security_report, reward-inprocess, Security_Impact-Extended
retention: Component default
Chromium Labels: Via-Wizard-Security, FoundIn-106, allpublic, allpublic
Component Ancestor Tags: UI, UI>Browser, UI>Browser>Permissions, UI>Browser>Permissions>Prompts
Component Tags: UI>Browser>Permissions>Prompts
CVE: 2023-7012
Milestone: 117
OS: Mac
Security_Release: 0-M117
vrp-reward: 1000
Generated by Google IssueTracker notification system.
You're receiving this email because you are subscribed to updates on Google IssueTracker issue 40061509 where you have the roles: starred
Unsubscribe from this issue.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061509)*
