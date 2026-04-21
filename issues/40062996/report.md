# Security: Bypass Issue 1385343 Extension with <all_urls> permission can read arbitrary local files although (Allow access to file URLs) is disabled

| Field | Value |
|-------|-------|
| **Issue ID** | [40062996](https://issues.chromium.org/issues/40062996) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | tj...@chromium.org |
| **Created** | 2023-02-09 |
| **Bounty** | $5,000.00 |

## Description

# **VULNERABILITY DETAILS** :

This Issue is a (Bypass <https://crbug.com/chromium/1385343>)

after fixing this <https://crbug.com/chromium/1385343> in 10-JAN-2023 ,and after Confirming from my side that this issue is fixed in (Chrome Canary Version 111.0.5529.0 official Build (64bit)) at Windows 10 Machine , I've found another Way to Bypass this as there is a miss-Checking for Extension Permission after getting updated by Chrome Browser Updater,so if a Normal User was installing one of affected versions of chrome before 10-JAN FIX , the update will not protect him and attacker will be able to Get All User Files Although (Allow access to file URLs) is disabled, the full details and Root Cause Analysis below.

An extension with the <all\_urls> permission can read any file on the file system and send it's content to a remote host, using chrome.tabs.captureVisibleTab although extension (Allow access to file URLs) is disabled.

# **VERSION** :-

Exploit tested with the following properties:

Google Chrome Version:

- Version 111.0.5563.19 (Official Build) dev (64-bit)

Operating System:

- Linux (Ubuntu 22.04.1 LTS)  
  
  **-------------------------** ---  
  
  Google Chrome Version:
- Version 110.0.5481.77 (Official Build) Beta (64-bit)
- Version 111.0.5563.8 (Official Build) dev (64-bit)

Operating System:

- Windows 10 Enterprise 2H1 Build (19043.1826)  
  
  **-------------------------** ----  
  
  Bisect:

---

# <https://chromium.googlesource.com/chromium/src/+/a5e2bf3eaeea3a0f7ba9af687f1ee99014aa26fe> refs/heads/main@{#1090642} Change-Id:I2de208b5e80b715515f613c55bf50b362913d1fa

## **REPRODUCTION CASE** :-

# \*\*For Good Repro as Shown in Video POCs follow the following steps Exactly, Any Change in Steps May Break and Fail the debugging process\*\*

# Steps on Linux Machine(Ubuntu 22.04.1 LTS)

# Before Going To the steps Below :

## Basline Step:

Open Terminal and run this command

`nc -vlp 8888`

to see the base64 data sent to attacker , why this command?! Because sometimes Diverting output to consol.log print blank so this is important to see the data leaked as base64 image also alert with data will be poped up.

# Part 1 :

1-Remove Any Exsisting Chrome Dev Version using command

`sudo apt --purge remove google-chrome-unstable`

2-Download Vulnerable Version to Prev Attack on Main Bug <https://crbug.com/chromium/1385343> using command  

`wget http://dl.google.com/linux/deb/pool/main/g/google-chrome-unstable/google-chrome-unstable_110.0.5478.4-1_amd64.deb`

3- Install the Old version Deb Package using Command

`sudo apt-get install -f ./google-chrome-unstable_110.0.5478.4-1_amd64.deb`

4- Open Chrome DEV using command

`google-chrome-unstable`

5-Repro the main Bug <https://crbug.com/chromium/1385343> or Simply

A- Download the extension files in one Folder  

B- Go to chrome://extensions/ and Enable Developer mode  

C- Load Unpacked and select Extension folder created at (A)  

D- Go to Extension Details Page and Disable Extension  

E- Remove "Allow access to file URLs"

Now Heading up to the second part.

\*\*VIP NOTE\*\*  

\*\*(Before going to [Part 2] make sure "Allow access to file URLs" is Disabled and "Extension also is Disabled")\*\*

# Part 2 :

1- Normally Update the (Chrome DEV) App using the following Commands

A) `sudo apt update`  

B) `sudo apt --only-upgrade install google-chrome-unstable`

2- Go to chrome://extensions/

3- Go to Extension Details Page and

A)-Just Only Enable Extension & < Don't > toggle "Allow access to file URLs" because this will break the root cause and this go thru the check of Reload Extension Applied by the main Bug fix.

4- you will see base64 image file was sent to netcat terminal console at Baseline step above.

5- You can take this base64 and decode it will be /etc/passwd contents as jpeg image .

## ======================= What's Go Wrong:

-Local files Still can be exfiltrated By the Extension Although (Allow access to file URLs) not activated After Browser Update.  

-Extension with <all\_urls> permission and without enabling (Allow access to file URLs) can Navigate file:/// scheme using chrome.tabs.create method.

## What's Expected:

-if the extension with <all\_urls> permission and without enabling (Allow access to file URLs) we should do the following

