# Security: Blockfile Media Cache UaF

| Field | Value |
|-------|-------|
| **Issue ID** | [40090939](https://issues.chromium.org/issues/40090939) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>Cache |
| **Platforms** | Fuchsia, Mac, Windows, iOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | mo...@chromium.org |
| **Created** | 2018-03-28 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

The disk\_cache component of the net subsystem in the browser process handles caching using a few different backends. The blockfile cache is the default cache when browsing the web. This is used by HTTP requests and media requests (video/audio tags in HTML5).

When destroying a sparse entry, it's possible for a cache trim to take place when closing its child, allowing reentry of the parent's destructor.

See the following snippet (media cache case where new\_eviction\_ is false):

```
bool Eviction::EvictEntry(CacheRankingsBlock\* node, bool empty,  
                          Rankings::List list) {  
...  
  if (empty || !new_eviction_) {  
    entry->DoomImpl();  
  } else {  
    entry->DeleteEntryData(false);  

```

The bug is in the empty || !new\_eviction\_ case. DeleteEntryData posts a task to the current thread, so we avoid reentering the destructor. empty is true when the user clears the cache explicitly. !new\_eviction\_ is true when the media cache is in use, which can be triggered without user interaction by opening a video/audio file in HTML5 and using javascript to seek within it, allowing us to make disjoint (non-sequential) range requests like I use in the WriteSparseData calls in my attached testcase.

Note that TrimCacheV2 (DISK\_CACHE case) also has this bug when the user is clearing the cache explicitly: they have the same construction

```
  if (empty) {  
    TrimDeleted(true);  
  } else if (ShouldTrimDeleted()) {  
    base::ThreadTaskRunnerHandle::Get()->PostTask(  
        FROM_HERE,  
        base::Bind(&Eviction::TrimDeleted, ptr_factory_.GetWeakPtr(), empty));  
  }  

```

where the PostTask case is safe but the immediate TrimDeleted(true) is unsafe because it can reentrantly Doom the entry. If my explanation here is confusing or inaccurate, please just use the provided test case and I can give pointers if there are still bugs lying around.

I did manage to repro this against the media cache backend at the http\_cache\_transaction.cc layer, but that required significant source modifications to enable mocked HTTP responses, so my attached test only triggers the bug immediately at the blockfile cache layer.

P.S. Cache trimming does not take place for the first 5 minutes of the session, but Pwn2Own rounds are 5 minutes max...

**VERSION**  

Chrome Version: 65 Stable (latest)  

Operating System: All

**REPRODUCTION CASE**  

Apply attached patch, then build and run the net\_unittests.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Browser  

Crash State: see attached log

## Attachments

- [testcase.patch](attachments/testcase.patch) (application/octet-stream, 1.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 12.3 KB)
- [likely_fix.diff](attachments/likely_fix.diff) (application/octet-stream, 3.3 KB)

## Timeline

### el...@chromium.org (2018-03-28)

Thanks for the report!

[Monorail components: Internals>Network>Cache]

### mm...@chromium.org (2018-03-28)

Maksim, would you mind taking a look at that?

### mo...@chromium.org (2018-03-28)

I can confirm, though OS = All is incorrect --- Linux based OSs (most importantly Android) do not use this backend; sadly I don't know blockfile well enough to immediately know how to fix this; though the idea of deferring is an interesting one.

(See also https://bugs.chromium.org/p/chromium/issues/detail?id=518908 https://crbug.com/chromium/826626#c8 and on, where I fail to realize the severity --- thank you for setting me straight on that; 802886 and 537063 are probably the same thing).

### ne...@gmail.com (2018-03-28)

@morlovich: thanks for pointing that out. I thought only Android was not affected (so my "OS: All" was inaccurate anyways, I apologize).

It looks like the simple/blockfile backend is selected here: https://cs.chromium.org/chromium/src/components/network_session_configurator/browser/network_session_configurator.cc?l=612

### mm...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-03-28)

CC'ing more folks.

### mo...@chromium.org (2018-03-28)

Possible fix attached --- it passes the testcase, and rest of net_unittests. Thank you for the inspiration of mentioning delaying stuff, this turned out simpler than what I first thought of (pinning entries). I haven't tried wider tests yet, though;  since I am not sure I should be uploading it.

@mmoroz: what should I be doing with this beyond this? Not really familiar with the process involved.

@reporter: is it OK to use your testcase (with somewhat less... descriptive name)? You do seem to have a CLA, and it looks like a pretty delicate piece of work.




### mm...@chromium.org (2018-03-28)

morlovich@, thanks for the fast reaction! You don't need to do anything special, just a regular development workflow: upload a CL for review, land it, etc. After that we'll probably have to merge it into Stable / Beta branches.

CC'ing awhalley@ for CLA question from c#7, but in general we do accept patches suggested by external reporters without any trouble and even issue an additional monetary bonus for that.

If you're paranoid to some degree, you may avoid using words like "Use-after-Free", "Security critical", etc in the CL description, but I'm afraid we usually don't do that :)

### ne...@gmail.com (2018-03-28)

This fix looks quite nice, and is along the lines of what I expected (delay in a way that prevents reentry). Feel free to use the testcase and rename it. There's a reason I didn't open a CL for that...

When I was playing with this the synchronous cache clearing case (requires user interaction through the settings) was also sensitive as I alluded to in the initial report. I'll let you know if those appear anywhere when I have a chance to check tonight and follow up with additional testcases if necessary.

### mo...@chromium.org (2018-03-28)

Thanks!

Hmm, while blockfile only uses one thread for I/O, sparse ops are indeed done in multiple steps, so they could conceivably interleave with a SyncDoomAll while they have a bunch of state right around here:
https://cs.chromium.org/chromium/src/net/disk_cache/blockfile/sparse_control.cc?rcl=3058c82b689803f9031a4fbfa1d7cd7f4b856b07&l=750

...Well, at least it's not triggerable with site-clear-data.


### ne...@gmail.com (2018-03-28)

@morlovich: what prevents syncdoomall from being interleaved here? That's the only reason I thought there could be an issue here and understanding that will let me figure out if there are any other bugs just in case. I'm pretty sure I managed to crash it before by interleaving things the way you mention in c10.

I'm looking here for the site-clear-data:
https://cs.chromium.org/chromium/src/content/browser/browsing_data/storage_partition_http_cache_data_remover.cc?l=151&rcl=ec0fe70383874453ccb756bf83c7cdfba670682f

### mo...@chromium.org (2018-03-28)

Not exactly sure as to what you're asking; what's "here" in your first sentence supposed to be bound to?

If it's about site-clear-data, I am assuming it would pass in a url_predicate_ that implement the 'site' part of the name, though I didn't actually verify it.


### aw...@google.com (2018-03-28)

Re mentioning security issues in commit messages: We try to be coy about the security implementations, and focus on describing the fix in general terms.

### ne...@gmail.com (2018-03-28)

@morlovich: The most direct version of my question is this: in my original testcase, where can `EXPECT_THAT(DoomAllEntries(), IsOk());` appear according to things possible via user interaction? (i.e. at the very end only, interleaved in any way, etc.) It seems clear that it can appear somewhere but it may be constrained depending on how site-clear-data actually works. Thanks for following up - fwiw I was able to repro this under only one domain, if that's what you mean by url_predicate_.

### ne...@gmail.com (2018-03-28)

By one domain I mean multiple requests of the pattern: http://localhost/<int> (you have to play with it because of the hashing).

### mo...@chromium.org (2018-03-28)

Ah, OK. My understanding is that:

DoomAllEntries can appear anywhere --- and beyond that can execute in between partial steps of something like WriteSparseData --- but I don't know much about the UI side of things. What I mean by partial steps is this: 
1) All I/O is done by blockfile on one background thread, using async I/O.
2) Blockfile implements sparse entries as a two-level tree. This means if one calls WriteSparseData that writes more than one child, it will relinquish control of the background thread until write to that specific child completes -- meaning SyncDoomAllEntries may also run during this time. 

