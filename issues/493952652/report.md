# heap-use-after-free READ in ElementRuleCollector InputRules path, page load, MiraclePtr unprotected

| Field | Value |
|-------|-------|
| **Issue ID** | [493952652](https://issues.chromium.org/issues/493952652) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 146.0.7680.x |
| **Reporter** | nn...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-03-18 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. Save the attached poc.html to disk
2. Open poc.html in Chrome (no flags required, works with file:// protocol)
3. Renderer crashes on page load ? no user interaction required

Tested on:

- Chrome 146.0.7680.x stable (Linux x64) ? ASAN build crashes
- Chrome 147.0.7722.0 ? ASAN build crashes
- Current main/ToT vulnerable code unchanged

The PoC requires two <style> elements with input[style][type="text"] selectors  

(creating two RuleSet bundles) and JavaScript that sets an inline style then  

forces style resolution via getComputedStyle().

# Problem Description

heap-use-after-free READ of size 8 in blink::AtomicString::LowerASCII(), called  

from ElementRuleCollector::CollectMatchingRulesInternal() on the InputRules path.

Root cause: element\_rule\_collector.cc (~line 952) takes a const AtomicString&  

reference into Vector<Attribute> heap storage. During CSS rule matching, the  

[style] selector triggers SynchronizeAttributeHinted(kStyleAttr), which appends  

the lazy style attribute via AppendAttributeInternal(). This grows the vector,  

calling ReallocateBuffer() which frees the old buffer. The reference is now  

dangling. The next bundle iteration calls input\_type.LowerASCII() ? reading  

StringImpl\* from offset 24 of the freed 32-byte region.

MiraclePtr Status: NOT PROTECTED. No raw\_ptr<T> wraps this allocation.

The freed buffer is in PartitionAlloc's 32-byte bucket. The dangling read  

dereferences a StringImpl\* at offset 24. If the slot is reclaimed via heap  

spray, the attacker controls what LowerASCII() reads, influencing which CSS  

InputRules are matched. Additionally, LowerASCII(AtomicString source) receives  

source by value ? the copy constructor calls AddRef() on the attacker-controlled  

StringImpl\*, producing a 4-byte write (refcount increment) at an  

attacker-influenced address.

Fix: change const AtomicString& to const AtomicString (value copy) at line ~952.

# Additional Comments

Attachments:

- poc.html: minimized 10-line PoC, crashes on page load, no flags
- asan\_trace.txt: full symbolized ASAN trace from Chrome 146 stable
- controlled\_uaf\_demo.cc: standalone C++ demonstrating controlled read/write
- README.md: full root cause analysis with memory layout and exploitability

# Summary

heap-use-after-free READ in ElementRuleCollector InputRules path, page load, MiraclePtr unprotected

# Custom Questions

#### Type of crash:

Renderer (tab) crash

#### Crash state:

ERROR: AddressSanitizer: heap-use-after-free on address 0x7b795a082658  

READ of size 8 at 0x7b795a082658 thread T0 (chrome)

Crash stack:  

#0 blink::AtomicString::LowerASCII() const  

#1 blink::ElementRuleCollector::CollectMatchingRulesInternal<false>()  

#2 blink::ScopedStyleResolver::CollectMatchingElementScopeRules()  

#3 blink::StyleResolver::MatchAuthorRules()  

#4 blink::StyleResolver::MatchAllRules()  

#5 blink::StyleResolver::ApplyBaseStyleNoCache()  

#6 blink::StyleResolver::ResolveStyle()  

#7 blink::Element::OriginalStyleForLayoutObject()

Freed by:  

#0 free  

#1 blink::Vector<blink::Attribute, 4u>::ReallocateBuffer()  

#2 blink::Vector<blink::Attribute, 4u>::ExpandCapacity()  

#3 blink::Vector<blink::Attribute, 4u>::AppendSlowCase[blink::Attribute](javascript:void(0);)()  

#4 blink::MutableAttributeCollection::Append()  

#5 blink::Element::AppendAttributeInternal()  

#6 blink::Element::SetSynchronizedLazyAttribute()  

#7 blink::Element::SynchronizeStyleAttributeInternal() const
#8 blink::Element::SynchronizeAttributeHinted() const  

#9 blink::ElementRuleCollector::CollectMatchingRulesForListInternal<false, false>()

0x7b795a082658 is located 24 bytes inside of 32-byte region [0x7b795a082640,0x7b795a082660)

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.

Full symbolized ASAN trace attached as asan\_trace.txt.

#### Reporter credit:

Anonymous

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 370 B)
- [asan_trace.txt](attachments/asan_trace.txt) (text/plain, 22.3 KB)
- [controlled_uaf_demo.cc](attachments/controlled_uaf_demo.cc) (text/x-c++src, 7.4 KB)
- [README.md](attachments/README.md) (text/markdown, 7.5 KB)
- [poc_addref_write.html](attachments/poc_addref_write.html) (text/html, 3.2 KB)
- [asan_head147_trace.txt](attachments/asan_head147_trace.txt) (text/plain, 43.1 KB)
- [asan_16bundle_trace.txt](attachments/asan_16bundle_trace.txt) (text/plain, 23.5 KB)
- [escalation_inputrules_data_exfil.html](attachments/escalation_inputrules_data_exfil.html) (text/html, 6.5 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4644379058798592.

### 24...@project.gserviceaccount.com (2026-03-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-19)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/beb11ee6e2b1e4f3d58f45ef96fa8c39fb097ae8 (Add a separate selector bucket for input[type="..."] rules.

Our UA stylesheet has 40+ rules of the form input[type="..." i]
(possibly with some pseudos after), which are currently bucketed
into the [type] attribute bucket, which nearly every input element
will match. This means that every input element needs to run
selector matching against UA rules meant for date pickers, telephone
numbers, password fields, etc., no matter what the actual type is.

Since this is an important special case for us, we add a separate
bucket for such rules, keyed by the type (so the key becomes
“checkbox”, “text”, “password”, etc.). There are still a couple of
rules that go into more generic buckets, such as the input:not([type...
rules, or some related to pseudos, but at least it's a significant
win in how much we can reject.

As an example, for a single Speedometer3 run, of all selectors that
were previously rejected in selector matching (i.e., passed bucketing
and both forms of fast-reject), ~40–45% of them are now rejected in
bucketing instead (i.e., in practice not looked at at all). There is
still theoretical potential for better bucketing and/or fast-rejection,
though; our selector matching reject rate went down from ~58% to
~44%, but it's still nowhere near zero.

We could get rid of ~4% more if we rewrote the two input:not() rules to
be positive instead, but then they would no longer match <input>s with
invalid type="" (which should generally otherwise behave like
type="text"). If so, we'd probably need to make an internal selector
that tests for the effective type, but then it would be effectively
UA-only.

We also fixed an issue where exact attribute matches would not be
properly registered (and bucketed) as such if there was a later selector
involved, e.g. in cases like `input[type="foo" i]:disabled`. (The code
looking at :disabled would reset the “is_exact_attr” boolean.) This
didn't mean all that much earlier (it was only used for an optimization
related to the empty string in Aho-Corasick matching), but now, it is
required for this new bucketing, so we fix it.

Style perftest (Zen 3, LTO but no PGO):

  Initial style (µs)     Before     After    Perf      95% CI (BCa)
  =================== ========= ========= ======= =================
  ECommerce                5422      5395   +0.5%  [ +0.3%,  +0.8%]
  Encyclopedia            41942     41666   +0.7%  [ -0.3%,  +1.5%]
  Extension               55441     55000   +0.8%  [ +0.5%,  +1.1%]
  News                    21868     21413   +2.1%  [ +1.9%,  +2.5%]
  Search                   7665      7588   +1.0%  [ +0.8%,  +1.3%]
  Social1                 13782     13622   +1.2%  [ +0.9%,  +1.8%]
  Social2                  8602      8508   +1.1%  [ +0.9%,  +1.5%]
  Sports                  26895     26614   +1.1%  [ +0.3%,  +1.9%]
  Video                   17618     17459   +0.9%  [ +0.6%,  +1.2%]
  Geometric mean                            +1.0%  [ +0.8%,  +1.3%]

  Recalc style (µs)      Before     After    Perf      95% CI (BCa)
  =================== ========= ========= ======= =================
  ECommerce                2887      2871   +0.6%  [ +0.2%,  +0.9%]
  Encyclopedia            33435     33347   +0.3%  [ -0.0%,  +0.6%]
  Extension               43835     43410   +1.0%  [ +0.6%,  +1.4%]
  News                    10937     10619   +3.0%  [ +2.7%,  +3.5%]
  Search                   2788      2765   +0.8%  [ +0.4%,  +1.2%]
  Social1                  6796      6690   +1.6%  [ +1.2%,  +2.0%]
  Social2                  4155      4112   +1.1%  [ +0.7%,  +1.5%]
  Sports                  12621     12535   +0.7%  [ +0.3%,  +1.0%]
  Video                    7066      7030   +0.5%  [ +0.2%,  +0.8%]
  Geometric mean                            +1.0%  [ +0.8%,  +1.3%]

Speedometer3 (M1 Pinpoint, LTO but no PGO, significant results at
99% CI only):

  NewsSite-Next                               [ -0.5%,  -0.1%]
  NewsSite-Nuxt                               [ -0.5%,  -0.1%]
  TodoMVC-JavaScript-ES6-Webpack-Complex-DOM  [ -1.1%,  -0.4%]
  TodoMVC-jQuery                              [ -1.1%,  -0.5%]
  TodoMVC-React-Complex-DOM                   [ -1.3%,  -0.6%]
  TodoMVC-React-Redux                         [ -1.2%,  -0.6%]
  TodoMVC-Backbone                            [ -1.4%,  -0.9%]
  TodoMVC-WebComponents                       [ -1.8%,  -1.2%]
  TodoMVC-Vue                                 [ -1.8%,  -1.3%]
  TodoMVC-Svelte-Complex-DOM                  [ -3.4%,  -1.7%]
  TodoMVC-Preact-Complex-DOM                  [ -4.0%,  -2.0%]
  TodoMVC-Lit-Complex-DOM                     [ -3.4%,  -2.8%]

  Score                                       [ +0.7%,  +1.1%]

Bug: 402346409
Change-Id: I7e6cdd246595901583d784cbf563cc37b528d1f5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6632977
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1473469}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2026-03-19)

Detailed Report: https://clusterfuzz.com/testcase?key=4644379058798592

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x74c55c4f5c98
Crash State:
  blink::AtomicString::ToAsciiLower
  bool blink::ElementRuleCollector::CollectMatchingRulesInternal<false>
  blink::ScopedStyleResolver::CollectMatchingElementScopeRules
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1473467:1473473

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4644379058798592

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### se...@chromium.org (2026-03-19)

This sounds like a duplicate of 492735384, which was fixed a couple of days ago.

### se...@chromium.org (2026-03-19)

Apparent duplicate, analysis looks confused, claims code is unchanged when it's not. Closing as invalid.

### nn...@gmail.com (2026-03-19)

Hello sesse &  team.
I would kindly ask for a reopen, as I provide more evidence.
The attached PoC (poc_addref_write.html) demonstrates 30 AddRef/Release WRITE operations through the dangling reference per page load, zero flags required.              
 
This bug was closed as a duplicate of 492735384, but the fix for that bug (commit 515ce02da3726) only patches the AttrRules path. 
The InputRules path at lines 950-964 is identical on HEAD zero commits touch it:                                       
                                                                                          
  $ git log 515ce02da3726..HEAD -- third_party/blink/renderer/core/css/element_rule_collector.cc                                 
  (empty)                                                                                                                        
                                                                                                                                 
  The one-character difference:                                                                                                  
                                                                                                                                 
  FIXED (AttrRules, line 923):                                                                                                   
  const AtomicString lower_name =  value copy                                                                                   
                                                              
  UNFIXED (InputRules, line 952):                                                                                                
  const AtomicString& input_type =  dangling reference            
                                                                                                                                 
  ASAN on Chrome 147 HEAD confirms heap-use-after-free in AtomicString::LowerASCII() through the InputRules path. MiraclePtr     
  Status: NOT PROTECTED.                                                          
                                                                                                                                        

### ch...@google.com (2026-03-20)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-03-20)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-03-20)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-03-20)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-03-20)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-03-20)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-03-20)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### se...@chromium.org (2026-03-20)

Reopening to investigate.

### se...@chromium.org (2026-03-20)

The line numbers given don't match up at all, but the PoC triggers ASAN.

### nn...@gmail.com (2026-03-20)

Re: line numbers

The report referenced `refs/remotes/branch-heads/7680` (Chrome 146 stable). The fix at `515ce02da3726` added ~5 lines to the AttrRules section, shifting the InputRules code from line 952 to ~957. Apologies for the confusion.

Re: why the PoC still triggers ASAN

The fix at `515ce02da3726` correctly addressed the `AttrRules` dangling reference:

```
// BEFORE (vulnerable):
const AtomicString& lower_name = ...
// AFTER (fixed):
const AtomicString lower_name = ...
//                 ^ removed &, now a value copy

```

But the `InputRules` path (line ~957 post-fix) still has the same pattern, unfixed:

```
if (const AtomicString& input_type =
//                     ^ dangling reference
        element.getAttribute(html_names::kTypeAttr);
    !input_type.IsNull()) {
  for (const auto bundle : match_request.RuleSetsWithInputRules()) {
    CollectMatchingRulesForList(
        bundle.rule_set->InputRules(input_type.ToAsciiLower()), ...);
//                                 ^^^^^^^^^^^ UAF read here
  }
}

```

`input_type` is `const AtomicString&` ? a reference into `Vector<Attribute>` backing store. When `CollectMatchingRulesForList` evaluates the `[style]` selector, `SynchronizeStyleAttributeInternal()` appends the style attribute ? `ReallocateBuffer()` frees the old buffer ? `input_type` dangles. The next bundle's `input_type.ToAsciiLower()` dereferences freed memory.

The one-character fix:

```
if (const AtomicString input_type =
//                    ^ remove &

```

Rules matching `input[style][type="text"]` are bucketed exclusively into `InputRules` via `rule_set.cc` (the `input+type+exact` early return), so `has_bucket_for_style_attr_` is never set ? `NeedStyleSynchronized()` returns false ? no pre-synchronization occurs before matching.

### dx...@google.com (2026-03-20)

Project: chromium/src  

Branch:  main  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7686835>

Fix another use-after-free with lazy style attributes.

---


Expand for full commit details
```
     
    This is a similar problem as regular attribute checks, just for 
    the special case of input type="" (which is a similar but separate 
    path). 
     
    Style perftest and Speedometer3 are neutral. 
     
    Fixed: 493952652 
    Change-Id: I264503545c345325e6d21afa0726f524bb9394b8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686835 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602570}

```

---

Files:

- M `third_party/blink/renderer/core/css/element_rule_collector.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-values/crashtests/chrome-bug-493952652.html`

---

Hash: [d8b01057f740d3bb0ec880b34372da63147c2521](https://chromiumdash.appspot.com/commit/d8b01057f740d3bb0ec880b34372da63147c2521)  

Date: Fri Mar 20 14:22:02 2026


---

### ch...@google.com (2026-03-21)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-21)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1602570) appears to be after stable branch point (1582197).

Requesting merge to beta (M147) because latest trunk commit (1602570) appears to be after beta branch point (1596535).

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2026-03-21)

ClusterFuzz testcase 4644379058798592 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1602565:1602597

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-21)

