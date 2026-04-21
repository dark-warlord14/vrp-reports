# Security: Keystroke side-channel leakage 

| Field | Value |
|-------|-------|
| **Issue ID** | [40059532](https://issues.chromium.org/issues/40059532) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | IO>Keyboard |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | er...@gmail.com |
| **Assignee** | we...@chromium.org |
| **Created** | 2022-04-30 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

**-------------------------** -------------------------------------------------------  

Current Google Chrome versions leak which keys a user is pressing through  

memory access patterns. Moreover, we observed the same type of leakage in  

Chromium and Signal-Desktop. We assume that all chromium-based products are  

affected.

An attacker can extract these memory access patterns through different  

kinds of side-channel attacks, e.g., Flush+Reload [1] or Prime+Probe [2]  

targeting CPU caches, but also Page Cache Attacks targeting the page cache of  

the Linux kernel.

While we recognize that Google does not consider attacks where the attacker has  

to gain control of a local user's account as inside their thread model, the  

above described side-channel leakage might also be exploitable across virtual  

machine instances using Prime+Probe.

The leakage source is key-dependent access to the code strings in the DOM code  

table [4]:  

e.g.: "KeyA" in DOM\_CODE(0x070004, 0x001e, 0x0026, 0x001e, 0x0000, "KeyA", US\_A);  

As these strings seem to appear more often at different places in the code they  

are spread out over the .rodata section with large gaps between (many of them are  

on a unique 4kB page). This layout allows spying on a large number of unique  

keystrokes, even with side-channel attacks that have a coarse spatial granularity  

(like 4kB pages).

Below follows a mapping of keystrokes to accessed offsets in the chrome binary  

(100.0.4896.127 stable x64 DEB). This table can be reproduced by searching  

for the string "Key[A-Z]" and "Digit[0-9]" in the .rodata section.

File Offset Character String  

0x15295a0 KeyA  

0x1523bfb KeyB  

0x15209d0 KeyC  

0x1514122 KeyD  

0x1502dd7 KeyE  

0x1501d63 KeyF  

0x14ff390 KeyG  

0x14fdb7b KeyH  

0x14fc61e KeyI  

0x14fc3ed KeyJ  

0x14fad63 KeyK  

0x14f476c KeyL  

0x14f0964 KeyM  

0x14ecb6a KeyN  

0x14ebd29 KeyO  

0x14ea585 KeyP  

0x14ea22f KeyQ  

0x14e42c4 KeyR  

0x14dc6bf KeyS  

0x14d5471 KeyT  

0x14d3f69 KeyU  

0x14d0465 KeyV  

0x14cf851 KeyW  

0x14cde32 KeyX  

0x14cc396 KeyY  

0x14cbf20 KeyZ  

0x156442c Digit0  

0x155e8af Digit1  

0x15562e7 Digit2  

0x15523aa Digit3  

0x154f53e Digit4  

0x154d125 Digit5  

0x154b553 Digit6  

0x154a4cd Digit7  

0x1548a06 Digit8  

0x154797f Digit9 (noisy, disabled in POC)

[1] <https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-yarom.pdf>  

[2] <https://eprint.iacr.org/2005/271.pdf>  

[3] <https://arxiv.org/pdf/1901.01161.pdf>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:ui/events/keycodes/dom/dom_code_data.inc>

**VERSION**  

**-------------------------** -------------------------------------------------------  

Chrome Version: 100.0.4896.127 stable  

Operating System: Ubuntu 20.04.02 LTS

**REPRODUCTION CASE**  

**-------------------------** -------------------------------------------------------  

To reproduce the leakage, a demonstration website and a POC using the F+R  

side channel is attached.

The demonstration website "index.html" is a simple static HTML page with  

a password and textarea input. The keystroke leakage can be observed by running  

the POC and typing in these input fields. The attack also works on real websites  

with such text input elements.

The Flush+Reload POC works on all Intel CPUs with a shared and inclusive  

last-level cache. To run the POC follow these steps (the POC works best if the  

attacker application and chrome run on different physical cores):

```
1) Download all attached files and run:  
	make  
2) Open the supplied index.html webpage in Google Chrome.  
3) Run the POC and pass the path to the chrome binary to it:  
   ./main /opt/google/chrome/chrome  
4) Type any of the above-listed keys in one of the text fields in the   
   index.html webpage. The typed keys should appear in the spy application.  

```

**CREDIT INFORMATION**  

**-------------------------** -------------------------------------------------------  

Reporter credit: Erik Kraft ([erik.kraft5@gmx.at](mailto:erik.kraft5@gmx.at)), Martin Schwarzl ([martin.schwarzl@iaik.tugraz.at](mailto:martin.schwarzl@iaik.tugraz.at))

## Attachments

- [Makefile](attachments/Makefile) (text/plain, 59 B)
- [main.cpp](attachments/main.cpp) (text/plain, 2.2 KB)
- [cacheutils.h](attachments/cacheutils.h) (text/plain, 10.8 KB)
- [POC.zip](attachments/POC.zip) (application/octet-stream, 4.0 KB)
- [index.html](attachments/index.html) (text/plain, 305 B)

## Timeline

### [Deleted User] (2022-04-30)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-05-02)

+cc clamy for some thoughts on how we should triage this. :)

