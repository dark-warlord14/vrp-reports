# Chrome allows "Always open files of this type" to be used with executables

| Field | Value |
|-------|-------|
| **Issue ID** | [40081498](https://issues.chromium.org/issues/40081498) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Reporter** | an...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2015-02-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36

Steps to reproduce the problem:
1. Download a legitimate executable program from a trustworthy site
2. Click the dropdown menu next to the downloaded file at the bottom of your screen and select "Always open files of this type"
3. Visit a malicious site
4. You've been pwned (remote code execution and browser sandbox escape).

What is the expected behavior?
Chrome should not allow "Always open files of this type" to be used with file types where that option would allow sites to perform remote code execution attacks simply be initiating a download.

Or, at the very least, it should warn uses of the potential negative consequences of selecting such an option.

What went wrong?
Chrome will happily follow the user's instructions to execute any program that any random website tells it to download, without prompting the user, or even warning the user beforehand of the consequences of selecting the "Always open files of this type" option for executable files.

Did this work before? N/A 

Chrome version: 40.0.2214.115  Channel: stable
OS Version: 8.1
Flash Version: Shockwave Flash 16.0 r0

I realize this vulnerability requires the user to make a dumb mistake beforehand (telling Chrome to automatically run any executables it downloads), so it is easy to write this off as PEBCAK and move on. Please don't.

Please consider that not all users are technically savvy enough to understand the security implications of selecting this option for executables, and even those who are technically savvy might select the option accidentally, or fail to take security into consideration when selecting the option initially. Once the option is selected, I think it's very unlikely that the user will realize their mistake later until after it's too late.

## Timeline

### me...@chromium.org (2015-02-26)

Thanks for the report. I agree we should exclude executables from "always open" list. Marking as low severity since this requires some user interaction.

asanka@: Can you please take a look?

### mb...@chromium.org (2015-04-21)

While trying to reproduce this, I did actually receive a warning that the file type could potentially be harmful and had to choose to keep the file before it was opened. Still, it doesn't seem like a good idea to allow this.

Switching some labels to track this as a security UX bug instead of a vulnerability.

asanka: Have you had a chance to look at this? If you won't be able to get to it soon, could you please suggest a new owner?

### an...@gmail.com (2015-04-21)

That's odd. I don't even get a "this file type could potentially be harmful" warning. I actually remember seeing that warning in Chrome in the past, but I just tested by downloading [Audacity](http://sourceforge.net/projects/audacity/) using Chrome 42 (stable) on Windows and that warning didn't appear for me. Even after temporarily enabling "Always open" and re-downloading, Chrome just executed the file immediately after downloading with no warning.

Is there a whitelist for certain executables, or maybe some setting I unknowingly have enabled? Or did I just stumble across another bug?

### pa...@google.com (2015-04-22)

andrewm.bpi: Try creating a fresh profile (chrome://settings) and see if you still get no warnings. It does sound like something is odd.

### an...@gmail.com (2015-04-22)

Haven't had a chance to test that on Windows yet, but on Ubuntu 12.04 LTS Chrome 42 I do get a "this file type could potentially be harmful" warning when initially downloading, but after setting "Always open files of this type" and re-downloading the warning does not appear (file just opens immediately).

This is less of a problem on Linux than it is on Windows though, since downloaded files don't have the execute bit set by default, and `.deb` package files (and presumably files for other package managers) don't install themselves when opened without further user interaction.

Will test your suggestion regarding Windows later today. I do have access to multiple Windows machines, so I'm pretty confident I can narrow down whether this is a problem unique to my computer. Only reason I asked you about it before doing further testing was that I wasn't sure whether or not it was expected behavior...

### an...@gmail.com (2015-04-23)

Okay, I just tested on a new blank profile and got the same result. Then I switched to a completely different computer (still Windows 8.1), created a new profile on there, and _still_ got the same result. Are you sure you can't reproduce the problem? Should I create a separate bug for this?

### an...@gmail.com (2015-04-23)

And just to clarify, by "same result" I mean the same as on the first Windows machine I tested with; no warnings when downloading an executable, with or without the "Always open files of this type" option set.

### as...@chromium.org (2015-04-23)

On Windows, .exe files (and a few others) don't trigger the "this file may be dangerous" warning. Instead we use Safe Browsing to get a better signal on whether the downloaded file is a known safe file. If so we don't show a warning.

If the file isn't known or is known to be unsafe, Chrome should display a suitable error message and prevent the file from being downloaded.

I'll work on blacklisting executable file types from being opened automatically. 

### an...@gmail.com (2015-04-23)

Okay, so it's expected behavior then. That makes sense, thanks for letting me know.

### pa...@chromium.org (2015-05-20)

asanka: Any ETA on not allowing executables to be opened automatically? Maybe M-45?

### pa...@chromium.org (2015-05-20)

Also, how does this interact with automatic downloads (e.g. Content-Disposition: attachment)? Can the attack be automated (assuming the user has previously selected Always Open...)?

### pa...@chromium.org (2015-05-20)

Heh, the answer is yes. :) I'm calling this a vulnerability. Hopefully if the fix is simple enough we can backport it to 44, rather than waiting for 45?

Medium because it requires previous user interaction.

### js...@chromium.org (2015-05-20)

Weird. I tried plamer's repro on my Win7 box and we're not setting the Zone.Identifier ADS. That seems bad.

### as...@chromium.org (2015-05-21)

The Zone.Identifier ADS may or may not be set depending on what the Windows Attachment Services thinks should happen. It's only guaranteed to be set if we set it manually.

Though I'd like to figure out the conditions under which Attachment Services decides not to annotate. Were you downloading a signed executable?

### as...@chromium.org (2015-05-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-05-21)

#14: No, the EXE was not signed (I used putty.exe).

### as...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### as...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### as...@chromium.org (2015-06-04)

From https://codereview.chromium.org/1165893004

Shall we blacklist all the DANGEROUS and ALLOW_ON_USER_GESTURE file types in download_extensions?

(quik link: https://code.google.com/p/chromium/codesearch#chromium/src/chrome/browser/download/download_extensions.cc)

I'm leaning towards yes. But if one were to be a bit more conservative, I could imagine creating a separate blacklist for executable file types that should be excluded from auto open.

I tried coming up with a curated subset of g_executables[] that should be excluded from auto-open, but it seems that all the file types  I looked at were either dangerous and hence should be excluded or I didn't know enough to decide one way or another.

If there's notable pushback about certain file types, then we can reconsider whether we want a separate blacklist.

Also while you are here, why are .apk files not considered dangerous on Android?

### rd...@chromium.org (2015-06-04)

So I'm not actually adverse to the "Do it and see how loud the screaming is", but I at least want to lay out the arguments on both sides before we go that way.  From my perspective, the question is not "Is this file type dangerous?"  The question is instead "Is this file type *so* dangerous that we should take away the user's ability to shoot themselves in the foot with it?"  

To me, executables are solidly in the "Yeah, no, if you want to be that stupid do it with some other browser" category.  But I"m not thinking of other file types that I personally feel that way about.  Asanka, can you name some other file types that you'd put in that category from your curation attempt?


### as...@chromium.org (2015-06-04)

Contains executable code that runs with user privileges and capabilities. Will execute code if opened:

 bat
 cmd
 com
 cpl
 dll
 drv
 exe
 hta
 htt
 js
 jse
 mmc
 msc
 ocx
 scr
 sys
 vbe
 vbs
 ws
 wsc
 wsf
 wsh
 class
 jar
 jnlp (Looks like auto-open is the preferred mode for this file type)
 pl
 py
 pyc
 pyw
 rb
 bash
 csh
 ksh
 sh
 shar
 tcsh
 command

Not directly executable, but associated with handlers that are often vulnerable, or executable in constrained environments:

 swf
 spl
 asx
 chi (MS Compiled HTML Help index file)
 chm (MS Compiled HTML Help)
 hlp (Old style MS Help file)
 mda (MS Access Add-in)
 mdb (MS Access DB)
 mde (MS Access Compiled DB)
 mht (Multipart HTML)
 mhtml (ditto)
 url

Installers / configuration changers and such that may indirectly execute code if opened:

 application (MS ClickOnce)
 cfg
 crx
 inf
 ini
 ins
 lnk
 local
 manifest
 mof
 msi
 msp
 mst
 pif
 reg
 scf
 xbap
 pkg
 deb
 rpm
 dex
 apk

Probably okay to allow opening:

 asp
 bas
 fxp
 vb
 vsd
 vsmacros
 vss
 vsw

No idea what these are. Are they Scrabble words?:

 ad
 ade
 adp
 app (ClickOnce?)
 crt
 grp
 isp
 mad
 maf
 mag
 mam
 maq
 mar
 mas
 mat
 mau
 mav
 maw
 mdt
 mdw
 mdz
 msh
 mshxml
 ops (Office Profile Settings?)
 pcd (Photo CD?)
 plg
 prf (Outlook Profile?)
 prg
 pst (Outlook Personal Storage)
 sct
 shb
 shs
 vst



### as...@chromium.org (2015-06-04)

In retrospect, things would've gone much more smoothly if some justification was included with the addition of file types to download_extension.cc.

### pa...@chromium.org (2015-06-04)

#19: "Also while you are here, why are .apk files not considered dangerous on Android?" 

felt changed this in: https://codereview.chromium.org/512983003

In my mind, the reasoning goes like this: Unlike (say) an EXE, when you open an APK, it does not immediately run. Instead, the Android APK installer takes it, and shows you its "Here is this package, do you really want to install it? Here are its permissions..."

(The same thinking could apply for .deb, .rpm, modulo the inability to limit the package's capabilities.)

Then, even if you do install, it runs as a distinct principal instead of having the full run of all your data like an EXE.

### as...@chromium.org (2015-06-05)

#23: Makes sense.

I'll try to come up with a consistent set of criteria and then create a blacklist based on those. Note that file types that I don't know about will not be in the blacklist.


### bu...@chromium.org (2015-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/39841e54180e2583dffa16fbbb9b99fd293821d0

commit 39841e54180e2583dffa16fbbb9b99fd293821d0
Author: asanka <asanka@chromium.org>
Date: Tue Jun 16 20:23:18 2015

[Downloads] Prevent executable files from being opened automatically.

Users can accidentally mark executable or other dangerous file types for
opening automatically upon download. This change prevents such file
types from being considered for auto open.

If the user already has any dangerous file types in the auto-open list,
those entries will be ignored on new browser sessions. Any action that
causes the persisted auto-open list to be updated will, as a
side-effect, premanently remove any dangerous file types that were
there.

Currently the list of file types that are excluded from auto open is
maintained by chrome/browser/download/download_extension.cc.

BUG=461858
TEST=(1) Download an .exe (on Windows) or .swf file.
     (2) Verify that the "Always open files of this type" option is
         disabled.

Review URL: https://codereview.chromium.org/1165893004

Cr-Commit-Position: refs/heads/master@{#334677}

[modify] http://crrev.com/39841e54180e2583dffa16fbbb9b99fd293821d0/chrome/browser/download/download_commands.cc
[modify] http://crrev.com/39841e54180e2583dffa16fbbb9b99fd293821d0/chrome/browser/download/download_extensions.cc
[modify] http://crrev.com/39841e54180e2583dffa16fbbb9b99fd293821d0/chrome/browser/download/download_extensions.h
[modify] http://crrev.com/39841e54180e2583dffa16fbbb9b99fd293821d0/chrome/browser/download/download_prefs.cc
[modify] http://crrev.com/39841e54180e2583dffa16fbbb9b99fd293821d0/chrome/browser/download/download_prefs.h
[add] http://crrev.com/39841e54180e2583dffa16fbbb9b99fd293821d0/chrome/browser/download/download_prefs_unittest.cc
[modify] http://crrev.com/39841e54180e2583dffa16fbbb9b99fd293821d0/chrome/chrome_tests_unit.gypi


### as...@chromium.org (2015-06-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-07-08)

Merge-Requested to M44 (branch 2403)

### ti...@google.com (2015-07-08)

[Empty comment from Monorail migration]

### pe...@google.com (2015-07-08)

[Automated comment] Less than 2 weeks to go before stable on M44, manual review required.

### pe...@google.com (2015-07-09)

Merge approved for M44 (2403).  Please get it merged before end of business PST Monday.

### as...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ea65713eae7ad5977b6af590eb45e9551ea1fb2e

commit ea65713eae7ad5977b6af590eb45e9551ea1fb2e
Author: Asanka Herath <asanka@chromium.org>
Date: Fri Jul 10 15:51:07 2015

[Downloads] Prevent executable files from being opened automatically.

Users can accidentally mark executable or other dangerous file types for
opening automatically upon download. This change prevents such file
types from being considered for auto open.

If the user already has any dangerous file types in the auto-open list,
those entries will be ignored on new browser sessions. Any action that
causes the persisted auto-open list to be updated will, as a
side-effect, premanently remove any dangerous file types that were
there.

Currently the list of file types that are excluded from auto open is
maintained by chrome/browser/download/download_extension.cc.

BUG=461858
TEST=(1) Download an .exe (on Windows) or .swf file.
     (2) Verify that the "Always open files of this type" option is
         disabled.

Review URL: https://codereview.chromium.org/1165893004

TBR=asanka@chromium.org

Cr-Commit-Position: refs/heads/master@{#334677}
(cherry picked from commit 39841e54180e2583dffa16fbbb9b99fd293821d0)

Review URL: https://codereview.chromium.org/1231103002 .

Cr-Commit-Position: refs/branch-heads/2403@{#483}
Cr-Branched-From: f54b8097a9c45ed4ad308133d49f05325d6c5070-refs/heads/master@{#330231}

[modify] http://crrev.com/ea65713eae7ad5977b6af590eb45e9551ea1fb2e/chrome/browser/download/download_commands.cc
[modify] http://crrev.com/ea65713eae7ad5977b6af590eb45e9551ea1fb2e/chrome/browser/download/download_extensions.cc
[modify] http://crrev.com/ea65713eae7ad5977b6af590eb45e9551ea1fb2e/chrome/browser/download/download_extensions.h
[modify] http://crrev.com/ea65713eae7ad5977b6af590eb45e9551ea1fb2e/chrome/browser/download/download_prefs.cc
[modify] http://crrev.com/ea65713eae7ad5977b6af590eb45e9551ea1fb2e/chrome/browser/download/download_prefs.h
[add] http://crrev.com/ea65713eae7ad5977b6af590eb45e9551ea1fb2e/chrome/browser/download/download_prefs_unittest.cc
[modify] http://crrev.com/ea65713eae7ad5977b6af590eb45e9551ea1fb2e/chrome/chrome_tests_unit.gypi


### as...@chromium.org (2015-07-10)

Marking as fixed while I monitor the beta builders.

### bu...@chromium.org (2015-07-15)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/ea65713eae7ad5977b6af590eb45e9551ea1fb2e

commit ea65713eae7ad5977b6af590eb45e9551ea1fb2e
Author: Asanka Herath <asanka@chromium.org>
Date: Fri Jul 10 15:51:07 2015


### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

As you've seen from our release notes, we decided to reward $500 for this report. Congrats! We'll be in contact within a week to collect payment details, but if you don't hear from anyone, please contact me directly at timwillis@.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### an...@gmail.com (2015-08-29)

Wow, thanks. :-) I'm glad you found my report helpful; I'll be in touch.

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### an...@gmail.com (2015-09-19)

Awesome! Payment received, thanks again. :-)

### cl...@chromium.org (2015-10-16)

Bulk update: removing view restriction from closed bugs.

### an...@gmail.com (2015-11-09)

Relevant XKCD? https://xkcd.com/1172/ ;-)

In all seriousness though, I'm not familiar with jnlp, but given the intent of this change, wouldn't having that file type set to auto-open basically let any site you visit anywhere on the internet gain control of your machine? (By executing arbitrary code with full user permissions.)

If so, it seems to me like this update fixed a serious security hole that was present on all your work PCs.

### go...@sven-haag.de (2015-11-09)

A site whitelist should be provided to allow auto start.

### an...@gmail.com (2015-11-09)

Seems like a kinda niche feature, but eh.

Anyway, regardless of what the Chrome team decides, you could always work around this by creating a specialized application that registers a protocol handler (e.g. `myapp://internal.site/path/to/file`) that does what you want. Implemented correctly, such a program would be far more secure than just trusting whatever website you happen to be browsing not to take over your machine with a malicious download.

### as...@chromium.org (2015-11-09)

We are very much unlikely to provide a general option to disable this restriction.

Could you open a new issue for considering an enterprise managed exception? The details of how such an exception is to be specified and security considerations can be discussed in that issue.


### ko...@gmail.com (2016-06-09)

I would like to discus jnlp auto open options. Will do so via https://crbug.com/chromium/518170 as my goal is to get options to enable this in my favorite browser. After all security measures for running jnlp / jar / class files has improved and has been  extremely tight for quite some time now and these files are not runnable by themselves, but need a Java installation on the client, which makes the possibility of accidental running a lot smaller.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/461858?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081498)*
