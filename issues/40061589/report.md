# Security: Debug check failed: kCanBeWeak || (!IsSmi() == HAS_STRONG_HEAP_OBJECT_TAG(ptr_)).

| Field | Value |
|-------|-------|
| **Issue ID** | [40061589](https://issues.chromium.org/issues/40061589) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Windows |
| **Reporter** | p4...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2022-11-04 |
| **Bounty** | $10,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

The bug seems to be an issue when deoptimizing in maglev. I am also working on analysing it.

Its performance is getting a wrong object from TranslationOpcode::REGISTER [1] in `CreateNextTranslatedValue`.

```
    case TranslationOpcode::REGISTER: {  
      int input_reg = iterator->NextUnsigned();  
      if (registers == nullptr) {  
        TranslatedValue translated_value = TranslatedValue::NewInvalid(this);  
        frame.Add(translated_value);  
        return translated_value.GetChildrenCount();  
      }  
      intptr_t value = registers->GetRegister(input_reg);//[1]  
      Address uncompressed_value = DecompressIfNeeded(value);  
      if (trace_file != nullptr) {  
        PrintF(trace_file, V8PRIxPTR_FMT " ; %s ", uncompressed_value,  
               converter.NameOfCPURegister(input_reg));  
        Object(uncompressed_value).ShortPrint(trace_file);  
      }  
      TranslatedValue translated_value =  
          TranslatedValue::NewTagged(this, Object(uncompressed_value));  
      frame.Add(translated_value);  
      return translated_value.GetChildrenCount();  
    }  

```

So it will crash when checking the correctness of that.

**VERSION**  

V8 version: 28545f7aeac5966ffdf4057f0880f834dccc17c0  

Operating System: Win10

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

Run the attached file in d8 with flag "--predictable --allow-natives-syntax --interrupt-budget=1024 --maglev --fuzzing", it will crash at a SegmentFault or a DCHECK failed.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab.  

Crash State:

=================================================================  

==9116==ERROR: AddressSanitizer: access-violation on unknown address 0x001a1fffffff (pc 0x7ff620039269 bp 0x00c77dbff2a0 sp 0x00c77dbff258 T0)  

==9116==The signal is caused by a READ memory access.  

==9116==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==9116==\*\*\* Most likely this means that the app is already \*\*\*  

==9116==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==9116==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==9116==\*\*\* or produce wrong results. \*\*\*  

==9116==WARNING: Failed to use and restart external symbolizer!

or

# 

# Fatal error in ....\src\objects\tagged-impl.h, line 140

# Debug check failed: kCanBeWeak || (!IsSmi() == HAS\_STRONG\_HEAP\_OBJECT\_TAG(ptr\_)).

# 

# 

# 

#FailureMessage Object: 0000131F95F0AC40

## Attachments

- [test.js](attachments/test.js) (text/plain, 1.5 KB)

## Timeline

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### p4...@gmail.com (2022-11-07)

Addition info: I found the bug seems to related to the commit f471ad0f8aa75eeaa96b5fea3b3faeb32c5c7377.


### p4...@gmail.com (2022-11-07)

[Comment Deleted]

### ke...@chromium.org (2022-11-07)

Thanks for the report, and apologies for the slow triage. Your analysis 

victorgomes@: Can you PTAL?

Clusterfuzz had hit this assert in https://crbug.com/chromium/1359690 but the repro stopped working at some point without a good explanation.

I'm marking this as Impact-None (because maglev) and Severity-High, which assumes possible memory corruption, but would be interested in comment on whether or not that is likely.

### le...@chromium.org (2022-11-09)

Victor can't repro but I can, so I'll take this.

### vi...@chromium.org (2022-11-09)

Assigning this to Leszek.

### gi...@appspot.gserviceaccount.com (2022-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8ceffab2b8fc94a78b2253bcfa419d5c5b37f864

commit 8ceffab2b8fc94a78b2253bcfa419d5c5b37f864
Author: Leszek Swirski <leszeks@chromium.org>
Date: Wed Nov 09 14:00:22 2022

[maglev] Fix deopt input clobbering in CheckMapsWithMigration

CheckMapsWithMigration performs a deferred runtime call, and can eager
deopt after this call. The registers saved by this runtime call might
not include the inputs into the eager deopt, since the register snapshot
is taken after use updates.

We had a similar issue in AttemptOnStackReplacement, where the solution
was to iterate eager deopt inputs and include them in the register
snapshot. We take the same solution here (unified in a helper), though
we may want to consider a less fragile approach.

Bug: v8:7700
Change-Id: I4e13f126af8b3028d8fcb1f0eebbaecae94b8670
Fixed: chromium:1381335
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4016389
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84147}

[modify] https://crrev.com/8ceffab2b8fc94a78b2253bcfa419d5c5b37f864/src/maglev/maglev-ir.cc


### le...@google.com (2022-11-09)

Thanks for the report, this was a tricky bug and your repro made it a lot easier to debug.

### [Deleted User] (2022-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-17)

Congratulations, Bohan Liu! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this tricky issue to us -- nice work! 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-16)

Hello OP, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them.

### gi...@appspot.gserviceaccount.com (2023-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/92d4e663fa8afc74876a39cab46476118a0c9c74

commit 92d4e663fa8afc74876a39cab46476118a0c9c74
Author: Victor Gomes <victorgomes@chromium.org>
Date: Thu Nov 09 10:31:59 2023

[maglev] Add eager deopt registers to register snapshot

We proactively add the deopt registers to the register snapshot in
nodes that can eagerly deopt and do a deferred call.

Currently, this happens to these nodes:
- CheckedObjectToIndex
- CheckMapsWithMigration
- CheckValueEqualsString
- MaybeGrowAndEnsureWritableFastElements
- TryOnStackReplacement

In 4 of these nodes we were already adding the deopt registers
in an ad-hoc fashion. {CheckedObjectToIndex} currently does not
need, since it is *currently* guaranteed that the eager deopt
registers are subset of the live registers due to the lifetime
extension of deopt inputs. This could easily change in the future
though. This CL guarantees that we don't shoot ourselves in the foot.

Bug: chromium:1381335, chromium:1500857

Change-Id: I213f2f02861c5911bc0da3cfb1f5c8189928efbd
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5013477
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Auto-Submit: Victor Gomes <victorgomes@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#90831}

[modify] https://crrev.com/92d4e663fa8afc74876a39cab46476118a0c9c74/src/maglev/maglev-regalloc.cc
[modify] https://crrev.com/92d4e663fa8afc74876a39cab46476118a0c9c74/src/maglev/maglev-ir-inl.h
[modify] https://crrev.com/92d4e663fa8afc74876a39cab46476118a0c9c74/src/maglev/maglev-ir.cc


### is...@google.com (2023-11-09)

This issue was migrated from crbug.com/chromium/1381335?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061589)*