### do...@chromium.org (2022-05-04)

Reporter: do you mind attaching the referenced PoC please?

### er...@gmail.com (2022-05-04)

Ah I just saw I missed the test page in the files I uploaded...
Attached the whole PoC to this comment.

### [Deleted User] (2022-05-04)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-05-04)

(uploading index.html)

### do...@chromium.org (2022-05-05)

+clamy - do you mind following up on some of the discussion threads on this? Also +cc sroettger who may have had thoughts.

### [Deleted User] (2022-05-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-05-10)

Will reassign to titouan@ who is looking at something similar.

### ti...@chromium.org (2022-05-17)

Took a look at this, but running the poc results in a crash with SIGBUS (TIL of its existence):

```
$ ./main /opt/google/chrome/google-chrome
Bus error (core dumped)
```

I'm running this in a VM environment, where things might not work exactly like on the developers' machines.

I compiled the poc with `-ggdb` instead of `-O3` and ran it inside gdb, which gave me the following stack trace:

```
Program received signal SIGBUS, Bus error.
0x0000555555555477 in maccess (p=0x7ffff4f9f580) at cacheutils.h:102
102	void maccess(void *p) { asm volatile("movq (%0), %%rax\n" : : "c"(p) : "rax"); }
(gdb) bt
#0  0x0000555555555477 in maccess (p=0x7ffff4f9f580) at cacheutils.h:102
#1  0x00005555555555ba in flush_reload (ptr=0x7ffff4f9f580) at cacheutils.h:293
#2  0x0000555555555bd7 in main (argc=2, argv=0x7fffffffe498) at main.cpp:88
```

### ti...@chromium.org (2022-05-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-05-17)

titouan@, clamy@: Security flags haven't been set on this yet. I would assume low severity, but is this something we consider a security bug to begin with? Do we try to mitigate these kinds of issues, given that (as the reporter notes) it is outside of our conventional threat model?

### ti...@chromium.org (2022-05-18)

As written, I believe the exploit is indeed outside the threat model of Chrome. sroettger@ had some thoughts around the feasability of this entirely within the web platform, however.

### mp...@chromium.org (2022-05-19)

I don't know if there have been separate discussions on this topic. But as far as I can tell this just relies on shared memory and on Linux all of this rodata will be shared across all processes, so why wouldn't this be at least usable from a compromised renderer, making this a medium or potentially high severity bug? And could these rodata loads be triggered speculatively from Javascript and therefore could be potentially timeable from the web platform with some extra noise (due to e.g. lack of clflush)?

### ti...@chromium.org (2022-05-20)