This is in-the-middle thing makes me suspect that it may indeed be possible, it would be a crash in something like SparseControl::DoChildIO or SparseControl::DoChildrenIO.

However, it is also my understanding that clear-site-data header will not ever call DoomAllEntries, since it's not deleting the entire cache, but only one domain 
(which is important since it keeps it at UI-interaction level).



### ne...@gmail.com (2018-03-29)

I got a chance to play with things again tonight, and I'm pretty sure this fix mitigates the problem in the new_eviction_ as well even in the face of DoomAllEntries. The basic issue here was trimming during the child destructor (who could bump the "free" bytes over the eviction threshold). When we went to Doom it we would look up its parent in InternalDoomEntry and add a reference back to the parent who was being destroyed. Awesome quick fix! Hopefully when the CL lands we don't see any serious regressions.

### mo...@chromium.org (2018-03-29)

+Matt because he feels like the most appropriate choice of reviewer for this, and would want context

### sh...@chromium.org (2018-03-29)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-03-29)

Is there anything that needs to be merged to M66 branch right now? Once ready, please make sure to add Merge-Request-66. 

### mo...@chromium.org (2018-03-29)

It hasn't landed yet; I presume the usual 24 hours in canary should happen beforehand, too?


### bu...@chromium.org (2018-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/df5b1e1f88e013bc96107cc52c4a4f33a8238444

