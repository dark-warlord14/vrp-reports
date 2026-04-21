# Path traversal using \.. causes sourceMappingURL to still load UNC paths on Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [468027781](https://issues.chromium.org/issues/468027781) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Sources |
| **Platforms** | Windows |
| **Reporter** | o....@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2025-12-12 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS

When using sourceMappingURL containing `\..` path-traversals before the hostname in a UNC file url (like for example `file:///abc\..//malicious-smb-server/Data/random.txt`) the existing security measures (introduced with [Issue 40060207](https://issues.chromium.org/issues/40060207) and improved in [Issue 40061586](https://issues.chromium.org/issues/40061586)) fail. This leads to Chrome trying to load the file from a SMB share once the Devtools are opened. As discussed in details in [Issue 40060207](https://issues.chromium.org/issues/40060207) this is a security problem (with severity S2) as it allows a malicious SMB server to steal NTLM hashes etc.

VERSION

Chrome Version: 143.0.7499.110 + stable
Operating System: Windows 11 Pro, 24H2

REPRODUCTION CASE

- Serve the attached index.html via a local webserver
  - for example using podman (or docker): `podman run --rm -it -p 8080:80 -v "./index.html:/usr/local/apache2/htdocs/index.html" httpd:2.4`
- Open served index.html in Chrome (<http://localhost:8080/index.html>)
- Open Devtools in Chrome
- Verify that loading SBM share file url was triggered
  - The most simple way I found to verify that loading was triggered is to look at the Windows Event Logs:
    - Open Windows Eventviewer
    - Go to Applications and Services Logs > Microsoft > Windows > SMBClient > Connectivity
    - An Error message is logged saying that
      ```
      The server name cannot be resolved.
      Error: The object was not found.
      Server name: malicious-smb-server
      
      ```
  - Alternative approaches for verficiation:
    - Responder.py
      - Suggested in [Issue 40060207](https://issues.chromium.org/issues/40060207)
      - Clone and run [Responder.py](https://github.com/lgandx/Responder)
      - Change `malicious-smb-server` in sourceMappingURL in `index.html` accordingly to IP/hostname of host running Responder.py
    - Run local samba server using podman/docker
      - I did that for local testing using [dockurr/samba](https://hub.docker.com/r/dockurr/samba). It did not attach this for shortness but I have (and can) attach/provide complete podman compose setup (including both webserver and samba server) if needed!

BISECT ANALYSIS

The problem with UNC file urls in sourceMappingURL has beend first reported in [Issue 40060207](https://issues.chromium.org/issues/40060207) and was fixed with [devtools/devtools-frontend/+/1a1e7c6f50b85ad086654f9a8562efa15a943de6](https://chromium.googlesource.com/devtools/devtools-frontend/+/1a1e7c6f50b85ad086654f9a8562efa15a943de6). Before that fix there seemed to be no check for UNC file urls at all. However, the fix only checks if url starts with `file:////` (c.f. [ResourceLoader.ts diff](https://chromium.googlesource.com/devtools/devtools-frontend/+/1a1e7c6f50b85ad086654f9a8562efa15a943de6%5E%21/#F0)). This allowed UNC file starting with `file://\` to be still loaded as reported in [Issue 40061586](https://issues.chromium.org/issues/40061586). The fix for [Issue 40061586](https://issues.chromium.org/issues/40061586) ([devtools/devtools-frontend/+/1223b5bb140c470b66f6f0a73de6064a643878f4](https://chromium.googlesource.com/devtools/devtools-frontend/+/1223b5bb140c470b66f6f0a73de6064a643878f4)) changed *detection* of UNC urls to checking if URL protocol is `file:` and the parsed `host` part of the url is non empty (see new function `canBeRemoteFilePath` in [ResourceLoader.ts diff](https://chromium.googlesource.com/devtools/devtools-frontend/+/1223b5bb140c470b66f6f0a73de6064a643878f4%5E%21/#F0)). This *detection* is still in place (c.f. [ResourceLoader.ts#207](https://chromium.googlesource.com/devtools/devtools-frontend/+/refs/heads/main/front_end/core/host/ResourceLoader.ts#207))

FURTHER ANALYSIS

In the current approach for *detecting* UNC (c.f. [ResourceLoader.ts#207](https://chromium.googlesource.com/devtools/devtools-frontend/+/refs/heads/main/front_end/core/host/ResourceLoader.ts#207)) sourceMappingURL is parsed using `new URL(...)` and then it is verified that the host part of the parsed URL object is non-empty. The problem is that the `URL` (as implemented in Chrome) does not take path-traversals (both `\..` and `/..`) before the actual host into account when parsing host. This results is host always being empty in such cases. That can easily be verified by executing the following javascript in Chrome (e.g. in Dev Console)

```
> new URL('file:///abc\\..//malicious-smb-server/Data/random.txt').host
< ''
> new URL('file:///abc/..//malicious-smb-server/Data/random.txt').host
< ''

```

This makes the *detection* fail. On the other hand when actually loading the url the path-traversal seems to be taken into account and the UNC file is tried to be loaded *correctly*

Note: Although `new URL(...)` behaves the same no matter if path traversal is `../` or `..\` only sourceMapURL with `..\` path traversal are actually loaded. The reason for this difference is that sourceMapURLs are normalized using `Common.ParsedURL.ParsedURL` in [SourceMapManager.ts#103](https://chromium.googlesource.com/devtools/devtools-frontend/+/refs/heads/main/front_end/core/sdk/SourceMapManager.ts#103) before calling ResourceLoader. This normalization does take `../` path traversals into account which results `file:///abc/..//malicious-smb-server/Data/random.txt` in being normalized to `file:////malicious-smb-server/Data/random.txt`. In that case `new URL(...).host` is `malicious-smb-server`. On the other hand, `..\` path traversal are not taken into accout by `Common.ParsedURL.ParsedURL` which results `file:///abc\..//malicious-smb-server/Data/random.txt` in remaining as it is.

POSSIBLE PATCH

While `new URL(...)` does not parse host part correctly of url with path traversal before hostname it does normalize such urls correctly (including `..\`).

```
> new URL('file:///abc\\..//malicious-smb-server/Data/random.txt').toString()
< 'file:////malicious-smb-server/Data/random.txt'
> new URL(new URL('file:///abc\\..//malicious-smb-server/Data/random.txt').toString())
< URL {origin: 'file://', protocol: 'file:', username: '', password: '', host: 'malicious-smb-server', …}

```

This could be used for a simple patch of `canBeRemoteFilePath` in `ResourceLoader.ts`:

```
diff --git a/front_end/core/host/ResourceLoader.ts b/front_end/core/host/ResourceLoader.ts
index 524e1c32..c74adbb8 100644
--- a/front_end/core/host/ResourceLoader.ts
+++ b/front_end/core/host/ResourceLoader.ts
@@ -206,7 +206,7 @@ async function fetchToString(url: string): Promise<string> {

 function canBeRemoteFilePath(url: string): boolean {
   try {
-    const urlObject = new URL(url);
+    const urlObject = new URL(new URL(url).toString());
     return urlObject.protocol === 'file:' && urlObject.host !== '';
   } catch {
     return false;

```

Note: As described above `Common.ParsedURL.ParsedURL` does not take path traversals with `..\` into account. As `ParsedURL` is used in many places that could also cause security issue in other places then the above described regarding sourceMapURL. The reason is (as far as I see) that normalization of path is done by splitting the path using `'/'` (instead of for example `/[/\\]/`), see [ParsedURL.ts#17](https://chromium.googlesource.com/devtools/devtools-frontend/+/refs/heads/main/front_end/core/common/ParsedURL.ts#17). This could be fixed by using `/[/\\]/` but I don't know if this wold cause any unwanted side-effects

CREDIT INFORMATION

Reporter credit: Ole SH

## Attachments

- [index.html](attachments/index.html) (text/html, 165 B)

## Timeline

### th...@chromium.org (2025-12-12)

[security shepherd] Nice find, and thank you for the clear explanations and poc. I am able to reproduce this on Windows M142. Copying over the severity S2 from the linked bugs in the description.

szuend@: Could you PTAL?

### ch...@google.com (2025-12-13)

Setting milestone because of s2 severity.

### ch...@google.com (2025-12-13)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-12-15)

Project: devtools/devtools-frontend  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7255782>

Normalize URLs first before checking for UNC path

---


Expand for full commit details
```
     
    R=bmeurer@chromium.org 
     
    Fixed: 468027781 
    Change-Id: I8d7c602657e45a8110e695ab4a91b9c4ef6f62aa 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7255782 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org>

```

---

Files:

- M `front_end/core/host/ResourceLoader.ts`
- M `front_end/core/sdk/PageResourceLoader.test.ts`

---

Hash: [8564770a55f6a9d1e18bb202ef4ba01d618bb2ac](https://chromiumdash.appspot.com/commit/8564770a55f6a9d1e18bb202ef4ba01d618bb2ac)  

Date: Mon Dec 15 07:06:47 2025


---

### sz...@google.com (2025-12-15)

Thanks for the great repro and the detailed description. Applied the suggested fix as it's the best band aid for now.

### ch...@google.com (2025-12-15)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
mitigated user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### o....@gmail.com (2025-12-18)

Hi :-) Thank you very much! I appreciate it. 

If I am allowed I would like to ask one additional question:

As this is my first vulnerability report I took a look at the award of similiar reported issues (https://issues.chromium.org/issues/40060207 and https://issues.chromium.org/issues/40061586). They both received a significantly higher award. As all issues have the same "impact" I wonder what I can do "better" next time. As far as I can see I provided a simpiflied POC (no use of Responder.py), a clear and complete analysis on source-code level and a bisect analysis. Furthermore, I provided a patch that was used in final merge request.

### dr...@chromium.org (2025-12-29)

Sorry for the delay on the merge review. This does seem very low risk, so it would be nice to merge it to M144.

### dx...@google.com (2025-12-30)

Project: devtools/devtools-frontend  

Branch:  chromium/7559  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7320487>

Normalize URLs first before checking for UNC path

---


Expand for full commit details
```
     
    R=bmeurer@chromium.org 
     
    Fixed: 468027781 
    Change-Id: I8d7c602657e45a8110e695ab4a91b9c4ef6f62aa 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7255782 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    (cherry picked from commit 8564770a55f6a9d1e18bb202ef4ba01d618bb2ac) 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7320487 
    Auto-Submit: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Mathias Bynens <mathias@chromium.org> 
    Reviewed-by: Mathias Bynens <mathias@chromium.org>

```

---

Files:

- M `front_end/core/host/ResourceLoader.ts`
- M `front_end/core/sdk/PageResourceLoader.test.ts`

---

Hash: [db79d590c9e51919e2ca6ff273aae559377d57d3](https://chromiumdash.appspot.com/commit/db79d590c9e51919e2ca6ff273aae559377d57d3)  

Date: Mon Dec 15 07:06:47 2025


---

### ch...@google.com (2026-01-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2026-01-05)

[Bulk Edit]

Please merge to M144 by 10:00 AM PT tomorrow, Jan 6th so we can take it in for M144 Early Stable RC cut.

If it is already merged to M144 and nothing pending, please mark the bug as fixed. 

### ch...@google.com (2026-01-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### wf...@chromium.org (2026-01-21)

Hi - Re: #9. The lower values are because MS have mostly mitigated the NTLM attacks since those previous bugs (which were in 2022), so the impact to users is mitigated. As a mitigated vulnerability the reward values are lower. See <https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules>

Thank you for your contribution to the VRP! Keep the bugs coming!

### ch...@google.com (2026-03-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> mitigated user information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/468027781)*