Ah, it's true that a compromised renderer could do this, you're right. As for JS/WASM, that was what Stephen was talking about and I was hoping to get his thoughts on. I'll set this to Medium severity for now.

I'll be OOO next week and this kind of side channel attack seems like something CSA team would be well placed to evaluate / mitigate. Handing it over to you for further triage.

### er...@gmail.com (2022-05-23)

Yes, we also thought of the possibility of exploiting this from JS, but did not try it yet. 
Detecting keystrokes with side channels is possible for a lot of applications, I think the unique (bad) thing about Chrome is that it is very easy to find the addresses (just search for the according strings in the binary) and -more importantly- that it leaks lots of the keystrokes on page-level granularity within the Chrome binary itsself (which could make it exploitable from JS).

@titouan@chromium.org:
You should use "/opt/google/chrome/chrome" as target for the POC (google-chrome seems to be just a startup script and not the main binary). Also the version number should match for best results (the binary layout may change between versions).

### ad...@google.com (2022-05-26)

Setting FoundIn to match Security_Impact-Stable from https://crbug.com/chromium/1321350#c15.

### [Deleted User] (2022-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@google.com (2022-06-01)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-06-02)

Adding wez@ and garykac@ as OWNERS of  //ui/events/keycodes. I think we need all of the keycode strings to be adjacent to each other (including in official builds, etc.). Otherwise, they will live on different cache lines and therefore an attacker (in an attacker-controlled renderer process) can view the keystrokes of another Chrome renderer.

Perhaps that means putting them all in a section (e.g. [1]), or perhaps that means dynamically allocating a buffer to hold all the keystrings and then initializing kDomCodeMappings with it.

[1] https://stackoverflow.com/questions/6447463/forcing-certain-compiler-generated-variables-into-specific-elf-sections-with-gc
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/events/keyboard_event.cc;drc=8d6a246c9be4f6b731dc7f6e680b7d5e13a512b5;l=117

[Monorail components: IO>Keyboard]

### we...@chromium.org (2022-06-03)

As described this seems inevitable even with a closely packed string table, since the granulraity of the attack is ~cache-lines?

We have other data structures which take the plain table as part of the build process, and compress it into an optimized tree, which we then include as raw data in the binary, with an appropriate decoder.  Following that model would address both the ease of location and layout issues, at the cost of runtime overhead looking up and allocating space for the values.

Since this table is pretty small we could ensure that we always touch all of the strings in it on every lookup, but that won't address the easy-of-location issue, and with cache-line granularity there would still likely be only a small number of candidate DOM Codes for each event.

We should also review how the DOM Key values are affected by this exploit.

### mp...@chromium.org (2022-06-03)

With key strings of 4 bytes and cache lines of 64 bytes, can't we fit 16ish keystrings on each cache line? That doesn't seem like an especially useful granularity. Even with a 32-byte cache line size it's not great granularity.

Regardless, your data structure sounds better. I haven't seen this "compile-time plain table -> optimized tree" trick used before though it seems good. Are you reconstructing the strings in DomCodeToCodeString() (called in [2] from https://crbug.com/chromium/1321350#c21)? If all the cache lines are accessed on every key stroke, that seems like a big win here, and even if not, it sounds like an optimized tree might have 'A', 'B', 'C' next to each other rather than "KeyA' and "KeyB" and "KeyC" next to each other.

### we...@chromium.org (2022-06-04)

Re #23: Yes, the idea would be to have DomCodeToCodeString() compose a std::string with the relevant DOM Code string in it, derived from the table.

Note that each entry in the lookup table at present contains int32_t, int, and const char*, so each entry is 24 bytes in size, on a 64-bit system - we only fit three keys in a single 64-byte cache-line, and that's ignoring the placement of the strings themselves, which are the specific problem highlighted here - I imagine that the exploit could instead search for the key-code table itself, rather than the strings, and still be good-enough to be a problem.

