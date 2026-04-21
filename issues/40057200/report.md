# Security: Possible to see the user's system environment variables like secrets, tokens or keys

| Field | Value |
|-------|-------|
| **Issue ID** | [40057200](https://issues.chromium.org/issues/40057200) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2021-09-07 |
| **Bounty** | $10,000.00 |

## Description

New issue based on my comment <https://bugs.chromium.org/p/chromium/issues/detail?id=1243802#c7> on Sun, Aug 29, 2021, 11:42 PM GMT+2

**VULNERABILITY DETAILS**  

By holding for 2 seconds ENTER button on the website, the hacker can steal the user's system environment variables. The user can store secrets like tokens, passwords, keys to some services (ex. Microsoft Azure or Twilio(SendGrid) or many more)

**VERSION**  

Chrome Version: 92.0.4515.159 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows

**REPRODUCTION CASE**  

Video PoC: <https://www.youtube.com/watch?v=q7OIEWtalg8>  

Code PoC: <https://pulik.io/msexploit/env> (need to be https) or in attachments

1. Open website
2. Hold Enter for 2 seconds
3. On windows OS, You will see some system environment variables

MORE INFO  

The problem persists in File System API in method showSaveFilePicker()

For instance, we can read a user's username on Windows.

Code PoC:  

let testA = await window.showSaveFilePicker({suggestedName: '%USERNAME%'})

When we check variable testA we can get:  

FileSystemFileHandle {kind: "file", name: "Maciej-pc"}

The user's username on Windows is "Maciej-pc".

I discovered that many popular services/applications recommend putting secrets in environments variables.

1. Microsoft Azure  
   
   <https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch>  
   
   "We make an effort to mask secrets from appearing in Azure Pipelines output, but you still need to take precautions.  
   
   Never echo secrets as output. Some operating systems log command line arguments. Never pass secrets on the command line.  
   
   INSTEAD, WE SUGGEST THAT YOU MAP YOUR SECRETS INTO ENVIRONMENT VARIABLES."
2. Twilio  
   
   <https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html>  
   
   "There are some things we just shouldn’t share with our code.  
   
   These are often configuration values that depend on the environment such as debugging flags or ACCESS TOKENS for APIs like Twilio.  
   
   Environment variables are a good solution and they are easy to consume in most languages."
3. python-binance library (Binance is the most popular cryptocurrency exchange)  
   
   <https://algotrading101.com/learn/binance-python-api-guide/>  
   
   264.000+ article views  
   
   "We recommend storing your API keys as environment variables. That way, if you upload your code to GitHub, or send it to someone, you don’t run at the risk of revealing your credentials."

Google search results for the phrase '"environment variables" token' are 1.350.000 results.

So the attacker can create a list of popular environment variables that are secrets:  

suggestedName:  `%username%@ //@ only to split variables %USERDOMAIN%@ %SESSIONNAME%@ %COMPUTERNAME%@ %PROCESSOR_ARCHITECTURE%@ %PROCESSOR_IDENTIFIER%@ %KEY_VAULT_URL%@ %SECRET_NAME%@ %SECRET_VERSION%@ %AZURE_TENANT_ID%@ %AZURE_CLIENT_ID%@ %AZURE_CLIENT_SECRET%@ %TWILIO_ACCOUNT_SID%@ %TWILIO_AUTH_TOKEN% f.f //filename`   

To gather secrets from users visited his website.

SOLUTION  

'%' character should be blocked.

## Attachments

- [env.html](attachments/env.html) (text/plain, 4.0 KB)
- [code.png](attachments/code.png) (image/png, 56.6 KB)
- [RightNowPublicVersion.png](attachments/RightNowPublicVersion.png) (image/png, 18.6 KB)
- [AfterMyFix.png](attachments/AfterMyFix.png) (image/png, 15.6 KB)

## Timeline

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-07)

Thanks for the cunning bug maciekpul@! :) (and also the really clear report and video).

Discussed with cthomp@ and we think this sounds like users could indeed be persuaded to hold down Enter in this fashion.

Severity:
- Ability to read local files is Critical, and I think stealing environment variables would count the same.
- The need to coerce the user into holding down Enter drops the severity by a notch.
- So ==> high.

FoundIn:
- I haven't reproduced this (I don't have a Windows machine or VM handy), but the video is very clear. I'm going to take the reporter at their word that this works in M92.


[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

mek: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-06)

mek: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-07)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2021-11-08)


adetaylor@ Thank you so much for your words :) I am pleased that you explained the severity level of the bug.

I would like to help more, so I downloaded the chromium source and fixed the bug by myself :)
Probably in not the best way, at least maybe it will help somehow.

Solution:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/file_system_access/file_system_chooser.cc;l=238?q=ResolveSuggestedNameExtension&ss=chromium%2Fchromium%2Fsrc

