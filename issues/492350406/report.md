# CHECK failure: offset <= view.length() && length <= view.length() - offset in string_view.h

| Field | Value |
|-------|-------|
| **Issue ID** | [492350406](https://issues.chromium.org/issues/492350406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Platform |
| **Platforms** | Linux |
| **Reporter** | 24...@project.gserviceaccount.com |
| **Assignee** | ts...@google.com |
| **Created** | 2026-03-13 |
| **Bounty** | $3,000.00 |

## Description

# OOB read in ShapeResultView::ForEachGraphemeClusters via multi-glyph cluster skip logic

## Summary

An out-of-bounds read in the Chromium renderer can be triggered from JavaScript on all platforms. The function `ShapeResultView::ForEachGraphemeClusters` advances the `cluster_start` position once per glyph instead of once per cluster when skipping glyphs outside the drawing range. When a custom web font uses OpenType GSUB Multiple Substitution to map a single character to multiple glyphs, the skip loop over-advances `cluster_start` past the actual character boundary. This corrupted position is then used to construct a `StringView` that extends beyond the underlying text buffer. The subsequent `NumGraphemeClusters` call iterates over this out-of-bounds view, reading adjacent heap memory. In release builds, `SECURITY_DCHECK` is a no-op and the OOB read proceeds silently, making this exploitable as an information disclosure primitive from web content.

## Bisect

Introducing Commit: `2ef8b65de690c3a2d83bd6b991763359a7c1f3d6`

- Date: 2018-09-14
- Author: Emil A Eklund <[eae@chromium.org](mailto:eae@chromium.org)>
- Review: <https://chromium-review.googlesource.com/1225101>

The bug was introduced in the original `ShapeResult::ForEachGraphemeClusters` API and then copied into `ShapeResultView::ForEachGraphemeClusters` in commit `a365a8203ccd7` (2018-10-31). Both copies contain the same flaw.

## Root Cause

`ShapeResultView::ForEachGraphemeClusters` iterates over glyphs and maintains a `cluster_start` variable to track the character offset of the current cluster. When a glyph falls outside the `[from, to)` drawing range, the function skips it and adjusts `cluster_start`:

```
// shape_result_view.cc — skip path for out-of-range glyphs
if ((rtl && current_character_index >= to) ||
    (!rtl && current_character_index < from)) {
  advance_so_far += glyph_data.advance.ToFloat();
  rtl ? --cluster_start : ++cluster_start;  // BUG: per-glyph, not per-cluster
  continue;
}

```

The increment/decrement is executed once for each glyph in the skip region. This is correct when every character produces exactly one glyph, but incorrect for multi-glyph clusters. With GSUB Multiple Substitution (lookup type 2), a single input character can produce an arbitrary number of output glyphs, all sharing the same `character_index`. In that case, the skip loop runs `N` times for `N` glyphs, advancing `cluster_start` by `N` when it should advance by 1.

After the skip loop, when the function encounters the first in-range cluster, it computes `cluster_end` from the next character boundary and constructs a `StringView` to count grapheme clusters:

```
// shape_result_view.cc — StringView construction with corrupted cluster_start
graphemes_in_cluster = NumGraphemeClusters(
    cluster_end >= cluster_start
        ? StringView(text, cluster_start, cluster_end - cluster_start)
        : StringView(text, cluster_end, cluster_start - cluster_end));

```

With `cluster_start` over-advanced, the arguments to `StringView` produce a view that starts at or beyond the end of the text buffer. The `StringView` range constructor guards this with `SECURITY_DCHECK`:

```
// string_view.h — the only protection
SECURITY_DCHECK(offset <= view.length());
SECURITY_DCHECK(length <= view.length() - offset);

```

`SECURITY_DCHECK` is compiled to a fatal check only when `ADDRESS_SANITIZER` is defined or `DCHECK_IS_ON()` is true. In production release builds, both conditions are false and the macro expands to `((void)0)`, so the out-of-bounds `StringView` is silently created. `NumGraphemeClusters` then creates an ICU `CharacterBreakIterator` over this view, iterating past the text buffer and reading heap memory that follows the `StringImpl` allocation.

A concrete trigger uses a two-character 16-bit string `"\u0100B"` with a web font whose `ccmp` feature decomposes U+0100 into three glyphs. When the Selection API selects only the second character (range `[1,2)`), `PaintSelectedText` calls `ForEachGraphemeClusters` with `from=1, to=2`. The skip loop runs three times for the three glyphs of U+0100, pushing `cluster_start` from 0 to 3. When processing the glyph for 'B', `cluster_end` is 2, and the function constructs `StringView(text, 2, 1)` on a text of length 2, which is one code unit past the end.

The same bug also exists in `ShapeResult::ForEachGraphemeClusters` in `shape_result.cc`.

## Reproduce

Tested on commit `d0f83d769eeed` (macOS arm64).

Build:

```
autoninja -C ~/chromium/src/out/asan-release chrome

```

Run:

```
ASAN_OPTIONS=detect_odr_violation=0 ~/chromium/src/out/asan-release/Chromium.app/Contents/MacOS/Chromium \
  --no-sandbox --disable-gpu \
  --user-data-dir=/tmp/poc-$(date +%s) \
  issue_find021/poc.html

```

The renderer process crashes immediately on paint. No user interaction required.

```
[26598:93931928:0313/193828.315734:FATAL:third_party/blink/renderer/platform/wtf/text/string_view.h:401] Security DCHECK failed: length <= view.length() - offset.
0   libbase.dylib                       0x0000000102eacd88 base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) + 28
1   libbase.dylib                       0x0000000102e62580 base::debug::StackTrace::StackTrace() + 80
2   libbase.dylib                       0x0000000102b40e3c logging::LogMessage::Flush() + 652
3   libbase.dylib                       0x0000000102b42aac logging::LogMessageFatal::~LogMessageFatal() + 12
4   libbase.dylib                       0x0000000102b42ad0 logging::LogMessageFatal::~LogMessageFatal() + 0
5   libblink_platform.dylib             0x000000014a6edbcc blink::ShapeResultView::ForEachGraphemeClusters(blink::StringView const&, float, unsigned int, unsigned int, unsigned int, void (*)(void*, unsigned int, float, unsigned int, float, blink::CanvasRotationInVertical), void*) const + 3756
6   libblink_platform.dylib             0x000000014a6d665c blink::ShapeResultBloberizer::FillTextEmphasisGlyphsNG::FillTextEmphasisGlyphsNG(blink::FontDescription const&, blink::StringView const&, unsigned int, unsigned int, blink::ShapeResultView const*, blink::GlyphData const&) + 1600
7   libblink_platform.dylib             0x000000014a5c494c blink::Font::DrawEmphasisMarks(cc::PaintCanvas*, blink::TextFragmentPaintInfo const&, blink::AtomicString const&, gfx::PointF const&, cc::PaintFlags const&) const + 560
8   libblink_platform.dylib             0x000000014a99f380 blink::GraphicsContext::DrawEmphasisMarks(blink::Font const&, blink::TextFragmentPaintInfo const&, blink::AtomicString const&, gfx::PointF const&, blink::AutoDarkMode const&) + 420
9   libblink_core.dylib                 0x00000001522f06c0 blink::TextPainter::Paint(blink::TextFragmentPaintInfo const&, blink::TextPaintStyle const&, int, blink::AutoDarkMode const&, blink::TextPainter::ShadowMode) + 2016
10  libblink_core.dylib                 0x00000001522f1afc blink::TextPainter::PaintSelectedText(blink::TextFragmentPaintInfo const&, unsigned int, unsigned int, blink::TextPaintStyle const&, blink::TextPaintStyle const&, blink::LineRelativeRect const&, int, blink::AutoDarkMode const&) + 1512
11  libblink_core.dylib                 0x0000000152116c10 blink::BoxFragmentPainter::PaintTextItem(blink::InlineCursor const&, blink::PaintInfo const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&, blink::PhysicalFixedOffset<blink::FixedPoint<6u, int>> const&) + 916

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 14.4 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6142180787781632.

### ts...@google.com (2026-03-13)

Tracking fix to underlying problem in https://chromium-review.git.corp.google.com/c/chromium/src/+/7667267

### 24...@project.gserviceaccount.com (2026-03-15)

Detailed Report: https://clusterfuzz.com/testcase?key=6142180787781632

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  length <= view.length() - offset in 444
  blink::ShapeResultView::ForEachGraphemeClusters
  blink::ShapeResultBloberizer::FillTextEmphasisGlyphsNG::FillTextEmphasisGlyphsNG
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1599546

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6142180787781632

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### 24...@project.gserviceaccount.com (2026-03-15)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### ch...@google.com (2026-03-16)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-16)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  main  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://chromium-review.googlesource.com/7667267>

Upgrade SECURITY\_DCHECK() to CHECK() in blink StringView and StringImpl

---


Expand for full commit details
```
     
    Otherwise, the UNSAFE_BUFFER() usage and // SAFETY: comments are 
    invalid, since the SECURITY_DCHECK is still a DCHECK and not present in 
    release builds. 
     
    This is the most secure approach to resolving the issue, vs. converting 
    these into UNSAFE_TODO() or propagating the unsafety to the caller via 
    UNSAFE_BUFFER_USAGE. 
     
    -- Remove redundant SECURITY_DCHECK() now that operator[] checked. 
    -- Update one comment while at it. 
     
    Bug: 492527423, 492350406 
    Change-Id: If74e2c78e38657b1d36a48afe83279d1340ae4a6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667267 
    Commit-Queue: Tom Sepez <tsepez@chromium.org> 
    Reviewed-by: Kentaro Hara <haraken@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1599980}

