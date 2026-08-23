# STTF allows to leaking text char by char from cross-origin page.

| Field | Value |
|-------|-------|
| **Issue ID** | [457771782](https://issues.chromium.org/issues/457771782) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Scroll |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 142.0.0.0 |
| **Reporter** | se...@gmail.com |
| **Assignee** | vm...@google.com |
| **Created** | 2025-11-04 |
| **Bounty** | $10,000.00 |

## Description

# Steps to reproduce the problem

Steps to reproduce:

1. Download attached files
2. Change `TARGET`, `PREFIX`, `FOUND`, `NOT_FOUND` if you want to test on another text/website.
3. Host this files on localhost/site
4. open `exploit_chrome.html`
5. Start typing text

You will see that symbols will gradually start appearing on the page.
See example in `PoC.mov`.

# Problem Description

We have discovered that using STTF (Scroll To Text Fragment) makes it possible to detect and exfiltrate text from another page. This is possible due to several factors:

## Bypass of Empty BCG check

Firstly, by default, Chromium does not allow the use of STTF if there are other windows in the current Browser Context Group and our page is cross-origin. This check can be found in [CheckSecurityResrictions](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fragment_directive/text_fragment_anchor.cc;drc=33aa41994c585274ba016ef43a3b8baa3c6334a0;l=86):

```
    if (frame.GetPage()->RelatedPages().size()) {
      TRACE_EVENT_INSTANT("blink", "CheckSecurityRestrictions", "Result",
                          "Non-Empty Browsing Context Group");
      return false;
    }

```

This check can be bypassed as follows:

```
window.location.href=`https://cross-origin-site/#:~:text=...`
window.open('/same-origin-with-attacker')

```

Based on my tests, this happens because the check of `frame.GetPage()->RelatedPages().size()` occurs during the redirect, and only after that does the new window begin to open.

## Time difference

We discovered that when Chromium opens a link with an STTF, redirects may fail to execute if the text search is under heavy load. This happens because:

1. First, the text is searched using [`void TextAnnotationSelector::FindRange`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/annotation/text_annotation_selector.cc;drc=7d116c4e09471ac9aa11cef21b584a3673db5c76;l=22), which performs a linear search for text.
2. When the text is found (even partially), [`bool IsWordBounded`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fragment_directive/text_fragment_finder.cc;drc=bd9a480027283342502ac6e044727bb53b2b2c02;l=34) and other checks are performed.
3. Only after these steps does the highlight and scroll to text occur.

It can be observed that the number of instructions executed will differ, but for a simple search, the difference is negligible.

Therefore, we used another STTF feature to increase the number of instructions and thus slow down the search time — `:~:text=...&text=...&text=...&text=......`.
Since STTF allows us to insert an unlimited number of text fragments, we can add tens of thousands of identical text fragments in a single URL. This slows execution down, as the operation will be performed tens of thousands of times instead of just once.

## Detect time difference by history length

There is no traditional way to detect STTF time. However, we have discovered a way to do this:

```
let w = window.opener
await sleep(TIME);
w.location = TARGET + "#1";
...
w.location = TARGET + "#5";
w.location = 'about:blank'
            
while(true){
    try{
        w.origin;
        ...
        if (w.history.length - previous_history_length==2){
            ... Triggered match
        }
    }catch(e){
        await sleep(100);
    }
}

```

We found that while STTF is being processed, the redirect process is blocked, and if we choose the correct timing, only the last redirect to `about:blank` will execute immediately. At this point, we can detect how many redirects actually occurred using `history.length`.

If `sleep(TIME)` ends before the STTF finishes, we get `2`. Otherwise, we get a higher value.
So, to guess the correct value, we need to choose a timing where we consistently get `2` only for the correct prefix.

## Timing estimate

Since each user will have different loading times (due to varying internet connections, OS, etc.), I had to implement dynamic timing detection directly in the exploit on the client side.

How it works:
Suppose we have a page that contains the text:

```
Your code: 21346375

```

So, you need to highlight the text fragment with `FOUND='Your cod'` and `NOT_FOUND='Your coA'` (that is, a valid and an invalid prefix before the target text you want to find; it's also important that neither triggers the boundary check).

After that, I use a binary search to find the appropriate timing.

I simply run the test with the current timing on both the `FOUND` and `NOT_FOUND` strings:

1. If the function succeeds for both strings, I decrease the upper bound (we are waiting too long)
2. If the function finds only one result and it is `FOUND`, I increase the lower bound
3. I repeat this with `(MIN_TIME + MAX_TIME) / 2`
   When the difference between the upper and lower bounds is minimal (in my tests, this difference was 100 milliseconds), I stop the search — we have found the timing.

## Tested

This exploit was tested by us on 3 different devices in different internet networks.
2 on MacOS, 1 on Windows 11 – on each device we were able to successfully exfiltrate the code.

# Additional Comments

## Other issues and limitations of the exploit

The limitations imposed on STTF can be found in [`bool TextFragmentAnchor::GenerateNewToken`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fragment_directive/text_fragment_anchor.cc;drc=7189da78436702acd8f20043b0f394b04f588093;l=114):

```
  return loader.LastNavigationHadTransientUserActivation() ||
         loader.IsBrowserInitiated();

```

Therefore, I used `onkeydown` on the `textarea` so that while the user is typing, a window appears in the lower right corner.

To hide the popup window and allow the user to continue typing text, I open a new tab in that window and immediately close it, which returns focus to exploit window:

```
            setTimeout(()=>{var a = window.open("about:blank");a.close();},100);
            setTimeout(()=>{var a = window.open("about:blank");a.close();},700);

```

Also, for this exploit to work, the window must be allowed to open other windows. This can also be bypassed, but I didn't do this to avoid making the PoC even more complicated (since it is already fairly complex). So for testing, make sure your origin is allowed to use `window.open.`

# Summary

STTF allows to leaking text char by char from cross-origin page.

# Custom Questions

#### Reporter credit:

Vsevolod Kokorin (Slonser) of Solidlab and Jorian Woltjer

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [etest.html](attachments/etest.html) (text/html, 5.9 KB)
- [exploit_chrome.html](attachments/exploit_chrome.html) (text/html, 1.4 KB)
- [time_detect.html](attachments/time_detect.html) (text/html, 2.9 KB)
- [PoC.mov](attachments/PoC.mov) (video/quicktime, 41.5 MB)
- [simpler_repro.html](attachments/simpler_repro.html) (text/html, 915 B)

## Timeline

### ma...@google.com (2025-11-05)

Thanks for the report!

There's some public work on attacks like this: <https://docs.google.com/document/d/1YHcl1-vE_ZnZ0kL2almeikAj2gkwCq8_5xwIae7PVik/edit?tab=t.0#heading=h.uoiwg23pt0tx>

Assigning to [mattdr@google.com](mailto:mattdr@google.com) for now

### ma...@google.com (2025-11-05)

I can confirm the repro seemed to leak data on macOS, Chrome Stable 141.0.7390.124: I hosted the files with `python3 -m http.server`, enabled all popups for the site, and typed a lot; eventually, fragments of a leaked code appeared. It was a different code than I saw pulling up the PoC site directly, but I see notes in the Python that the server has logic to start a new attack -- I assume that's what happened here.

Assigning S1 since this is a Site Isolation bypass with content disclosure. The check at issue has been the same for a long time, so assuming this applies back to Extended Stable.

Reached out to bokan@, who suggested domfarolino@ as a possible assignee.

**Reporters**: would you agree the root issue is "Bypass of Empty BCG check", and if that check worked as intended then this leak is closed?

### se...@gmail.com (2025-11-05)

Yes it's enough to improve BCG check.
But while the root of the problem lies in the `Bypass of Empty BCG check`, in the future I would recommend limiting the number of simultaneous `:~:text` entries. It seems to me that in normal user flow, there will never be a situation where thousands of fragment directives are inserted into a single URL.

### bo...@chromium.org (2025-11-05)

Thanks - to make sure I understand, the time difference comes from the ancillary checks that happen when some text is matched and since those checks are trivial - the exploit magnifies the difference by using a huge number of equal `text=` directives - is that right?

Yeah, I agree we could cap the number of terms to some reasonable number (100?)

I think another thing that could help here is to perform the search asynchronously which we have some support for - that might give less signal since it wouldn't block the main thread (though would increase contention so not 0 signal)

I'm assuming the BCG check is bypassed because the check and search start don't happen in the same task...we should probably move the security checks to happen into the same task as the search begins in.

### se...@gmail.com (2025-11-05)

> the exploit magnifies the difference by using a huge number of equal text= directives - is that right

Yes, this is true.

> Yeah, I agree we could cap the number of terms to some reasonable number (100?)

Yes, it is possible to add a size check directly in [`FragmentDirective::ParseDirectives`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fragment_directive/fragment_directive.cc;drc=e9787bf37665a37b5c7f09c2cca23a7443c317dc;l=169). Also, this would stop working if duplicate selectors are not stored (although that might be a more complex task, it's just an idea). Because if it were not possible to insert the same selector multiple times, it would not be possible to achieve this behavior in exploit. (For the normal user, there is never a need to insert >1 identical directives.)
Value at the level of < 512 should not allow this behavior to be exploited (From my tests)

> I think another thing that could help here is to perform the search asynchronously

Yes, currently in [this](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/annotation/annotation_agent_impl.cc;l=324-326;drc=e9787bf37665a37b5c7f09c2cca23a7443c317dc) fragment (if I am not mistaken) the call is made synchronously, although there is support for an asynchronous call inside [`TextAnnotationSelector::FindRange`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/annotation/text_annotation_selector.cc;drc=7d116c4e09471ac9aa11cef21b584a3673db5c76;l=22), which supports asynchronous operation.
If you change from synchronous to asynchronous, our method for detecting the timing using history will be broken.

### do...@chromium.org (2025-11-05)

Sorry, I am working on the spec upstreaming but am not taking on any work for the implementation.

### se...@gmail.com (2025-11-05)

Note on STTF specs:

We were also able to achieve similar behavior (by other methods) in other popular engines (WebKit/Firefox).

And it seems this wouldn't have happened if the specifications had imposed a limit on the number of directives. (Just my thoughts)

### ma...@google.com (2025-11-05)

Just to be clear, once we find an owner for this: the priority in this bug is to prevent STTF from inducing observable action across origins, i.e. fixing the BCG check to match the intention (if not the letter?) of the [spec](https://wicg.github.io/scroll-to-text-fragment/#restricting-the-text-fragment).

Limiting number of directives and changing the search to be asynchronous seem like reasonable defense-in-depth measures but can be done as followup work.

dom@ -- do you think there is any spec work implicated here? At the very least, it may be worth a non-normative comment about the time-of-check/time-of-use race condition we encountered implementing section 3.5.4. And, echoing [comment#8](https://issues.chromium.org/issues/457771782#comment8), it seems good to agree on a commensense limit to the number of directives.

### ch...@google.com (2025-11-06)

The Found In field may only contain numeric values.
Some values were corrected.
You can see the changes by toggling full history on the issue.

### ch...@google.com (2025-11-06)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-11-06)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### lb...@google.com (2025-11-06)

I made a simpler repro file that I think gets to the core of the issue. It seems the root issue is that the information about the browsing context group is either sent to the renderer too early in the navigation process or it's checked too early. Because of that, there is a chance that between when the renderer gets/checks that information and when the scroll takes place, there could be a whole new window that has access to that frame that has navigated.

A word of caution: this simpler repro is used to check if the scroll/highlighting actually takes place; it does not look at anything timing related. If the fix for this does not fix the underlying observable timing issue from the computationally expensive text search (i.e. it still does the search even if it doesn't scroll/highlight anything), this repro won't catch that.

### vm...@google.com (2025-11-19)

It sounds like the code change here could be quite small (size check in <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fragment_directive/fragment_directive.cc;l=169-190;drc=e9787bf37665a37b5c7f09c2cca23a7443c317dc> from my understanding)

It's unclear to me if this needs a spec change or a non-normative note.

@ma...@google.com is that something the DOM team can do?

### bo...@chromium.org (2025-11-19)

I believe dom@ is working on spec and could add note, depending on the ultimate resolution...

### ch...@google.com (2025-11-20)

bokan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### bo...@chromium.org (2025-11-20)

Spoke offline to mattdr@ - I'm currently not working on web platform and will not have time in the next few weeks to land a fix here so this should probably have a different owner.

### za...@google.com (2025-11-20)

[security shepherd] hey mattdr@, do you know who would be a better assignee here?

### ma...@google.com (2025-11-20)

Assigning to vmpstr@ per discussions on Chat yesterday with him + bokan@.

### vm...@google.com (2025-11-20)

I can alleviate some of the timing by reducing the number of text fragments and eliminating duplicates (I'm working on this now), but I believe the underlying issue is still there because RelatedPages size check is incorrect at the time it is checked. @ra...@google.com can you route this to someone who may help here?

### dx...@google.com (2025-11-21)

Project: chromium/src  

Branch:  main  

Author:  Vladimir Levin [vmpstr@chromium.org](mailto:vmpstr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7180040>

TextFragments: Limit the text fragments to only unique strings.

---


Expand for full commit details
```
     
    This patch limits the amount of work we'll need to do for text 
    fragments by limiting it to only consider unique fragments. 
     
    R=flackr@chromium.org 
     
    Bug: 457771782 
    Change-Id: I2bc88bd65cb9fa4df2e7cfbfffaf78e6cac37bc0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7180040 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Robert Flack <flackr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1548596}

