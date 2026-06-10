# Security: Minor data leak in pdfium

| Field | Value |
|-------|-------|
| **Issue ID** | [40082700](https://issues.chromium.org/issues/40082700) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF, Privacy |
| **Reporter** | [Deleted User] |
| **Assignee** | th...@chromium.org |
| **Created** | 2015-08-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

This is about an overlooked aspect of <https://code.google.com/p/chromium/issues/detail?id=425025> - there's no way to prevent a local, malicious PDF file from leaking its path to a remote server.

**VERSION**

Chrome Version: 44.0.2403.155 stable  

Operating System: OSX 10.10.5

**REPRODUCTION CASE**

1. Download server.py and run it (you can also adjust the IP or port in the code)
2. Download MalForm.pdf (attached to #425025), edit it so that the URL in /SubmitForm points to the server.py's socket
3. Open MalForm.pdf in Chrome and observe that pdfium leaks the path of the PDF file (server.py's output should be similar to sample\_output.txt)  
   
   3a. Disable JavaScript in Chrome settings, repeat the above step and observe the same outcome

COMMENT

Pdfium exposes the local path of the PDF file to the JS code. It's very likely that the path is inside the home folder or some project's folder, which means that the username and project name, combined with IP, can be revealed to a remote attacker.

Now, this might not sound like a security issue as if I save a web page to a html file and open that file in the browser then bad things can happen as well and it's like that by design. But unlike HTML/JS, downloading PDF documents is a common use case and a lot of sites force people to download PDF documents by setting relevant HTTP headers.

Moreover, if a user is blocking Javascript (in Chrome settings), such malicious web page won't do any harm whereas a malicious PDF will still be able to leak data as pdfium doesn't honor Javascript settings.

As a side note, there seem to be an inconsistency in pdfium's code - in <https://pdfium.googlesource.com/pdfium/+/chromium/2444/fpdfsdk/src/javascript/app.cpp>, line 766, launchURL() is marked as "Unsafe, not supported". And if launchURL is unsafe then IMHO form submissions should also be treated as unsafe.

## Attachments

- [sample_output.txt](attachments/sample_output.txt) (text/plain, 946 B)
- [server.py](attachments/server.py) (text/plain, 629 B)
- [js-leak.pdf](attachments/js-leak.pdf) (application/pdf, 845 B)

## Timeline

### th...@chromium.org (2015-08-20)

[Empty comment from Monorail migration]

### np...@chromium.org (2015-08-20)

I repro'd this on linux M44.  I agree it is a slight privacy leak, but not much of a security issue.

+battre in case privacy team would like to track this.

tsepez -- Can you help find an owner?

### ba...@chromium.org (2015-08-24)

I am no expert in PDF or FDF but I agree that this is surprising and should be changed. Maybe we can just truncate the file field to the filename.

### [Deleted User] (2015-08-26)

Just want to let you know that apparently I "merged" two similar issues together.

One issue is that pdfium sends the full path of a local PDF file on form submission. And that's what MalForm.pdf shows.

The other is that a JS script can read the path from "app.activeDocs[0].path". So even if you fix the first issue, a malicious PDF will still be able to submit the local path to a remote server (the attached js-leak.pdf uses an alert box to demonstrate that).

### ts...@chromium.org (2015-08-31)

The data originates in PDFiumEngine::Form_GetFilePath(); I suspect chromium doesn't want to supply this information.  Other emebedders of PDFium may want to so I don't think we should de-support this at the JS level itself.

### th...@chromium.org (2015-08-31)

http://www.adobe.com/content/dam/Adobe/en/devnet/acrobat/pdfs/js_api_reference.pdf page 85 has the red 'S' icon for activeDocs. Page 32 describe the 'S' icon as methods that can only run in a privileged context. Do we have an equivalent notion in Chromium?

### ba...@chromium.org (2015-08-31)

+mkwst: Mike, do we have something like a privileged context in Chrome?

### th...@chromium.org (2015-08-31)

OTOH, accessing this.path (Adobe JS API, page 252) has no restrictions. I wonder what the Acrobat NPAPI plugin does.

### th...@chromium.org (2018-04-17)

And now it's 2018 and I'm not going to go look around for NPAPI plugins.

PDFium has FSDK_IsSandBoxPolicyEnabled() and FSDK_SetSandBoxPolicy(). It only supports FPDF_POLICY_MACHINETIME_ACCESS right now. Maybe we should extend it to make our own concept of a privileged context.

We may also want to collect metrics on how often some of these JS features are being used.

### ts...@chromium.org (2019-01-02)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-01-02)

Raising severity as it seems some folks are abusing this in the wild in the referenced bug.

### th...@chromium.org (2019-02-14)

I think we should duplicate this into https://crbug.com/chromium/851821, and undupe https://crbug.com/chromium/917897.

### th...@chromium.org (2019-02-14)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-02-14)

awhalley: Can we nominate this for a reward, since this was reported way before https://crbug.com/chromium/851821.

### aw...@google.com (2019-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-14)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-28)

Congrats! The Panel decided to reward $500 for this report :) 

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-04-21)

maskthelatency@gmail.com - Please claim your reward by April 30 2020 otherwise it will be donated to charity.

### na...@google.com (2020-05-05)

processing this as a donation. 

### is...@google.com (2020-05-05)

This issue was migrated from crbug.com/chromium/522717?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, Privacy]
[Monorail mergedwith: crbug.com/chromium/917897]
[Monorail mergedinto: crbug.com/chromium/851821]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082700)*