1-Check permissions while using (chrome.tabs.create) method ,and not allow (Exclude) file:/// scheme from being opened by the extension.

2-Checking Permissions also like (1) and if the extension need to use (tabs.captureVisibleTab) and not to allow file:/// scheme files from being captured.

# From there it is easy to create a command and control server( here we can add netcat listner to see using `nc -vlp 8888` at linux terminal) and By the Above Way an attacker could navigate through the file system and fetch arbitrary local files to His C&C Server.

## Repro in Windows Enviroment:

Similar to Above but instead of Command line in linux Go to Help>>About Chrome to Check for new Updates in Part2  

and for Getting Older Versions Go to Googlers trusted source to download Google DEV/Canary

Test in Windows I've Used the following Properties:  

Old Version: Chrome V 110.5478.4(Official Build) DEV (64-bit)  

Upgraded to Version 111.0.5563.8 (Official Build) dev (64-bit)

---

Old Version: Older Version Before FIX 10 JAN

Upgraded to Version:Version 110.0.5481.77 (Official Build) Beta (64-bit)

## ======================= Root Cause Analysis:

Main <https://crbug.com/chromium/1385343> was fixed by this CL  

<https://chromium.googlesource.com/chromium/src/+/a5e2bf3eaeea3a0f7ba9af687f1ee99014aa26fe>

[Extensions] Reload extension on changing fileAccess even if disabled

Changes to file access settings for an extension were not being applied  

correctly for extensions which were disabled while the setting was  

changed.

This CL forces a reload of an extension when changing the file  

access setting even if it is disabled, to ensure it is reinitialized  

correctly. Also adds tests to better cover this case.

# This Issue Root Cause:

Browser Updater and FirstRun Overwrite BrowserState "AllowFileAccess Permissions" for Extensions after Being Updated.

Reload to update browser state. Only bother if the value AllowFileAccess changed even if enabled/disabled extension.

# Mitigation/FIX:

After Chrome Updater install Updates we should do:  

1-Check Extensions Permissions (Allow access to file URLs, Allow in Incognito).  

2-We should re-initialize Extensions (Reload)and Update Browser State accordingly.

## POC Videos:

Full Detailed Steps on Linux shows in the two parts below:

- Part 1 POC Video:  
  
  <https://drive.google.com/file/d/1oeZ8rnX0FtWaHiqxhnNRRpFZ04mN6YR1/view?usp=sharing>
- Part 2 POC Video from step 5 in Repro steps to End:  
  
  <https://drive.google.com/file/d/1EZ2CwoXHShtRmEjJ3tCH08UoLc3WNFgo/view?usp=sharing>
- Windows Environment POCs Attached Directly.
- Extension Files Attached Also

---

**CREDIT INFORMATION**

## Reporter credit: Ahmed ElMasry

Thank you for your attention. with kind Regards

## Attachments

- [background.js](attachments/background.js) (text/plain, 1.1 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 352 B)
- [last-DEV-Spy-Leak-After-FIX.mp4](attachments/last-DEV-Spy-Leak-After-FIX.mp4) (video/mp4, 4.0 MB)
- [last-BETA-Spy-leak-After-Fix.mp4](attachments/last-BETA-Spy-leak-After-Fix.mp4) (video/mp4, 4.6 MB)

## Timeline

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-02-09)

Hi.., 

Could You Add Same Folks of Main One here and Ask Tim for any empty cycles to take a look?

Owner: tjudkins@chromium.org
 adetaylor@chromium.org
 solomonkinard@chromium.org
rdevl...@chromium.org

Thanks 

### ma...@google.com (2023-02-09)

tjudkins@, could you PTAL?

Speculatively assigning labels to match 1385343

[Monorail components: Platform>Extensions>API]

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-23)

tjudkins: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-03-01)

Friendly Ping: tjudkins@ any further updates? Is this under your radar?

Thanks


### tj...@chromium.org (2023-03-01)

Sorry for the lack of updates here, I've been thinking about this one and whether the priority could be dropped due to the fact it requires an extension to be in this state before the previous fix landed and so can't be actively targeted (as an extension update breaks the exploitable state). It's also a tricky one to resolve in a non-disruptive way, but it might be possible to do a single time sweep through installed extensions and look for a mismatch between the pref value and the creation flag, forcing a reload if it is detected. I'm going to talk to someone tomorrow to see if this is a pattern we've used before and see what the options might be.

### el...@gmail.com (2023-03-01)

Thanks Tim tjudkins@ for your feedback and efforts,