Merge review required: M147 is already shipping to beta.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-21)

Merge review required: M146 is already shipping to stable.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### se...@chromium.org (2026-03-23)

1. Security fix (use-after-free)
2. <https://chromium-review.googlesource.com/7686835>
3. No crashes on Canary from what I know
4. No
5. N/A
6. No

### dr...@chromium.org (2026-03-23)

No crashes in Canary, approved to merge to M146 and M147.

### nn...@gmail.com (2026-03-24)

Thank you for that fast patch. It seems complete and I am unable to get around it.

I would still like add more impact (as it is still live) (if accepted by the panel).
The attached PoC leaks all input field values credit cards, CSRF tokens, SSNs, passwords 100% reliably.

The :has() pseudo-class forces cross-element style evaluation DURING the dangling reference window in CollectMatchingRulesForList. This gives attacker-controlled CSS rule injection the attacker decides which CSS rules apply to which inputs.

Combined with ::after { content: attr(value) } and CSS attribute prefix selectors [value^="X"] with background-image: url(), this enables character-by-character extraction via network
requests.

Works under Content-Security-Policy script-src nonce-only. The CSS exfiltration requires no JavaScript after the initial page load trigger.
Tested 100% reliable on Brave 146 and Chrome 146 Release builds (50/50 trials, 30/30 controlled injection, 20/20 password bypass).

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7695456>

