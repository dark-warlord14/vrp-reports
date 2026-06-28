# Use-after-free in shared WordBreakIteratorPool via Proofreader API

| Field | Value |
|-------|-------|
| **Issue ID** | [492421936](https://issues.chromium.org/issues/492421936) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>AI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2026-03-13 |
| **Bounty** | $11,000.00 |

## Description

## Summary

The Proofreader API (`Exposed=(Window,Worker)`) calls `WordBreakIterator()` in the renderer to tokenize text after receiving model results. `WordBreakIterator()` returns a raw pointer to a single ICU `RuleBasedBreakIterator` held in a process-level static `WordBreakIteratorPool` singleton with no synchronization. When multiple DedicatedWorkers call `Proofreader.proofread()` concurrently with CJK input, their `Tokenize()` invocations race on the shared iterator. One thread can destroy and replace the pooled iterator while another thread is still iterating it, producing a heap-use-after-free. ASAN confirms the crash is not protected by MiraclePtr. This vulnerability affects stable Chrome on all desktop platforms (Windows, macOS, Linux, ChromeOS). The Proofreader API is in an active origin trial from Chrome 141 through 145, with third-party token support (`origin_trial_allows_third_party: true`). An attacker can embed a third-party origin trial token in any page to activate the API on a visiting user's stable browser without requiring any flags or user opt-in.

## Bisect

Introducing Commit: `426b0b49d7e15a12466c5ee3ce43f0e1b7941b7d`

- Date: `Fri Aug 22 2025`
- Author: Queenie Zhang
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6635091>

The Proofreader IDL has had `Exposed=(Window,Worker)` since its first commit (`b4a7395049a15`, May 2025), but that initial version was a stub with no tokenization. The introducing commit added `GetCorrections()` and `Tokenize()`, which calls `WordBreakIterator()`, making the thread-unsafe shared iterator reachable from Worker threads for the first time.

## Root Cause

Blink maintains a `WordBreakIteratorPool` as a process-level static singleton in `text_break_iterator_icu.cc`. The pool holds a single `std::unique_ptr<TextBreakIterator>` and hands out the raw pointer to every caller:

```
// third_party/blink/renderer/platform/text/text_break_iterator_icu.cc:641-696
class WordBreakIteratorPool {
 private:
  TextBreakIterator* Get() {
    if (!pool_) {
      pool_ = Create(locale_);
    }
    return pool_.get();
  }
  std::unique_ptr<TextBreakIterator> pool_;
};

TextBreakIterator* WordBreakIterator(base::span<const UChar> string) {
  DEFINE_THREAD_SAFE_STATIC_LOCAL(WordBreakIteratorPool, pool, ());
  return pool.Get(string);
}

```

Despite the `DEFINE_THREAD_SAFE_STATIC_LOCAL` name, this macro only ensures thread-safe initialization of the static variable; it provides no locking or per-thread isolation for subsequent access. The source itself documents this:

```
// third_party/blink/renderer/platform/wtf/std_lib_extras.h:63-70
// |DEFINE_THREAD_SAFE_STATIC_LOCAL()| doesn't provide additional thread-safety,
// but it effectively bypasses the `IsNotRacy` DCHECK present in
// |DEFINE_STATIC_LOCAL()|; use it if the singleton can be accessed by
// multiple threads.
#define DEFINE_THREAD_SAFE_STATIC_LOCAL(Type, Name, Arguments) \
  DEFINE_STATIC_LOCAL_IMPL(Type, Name, Arguments, true)

```

Every call to `WordBreakIteratorPool::Get(span)` rebinds the single ICU iterator to the caller's text buffer via `SetText16()`, then returns the same raw pointer. If two threads call `Get()` concurrently, they both obtain the same `TextBreakIterator*` and proceed to call `first()`, `next()`, and the iterator's internal dictionary break engine methods in parallel.

The Proofreader API introduces a Worker-accessible path into this code. When `Proofreader.proofread()` completes, the renderer-side callback `OnProofreadComplete()` calls `GetCorrections()`, which calls `Tokenize()` twice:

```
// third_party/blink/renderer/modules/ai/proofreader.cc:228-232
Vector<Correction> GetCorrections(const String& input,
                                  const String& corrected_input) {
  Vector<String> tokenized_input = Tokenize(input);
  Vector<String> tokenized_corrected_input = Tokenize(corrected_input);
  ...
}

```

`Tokenize()` calls `WordBreakIterator(text)` and then iterates the returned pointer:

```
// third_party/blink/renderer/modules/ai/proofreader.cc:43-65
Vector<String> Tokenize(const String& text) {
  TextBreakIterator* it = WordBreakIterator(text);
  int32_t start = it->first();
  for (int32_t end = it->next(); end != -1; end = it->next()) {
    tokens.push_back(text.Substring(start, end - start));
    start = end;
  }
  return tokens;
}

```

Since Proofreader is `Exposed=(Window,Worker)`, each DedicatedWorker runs `OnProofreadComplete` on its own thread. With CJK input, ICU's `RuleBasedBreakIterator::next()` enters the `CjkBreakEngine::divideUpDictionaryRange()` path, which uses internal heap-allocated structures (`UVector32` buffers, `DictionaryCache`, language break engines). When two Worker threads enter this path concurrently on the same shared iterator, the race manifests in two ways observed across runs: (1) one thread destroys and recreates the pooled iterator via the `unique_ptr` while another thread still holds a raw pointer to the old one, causing a heap-use-after-free when the victim thread reads freed ICU internal state; (2) concurrent `UVector32::expandCapacity()` calls from the CJK dictionary break engine cause both threads to `realloc` the same backing buffer, producing a double-free.

## Reproduce

Tested on commit `f51a685e768b632262beaf8bd95387fffe096655` (Linux x64). Build `content_shell` with the existing ASAN release configuration:

```
autoninja -C ~/chromium/src/out/asan-release content_shell

```

Launch:

```
xvfb-run -a env ASAN_OPTIONS=detect_odr_violation=0 \
  ~/chromium/src/out/asan-release/content_shell \
  --no-sandbox \
  --enable-experimental-web-platform-features \
  --user-data-dir=/tmp/poc-$(date +%s) \
  --enable-logging=stderr \
  poc.html

```

The PoC spawns four DedicatedWorkers, each creating a `Proofreader` instance and calling `proofread()` in a loop with CJK text. The renderer crashes within seconds of all workers starting their race loops. `content_shell` is used here instead of `chrome` because reproducing in `chrome` requires downloading the on-device AI model (22 GB+). `content_shell` provides `EchoAIProofreader`, the content-layer's built-in test implementation that echoes back input immediately. This exercises the exact same renderer-side code path (`OnProofreadComplete` -> `GetCorrections` -> `Tokenize` -> `WordBreakIterator`) that production Chrome executes after receiving model output.

```
=================================================================
==2689941==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d067052d818 at pc 0x7fe6d7e5a40b bp 0x7be1002abbb0 sp 0x7be1002abba8
READ of size 8 at 0x7d067052d818 thread T9 (DedicatedWorker)
    #0 0x7fe6d7e5a40a in icu_77::RuleBasedBreakIterator::getLanguageBreakEngine(int, char const*) third_party/icu/source/common/rbbi.cpp:1234:9
    #1 0x7fe6d7e4a33d in icu_77::RuleBasedBreakIterator::DictionaryCache::populateDictionary(int, int, int, int) third_party/icu/source/common/rbbi_cache.cpp:161:47
    #2 0x7fe6d7e4d8c0 in icu_77::RuleBasedBreakIterator::BreakCache::populateFollowing() third_party/icu/source/common/rbbi_cache.cpp:489:32
    #3 0x7fe6d7e4d4fd in icu_77::RuleBasedBreakIterator::BreakCache::nextOL() third_party/icu/source/common/rbbi_cache.cpp:275:19
    #4 0x7fe6d7e52ed8 in icu_77::RuleBasedBreakIterator::next() third_party/icu/source/common/rbbi_cache.h:92:33
    #5 0x7fe697860dd5 in blink::Tokenize(blink::String const&) third_party/blink/renderer/modules/ai/proofreader.cc:60:26
    #6 0x7fe6978632b5 in blink::GetCorrections(blink::String const&, blink::String const&) third_party/blink/renderer/modules/ai/proofreader.cc:231:36
    #7 0x7fe69786ad63 in blink::Proofreader::OnProofreadComplete(...) third_party/blink/renderer/modules/ai/proofreader.cc:556:26
    #8 0x7fe697877193 in base::internal::Invoker<...>::RunOnce(...) base/functional/bind_internal.h:740:12
    #9 0x7fe697824b4e in blink::(anonymous namespace)::Responder::OnCompletion(...) base/functional/callback.h:155:12
    #10 0x7fe6a77257b6 in blink::mojom::blink::ModelStreamingResponderStubDispatch::Accept(...) gen/third_party/blink/public/mojom/ai/model_streaming_responder.mojom-blink.cc:429:13
    ...
    #26 0x7fe6a68790dc in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:178:14

0x7d067052d818 is located 216 bytes inside of 304-byte region [0x7d067052d740,0x7d067052d870)
freed by thread T8 (DedicatedWorker) here:
    #0 0x556b00b15216 in free
    #1 0x7fe6a6303067 in blink::WordBreakIterator(base::span<...>) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x7fe6a6303560 in blink::WordBreakIterator(blink::StringView const&) third_party/blink/renderer/platform/text/text_break_iterator_icu.cc:706:10
    #3 0x7fe697860d4a in blink::Tokenize(blink::String const&) third_party/blink/renderer/modules/ai/proofreader.cc:51:27
    #4 0x7fe6978632b5 in blink::GetCorrections(blink::String const&, blink::String const&) third_party/blink/renderer/modules/ai/proofreader.cc:231:36
    #5 0x7fe69786ad63 in blink::Proofreader::OnProofreadComplete(...) third_party/blink/renderer/modules/ai/proofreader.cc:556:26
    ...
    #24 0x7fe6a68790dc in blink::scheduler::NonMainThreadImpl::SimpleThreadImpl::Run() third_party/blink/renderer/platform/scheduler/worker/non_main_thread_impl.cc:178:14

previously allocated by thread T9 (DedicatedWorker) here:
    #0 0x556b00b154b4 in malloc
    #1 0x7fe6d7d91f7e in icu_77::BreakIterator::buildInstance(...) third_party/icu/source/common/brkiter.cpp:120:14
    #2 0x7fe6d7d937d7 in icu_77::BreakIterator::makeInstance(...) third_party/icu/source/common/brkiter.cpp:436:22
    #3 0x7fe6d7d9257f in icu_77::BreakIterator::createInstance(...) third_party/icu/source/common/brkiter.cpp:409:16
    #4 0x7fe6a6302fee in blink::WordBreakIterator(...) third_party/blink/renderer/platform/text/text_break_iterator_icu.cc:653:26
    #5 0x7fe6a6303560 in blink::WordBreakIterator(blink::StringView const&) third_party/blink/renderer/platform/text/text_break_iterator_icu.cc:706:10
    #6 0x7fe697860d4a in blink::Tokenize(blink::String const&) third_party/blink/renderer/modules/ai/proofreader.cc:51:27
    #7 0x7fe6978632b5 in blink::GetCorrections(blink::String const&, blink::String const&) third_party/blink/renderer/modules/ai/proofreader.cc:231:36
    #8 0x7fe69786ad63 in blink::Proofreader::OnProofreadComplete(...) third_party/blink/renderer/modules/ai/proofreader.cc:556:26
    ...

SUMMARY: AddressSanitizer: heap-use-after-free third_party/icu/source/common/rbbi.cpp:1234:9 in icu_77::RuleBasedBreakIterator::getLanguageBreakEngine(int, char const*)

MiraclePtr Status: NOT PROTECTED
This crash is still exploitable with MiraclePtr.

```
## References

- [text\_break\_iterator\_icu.cc: WordBreakIteratorPool and WordBreakIterator()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/text/text_break_iterator_icu.cc;l=641-706)
- [proofreader.cc: Tokenize()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ai/proofreader.cc;l=43-65)
- [proofreader.cc: GetCorrections()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ai/proofreader.cc;l=228-237)
- [proofreader.cc: OnProofreadComplete()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ai/proofreader.cc;l=545-564)
- [proofreader.idl: Exposed=(Window,Worker)](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ai/proofreader.idl;l=49-53)
- [std\_lib\_extras.h: DEFINE\_THREAD\_SAFE\_STATIC\_LOCAL](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/std_lib_extras.h;l=63-70)

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 51.7 KB)
- [poc.html](attachments/poc.html) (text/html, 3.4 KB)

