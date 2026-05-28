# Security: CRX3 File Signature Verification Bypass via Embedded ZIP64 Payload

| Field | Value |
|-------|-------|
| **Issue ID** | [41485950](https://issues.chromium.org/issues/41485950) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Cast, Internals>Installer>Components, Internals>Updater, Platform>Extensions |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ma...@sodium24.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2023-12-20 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**

A vulnerability has been found in Google Chrome's CRX3 file signature validation, which would allow an attacker to embed their own malicious payload inside a legitimate CRX extension with a valid signature and key. The CRX file will still contain valid signatures, but the attacker-controlled embedded files will be extracted by Chrome whenever the CRX file is unpacked.

This vulnerability exists due to unexpected file handling by the Minizip library, which allows earlier-occurring portions of a ZIP file to be used instead of later-occurring portions of the file. Specifically, if an EOCD64 (64-bit end-of-central-directory locator) token is present earlier in the file, it will be used instead of a later-occuring EOCD (32-bit end-of-central-directory locator) token. Since the CRX file contains a protobuf header which is mostly unsigned and can be thus be arbitrarily-controlled by an attacker, the attacker can embed their own ZIP64 payload in the CRX file header, ensuring it contains a valid EOCD64 token. This can be done without modifying the signature of the file, since only the unsigned portions of the file header have been modified by the attacker.

When Minizip extracts the file, as long as the original, intended, payload is less than 64kB, Minizip will locate the EOCD64 token in the header portion of the file, and extract the attacker-controlled, unsigned, ZIP64 payload instead of the intended, signed, ZIP payload.

SOURCE CODE ANALYSIS

CRX file verification code is mostly contained within crx\_verifier.cc (<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/crx_file/crx_verifier.cc>), with the protobuf header of the file documented in crx3.proto (<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/crx_file/crx3.proto>).

The comment on "signed\_header\_data" indicates how the signature verification is performed:

// All proofs in this CrxFile message are on the value  

// "CRX3 SignedData\x00" + signed\_header\_size + signed\_header\_data +  

// archive, where "\x00" indicates an octet with value 0, "CRX3 SignedData"  

// is encoded using UTF-8, signed\_header\_size is the size in octets of the  

// contents of this field and is encoded using 4 octets in little-endian  

// order, signed\_header\_data is exactly the content of this field, and  

// archive is the remaining contents of the file following the header.  

optional bytes signed\_header\_data = 10000;

The "VerifyCrx3" function in crx\_verifier.cc is used to extract the header and perform this hashing for signature validation. Notably, all fields in the header, with the exception of "signed\_header\_data", are exempt from signature validation.

After a CRX file signature is successfully verified, the Minizip library contained in Zlib is used to perform the extraction (<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/third_party/zlib/contrib/minizip/unzip.c>).

The "unzOpenInternal" function, on line 580, is responsible for opening and performing initial parsing of the ZIP file. On line 619, Minizip first attempts to find an EOCD64 token ("PK\x06\x07") stored within the last 64kB of the file:

```
central_pos = unz64local_SearchCentralDir64(&us.z_filefunc,us.filestream);  

```

Only if this search is unsuccessful, or cannot be successfully validated, is a 32-bit EOCD token ("PK\x05\x06") found as a fallback on line 681:

```
central_pos = unz64local_SearchCentralDir(&us.z_filefunc,us.filestream);  

```

As long as the original ZIP payload is < 64kB, an attacker's valid ZIP64 payload within the file header containing "PK\x06\x07" will be found and used by Minizip's "unz64local\_SearchCentralDir64" function.

**VERSION**  

Chrome Version: 119.0.6045.159 (Official Build) (64-bit)  

Operating System: Ubuntu 20.04

**REPRODUCTION CASE**

1. Download the following attached file:
   
   - "my\_sample\_app.crx": sample Chrome extension
   - "my\_sample\_app.xml": malicious update manifest file
   - "payload.zip": malicious payload to inject into the sample extension
   - "payload\_embedder.py", "crx3\_pb2.py": Python script and supporting files to create the attack CRX file
   
   The extension, "my\_sample\_app.crx", is signed with a CRX ID of "pgjekmobohkakcbceofnhpgjolabonjl".
2. Navigate to chrome://extensions and enable developer mode. Drag "my\_sample\_app.crx" to the browser window to install it.  
   
   Note that this step could be similarly completed using enterprise policy files instead of enabling developer mode (<https://support.google.com/chrome/a/answer/9867568>).
   
   The installed extension is set up to use a local update server of "<http://localhost:8000/my_sample_app.xml>"
3. Verify the extension has been successfully installed. When navigating to any website, such as <https://www.google.com>, you should see the following green banner:
   
   Sample extension has been installed! :)
4. Create the attack CRX file ("attack.crx") with an embedded ZIP64 payload by running the following:
   
   $ python3 payload\_embedder.py my\_sample\_app.crx payload.zip attack.crx
5. Start up a Python http server to host the attack files:
   
   $ python3 -m http.server 8000
6. Close and restart Chrome to trigger an immediate extension update. The extension will update to the malicious version.
7. Verify the malicious extension has been successfully installed. When navigating to any website, such as <https://www.google.com>, you will see the following red banner:
   
   Page contents have been pwned! :(

POSSIBLE ATTACK SCENARIOS

**-------------------------** ---------------------------------  

Attacking a self-hosted enterprise extension (unmitigated)  

**-------------------------** ---------------------------------

A likely attack scenario for this vulnerability would be the case where an enterprise extension, self-hosted outside of the Chrome Web Store, has been made available to company employees with an update URL set to an HTTP server on the company's intranet. An employee leaves the building with their laptop and heads over to a coffee shop. A local attacker, also in this coffee shop, sets up their IP or host name to match the company's internal update server. The next time Chrome runs extension updates on the employee's device, it will download the maliciously modified extension from the attacker's device. Because it still contains a valid signature, the employee's laptop will upgrade to the malicious extension.

**-------------------------** --------------------------------------------  

Attacking Chrome Web Store (CWS) hosted extensions (highly mitigated)  

**-------------------------** --------------------------------------------

Mitigations:

1. Would require HTTPS MITM.
2. Chrome immediately detects an installed attacker-modified extension as being corrupt and disables it due to it containing an invalid "verified\_contents.json" file, which is needed for CWS-installed extensions.

**-------------------------** ------------------------------  

Attacking internal Chrome components (highly mitigated)  

**-------------------------** ------------------------------

Mitigations:

1. Would require HTTPS MITM.
2. Chrome uses the Omaha CUP protocol (<https://chromium.googlesource.com/chromium/src.git/+/master/docs/updater/protocol_3_1.md>) which signs each HTTPS request and response body. This heavily mitigates any tampering from taking place.

**-------------------------** -------------  

Windows user to system LPE (near-miss)  

**-------------------------** -------------

A low-privileged executable can use the "Google Chrome Elevation Service" to run a CRX file containing an executable as the highly-privileged "nt authority\system" user. The CRX file is first validated to ensure it has been signed by the correct hard-coded signature ("GetRecoveryCRXHash" from <https://github.com/chromium/chromium/blob/main/chrome/elevation_service/elevated_recovery_impl.cc>).

This scenario could not be demonstrated \*only\* because the smallest publicly-available CRX file signed with this key was found to be 73.2kB (<https://github.com/google/omaha/blob/main/omaha/testing/unittest_support/CodeRed.crx3>), with a payload approximately 7kB too big to be exploitable.

If the Chrome team can sign a slightly smaller CRX file with this same private key, you may be able to demonstrate the LPE with the following steps:

1. Download the attached "windows\_lpe\_poc.exe", "windows\_lpe\_payload.zip", and "windows\_lpe\_poc.bat". Place these files in a directory "C:\poc" along with the previously downloaded "payload\_embedder.py" and "crx3\_pb2.py".
2. Inject the "windows\_lpe\_payload.zip" payload into the signed CRX file ("CodeRed.crx") as follows:
   
   $ python3 payload\_embedder.py CodeRed.crx windows\_lpe\_payload.zip CodeRedAttack.crx
3. Run "windows\_lpe\_test.exe" as follows to perform the COM call necessary for LPE (note that the full path of "CodeRedAttack.crx" must be used):
   
   $ .\windows\_lpe\_poc.exe C:\poc\CodeRedAttack.crx
4. Verify that "windows\_lpe\_poc.bat" has run, placing the output of several commands including "whoami" into "C:\poc\output.txt". This file should indicate that the attacker's code was running as the "nt authority\system" user.

SUGGESTED PATCH

A simple yet effective way to patch this vulnerability would be to add an additional verification to the "VerifyCrx3" function, in order to detect any EOCD or EOCD64 token embedded within the header bytes. Since "VerifyCrx3" is called every time a CRX3 file has its signature validated, there is little chance of missing any affected code paths within the Chromium codebase. The header size in a CRX3 file is typically < 2kB, so this would have very minimal performance impact.

diff --git a/components/crx\_file/crx\_verifier.cc b/components/crx\_file/crx\_verifier.cc  

index 2378aa5a95..b0f5559cc3 100644  

--- a/components/crx\_file/crx\_verifier.cc  

+++ b/components/crx\_file/crx\_verifier.cc  

@@ -10,6 +10,7 @@  

#include <memory>  

#include <set>  

#include <utility>  

+#include <algorithm>

#include "base/base64.h"  

#include "base/files/file.h"  

@@ -109,6 +110,15 @@ VerifierResult VerifyCrx3(  

header\_size) {  

return VerifierResult::ERROR\_HEADER\_INVALID;  

}  

+

- // Detect any attempt to embed a malicious ZIP EOCD or EOCD64 token within the header bytes
- const uint8\_t eocd[] = {'P', 'K', 0x05, 0x06};
- const uint8\_t eocd64[] = {'P', 'K', 0x06, 0x07};
- if (std::search(header\_bytes.begin(), header\_bytes.end(), eocd, eocd + sizeof(eocd)) != header\_bytes.end())
- return VerifierResult::ERROR\_HEADER\_INVALID;
- if (std::search(header\_bytes.begin(), header\_bytes.end(), eocd64, eocd64 + sizeof(eocd64)) != header\_bytes.end())
- return VerifierResult::ERROR\_HEADER\_INVALID;
- CrxFileHeader header;  
  
  if (!header.ParseFromArray(header\_bytes.data(), header\_size))  
  
  return VerifierResult::ERROR\_HEADER\_INVALID;

FIRST AFFECTED GIT COMMIT

The CRX2 format (<https://chromium.googlesource.com/chromium/src/+/8c83fe076ebe86c04e6d703be2bfb2f2e8729158/components/crx_file/crx_file.h>) appears to only support a single key and signature in the file header, so it is unlikely an attacker would have enough control over this header to perform the necessary payload injection without invalidating the existing signature.

Thus, it seems this vulnerability was introduced when the CRX3 format was first implemented, in the following commit:  

<https://chromium.googlesource.com/chromium/src/+/11f044437561f28e16d0a2549714d860310fb3fd>

At this point, the verifier code was expanded to verify both CRX2 and CRX3 files, including CRX3 files with a malicious ZIP64 payload embedded in the header.

**CREDIT INFORMATION**

Reporter credit: Malcolm Stagg (@malcolmst) of SODIUM-24, LLC

## Attachments

- [payload_embedder.py](attachments/payload_embedder.py) (text/plain, 7.3 KB)
- [crx3_pb2.py](attachments/crx3_pb2.py) (text/plain, 6.6 KB)
- [my_sample_app.crx](attachments/my_sample_app.crx) (application/octet-stream, 47.2 KB)
- [my_sample_app.xml](attachments/my_sample_app.xml) (text/plain, 266 B)
- [payload.zip](attachments/payload.zip) (application/octet-stream, 46.9 KB)
- [windows_lpe_poc.exe](attachments/windows_lpe_poc.exe) (application/octet-stream, 145.5 KB)
- [windows_lpe_payload.zip](attachments/windows_lpe_payload.zip) (application/octet-stream, 60.9 KB)
- [windows_lpe_poc.bat](attachments/windows_lpe_poc.bat) (text/plain, 114 B)

## Timeline

### [Deleted User] (2023-12-20)

[Empty comment from Monorail migration]

### bb...@google.com (2023-12-20)

I have verified the first case, not the subsequent windows one. 

Setting security severity high initially. 

[Monorail components: Internals>Cast Platform>Extensions]

### bb...@google.com (2023-12-20)

[Empty comment from Monorail migration]

### bb...@google.com (2023-12-20)

[Empty comment from Monorail migration]

### bb...@google.com (2023-12-20)

@waffles, I'm initially assigning to you, please reassign as appropriate if this isn't for you.

### wa...@chromium.org (2023-12-20)

[Empty comment from Monorail migration]

[Monorail components: Internals>Installer>Components Internals>Updater]

### [Deleted User] (2023-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2023-12-20)

Thanks for reporting.

I'm happy that other defenses (CUP, HTTPS) mitigate most of the remote attacks, and that we are fortunate on the LPE. I'm uncertain how common it is for enterprises to self-host extensions over HTTP (not HTTPS).

I think it is likely we will implement the suggested solution at least for the short term, because it has little performance impact and isn't very likely (I hope) to have false positives. I am concerned that it doesn't fully address what I see as the underlying issue: we pass some unverified bytes to the unzipper, and yet we fully trust the unzipper's output.

A solution for that underlying issue could be for CRX verification to output the verified archive (i.e. transform CRX -> optional<ZIP>). Perhaps this could be done in-place (overwriting the input file) but if so at least some callers would need to make a copy of the CRX for caching prior to validation. I'm uncertain about other options to pass streams, spans, offsets, etc into the unzip library but they may be worth exploring. This will take time, and I prefer to land the suggested change in the meanwhile.

### tj...@chromium.org (2023-12-20)

[Empty comment from Monorail migration]

### ma...@sodium24.com (2023-12-20)

Thank you for looking into my report!

For what it’s worth, I also looked at the Omaha codebase and it does not seem to be vulnerable to this issue, since it first strips away the header bytes before unzipping as you suggest: https://github.com/google/omaha/blob/b6b518403a231349a0fce07eecf8a966ca3ae87e/omaha/third_party/chrome/files/src/components/crx_file/crx_verifier.cc#L489

Completely agree that removing the header will ultimately be the best way to patch it, but it seemed likely to be a larger change which may hit some edge cases. 

### gi...@appspot.gserviceaccount.com (2023-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/989eddc218273a46801d3489f5eb30b7603580fb

commit 989eddc218273a46801d3489f5eb30b7603580fb
Author: Joshua Pawlicki <waffles@chromium.org>
Date: Wed Dec 20 22:33:06 2023

crx_file: Error early for CRXs with ZIP markers in header.

Bug: 1513379
Change-Id: I029b4f15778df0c150866b1f49a9b5b2924690ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5141787
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Sorin Jianu <sorin@chromium.org>
Reviewed-by: Sorin Jianu <sorin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1239849}

[modify] https://crrev.com/989eddc218273a46801d3489f5eb30b7603580fb/components/crx_file/crx_verifier.cc


### [Deleted User] (2023-12-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2024-01-02)

Adding merge request for 989eddc218273a46801d3489f5eb30b7603580fb

### [Deleted User] (2024-01-02)

Merge review required: M121 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-02)

Merge review required: M120 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2024-01-02)

1. Yes - security fix.
2. https://chromium-review.googlesource.com/c/chromium/src/+/5141787
3. Yes.
4. Not a new feature.
5. N/A
6. Does not require manual verification by the test team.

### wa...@chromium.org (2024-01-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-04)

120 and 121 merges approved for https://crrev.com/c/5141787
please merge this fix to M120 Stable / branch 6099 (by EOD today for the fix to be included in next week's Stable channel update) and M121 Beta / branch 6167 at your earliest convenience -- thank you


### [Deleted User] (2024-01-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3223ac2d9da5b09009127d6ff7ef38fd7b0a5a78

commit 3223ac2d9da5b09009127d6ff7ef38fd7b0a5a78
Author: Joshua Pawlicki <waffles@chromium.org>
Date: Thu Jan 04 20:49:10 2024

crx_file: Error early for CRXs with ZIP markers in header.

Bug: 1513379
Change-Id: I029b4f15778df0c150866b1f49a9b5b2924690ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5141787
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Sorin Jianu <sorin@chromium.org>
Reviewed-by: Sorin Jianu <sorin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1239849}
(cherry picked from commit 989eddc218273a46801d3489f5eb30b7603580fb)

# Presubmit seems broken (not by this CL)

No-Presubmit: true
Change-Id: I029b4f15778df0c150866b1f49a9b5b2924690ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5169431
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Reviewed-by: Sorin Jianu <sorin@chromium.org>
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Cr-Commit-Position: refs/branch-heads/6167@{#1027}
Cr-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}

[modify] https://crrev.com/3223ac2d9da5b09009127d6ff7ef38fd7b0a5a78/components/crx_file/crx_verifier.cc


### [Deleted User] (2024-01-04)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2024-01-04)

1. No.
2. No.

### gi...@appspot.gserviceaccount.com (2024-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d93cc7978dd45ea73b73037afdb268f99e7f27d4

commit d93cc7978dd45ea73b73037afdb268f99e7f27d4
Author: Joshua Pawlicki <waffles@chromium.org>
Date: Thu Jan 04 21:25:50 2024

crx_file: Error early for CRXs with ZIP markers in header.

(cherry picked from commit 989eddc218273a46801d3489f5eb30b7603580fb)

Bug: 1513379
Change-Id: I029b4f15778df0c150866b1f49a9b5b2924690ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5141787
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Sorin Jianu <sorin@chromium.org>
Reviewed-by: Sorin Jianu <sorin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1239849}
No-Presubmit: True
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5169629
Cr-Commit-Position: refs/branch-heads/6099@{#1691}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/d93cc7978dd45ea73b73037afdb268f99e7f27d4/components/crx_file/crx_verifier.cc


### rz...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-08)

setting a next action date for coordinated disclosure based on when the fix for this issue was landed 

### am...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-10)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2024-01-10)

[VRP panel] thanks for this excellent report. great find!

### am...@google.com (2024-01-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### rz...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-11)

Congratulations Malcolm! The Chrome VRP Panel has has decided to award you $5,000 for this high-quality report of an exploit mitigation bypass + $1,000 patch bonus for providing a detailed pathway to mitigation. While you didn't technically provide a functional exploit, the thorough analysis you provided to detail the exploitability of this issue in the various ways, including the ways which they were mitigated, felt substantial enough to consider that categorization and the reward amount as appropriate for this report. 
All of us on the panel were very impressed by this finding and your reporting of it.

In terms of reward, a member of our Google finance team from the p2p-vrp team will be in touch with you soon to arrange payment. 
Thank you for your efforts in discovering and reporting this issue to us -- very excellent work! 


### [Deleted User] (2024-01-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2024-01-11)

1. Just http://ag/q/topic:%222024_JAN_SEC_LTS_114_R%22
2. Low, no conflicts
3. 120, 121
4. Yes

### ma...@sodium24.com (2024-01-11)

Thank you so much Amy, @wfh, and all for your kind words and the generous reward! Really appreciate everyone’s great work handling this issue quickly and efficiently. 

### na...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### na...@google.com (2024-01-11)

LTS-114 will pick up this merge once the fix is released in M120 Stable.

### am...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### na...@google.com (2024-01-22)

Merge approved for LTS-114

### gi...@appspot.gserviceaccount.com (2024-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/51a170a8a9bac5039e75553047216eee5d476eb5

commit 51a170a8a9bac5039e75553047216eee5d476eb5
Author: Joshua Pawlicki <waffles@chromium.org>
Date: Tue Jan 23 14:24:36 2024

[M114-LTS] crx_file: Error early for CRXs with ZIP markers in header.

(cherry picked from commit 989eddc218273a46801d3489f5eb30b7603580fb)

Bug: 1513379
Change-Id: I029b4f15778df0c150866b1f49a9b5b2924690ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5141787
Commit-Queue: Joshua Pawlicki <waffles@chromium.org>
Auto-Submit: Joshua Pawlicki <waffles@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Sorin Jianu <sorin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1239849}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5177067
Reviewed-by: Joshua Pawlicki <waffles@chromium.org>
Reviewed-by: Michael Ershov <miersh@google.com>
Commit-Queue: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1671}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/51a170a8a9bac5039e75553047216eee5d476eb5/components/crx_file/crx_verifier.cc


### rz...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1513379?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Cast, Internals>Installer>Components, Internals>Updater, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-27)

The NextAction date has arrived: 2024-03-27 
 To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### am...@chromium.org (2024-03-27)

The reporter of this issue has been cooperatively engaging with us throughout the reporting and disclosure of this issue. They would like to publish a blog post about this bug at this time. The fix for this issue landed on 20 December 2023 and shipped in Stable update of M120. Current Stable is M123 and Extended Stable is M120.
We, therefore, believe it to be acceptable to open this issue a couple of days early to allow for their post to be published at this time and have opened this issue for disclosure in tandem to that.

Thank you again, Malcolm, for your contributions and your patience to allow this fix to be matriculated to users in Stable updates!

### am...@gmail.com (2024-11-12)

deleted

### am...@gmail.com (2024-11-12)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41485950)*