Fix another use-after-free with lazy style attributes.

---


Expand for full commit details
```
     
    This is a similar problem as regular attribute checks, just for 
    the special case of input type="" (which is a similar but separate 
    path). 
     
    Style perftest and Speedometer3 are neutral. 
     
    (cherry picked from commit d8b01057f740d3bb0ec880b34372da63147c2521) 
     
    Fixed: 493952652 
    Change-Id: I264503545c345325e6d21afa0726f524bb9394b8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686835 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602570} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695456 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Auto-Submit: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1457} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/core/css/element_rule_collector.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-values/crashtests/chrome-bug-493952652.html`

---

Hash: [283ce2470167ab074eb6bba4f3e6bfc9ec9e78a9](https://chromiumdash.appspot.com/commit/283ce2470167ab074eb6bba4f3e6bfc9ec9e78a9)  

Date: Wed Mar 25 08:59:02 2026


---

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7695516>

Fix another use-after-free with lazy style attributes.

---


Expand for full commit details
```
     
    This is a similar problem as regular attribute checks, just for 
    the special case of input type="" (which is a similar but separate 
    path). 
     
    Style perftest and Speedometer3 are neutral. 
     
    (cherry picked from commit d8b01057f740d3bb0ec880b34372da63147c2521) 
     
    Fixed: 493952652 
    Change-Id: I264503545c345325e6d21afa0726f524bb9394b8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686835 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1602570} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695516 
    Auto-Submit: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3185} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/css/element_rule_collector.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-values/crashtests/chrome-bug-493952652.html`

---

Hash: [956fc9e3241f825df49647527c63fc87967f0674](https://chromiumdash.appspot.com/commit/956fc9e3241f825df49647527c63fc87967f0674)  

Date: Wed Mar 25 09:01:38 2026


---

### wf...@chromium.org (2026-04-01)

Renderer memory corruption is sev-high.

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Below baseline. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493952652)*