commit df5b1e1f88e013bc96107cc52c4a4f33a8238444
Author: Maks Orlovich <morlovich@chromium.org>
Date: Fri Mar 30 03:51:06 2018

Blockfile cache: fix long-standing sparse + evict reentrancy problem

Thanks to nedwilliamson@ (on gmail) for an alternative perspective
plus a reduction to make fixing this much easier.

Bug: 826626, 518908, 537063, 802886
Change-Id: Ibfa01416f9a8e7f7b361e4f93b4b6b134728b85f
Reviewed-on: https://chromium-review.googlesource.com/985052
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/heads/master@{#547103}
[modify] https://crrev.com/df5b1e1f88e013bc96107cc52c4a4f33a8238444/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/df5b1e1f88e013bc96107cc52c4a4f33a8238444/net/disk_cache/blockfile/backend_impl.cc
[modify] https://crrev.com/df5b1e1f88e013bc96107cc52c4a4f33a8238444/net/disk_cache/blockfile/backend_impl.h
[modify] https://crrev.com/df5b1e1f88e013bc96107cc52c4a4f33a8238444/net/disk_cache/blockfile/in_flight_backend_io.cc


### bu...@chromium.org (2018-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/87b3e251dc1941e7e14a17f150c6cc1f39ccf748

commit 87b3e251dc1941e7e14a17f150c6cc1f39ccf748
Author: Findit <findit-for-me@appspot.gserviceaccount.com>
Date: Fri Mar 30 06:36:25 2018

Revert "Blockfile cache: fix long-standing sparse + evict reentrancy problem"

This reverts commit df5b1e1f88e013bc96107cc52c4a4f33a8238444.

Reason for revert:

Findit (https://goo.gl/kROfz5) identified CL at revision 547103 as the
culprit for failures in the build cycles as shown on:
https://findit-for-me.appspot.com/waterfall/culprit?key=ag9zfmZpbmRpdC1mb3ItbWVyRAsSDVdmU3VzcGVjdGVkQ0wiMWNocm9taXVtL2RmNWIxZTFmODhlMDEzYmM5NjEwN2NjNTJjNGE0ZjMzYTgyMzg0NDQM

Sample Failed Build: https://ci.chromium.org/buildbot/chromium.memory/Linux%20MSan%20Tests/8841

Sample Failed Step: net_unittests

Original change's description:
> Blockfile cache: fix long-standing sparse + evict reentrancy problem
> 
> Thanks to nedwilliamson@ (on gmail) for an alternative perspective
> plus a reduction to make fixing this much easier.
> 
> Bug: 826626, 518908, 537063, 802886
> Change-Id: Ibfa01416f9a8e7f7b361e4f93b4b6b134728b85f
> Reviewed-on: https://chromium-review.googlesource.com/985052
> Reviewed-by: Matt Menke <mmenke@chromium.org>
> Commit-Queue: Maks Orlovich <morlovich@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#547103}

Change-Id: I79f8547110bb29265e17dd38f751c948de1910c4
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 826626, 518908, 537063, 802886
Reviewed-on: https://chromium-review.googlesource.com/987692
Cr-Commit-Position: refs/heads/master@{#547120}
[modify] https://crrev.com/87b3e251dc1941e7e14a17f150c6cc1f39ccf748/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/87b3e251dc1941e7e14a17f150c6cc1f39ccf748/net/disk_cache/blockfile/backend_impl.cc
[modify] https://crrev.com/87b3e251dc1941e7e14a17f150c6cc1f39ccf748/net/disk_cache/blockfile/backend_impl.h
[modify] https://crrev.com/87b3e251dc1941e7e14a17f150c6cc1f39ccf748/net/disk_cache/blockfile/in_flight_backend_io.cc


### mo...@chromium.org (2018-03-30)

Looks like msan just wants the buffer in the new test initialized, considering it's being written to disk. Simple enough, but the process stuff will take a bit. 

### bu...@chromium.org (2018-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dd44592937e7d78c7c75489d5a6e9bb0b4967f4a

commit dd44592937e7d78c7c75489d5a6e9bb0b4967f4a
Author: Maks Orlovich <morlovich@chromium.org>
Date: Fri Mar 30 15:06:52 2018

Blockfile cache: fix sparse + evict reentrancy problem, take 2.

Thanks to nedwilliamson@ (on gmail) for an alternative perspective
plus a reduction to make fixing this much easier.

Difference to take 1 is call to CacheTestFillBuffer in new test,
to address msan's reasonable complaints and not try to write an
unitialized buffer to disk (cache).

Bug: 826626, 518908, 537063, 802886
Change-Id: I1109f51511391c3c91bbeb76db0a09c319905819
Reviewed-on: https://chromium-review.googlesource.com/987515
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/heads/master@{#547159}
[modify] https://crrev.com/dd44592937e7d78c7c75489d5a6e9bb0b4967f4a/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/dd44592937e7d78c7c75489d5a6e9bb0b4967f4a/net/disk_cache/blockfile/backend_impl.cc
[modify] https://crrev.com/dd44592937e7d78c7c75489d5a6e9bb0b4967f4a/net/disk_cache/blockfile/backend_impl.h
[modify] https://crrev.com/dd44592937e7d78c7c75489d5a6e9bb0b4967f4a/net/disk_cache/blockfile/in_flight_backend_io.cc


### mo...@chromium.org (2018-04-02)

No signs of trouble caused by this in Canary over weekend, so requesting merge to beta.

@mmoroz : please let me know if it's not the right process for this sort of bug.


### sh...@chromium.org (2018-04-02)

This bug requires manual review: Less than 11 days to go before AppStore submit on M66
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-02)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-04-02)

Approving merge to M66. Branch:3359

### bu...@chromium.org (2018-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d7bf5f00c28ebb2e367830c8f371616208379d5f

commit d7bf5f00c28ebb2e367830c8f371616208379d5f
Author: Maks Orlovich <morlovich@chromium.org>
Date: Mon Apr 02 17:37:35 2018

Blockfile cache: fix sparse + evict reentrancy problem, take 2.

Thanks to nedwilliamson@ (on gmail) for an alternative perspective
plus a reduction to make fixing this much easier.

Difference to take 1 is call to CacheTestFillBuffer in new test,
to address msan's reasonable complaints and not try to write an
unitialized buffer to disk (cache).

Bug: 826626, 518908, 537063, 802886
Change-Id: I1109f51511391c3c91bbeb76db0a09c319905819
Reviewed-on: https://chromium-review.googlesource.com/987515
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Maks Orlovich <morlovich@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#547159}(cherry picked from commit dd44592937e7d78c7c75489d5a6e9bb0b4967f4a)
Reviewed-on: https://chromium-review.googlesource.com/990212
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/branch-heads/3359@{#526}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/d7bf5f00c28ebb2e367830c8f371616208379d5f/net/disk_cache/backend_unittest.cc
[modify] https://crrev.com/d7bf5f00c28ebb2e367830c8f371616208379d5f/net/disk_cache/blockfile/backend_impl.cc
[modify] https://crrev.com/d7bf5f00c28ebb2e367830c8f371616208379d5f/net/disk_cache/blockfile/backend_impl.h
[modify] https://crrev.com/d7bf5f00c28ebb2e367830c8f371616208379d5f/net/disk_cache/blockfile/in_flight_backend_io.cc


### sh...@chromium.org (2018-04-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-11)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-20)

And $10,000 for this one - cheers!

### aw...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### ne...@gmail.com (2018-04-20)

And thank you for this one too!

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/826626?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090939)*