While the compiled-table approach is a satisfying concept, simpler changes we can make to the current implementation are:
1. Copy the table data from the binary into process memory. It is small, so this shouldn't impact per-process memory footprint adversely, and it can be instantiated on-demand. We'll no longer be touching any binary pages specific to the keys being pressed.
2. Split the lookup into two parts (USB-code <-> platform-code, and USB-code <-> DOM Code string) so that individual entries are smaller, making the cache-line size more helpful.
3. Dynamically generate the name taking advantage of contiguous "runs" in the USB-code space, e.g. for "KeyA"-"KeyZ", "Digit1"->"Digit0" we can bake in special-casing to synthesize those, so that the code->string table only need mention the keys that don't form part of runs.  The exploit would be able to distinguish special keys, and digit vs letter, for example, but no more fidelity than that.

Option #1 seems the quickest mitigation to land, at a cost of ~6KB per process that handles key events, I would expect.

#2 + #3 seem sufficient, and without the private memory overhead.

WDYT?

### mp...@chromium.org (2022-06-04)

The entries are 16 bytes (at least on Linux x64, I don't think it's different on other systems?) which is still only 4 entries per table, but good point that keystrokes can also leak through the table, which is linearly scanned and also stored in rodata.

For #1 we'd probably want to make sure to allocate after fork to make very sure the page isn't shared among processes.

But I think we have time to do #2 and #3 as this bug has been around forever.

For #3 would the attacker be able to distinguish exactly which special key is pressed?

### we...@chromium.org (2022-06-07)

[Empty comment from Monorail migration]

### we...@chromium.org (2022-06-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/31103fab10169feb448d4d0c18bc73ed946c6628

commit 31103fab10169feb448d4d0c18bc73ed946c6628
Author: Wez <wez@chromium.org>
Date: Tue Jun 14 02:43:06 2022

[dom][events] DOM Code conversion cleanups

Improvements to the DOM Code conversion APIs:
- All APIs now accept strings via StringPiece, and return them
  as std::strings, since almost all callers store returned
  values in std::strings anyway.
- Common contiguous DomCodes (e.g. US_A->US_Z) have their names
  dynamically generated, rather than requiring a lookup through
  the table.

Some incidental cleanups:
- Removed unused code-string to USB & native conversions.
- Tidied up comments to group conversions better.

Bug: 1321350
Change-Id: I67f2603c281fa11d1b4d8dce86f3455a1f7c75c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3695189
Reviewed-by: Matthew Denton <mpdenton@chromium.org>
Commit-Queue: Michael Spang <spang@chromium.org>
Reviewed-by: Kevin Marshall <kmarshall@chromium.org>
Auto-Submit: Wez <wez@chromium.org>
Reviewed-by: Michael Spang <spang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1013780}

[modify] https://crrev.com/31103fab10169feb448d4d0c18bc73ed946c6628/ui/events/keycodes/dom/keycode_converter.cc
[modify] https://crrev.com/31103fab10169feb448d4d0c18bc73ed946c6628/ui/events/keycodes/dom/keycode_converter_unittest.cc
[modify] https://crrev.com/31103fab10169feb448d4d0c18bc73ed946c6628/ui/events/keycodes/keyboard_code_conversion_unittest.cc
[modify] https://crrev.com/31103fab10169feb448d4d0c18bc73ed946c6628/ui/base/ime/fuchsia/keyboard_client.cc
[modify] https://crrev.com/31103fab10169feb448d4d0c18bc73ed946c6628/ui/events/keycodes/dom/keycode_converter.h
[modify] https://crrev.com/31103fab10169feb448d4d0c18bc73ed946c6628/ui/events/ozone/layout/keyboard_layout_engine_unittest.cc


### we...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

### we...@chromium.org (2022-06-14)

Requesting merge for https://chromium-review.googlesource.com/c/chromium/src/+/3695189 to the affected branches.  The CL implements a partial mitigation for the issue, in particular for the letter, digit and function keys.

### we...@chromium.org (2022-06-14)

mpdenton: Revising the proposed mitigations:

1. [DONE] Generate "contiguous" DOM Code strings dynamically, based on DomCode.
2. Parse "contiguous" DOM Code strings specially, to derive the DomCode (i.e. reverse of #1).
3. Split the DomCode<->native and DomCode<->CodeString mappings apart.
4. Move non-contiguous/special DOM Code strings into process-private memory.  This should have viable overhead given that the continuous codes don't need to be stored.
5. Move the DomCode<->native mapping into process-private memory.  This is 8 bytes per entry, <256 entries, so a little under 2k per process that initializes it.

Do you think it makes sense to merge-back mitigation #1 as-is?

Do you think any of the suggestions above are unnecessary? :)

### mp...@chromium.org (2022-06-14)

Sorry going OOO, adding mattdr@ to help.

(yes please merge back #1)

### [Deleted User] (2022-06-15)

Merge approved: your change passed merge requirements and is auto-approved for M104. Please go ahead and merge the CL to branch 5112 (refs/branch-heads/5112) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-15)

Merge review required: M103 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-15)

Merge review required: M102 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-06-15)

I suspect (4) and (5) add minimal new protection unless we somehow randomize the order of the private copy. An adversary could run a PRIME+PROBE attack to observe the access pattern at a 64-byte granularity within the buffer and still gain interesting information on which strings were accessed.

I think that (1) -- and (2), if it's necessary to avoid corresponding lookups on key events -- is 98% of the benefit we can provide. Rather than working on later steps I'd prefer to spend the time testing if we can reproduce the vulnerability with (1) and (2) implemented, to try to be sure we caught any variants of the attack method.

### ma...@google.com (2022-06-15)

(I was responding to https://bugs.chromium.org/p/chromium/issues/detail?id=1321350#c31, in case of numbered-list collision)

### pb...@google.com (2022-06-15)

[Bulk Edit] Your change has been approved for M104 branch,please go ahead and merge the CL's to M104 branch manually asap by 4pm PST today so that they would be part of tomorrows M104 Dev release.

### we...@chromium.org (2022-06-15)

Re merges to M102 and M103:

1. Why does your merge fit within the merge criteria for these milestones?
Issue is Security_Severity "Medium".

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3695189

3. Have the changes been released and tested on canary?
Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
Not a user-visible issue.

### we...@chromium.org (2022-06-16)

The mitigation:
  2. Parse "contiguous" DOM Code strings specially, to derive the DomCode (i.e. reverse of #1).
will only impact lookups from string to internal representation; I'm not sure where those would ever actually occur, but I suspect they're rare.

I'll draft a CL for that, but won't plan to back-merge unless I hear otherwise.

### pb...@google.com (2022-06-16)

[Bulk Edit] Your change has been already approved for M104 Branch(go/chromebranches) and I will cut M104 Branch today i.e., June-16th, for tomorrows release please cherry pick the changes by noon PST so that they would be part of tomorrows Dev release.

### we...@chromium.org (2022-06-17)

Re #41: My change is cherry-picked to M104, awaiting CR+1 from a TPM.

### [Deleted User] (2022-06-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### we...@chromium.org (2022-06-23)

CL is ready, simply awaiting +1 from a suitable owner, at https://chromium-review.googlesource.com/c/chromium/src/+/3707218

### gi...@appspot.gserviceaccount.com (2022-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/297345c6b8febc470808414f549dc15e4a7f9144

commit 297345c6b8febc470808414f549dc15e4a7f9144
Author: Wez <wez@chromium.org>
Date: Thu Jun 23 18:56:12 2022

[dom][events] DOM Code conversion cleanups

Improvements to the DOM Code conversion APIs:
- All APIs now accept strings via StringPiece, and return them
  as std::strings, since almost all callers store returned
  values in std::strings anyway.
- Common contiguous DomCodes (e.g. US_A->US_Z) have their names
  dynamically generated, rather than requiring a lookup through
  the table.

Some incidental cleanups:
- Removed unused code-string to USB & native conversions.
- Tidied up comments to group conversions better.

(cherry picked from commit 31103fab10169feb448d4d0c18bc73ed946c6628)

Bug: 1321350
Change-Id: I67f2603c281fa11d1b4d8dce86f3455a1f7c75c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3695189
Reviewed-by: Matthew Denton <mpdenton@chromium.org>
Commit-Queue: Michael Spang <spang@chromium.org>
Reviewed-by: Kevin Marshall <kmarshall@chromium.org>
Auto-Submit: Wez <wez@chromium.org>
Reviewed-by: Michael Spang <spang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1013780}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3707218
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Wez <wez@chromium.org>
Reviewed-by: Wez <wez@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#236}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/297345c6b8febc470808414f549dc15e4a7f9144/ui/events/keycodes/dom/keycode_converter.cc
[modify] https://crrev.com/297345c6b8febc470808414f549dc15e4a7f9144/ui/events/keycodes/dom/keycode_converter_unittest.cc
[modify] https://crrev.com/297345c6b8febc470808414f549dc15e4a7f9144/ui/events/keycodes/keyboard_code_conversion_unittest.cc
[modify] https://crrev.com/297345c6b8febc470808414f549dc15e4a7f9144/ui/base/ime/fuchsia/keyboard_client.cc
[modify] https://crrev.com/297345c6b8febc470808414f549dc15e4a7f9144/ui/events/keycodes/dom/keycode_converter.h
[modify] https://crrev.com/297345c6b8febc470808414f549dc15e4a7f9144/ui/events/ozone/layout/keyboard_layout_engine_unittest.cc


### we...@chromium.org (2022-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-24)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### we...@chromium.org (2022-06-24)

Re #47 questions:
1) No, it was not a regression.
2) No, it is a security fix.