>>I've been thinking about this one and whether the priority could be dropped due to the fact it requires an extension to be in this state before the previous fix landed and so can't be actively targeted .
----
Rep: Simply as i stated in main bug description " if a Normal User was installing one of affected versions of chrome before 10-JAN FIX of dev  version (and not shipped to stable release) , the update will not protect him at all and attacker will be able to Get All User Files Although (Allow access to file URLs) is disabled." , Moreover if current users protect themselves now by unchecking Allow file access and think that they are protected ,the fact is  "NOT" even after updates, because the miss-check of current extensions permissions will totally break the previous fix , so this case is so tricky as you mentioned but still be easy exploitable as was in the main bug , and straight forward.

(All chrome users who disabled allow file access to some extensions ,these extensions could reach and get  local files breaking the previous check without user know ).
Hope i've explained well.

**Waiting for your feedback after internal discussions about the fix ..**

Thanks , appreciate your help in advance.

### tj...@chromium.org (2023-03-03)

I think these problems all boil down to the fact there is two stored sources of "truth" for file access: a stored pref that directly relates to the toggle shown on the management page and the stored creation flags used when an extension is installed / reinstalled / reloaded. Due to a series of small changes over time these are essentially OR'd together in the InstalledLoader [1], which is specifically why in this case either of the two being set will lead to the extension being loaded with file access.

One option here is to wipe out the stored creation flag value when going through the InstalledLoader::GetCreationFlags and just rely on the AllowFileAccess pref as the single source of truth. But the creation flags run pretty deep in other places as well and I would want to be sure there's no other unexpected behavior that might come from this.

Another option would be to actually use this point in the InstalledLoader to just look for a mismatch between the values and modify the stored creation flag value if there is a mismatch. Although again this doesn't really resolve the problem that there can be a mismatch and just feels like a bandied solution to the unexpected happens.

Really the ideal solution would be to just have a single source of truth in the pref value and get rid of this being something that is passed through and stored on the creation flags. That however would require a fair bit more of a rework of the install flow and there's a few points in there where getting at the related pref might be awkward.

@rdevlin.cronin what are your thoughts on these different approaches? 

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/installed_loader.cc;l=958;drc=75210aa72abfee0ddc6d8003ce00b998bf4ba310

### rd...@chromium.org (2023-03-03)

> But the creation flags run pretty deep in other places as well and I would want to be sure there's no other unexpected behavior that might come from this.

Yeah, this is also tricky because the advantage of the creation flag is that it's stored on the extension object, which means it's accessible from layers outside of browser (like common and renderer).

> Another option would be to actually use this point in the InstalledLoader to just look for a mismatch between the values and modify the stored creation flag value if there is a mismatch. Although again this doesn't really resolve the problem that there can be a mismatch and just feels like a bandied solution to the unexpected happens.

I think this is what I'd go for.  Extensions are (mostly) const, so as long as we instantiate the extension properly, we should have _reasonable_ confidence that it won't get mismatched again.

> Really the ideal solution would be to just have a single source of truth in the pref value and get rid of this being something that is passed through and stored on the creation flags. That however would require a fair bit more of a rework of the install flow and there's a few points in there where getting at the related pref might be awkward.

Yep, I think this would be nice, but is probably more trouble than it's worth at this point.

### el...@gmail.com (2023-03-15)

Hi Tim tjudkins@, any further updates? , have you figured out how to fix this issue?
Thanks for your time and hard work in advance.

### [Deleted User] (2023-03-18)

tjudkins: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2023-04-05)

Hello Tim tjudkins@ 
VIP Note: All Chrome Users received the fix of the Main https://crbug.com/chromium/1385343
Which was rolled out to Chrome 111.0.5563.64 (Linux and Mac), 111.0.5563.64/.65( Windows) at Mar 6 2023 , But due to the Issue highlighted here , chrome users  will not be fully protected , as all Extensions with disabled ( Allow access to file URL) can access all local files and get sensitive data from user without being aware although the file access permission is not permitted .

Could you prioritize this please to keep all users secure.

Thanks, Appreciate your time and hard work in advance.



### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### tj...@chromium.org (2023-04-11)

This issue should mostly be resolved with the following change:
https://chromium.googlesource.com/chromium/src/+/daae694a4e92f8c97b0df0947e4cdcc2d0f69b23 

Although the reproduction steps exactly as described will still produce the issue, the file access mismatch will be resolved with any extension reload (i.e. Chrome restart). This basically means that the file access as shown to a user on the extension management page is the base truth for file access.

Also, in going through to expand out related testing to properly document weirdness in how creation flags are saved and propagated, it highlighted that this requires a few more steps to actually get into the exploitable state for normal (non-unpacked) extensions installed through the webstore. After a user has installed the extension and manually granted it file access, it would then require that the extension had received an update through the webstore (which causes the creation flags file access stored in the prefs to be persisted), at which point you then can carry on from D in the reproduction steps.

### tj...@chromium.org (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-20)

Congratulations, Ahmed! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and reporting this issue to us! 

### el...@gmail.com (2023-04-23)

Thanks Amy!


### am...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1414398?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062996)*