Here you can add these lines of code:

  //On Windows, an environment variable is retrieved by placing a % sign before and after it.
  //ex. %USERNAME% will be replaced with "maciej-pc".
  //By using this technique, the attacker could get users' secrets stored as an environment variable.
  //So replace any '%' character with '_' in suggestedName of a filename
  std::string name = suggested_name.AsUTF8Unsafe();
  base::ReplaceChars(name, "%", "_", &name);
  suggested_name = base::FilePath::FromUTF8Unsafe(name);

Screenshot: Code.png

I have tested it locally on version Chromium 98.0.4693.0 (Developer Build) (64-bit), and it fixed the problem.

Screenshot: RightNowPublicVersion.png (before fix/now)
Screenshot: AfterMyFix.png (after fix)


There are two more ways to fix it:

1.
There is IsFilenameLegal(...) we could extend IllegalCharcters with '%', but not sure what consequences will it brings elsewhere
https://source.chromium.org/chromium/chromium/src/+/main:base/i18n/file_util_icu.cc;l=123?q=IsFilenameLegal&ss=chromium%2Fchromium%2Fsrc

2.
We could leave '%' as a legal character, and before releasing it to the website, double-check if the filename is the same. However, I do not think anyone needs '%' characters in the filename.



### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### pw...@chromium.org (2021-12-06)

Let's remove '%' from the list of legal characters everywhere, for predictability. We can always add it back later, if developers present us with a good use case.

Let's land a fix and then do a PSA to blink-dev.

### as...@chromium.org (2021-12-10)

https://crrev.com/c/3324687 just landed, which should fix the environment variable issue

### as...@chromium.org (2021-12-10)

Marking fixed as per guidelines, since this is fixed on main. Not sure if we want to back-merge this? +adetaylor for thoughts

### [Deleted User] (2021-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-12-10)

Sheriffbot will add suitable merge requests today or tomorrow, thanks for the fix!

### [Deleted User] (2021-12-10)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M96. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M97. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-10)

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-10)

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2021-12-10)

1. Why does your merge fit within the merge criteria for these milestones?

High severity security issue

2. What changes specifically would you like to merge? Please link to Gerrit.

https://crrev.com/c/3324687

3. Have the changes been released and tested on canary?

Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Yes. See repro described in the issue description. %USERNAME% should be sanitized to _USERNAME_ rather than exposing your system's username, for example

### ad...@google.com (2021-12-13)

Fix landed at 950335 which is just before M98 branch point. Approving merge to M96 (branch 4664) and M97 (branch 4692) - please go ahead and merge.

### pb...@google.com (2021-12-13)

Your change has been approved for M97 branch,please go ahead and merge the CL's to M97 branch:4692 manually asap so that they would be part of this Wednesday's M97 Beta release.

### as...@chromium.org (2021-12-14)

Since I forgot to tag the initial CL (https://crrev.com/c/3324687) with this bug, the cherry-picks were also not tagged. This change has since been merged to M97 and M96

M97: https://crrev.com/c/3334100
M96: https://crrev.com/c/3335097

Sorry about that!

### pb...@google.com (2021-12-14)

The change has been merged as part of https://chromium-review.googlesource.com/c/chromium/src/+/3334100, the git watcher didn't update the labels since there wasn't no mention of this bug in cherry pick.

### sr...@google.com (2021-12-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

Congratulations, Maciej! The VRP Panel has decided to award you $10,000 for this report. Thank you for your report and great work! 

### ma...@gmail.com (2022-01-06)

Wow, thank you so much! I am super happy :)

I think that the issue thread shouldn't be public before https://crbug.com/chromium/1243802 got fixed.

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### ma...@gmail.com (2022-01-10)

amyressler@ 
I have a small question. I see that Chrome version 97 includes the fix.

Here is the news about Google Chrome 97 version https://chromereleases.googleblog.com/2022/01/stable-channel-update-for-desktop.html . The log shows the fix. However, the security bug is not listed.

Will the bug get a CVE number?

Thanks :)

### ad...@chromium.org (2022-01-10)

+amyressler@

### am...@chromium.org (2022-01-10)

Hi, Maciej, thanks for reaching out about this-- it looks fix merge for M97 didn't attribute this bug report to it, so it wasn't picked up by our tooling for release notes. I'll need to manually update the release notes and allocate a CVE ID for this bug. I'll try and get this done by EOW and will update here when it is complete. Thanks again! 

### ma...@gmail.com (2022-01-12)

No worries, thanks :) 

### am...@chromium.org (2022-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-22)

Hi, Maciej, CVE added and acknowledgements added in the release notes for the appropriate stable channel release of M97: https://chromereleases.googleblog.com/2022/01/stable-channel-update-for-desktop.html

### ma...@gmail.com (2022-01-22)

@amyressler

Amy, thank you so much! :)

### [Deleted User] (2022-03-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-02)

release notes updated here: https://chromereleases.googleblog.com/2022/01/stable-channel-update-for-desktop.html

### pg...@google.com (2023-01-02)

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1247389?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057200)*