### [Deleted User] (2022-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-24)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-06-27)

[Comment Deleted]

### rz...@google.com (2022-06-27)

1. Just https://crrev.com/c/3726110
2. Low, conflicts on keycode_converter.cc because the types of a variable differ from main to M96
3. 104
4. Yes

### gm...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-29)

Congratulations, Erik and Martin! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch shortly to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### er...@gmail.com (2022-07-02)

Thank you all for taking the report seriously and providing a countermeasure. 
And, of course, thanks for the reward!

### am...@chromium.org (2022-07-08)

When this fix landed, 102 ES and 103 Stable had just been cut, but were not yet shipped as such. 
Merge reviews for ES/Stable were put on hold just after milestone for an unplanned functional respin and then an unplanned/emergency security respin shortly thereafter. At this time there is a single security respin planned for ES/102 and Stable/103.

Given the severity vs changes in this fix, I am going to suggest that we not backmerge this fix to 102 and 103 and it can instead ship in 104, to which it has already been merged. Please let me know if there are any concerns I may not be considering in this regard. 

### ma...@google.com (2022-07-08)

I'm okay not backporting -- it doesn't seem likely we will see attacks against users using this vector in the short or medium term.


### er...@gmail.com (2022-07-17)

Hi,
I would have one quick question: Will this get a CVE assigned after the fix is merged?

### am...@chromium.org (2022-07-18)

Hi Erik, CVE is assigned when the fix ships in a stable channel release. This has been merged into 104 and should be included in the M104 release on 2 August. 

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-10)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-10)

1. Just https://crrev.com/c/3822624
2. Low, conflicts on keycode_converter.cc because the types of a variable differ from main to M102
3. 104
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a28bfc7133943b3154abc04d0144aa9f7a651fdb

commit a28bfc7133943b3154abc04d0144aa9f7a651fdb
Author: Wez <wez@chromium.org>
Date: Fri Aug 12 10:36:12 2022

[M102-LTS][dom][events] DOM Code conversion cleanups

M102 merge issues:
  keycode_converter.cc:
    Conflicting types od var character; uint32_t in M96,
    base_icu::UChar32 in the original CL.

Improvements to the DOM Code conversion APIs:
- All APIs now accept strings via StringPiece, and return them
  as std::strings, since almost all callers store returned
  values in std::strings anyway.