```

---

Files:

- M `third_party/blink/renderer/platform/wtf/text/string_impl.h`
- M `third_party/blink/renderer/platform/wtf/text/string_view.cc`
- M `third_party/blink/renderer/platform/wtf/text/string_view.h`

---

Hash: [2bb6d1ef9a81ebbbe7b9169333b4d2a8ec690bc5](https://chromiumdash.appspot.com/commit/2bb6d1ef9a81ebbbe7b9169333b4d2a8ec690bc5)  

Date: Mon Mar 16 17:19:10 2026


---

### 24...@project.gserviceaccount.com (2026-03-17)

ClusterFuzz testcase 6142180787781632 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1599961:1599980

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1599980) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1599980) appears to be after beta branch point (1596535).
Security Merge Request - Manual Review: Merge review required: M146 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M147 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-03-18)

Tom, can I assign this to you, thanks for the fix - would you handle the merges?

### ts...@google.com (2026-03-18)

My CL removes this entire class of vulnerability from the code base, but has likely hit the perf bots. Will need to revert, and the specific instance of this will need fixing on its own.

### dr...@chromium.org (2026-03-18)

Since the fix is being reverted, reopening the bug.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Tom Sepez [tsepez@chromium.org](mailto:tsepez@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7681261>

Revert "Upgrade SECURITY\_DCHECK() to CHECK() in blink StringView and StringImpl"

---


Expand for full commit details
```
     
    This reverts commit 2bb6d1ef9a81ebbbe7b9169333b4d2a8ec690bc5. 
     
    Reason for revert: Perf regression 
     
    Original change's description: 
    > Upgrade SECURITY_DCHECK() to CHECK() in blink StringView and StringImpl 
    > 
    > Otherwise, the UNSAFE_BUFFER() usage and // SAFETY: comments are 
    > invalid, since the SECURITY_DCHECK is still a DCHECK and not present in 
    > release builds. 
    > 
    > This is the most secure approach to resolving the issue, vs. converting 
    > these into UNSAFE_TODO() or propagating the unsafety to the caller via 
    > UNSAFE_BUFFER_USAGE. 
    > 
    > -- Remove redundant SECURITY_DCHECK() now that operator[] checked. 
    > -- Update one comment while at it. 
    > 
    > Bug: 492527423, 492350406 
    > Change-Id: If74e2c78e38657b1d36a48afe83279d1340ae4a6 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667267 
    > Commit-Queue: Tom Sepez <tsepez@chromium.org> 
    > Reviewed-by: Kentaro Hara <haraken@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1599980} 
     
    Bug: 492527423, 492350406 
    Change-Id: Ib7508aa5a170939a103359081c2986890cc06434 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7681261 
    Reviewed-by: Kentaro Hara <haraken@chromium.org> 
    Auto-Submit: Tom Sepez <tsepez@chromium.org> 
    Commit-Queue: Tom Sepez <tsepez@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1601625}