## Timeline

### ms...@google.com (2026-03-17)

@qu...@google.com please acknowledge receipt and give an ETA on a fix, thanks.

### qu...@google.com (2026-03-17)

Thanks to @ch...@google.com, this is already being addressed by <https://chromium-review.git.corp.google.com/c/chromium/src/+/7669269>. Reassigning now to better track the progress.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  chiyotsai [chiyotsai@google.com](mailto:chiyotsai@google.com)  

Link:    <https://chromium-review.googlesource.com/7669269>

[Blink] Use ThreadSpecific for WordBreak and SentenceBreak Iterators

---


Expand for full commit details
```
     
    The DEFINE_THREAD_SAFE_STATIC_LOCAL macro only ensures thread-safe 
    initialization. Prior to the Proofreader API, these iterators were 
    exclusively accessed from the main thread, making unprotected shared 
    instances safe. 
     
    However, the Proofreader API is Exposed=(Window,Worker), allowing 
    background Worker threads to tokenize text concurrently via 
    WordBreakIterator(). Concurrent access from multiple threads to the same 
    RuleBasedBreakIterator causes heap-use-after-free and double-free 
    vulnerabilities when ICU's internal buffers race. 
     
    This CL wraps the iterator pools in ThreadSpecific to lazily provision 
    thread-local iterators. This prevents data races and fixes the UAF 
    without negatively impacting Main Thread performance due to 
    ThreadSpecific's Main Thread caching optimization. 
     
    Bug: b:492421936 
    Change-Id: I6cfba1aaf5799f188761fb83abdb071f7e9f59e3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7669269 
    Reviewed-by: Mike Wasserman <msw@chromium.org> 
    Commit-Queue: Chi Yo Tsai <chiyotsai@google.com> 
    Reviewed-by: Koji Ishii <kojii@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601687}

```

---

Files:

- M `third_party/blink/renderer/platform/text/text_break_iterator_icu.cc`

---

Hash: [d72e069671f4498891f27f42cc6c2b7345c841ad](https://chromiumdash.appspot.com/commit/d72e069671f4498891f27f42cc6c2b7345c841ad)  

Date: Thu Mar 19 01:38:56 2026


---

### sp...@google.com (2026-05-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High quality with bisect. Renderer RCE / memory corruption in a sandboxed process


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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492421936)*