- Common contiguous DomCodes (e.g. US_A->US_Z) have their names
  dynamically generated, rather than requiring a lookup through
  the table.

Some incidental cleanups:
- Removed unused code-string to USB & native conversions.
- Tidied up comments to group conversions better.

(cherry picked from commit 31103fab10169feb448d4d0c18bc73ed946c6628)

Bug: 1321350
Change-Id: I67f2603c281fa11d1b4d8dce86f3455a1f7c75c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3695189
Commit-Queue: Michael Spang <spang@chromium.org>
Auto-Submit: Wez <wez@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1013780}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3822624
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1295}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/a28bfc7133943b3154abc04d0144aa9f7a651fdb/ui/events/keycodes/dom/keycode_converter.cc
[modify] https://crrev.com/a28bfc7133943b3154abc04d0144aa9f7a651fdb/ui/events/keycodes/dom/keycode_converter_unittest.cc
[modify] https://crrev.com/a28bfc7133943b3154abc04d0144aa9f7a651fdb/ui/events/keycodes/keyboard_code_conversion_unittest.cc
[modify] https://crrev.com/a28bfc7133943b3154abc04d0144aa9f7a651fdb/ui/base/ime/fuchsia/keyboard_client.cc
[modify] https://crrev.com/a28bfc7133943b3154abc04d0144aa9f7a651fdb/ui/events/keycodes/dom/keycode_converter.h
[modify] https://crrev.com/a28bfc7133943b3154abc04d0144aa9f7a651fdb/ui/events/ozone/layout/keyboard_layout_engine_unittest.cc


### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f6a755b0ba223b278552c28357a5ea8ff46ddd06

commit f6a755b0ba223b278552c28357a5ea8ff46ddd06
Author: Wez <wez@chromium.org>
Date: Fri Aug 12 11:08:43 2022

[M96-LTS][dom][events] DOM Code conversion cleanups

M96 merge issues:
  keycode_converter.cc:
    Conflicting types of var character; uint32_t in M96,
    base_icu::UChar32 in the original CL.

Improvements to the DOM Code conversion APIs:
- All APIs now accept strings via StringPiece, and return them
  as std::strings, since almost all callers store returned
  values in std::strings anyway.
- Common contiguous DomCodes (e.g. US_A->US_Z) have their names
  dynamically generated, rather than requiring a lookup through
  the table.

Some incidental cleanups:
- Removed unused code-string to USB & native conversions.
- Tidied up comments to group conversions better.

(cherry picked from commit 31103fab10169feb448d4d0c18bc73ed946c6628)

Bug: 1321350
Change-Id: I67f2603c281fa11d1b4d8dce86f3455a1f7c75c2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3695189
Commit-Queue: Michael Spang <spang@chromium.org>
Auto-Submit: Wez <wez@chromium.org>
Reviewed-by: Michael Spang <spang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1013780}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3726110
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1677}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/f6a755b0ba223b278552c28357a5ea8ff46ddd06/ui/events/keycodes/dom/keycode_converter.cc
[modify] https://crrev.com/f6a755b0ba223b278552c28357a5ea8ff46ddd06/ui/events/keycodes/dom/keycode_converter_unittest.cc
[modify] https://crrev.com/f6a755b0ba223b278552c28357a5ea8ff46ddd06/ui/events/keycodes/keyboard_code_conversion_unittest.cc
[modify] https://crrev.com/f6a755b0ba223b278552c28357a5ea8ff46ddd06/ui/base/ime/fuchsia/keyboard_client.cc
[modify] https://crrev.com/f6a755b0ba223b278552c28357a5ea8ff46ddd06/ui/events/keycodes/dom/keycode_converter.h
[modify] https://crrev.com/f6a755b0ba223b278552c28357a5ea8ff46ddd06/ui/events/ozone/layout/keyboard_layout_engine_unittest.cc


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1321350?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059532)*