```

---

Files:

- M `third_party/blink/renderer/core/fragment_directive/build.gni`
- M `third_party/blink/renderer/core/fragment_directive/fragment_directive.cc`
- M `third_party/blink/renderer/core/fragment_directive/fragment_directive.h`
- A `third_party/blink/renderer/core/fragment_directive/fragment_directive_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_directive.h`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_finder_test.cc`
- M `third_party/blink/renderer/core/frame/directive.h`
- M `third_party/blink/renderer/core/frame/selector_directive.h`

---

Hash: [2bb281fb1060fb33dcd3bce0c367e1493ca6dfa6](https://chromiumdash.appspot.com/commit/2bb281fb1060fb33dcd3bce0c367e1493ca6dfa6)  

Date: Fri Nov 21 18:37:00 2025


---

### se...@gmail.com (2025-11-21)

Considering the latest commit,
you should also take into account that:

1. STTF search is case-insensitive, meaning `#:~:text=slonser`, `#:~:text=sLonser`, `#:~:text=slONser`, etc. are identical for text search, but are treated as different when inserted into a `HashSet`.
2. STTF has a syntax for highlighting between words — `#:~:text=Lorem%20ipsum,slonser` — which can also be used to bypass the HashSet-based fix.

I think the second point will be difficult for you to resolve (which is why I initially mentioned in <https://issues.chromium.org/issues/457771782#comment6> that it’s not realistic).
So I hope you will also implement the length-based fix.

### vm...@google.com (2025-11-27)

Thanks, yeah it's a good point about case sensitivity. I can address that. The length fix likely requires spec adjustments. The spec is currently going through a rework so it's an unfortunate timing to also be making changes. However, I can file an issue to discuss this.

### vm...@google.com (2025-11-27)

Filed <https://github.com/whatwg/html/issues/11968> to discuss the length-based fix and the case sensitivity (along with the killswitch) is in review

### se...@gmail.com (2025-11-28)

I reviewed this [fix](https://chromium-review.googlesource.com/c/chromium/src/+/7205570/2/third_party/blink/renderer/core/fragment_directive/fragment_directive.cc#182)

It's uses:

```
value.LowerASCII()

```

This is problematic in itself as it won't affect other languages.

But most importantly - the [text searcher](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/editing/iterators/text_searcher_icu.cc;drc=a1bff76010bbe4df2582255696963322e563c4d0;l=165) uses Unicode normalization:

```
normalized_search_text_ = NormalizeCharactersIntoNfc(pattern.Span16())

```

Accordingly, a payload like:
`https://pocs.neplox.security/demo_text_1337.html#:~:text=S%F0%9D%93%94CRET` will match the text, but will also pass this check.

Therefore, it's better to use [`NormalizeCharactersIntoNfc`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/text/unicode_utilities.cc;l=307;drc=a1bff76010bbe4df2582255696963322e563c4d0;bpv=0;bpt=1) + [`UnicodeString& toLower()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/icu/source/common/unicode/unistr.h;drc=a1bff76010bbe4df2582255696963322e563c4d0;l=2771)

Also, The [Unicode Collation Algorithm](https://www.unicode.org/reports/tr10/) defines certain [characters](https://www.unicode.org/Public/UCA/latest/allkeys.txt) with zero weight, which will be ignored. For example, `https://pocs.neplox.security/demo_text_1337.html#:~:text=S%E2%80%8BECRET` will successfully find the text. It seems this can only be fixed by obtaining the collation key via [ucol\_getSortKey](https://source.chromium.org/chromium/chromium/src/+/main:third_party/icu/source/i18n/ucol.cpp;l=198;drc=a1bff76010bbe4df2582255696963322e563c4d0;bpv=1;bpt=1) (just thoughts, I haven't tested this).

I know this code hasn't passed review yet, but I decided to help and share my thoughts on why the current fix is ineffective.

### vm...@google.com (2025-11-28)

Thank you for the review and detailed thoughts.

Just to note the code fixes here are mitigations that make it less likely for this exploit. As you pointed out in your previous comments, even with unicode normalization, the range searches will still count as unique. A stronger mitigation is the html issue that I filed. Again, it's only a mitigation.

I think the proper fix is to actually address the problem that Liam pointed out in comment 13: we shouldn't be scrolling at all for these cases. @ra...@google.com should be able to comment on how feasible it is to address this core problem.

### dx...@google.com (2025-11-28)

Project: chromium/src  

Branch:  main  

Author:  Vladimir Levin [vmpstr@chromium.org](mailto:vmpstr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7205570>

TextFragments: Use ASCII lower case when considering unique fragments.

---


Expand for full commit details
```
     
    Since Scroll to Text Fragment is case insensitive, only use LowerASCII 
    to ensure uniqueness of text fragments. 
     
    This patch also adds a killswitch in case this regresses a case in 
    the wild. 
     
    R=flackr@chromium.org 
     
    Bug: 457771782 
    Change-Id: I4dde41fad4602f11747794f4b3e4f7b3eddb0780 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7205570 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Robert Flack <flackr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1551548}

```

---

Files:

- M `third_party/blink/renderer/core/fragment_directive/fragment_directive.cc`
- M `third_party/blink/renderer/core/fragment_directive/fragment_directive_test.cc`
- M `third_party/blink/renderer/platform/runtime_enabled_features.json5`

---

Hash: [5173e4b34d63b58a9262d615962664b4e7ee3a42](https://chromiumdash.appspot.com/commit/5173e4b34d63b58a9262d615962664b4e7ee3a42)  

Date: Fri Nov 28 15:50:23 2025


---

### ra...@chromium.org (2025-12-01)

I'm trying to understand the problem here. Is my understanding correct:

1. Navigation to URL that triggers STTF then commits in the renderer, but the actual scrolling that happens (synchronously at commit?) is slow and blocks the renderer. This slowness is triggered only if the match happens, so it's possible to differentiate match result if it's possible to detect renderer being busy.
2. The window.open updates RelatedPages in the attacker renderer, but with unfortunate timing, the update to the target renderer didn't arrive before the commit at #1. Thus this isn't detected at commi, and the scroll will still happen.
3. The opener can detect that the STTF match happens by checking if same-document navigations get committed or not before the about:blank navigation. The same-document navs are usually fast, unless the renderer is busy. Thus it can detect whether a match happens at #1.

It looks like there are many steps that need to happen in order to do this attack, so there are a couple options on how to fix this:

**Make the RelatedPages check accurate when committing STTF navigations**: This is because the RelatedPages update need to go from attacker process -> browser process -> target process, and it might not get updated in time before the STTF navigation commit. I think this is hard because the attacker page / initiator can trigger window creation at any point, potentially really close to when the commit happens, so timely checks isn't really possible to guarantee. But at least we can make the time window where it's possible to create window of time where it's possible smaller, by e.g. creating check on the browser side at ReadyToCommitNavigation time that checks for opener existence, and ban the triggering of STTF in the renderer if any exists. Thus we only need to care about cases where a window is created after ReadyToCommit is sent. If we want to limit this window of time entirely, maybe something like "ban all popup creation while an STTF search is in progress" but that probably needs standardization and I'm not sure if it's possible to add such a powerful policy (and if not careful, it can be another easy way to detect STTF match vs not).

**Make the difference between STTF match vs no match not observable**: If we can somehow skip the expensive operation, or make it not observable. I'm not sure if it's possible, but the fixes above are doing this direction I guess. If there's no/negligible difference in renderer business, then the attacker can't infer anything. I'll let STTF owners comment on this feasibility.

**Make the opener not able to detect the renderer being busy**:. STTF is just one of the potentially many ways to infer information from renderer being busy or not. If we can remove the way we detect the renderer being busy or not, we can prevent more this class of bug. I think there's actually some similar conversations around this already around not exposing history.length or making fragment navigations be cross-document when the initiator is cross-origin (so that it can't be determined that the about:blank wins because the renderer is busy). See also [crbug.com/40062026](https://crbug.com/40062026).

I'm temporarily assigning to clamy@ because of the last point (and also this is about web platform security), but I think the STTF owners should also chime in about the options above.

### ma...@google.com (2025-12-01)

Rakina, I believe your understanding is correct. One note:

> but that probably needs standardization and I'm not sure if it's possible to add such a powerful policy

If STTF as-spec'd isn't possible to implement securely, that probably needs to feed back into a refinement of the spec.

More broadly -- my experience with side-channel information leaks is that our priorities should be:

1. First, try not to create information that can be leaked in the first place. Here, that means "fix the cross-origin check for STTF navigation and make it reliable". As discussed in [comment#4](https://issues.chromium.org/issues/457771782#comment4), if we fix this, we win. **We have to at least try to do this**, even if -- for the reasons detailed in [comment#28](https://issues.chromium.org/issues/457771782#comment28) -- we may come up short.
2. If not (1), then try to reduce the amount of information leaked. Here, that's "avoid amplification attacks due to unbounded number of potentially-duplicated fragments", which seems like a fine defense-in-depth measure -- but, again, **we have to try to solve (1) first**.
3. **Only if all else fails**, try to reduce the attacker's ability to observe the difference in behavior. This is almost always a losing game, and usually ends up with reporters coming back with clever ways we didn't think of to pick up the information we leaked into a domain where it doesn't belong.

### se...@gmail.com (2025-12-01)

Let me also remind you that you have the option to make the search asynchronous.

This option might be worse than a proper BCG check, but it should also completely solve the problem (since if the search does not create a side effect like blocking the process, it becomes impossible to detect).

It seems that the reasons why this solution is bad weren't explicitly discussed, so I decided to state this option clearly again.

### cl...@google.com (2025-12-05)

I agree with Matt that we should really try to fix the cross-origin check for STTF navigation, because if we make this work we solve the issue. Making the search asynchronous would prevent this specific POC from working, but I would not bet there are no other ways to detect it.

If we want to make the cross-origin check for STTF navigation work, I wonder if we should move the check to the browser process in the first place, and pass down the result to the renderer process. In fact, if I were to implement it from scratch this is what I would do to avoid this kind of race conditions.

Navigations are coordinated in the browser process. So we can check at commit time whether there is any other page in the BCG and pass down the information to the renderer process. Unfortunately, there is a delay between the moment we ask a renderer process to commit a navigation and the moment it actually does and we get rid of the old document. So it might be possible to trigger the window.open in this brief period? If this is possible, I wonder if we can just record that we're trying to commit the STTF navigation and just prevent the window.open during the commit timing. This would ensure our only one page in the BCG invariant is properly preserved.

### ra...@chromium.org (2025-12-15)

For [#comment31](https://issues.chromium.org/issues/457771782#comment31), I think if we prevent window.open during the navigation commit, it might reveal to the window.opener page that the lengthy STTF find step is still running. So instead of detecting by doing fragment navigations, the attacker can do window.open and see if it works (or is delayed, if we delay window.open/actions sent through it instead). Not sure how hard it is to time that though, as that needs to happen after CommitNavigation is sent.

If we really want to close the gap 100% I think making the search asynchronous like mentioned in [#comment30](https://issues.chromium.org/issues/457771782#comment30) might be necessary. That will unblock the DidCommitNavigation call to the browser and then the previous page can be unloaded, and even if window.open successfully runs before that happens, it can't tell that the lengthy find takes a long time.

### ch...@google.com (2025-12-16)

clamy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-31)

clamy: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-04)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### xi...@chromium.org (2026-01-08)

[Secondary Shepherd] Thanks for the discussion so far. If I'm following it correctly, Rakina, it seems that you are the point person for the next step?

### ch...@google.com (2026-01-23)

rakina: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### th...@chromium.org (2026-01-23)

[secondary shepherd] rakina@, could you please respond to #comment36? (will send a ping over chat as well)

### ra...@chromium.org (2026-01-26)

I think the decision here should be taken by the STTF owners or the Web Platform Security folks re [#comment28](https://issues.chromium.org/issues/457771782#comment28), so let me assign to vmpstr@ for now. Option 1 in my comment isn't really possible without some potential STTF observable behavior/spec changes, see [#comment32](https://issues.chromium.org/issues/457771782#comment32). Option 2 & 3 are also observable behavior changes.

If making the attack less reliable by making the window of time smaller is acceptable as a fix, we can implement the change mentioned in [#comment31](https://issues.chromium.org/issues/457771782#comment31) (but with caveats mentioned in [#comment32](https://issues.chromium.org/issues/457771782#comment32)) through adding a check in the browser process at the last possible moment before going to the renderer. Again, I don't think that fixes this problem fully, but just in case other options are not feasible.

### vm...@google.com (2026-01-29)

My understanding of the timing here is a bit limited, but is it an option to not find/scroll until we have received the information that lets us know whether or not we're permitted to do the scroll.

STTF doesn't seem like it's a particularly timing sensitive feature as long as the scroll does happen fairly quickly from the user's perspective. However, sending these related sites (or generally whatever is necessary to detect that we're not allowed to scroll) seems more timing critical.

So if we can say "we have a pending STTF" but we're waiting until we know whether we can execute it. Then when we find out with the signal, we either drop the pending STTF or execute it with a synchronous search/scroll.

The reason I'm proposing this is that the asynchronous search is not something we would be able to implement in any reasonable time frame, since it's not being prioritized. The only priority for it would be to fix this particular bug.

I don't know what it takes to fixing the "allowed to scroll" information timing though.
-> rakina@, wdyt?

### ra...@chromium.org (2026-01-30)

Re: pending STTF until some signal, I think alexmos@ mentioned that we block popup creation from a pending delete document, so the "RelatedPages" value that can be influenced cross-process should be final at that point. So we can make cross-process STTF wait until the previous document has reached "pending delete" state, maybe by sending an IPC from the browser -> renderer for that. It might add some delay but I guess there's not a big concern.

BTW I thought find-in-page can already run async / not blocking the renderer in big chunks, is it possible to make the STTF search async in that way too if that's easier?

### ch...@google.com (2026-02-14)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### vm...@google.com (2026-02-17)

I think the renderer is set up to run async find-in-page after the initial chunk has been synchronously processed (this knowledge may be out of date). Maybe @bo...@google.com knows whether it's possible to always make this async.

My preference would be to have correct RelatedPages information before we do anything at all though. Rakina, do you know how much effort that would be? It sounds like we have the right signals already in the browser

### ra...@chromium.org (2026-03-02)

OK I think the solution on #c41 might be what you want then, although that also doesn't let you to process the initial chunk synchronously. When committing the navigation, don't immediately trigger the initial chunk processing. Instead, wait for the signal that the previous document is already pending delete before processing, which should be sent from somewhere in [RenderFrameHostManager::UnloadOldFrame()](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=1199;drc=56c66e417c83e2096a4e4e8a5c4ab7bbd525c9f3). That guarantees the RelatedPages value is up-to-date and won't change. Not sure where the STTF processing starts so it might be best for STTF people to implement the fix, let me know if you need more pointers.

### vm...@google.com (2026-03-02)

Yeah, I'm happy to try my hand at implementing this.

I do need some pointers/clarifications if you don't mind: I assume you mean that in RendererFrameHostManager::UnloadOldFrame we should send a new IPC to the new frame to let it know that its RelatedPages is finalized. Then we can use this signal to actually allow STTF that may be pending (and obviously disallow it prior to this signal). Or do you mean that such an IPC exists already and we can just do the STTF part?

### ra...@chromium.org (2026-03-03)

Yeah that would be a new IPC, and it doesn't have to contain any info. It's just to let the renderer know that there can be no further RelatedPages update from the previous document (since it's already unloading)

### vm...@google.com (2026-03-03)

Got it. I'm gonna work on the assumption that exposing the timing of unload from the previous renderer to the new one is ok from security perspective.

### vm...@google.com (2026-03-03)

hmm so I have this <https://chromium-review.googlesource.com/c/chromium/src/+/7629937>. This doesn't seem to address the simpler case from #13. Specifically the printfs I have there say that we delayed the fragment processing but when we did process it, the related pages size was still 0.

I haven't closely followed the discussion here, but my understanding is that that should be 1 since the window.open opened a window to the same site

FWIW, I haven't tried the OP repro case yet.

@ra...@chromium.org wdyt?

### ra...@chromium.org (2026-03-13)

Sorry finally got a chance to try the repro and investigate now. I think there is actually a race condition with RelatedPages here. It looks like the RelatedPages in the popup is correctly updated to 1 when it commits, but the one in the victim page is 0 if the victim page commits first in the tab, because it's in a different process and didn't know it has an openee (as the popup doesn't exist yet). When the proxy for the popup is created in the victim's process, the RelatedPages of the victim still doesn't get updated if it uses the previous page's FrameToken for the `opener`. So yeah this is definitely prone to race conditions, might be worth a separate bug since I think this would likely need a big rethink.

For now, since there is a quick fix for the security bug here is to do it async, and it seems like with [crrev.com/c/7629937](https://crrev.com/c/7629937) that is actually possible, although not done in chunks yet. Maybe going with the async + probably doing in chunks solution makes more sense at this point? The RelatedPages part definitely is buggy so that needs to be fixed, but I'm not confident that there is bandwidth to do that soon.

### ch...@google.com (2026-03-18)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### vm...@google.com (2026-04-29)

This CL <https://chromium-review.git.corp.google.com/c/chromium/src/+/7629937> is likely to address the problem. It bypasses the browser race by simply telling the renderer whether there are any other related pages that it may not know about. The renderer then uses that to determine whether or not it can do the text fragment operations.

### dx...@google.com (2026-05-05)

Project: chromium/src  

Branch:  main  

Author:  Vladimir Levin [vmpstr@chromium.org](mailto:vmpstr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7629937>

STTF: Delay sttf until related pages are finalized.

---


Expand for full commit details
```
     
    This patch delays sttf until related pages are finalized. It also 
    sends the browser-authoritative bool indicating whether there are 
    related pages associated with this renderer. 
     
    R=rakina@chromium.org 
     
    Bug: 457771782 
    Change-Id: Ifc03488451bd3d1e99c4ab447362437778ddf96d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7629937 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Ken Buchanan <kenrb@chromium.org> 
    Reviewed-by: Ari Chivukula <arichiv@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1625391}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `third_party/blink/public/mojom/frame/frame.mojom`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor_metrics_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_generation_navigation_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_handler_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_test_util.cc`
- M `third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc`
- M `third_party/blink/renderer/core/frame/local_frame_mojo_handler.h`
- M `third_party/blink/renderer/core/loader/document_loader.h`
- M `third_party/blink/renderer/core/loader/frame_loader.cc`
- M `third_party/blink/renderer/core/loader/frame_loader.h`
- M `third_party/blink/renderer/core/page/page.h`
- M `third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/resources/text-fragment-target-auto.html`
- A `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/popup1.sub.html`
- A `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/popup2.html`
- A `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/target.html`
- A `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/scroll-to-text-fragment-cross-window.html`

---

Hash: [bd673b924ed9683f485674d2b9b702bdc5855aaa](https://chromiumdash.appspot.com/commit/bd673b924ed9683f485674d2b9b702bdc5855aaa)  

Date: Tue May 5 14:05:38 2026


---

### dx...@google.com (2026-05-05)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7818407>

Revert "STTF: Delay sttf until related pages are finalized."

---


Expand for full commit details
```
     
    This reverts commit bd673b924ed9683f485674d2b9b702bdc5855aaa. 
     
    Reason for revert: TextFragmentAnchorTest.AvoidScrollingIfHasOtherRelatedPages failed at https://ci.chromium.org/ui/p/chromium/builders/ci/Linux%20UBSan%20Tests/15610/overview 
     
    Original change's description: 
    > STTF: Delay sttf until related pages are finalized. 
    > 
    > This patch delays sttf until related pages are finalized. It also 
    > sends the browser-authoritative bool indicating whether there are 
    > related pages associated with this renderer. 
    > 
    > R=rakina@chromium.org 
    > 
    > Bug: 457771782 
    > Change-Id: Ifc03488451bd3d1e99c4ab447362437778ddf96d 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7629937 
    > Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    > Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    > Reviewed-by: Ken Buchanan <kenrb@chromium.org> 
    > Reviewed-by: Ari Chivukula <arichiv@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1625391} 
     
    Bug: 457771782 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I09963b56dd4e42b8402fd3a5533c012d11c31b58 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7818407 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Ari Chivukula <arichiv@chromium.org> 
    Owners-Override: Dale Curtis <dalecurtis@chromium.org> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1625666}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `third_party/blink/public/mojom/frame/frame.mojom`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor_metrics_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_generation_navigation_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_handler_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_test_util.cc`
- M `third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc`
- M `third_party/blink/renderer/core/frame/local_frame_mojo_handler.h`
- M `third_party/blink/renderer/core/loader/document_loader.h`
- M `third_party/blink/renderer/core/loader/frame_loader.cc`
- M `third_party/blink/renderer/core/loader/frame_loader.h`
- M `third_party/blink/renderer/core/page/page.h`
- M `third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/resources/text-fragment-target-auto.html`
- D `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/popup1.sub.html`
- D `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/popup2.html`
- D `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/target.html`
- D `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/scroll-to-text-fragment-cross-window.html`

---

Hash: [a257d3550c097f9c4550f7bb229ca7cedeaf7485](https://chromiumdash.appspot.com/commit/a257d3550c097f9c4550f7bb229ca7cedeaf7485)  

Date: Tue May 5 19:57:44 2026


---

### dx...@google.com (2026-05-07)

Project: chromium/src  

Branch:  main  

Author:  Vladimir Levin [vmpstr@chromium.org](mailto:vmpstr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7818478>

Reland "STTF: Delay sttf until related pages are finalized."

---


Expand for full commit details
```
     
    Fixed the test. 
     
    Original reason for revert: TextFragmentAnchorTest.AvoidScrollingIfHasOtherRelatedPages failed at https://ci.chromium.org/ui/p/chromium/builders/ci/Linux%20UBSan%20Tests/15610/overview 
     
    Original change's description: 
    > STTF: Delay sttf until related pages are finalized. 
    > 
    > This patch delays sttf until related pages are finalized. It also 
    > sends the browser-authoritative bool indicating whether there are 
    > related pages associated with this renderer. 
    > 
    > R=rakina@chromium.org 
    > 
    > Change-Id: Ifc03488451bd3d1e99c4ab447362437778ddf96d 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7629937 
    > Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    > Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    > Reviewed-by: Ken Buchanan <kenrb@chromium.org> 
    > Reviewed-by: Ari Chivukula <arichiv@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1625391} 
     
    Bug: 457771782 
    Change-Id: I9a36bfc18d12af87e96880bd565e670a2c9068ff 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7818478 
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org> 
    Reviewed-by: Joe Mason <joenotcharles@google.com> 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1627144}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `third_party/blink/public/mojom/frame/frame.mojom`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor_metrics_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_anchor_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_generation_navigation_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_handler_test.cc`
- M `third_party/blink/renderer/core/fragment_directive/text_fragment_test_util.cc`
- M `third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc`
- M `third_party/blink/renderer/core/frame/local_frame_mojo_handler.h`
- M `third_party/blink/renderer/core/loader/document_loader.h`
- M `third_party/blink/renderer/core/loader/frame_loader.cc`
- M `third_party/blink/renderer/core/loader/frame_loader.h`
- M `third_party/blink/renderer/core/page/page.h`
- M `third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/resources/text-fragment-target-auto.html`
- A `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/popup1.sub.html`
- A `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/popup2.html`
- A `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/target.html`
- A `third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/scroll-to-text-fragment-cross-window.html`

---

Hash: [edf09a64a6e305874741d429931de797eb63c1f4](https://chromiumdash.appspot.com/commit/edf09a64a6e305874741d429931de797eb63c1f4)  

Date: Thu May 7 19:35:15 2026


---

### vm...@google.com (2026-05-08)

Bugjuggler: wait 1 week -> fixed

### bu...@google.com (2026-05-08)

Hi. I've received your bug and will wait until 2026-05-15 10:40 -0400 EDT and then change assignee to vmpstr@google.com and mark as fixed.

### ch...@google.com (2026-05-15)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High quality. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514926548](https://crbug.com/514926548) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514929028](https://crbug.com/514929028) to have this merge reviewed.**

### ch...@google.com (2026-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/457771782)*
