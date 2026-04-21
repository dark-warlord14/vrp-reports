# File System Access API - Save shows saving as JPEG, however, downloaded as an executable .bat

| Field | Value |
|-------|-------|
| **Issue ID** | [40055833](https://issues.chromium.org/issues/40055833) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2021-21223 |
| **Reporter** | ar...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2021-05-12 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15

Steps to reproduce the problem:
1. Click on "Save Image"
2. The downloaded file will be detected to be of .jpeg extension but in reality will be an executable .bat file that opens system calculator
3. Open the downloaded file, the calculator application will run

What is the expected behavior?
The "save image" button should not result in any action and the file should not be allowed to be downloaded.

What went wrong?
Saved file shows saving as JPEG, however, downloaded as an executable .bat

Did this work before? N/A 

Does this work in other browsers? N/A

Chrome version: 90.0.4430.212  Channel: n/a
OS Version: 20H2(Build:19042.870)
Flash Version: 

https://bugs.chromium.org/p/chromium/issues/detail?id=1137247, according to this page, the reported bug has been patched but the testing results indicate otherwise

## Attachments

- [Script.html](attachments/Script.html) (text/plain, 1.4 KB)
- [explanation.png](attachments/explanation.png) (image/png, 41.7 KB)
- [Downloaded file.jpeg](attachments/Downloaded file.jpeg) (image/jpeg, 43.9 KB)
- [download dialogue box.jpeg](attachments/download dialogue box.jpeg) (image/jpeg, 50.2 KB)
- [html page content.jpeg](attachments/html page content.jpeg) (image/jpeg, 61.3 KB)
- [Video PoC for Issue 1208439.mov](attachments/Video PoC for Issue 1208439.mov) (video/quicktime, 8.1 MB)
- [PoC.gif](attachments/PoC.gif) (image/gif, 205.0 KB)

## Timeline

### ar...@gmail.com (2021-05-12)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-05-12)

Are you sure you're testing against a chrome version where this is fixed? 88.0.4324.79 or newer should have the fix, and I can't reproduce this issue myself anymore either.

[Monorail components: -Blink>Storage Blink>Storage>FileSystem]

### ar...@gmail.com (2021-05-12)

mek@chromium.org, Im testing this in the most recent version 90.0.4430.212 of chrome

### me...@chromium.org (2021-05-12)

Not sure what's going on then, I'm not getting the behavior you describe when trying your test case in the current version of chrome on windows...

### [Deleted User] (2021-05-12)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@gmail.com (2021-05-12)

mek@chromium.org, I was doing research on the issue described on the page "https://bugs.chromium.org/p/chromium/issues/detail?id=1137247" when i tried to replicate the same on the most recent version of chrome and i was surprised to see it not patched, contradictory to the page saying that it has been patched. I followed the same steps, visited the page described in that issue and i was able to download the .bat file

### va...@gmail.com (2021-05-12)

Hi Please see the video for the same PoC

### va...@gmail.com (2021-05-12)

Attaching a GIF for the same

### me...@chromium.org (2021-05-12)

Ah, I think the difference is in if the "hide extensions for known file types" system setting is turned on or off. With the setting turned off, that apparently also applies to file dialogs, so no extension is shown in the file dialog. I'm not sure if there is a way for us to work around that/force the extension to show up regardless. Also not sure if there is much benefit to doing so if we could; if a user doesn't have extensions shown to begin with, it seems rather unlikely that they'll have any idea what the implications might or might not be for using specific file extensions in a save as dialog...

### sa...@chromium.org (2021-05-13)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-05-13)

+nattestad: Do you have opinions on if we should ignore the "hide known extensions" system setting and always make sure to show known extensions in the file system access related file pickers? I suspect we probably should, although it feels a bit weird to be ignoring the system setting like that (but the alternative where websites can show something that looks like an extension but isn't really the extension isn't great either).

### na...@google.com (2021-05-17)

Thanks for looping me in on this issue. Generally I do think this is a concern we need to do something about. If a site can make it so easily seem like they're saving an image but it's actually a different type, I could see that being a security concern. To me though, the issue is not that the extension in the file name is wrong but that the description can be made to not at all match the actual file type being saved. I'm not familiar with OS level file saving dialogs but as a user I had always assumed the file type descriptor had to match the type being saved - I'm gathering that was a false assumption? Is that a pattern we could enforce or do we have to let the developer pick anything for the description field? 

### va...@gmail.com (2021-05-28)

Hi team, I have a small concern regarding the latest update from chromium. This vulnerability has trickled down to the following builds.

-Microsoft Edge - Version 91.0.864.37 (Official build) (64-bit)
-Google Chrome - Version 91.0.4472.77 (Official Build) (x86_64)

Input for the previous comment, I would like to suggest that 
-yes, the pattern of the description matching to the actual file type being saved could be enforced 
-in case it cannot be then maybe in such cases the browser can restrict the download itself 

Though I don't know how this will be implemented as I limited information on the same. 

Lastly, may I ask the status of this issue since our team was researching on the CVE-2021-21223.

Thanks.

### er...@microsoft.com (2021-08-26)

> yes, the pattern of the description matching to the actual file type being saved could be enforced

That would entail having the registry file type information override the information in the showSaveFilePicker API, which would have some interesting implications for scenarios where the web application is in a different language than the client OS. But it's an interesting idea.


### er...@microsoft.com (2021-08-26)

SafeBrowsing has the concept of dangerous file extensions, and other places in the code [1] are willing to treat files of potentially-dangerous extensions more cautiously. We might consider a force-override of the |description| for just those extensions that SafeBrowsing considers dangerous.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/download_target_determiner.cc;l=299;drc=bfa44073e9d2d43e46ee27d7c03b3c11e3ca0e7e

### ab...@microsoft.com (2021-08-26)

How about invoking the download shelf when 'save as' is used? This way the user could tell what is happening with more clarity.

### va...@gmail.com (2021-12-19)

What really peaks my curiousity is that there are products dealing with this issue, I tested a few and my observation was:

>either they are running some scripts to disable that button that had the malicious code itself
>or they render the downloaded file disabled(? -not able to open it on my local)

Note: I had checked with two browsers only and not all of them

### va...@gmail.com (2021-12-19)

>> How about invoking the download shelf when 'save as' is used? This way the user could tell what is happening with more clarity.

This could be an option though again I'm not sure how the flag work and where it might not

### ym...@ym.kim (2022-01-02)

IMHO, this is a security vulnerability and should be triaged as such.

### va...@gmail.com (2022-01-07)

Definately agreed since there is a high chance it can be a key component in chain of attacks for malware spreading and installation, specifically for non technical audiences. 

### er...@microsoft.com (2022-01-07)

It seems worthwhile to allow the Security team to weigh in on this issue, as this primitive does seem useful in exploit chains.

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-18)