```

---

Files:

- M `third_party/blink/renderer/platform/wtf/text/string_impl.h`
- M `third_party/blink/renderer/platform/wtf/text/string_view.cc`
- M `third_party/blink/renderer/platform/wtf/text/string_view.h`

---

Hash: [31b23ad60a715b5b478f8dc1d6f9bd5761fcc37b](https://chromiumdash.appspot.com/commit/31b23ad60a715b5b478f8dc1d6f9bd5761fcc37b)  

Date: Wed Mar 18 23:39:33 2026


---

### ts...@google.com (2026-03-19)

Alas, had this been a CHECK(), the fuzzer would have found it.

### ts...@google.com (2026-03-23)

New CL following the revert at https://crrev.com/c/7695218

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://chromium-review.googlesource.com/7695218>

Avoid unsafe buffers in StringView(view, offset, length) constructor.

---


Expand for full commit details
```
     
    Use the subspan() method which will perform these bounds checks 
    under the covers before extracting a data() pointer. 
     
    This is a simpler way to get part of the benefit of the CL at 
    https://crrev.com/c/7667267 but without the performance impact 
    of making all the other methods touched in that CL safe. 
     
    -- Do the same for StringView::Set(). 
     
    Bug: 492350406 
    Change-Id: If2741f7241204862d28f3b662d897f9cba3e0b1c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7695218 
    Reviewed-by: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Kentaro Hara <haraken@chromium.org> 
    Commit-Queue: Tom Sepez <tsepez@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1604199}

```

---

Files:

- M `third_party/blink/renderer/platform/wtf/text/string_view.h`

---

Hash: [f74f78b6aeb94b13f2a706bb4a3701738f6ab36a](https://chromiumdash.appspot.com/commit/f74f78b6aeb94b13f2a706bb4a3701738f6ab36a)  

Date: Tue Mar 24 16:42:58 2026


---

### ts...@google.com (2026-04-02)

We can track the remaining work as found by the fuzzer in https://g-issues.chromium.org/issues/498816088

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline with bisect. User information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492350406)*