reopening visibility (as this has been visible for a while) and CC'ing some safe browsing people.

(eric: it's helpful to CC in a few people before turning something into a security bug as doing so can hide it from everyone else.)

[Monorail components: Blink>SecurityFeature Services>Safebrowsing]

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### er...@microsoft.com (2022-01-18)

RE #23: Ah, thanks. I was under the apparently mistaken impression that changing the flags to Security would add it to the Sheriff queue, and they would be responsible for deciding who to CC.

### xi...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-01-19)

On the Safe Browsing side, I checked the chrome://safe-browsing page and was able to confirm that Safe Browsing check for the file saved through the file picker with a dangerous file extension is not bypassed. So I think it's WAI from the Safe Browsing side.

Agree that the description field can be spoofed by malicious websites. Adding some restrictions for the description field sound like a good approach to mitigate that.

### xi...@chromium.org (2022-01-19)

Assigning to mek@ to weigh in on the approach. Thanks!

### dr...@chromium.org (2022-02-09)

(Triaging SB bugs with owners)

### me...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-18)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-04-28)

We'll be adding a new prompt to be shown when saving a file with a dangerous extension. https://crbug.com/1320877 tracks the status of this new prompt

### as...@chromium.org (2022-05-16)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-08-16)

Fixed in https://crrev.com/c/3829770

### ar...@gmail.com (2022-08-16)

Hello Team,

Thank you for addressing this bug!
I feel happy that I could play a part in initiating a conversation on this.

A request: Since the issue has now been fixed, is there any acknowledgment/bounty/etc that comes along? As I have begun my career in information security, these things go a long way!

Looking forward to your kind response.

Best,
Archie


### [Deleted User] (2022-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-16)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-08-16)

Hi Archie, thank you for starting this conversation! I'm looking forward to fixing many more bugs you send our way :P

The sheriffbot is adding the right labels so this will be looked at by folks who decide bounties/etc. Hold tight!

### am...@chromium.org (2022-10-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-07)

Congratulations, Archie! The VRP Panel has decided to award you $1,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the meantime, please let us know the name/handle/tag you would like us to use for acknowledging you for this issue. 
Thank you for your efforts in reporting this issue to us! 

### ar...@gmail.com (2022-10-07)

Thank you Amy! I am really humbled and very excited!
This is amazing!

Though, I would like to put forth a request:
Since this issue was reported here when I was in uni, a friend of mine also supported me in creating this poc. She was unfortunately restricted to comment on this post since she wasn’t the one who reported this. I wish if she could also be given the acknowledgment.

Is there any possibility this can be done?


### am...@chromium.org (2022-10-07)

Yes, she can be given acknowledgement (either instead of you or with you), please feel free to drop her name in a comment here and we'll make that possible when we update the release notes with this fix. 

### ar...@gmail.com (2022-10-07)

Thank you! 

Please see below the names for acknowledgment:

Archie Midha (linkedin.com/in/archiemidha) & Vallari Sharma (linkedin.com/in/vallari-sharma)

—
Looking forward to this and contributing more to chromium ahead :))

### am...@chromium.org (2022-10-07)

+ pgrace@ - addition for the release notes and issuing CVE 

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### pg...@google.com (2022-10-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-10)

Just closing the loop on this, CVE and acknowledgement has been included and updated here: https://chromereleases.googleblog.com/2022/09/stable-channel-update-for-desktop_27.html

### mo...@chromium.org (2022-10-11)

Looking back at this bug, I think this was a simple off-by-one error. The browser downloaded a JPEG of a cat, but thought it was a .bat. "b", not "c".

:P

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-11-23)

This issue was migrated from crbug.com/chromium/1208439?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Blink>Storage>FileSystem, Services>Safebrowsing]
[Monorail blocked-on: crbug.com/chromium/1320877]
[Monorail mergedwith: crbug.com/chromium/1243872, crbug.com/chromium/1244076, crbug.com/chromium/1290130, crbug.com/chromium/1308142, crbug.com/chromium/1324528]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055833)*
