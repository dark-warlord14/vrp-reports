# Security vulnerability in WebP

| Field | Value |
|-------|-------|
| **Issue ID** | [40071416](https://issues.chromium.org/issues/40071416) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mk...@chromium.org |
| **Assignee** | jz...@chromium.org |
| **Created** | 2023-09-06 |
| **Bounty** | $10,000.00 |

## Description

Copying this from an email to security@chromium.org. Marking as critical based on evidence of use in the wild:

"""
OE095807245816 - please include this ID in replies to this thread.

Portions Copyright (c) 2023 Apple Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

The material provided herein is NOT A CONTRIBUTION to the WebP project.

Hello Google,

Please treat the following as confidential.

We are reaching out to report a security issue affecting the open source WebP project. Please note that we have received reports that this issue is being exploited in the wild on Apple platforms, and our Threat Intel team has separately reached out to your Threat Analysis Group. We have attached the report and PoC to this email, both are password protected (pw: f@hbess8*(&fdja&qq!). Given the sensitivity of this report, we’ve refrained from reporting this through your portal, and we are hoping you can help relay it to the appropriate internal channels.

Our current plan is to remediate this issue in a software update to iOS and macOS later this week. We are requesting coordinated disclosure of this issue to ensure that both Apple and Google users are protected. Please confirm that you are willing to withhold publishing of this issue until Thursday, September 7.

Thank you,
Apple Product Security
"""

## Attachments

- [libwebp_HuffmanCodes-copy.pdf](attachments/libwebp_HuffmanCodes-copy.pdf) (application/pdf, 185.7 KB)
- [replicatevalue_poc.not_webp](attachments/replicatevalue_poc.not_webp) (application/octet-stream, 1.0 KB)
- [patch](attachments/patch) (text/plain, 9.9 KB)
- [patch](attachments/patch_53345418) (text/plain, 14.6 KB)

## Timeline

### mk...@google.com (2023-09-06)

[Empty comment from Monorail migration]

[Monorail components: Internals>Images>Codecs]

### mk...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-06)

[Empty comment from Monorail migration]

### ad...@google.com (2023-09-06)

I chatted with Mike about severity. If there's evidence of use in the wild, a bug is Pri-0 but severity remains unchanged.

So, *if* libwebp is used only in a sandboxed process, this would "only" be Security_Severity-High.

Here's my attempt at working out where libwebp is actually used, based on https://source.chromium.org/search?q=f:.gn$%20libwebp

Sandboxed (renderer) code
======================
* //third_party/blink/renderer/core
* //chrome/renderer

Test only or otherwise Security_Impact-None
================================
* //chrome/test
* //media/gpu/vaapi
* //third_party/blink/renderer/controller
* Various "unbundle" directories described as "files that make it possible for Linux distributions to build Chromium using system libraries and exclude the source code for Chromium's bundled copies of system libraries in a consistent manner. Nothing here is used in normal developer builds."

Unsure about
===========
* //components/image_fetcher/ios <-- BUILD.gn depends on webp, but the source code doesn't actually seem to do so. Assuming there is some dependency here, this wouldn't be sandboxed, therefore on iOS this would indeed be Critical severity.
* Skia. //ui/gfx depends on skia, so it would not be surprising if various bits of browser process or GPU process code end up transitively depending on libwebp. In fact, the "test only" dependencies above suggest that this is exactly the case. (NB we would now consider this Critical if it's reachable in the GPU process).

These last two cases give enough uncertainty that I'm going to stick with Critical until or unless we're sure that this code can't be reached outside the renderer process.

### ad...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### ad...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### ad...@google.com (2023-09-06)

yguyon@ and vrabaud@ have a mitigation in progress at internal Google CL 563045672.

### vr...@google.com (2023-09-06)

Here is a patch to mitigate it. Just "git apply -p3 /tmp/patch1 --reject"

### vr...@google.com (2023-09-06)

The patch seems fine:
- it has been tested against that input
- the offending file has been added to the fuzzing seeds and more fuzzing is running
- all the direct internal WebP tests pass
- all the internal tests using WebP directly are passing so far

This is hairy code written a very loooong time ago. A better patch can be made that actually fixes the proper spot that defines the memory to write to instead of where the memory write happens. But the current one mitigates it properly.

### vr...@google.com (2023-09-06)

BTW, this fixes the WebP issue but similar code (written by the same team) is in brotli: https://chromium.googlesource.com/chromium/src/third_party/+/refs/heads/main/brotli/dec/huffman.c#169

### am...@chromium.org (2023-09-06)

[Description Changed]

### am...@chromium.org (2023-09-06)

Issue description was updated to replace the password protected PDF with a non-password protected version. Ordinarily we would dump the contents / details into this report/ original description itself, but the PDF is lengthy and the formatting doesn't convert well. Please refer to the PDF attachment for details. 

### [Deleted User] (2023-09-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### jz...@chromium.org (2023-09-06)

> * //components/image_fetcher/ios <-- BUILD.gn depends on webp, but the source code doesn't actually seem to do so. Assuming there is some dependency here, this wouldn't be sandboxed, therefore on iOS this would indeed be Critical severity.

It looks like the platform is being used for decoding now [1]. Maybe it's a leftover dependency. I'll see if it can be removed.

> * Skia. //ui/gfx depends on skia, so it would not be surprising if various bits of browser process or GPU process code end up transitively depending on libwebp. In fact, the "test only" dependencies above suggest that this is exactly the case. (NB we would now consider this Critical if it's reachable in the GPU process).

I don't have any detail to add here at this point.

[1] https://source.corp.google.com/h/chrome-internal/codesearch/chrome/src/+/main:components/image_fetcher/ios/ios_image_decoder_impl.mm;l=50;drc=a4800ad29f2c50f7578c064a2404a7e5e44b1b02

### ke...@chromium.org (2023-09-06)

jzern@ or vrabaud@ do either of you have any context on WebP usage outside of sandboxed processes, which adetaylor@ was trying to figure out in https://crbug.com/chromium/1479274#c4?

### am...@chromium.org (2023-09-06)

[summarizing on going off bug discussions] I've spent the better part of the morning looking at this bug and trying to breadcrumb webp in Chrome and it doesn't seem like there is a concrete assertion that this is not the webp issue isn't reachable in the GPU process, and given that this is an ITW bug, it seems best that that the (a) fix landed and shipped as soon as possible, continuing to treat this as a critical issue. 

jzern@ has completed dependency analysis and iOS doesn't appear to be an issue. 
There is a potential issue with the proposed fix that it may break valid files. vrabaud@ and jzern@ are discussing alternatives. 


### ti...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-06)

for evaluation of potential impact in brotli 

### am...@chromium.org (2023-09-06)

Further investigation and analysis is ongoing, likely to roll into tomorrow. 
brotli team is CET timezone based and they'll evaluate tomorrow as well 

### am...@chromium.org (2023-09-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-06)

Adding Apple Product Security POCs as requested by Apple (who kindly reported this issue to us)

### am...@chromium.org (2023-09-06)

[Empty comment from Monorail migration]

### eu...@chromium.org (2023-09-07)

Brotli seems to be safe: shape of Huffman tree is checked before actual lookup table is built. Going to double- and tripple-check.

### vr...@google.com (2023-09-07)

Please find a proper patch enclosed. You can apply it with "git apply -p3 patch --reject".

The first mitigation was just checking that data fit into the optimized tables.
In practice, encoders write optimized tables but unoptimized ones (with unbalanced codes) are still valid according to the spec. In order to preserve the decodability of those unoptimized streams, this new patch is proposed: 
- a memory size check is done before writes (which can also prune some invalid data)
- allocation is done if necessary

This patch is still under review.

### am...@chromium.org (2023-09-07)

Thank you for completing the evaluation for Brotli eustas@ 
And vrabaud@ for the the work on the new patch [ internally is CL 563242566, currently in review] 
Once jzern@ has reviewed and if it can be landed, then we'll need to work migrate public tree and get this on Canary to start getting bake time right away

### jt...@google.com (2023-09-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/902bc9190331343b2017211debcec8d2ab87e17a

commit 902bc9190331343b2017211debcec8d2ab87e17a
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741

[modify] https://crrev.com/902bc9190331343b2017211debcec8d2ab87e17a/src/dec/vp8l_dec.c
[modify] https://crrev.com/902bc9190331343b2017211debcec8d2ab87e17a/src/utils/huffman_utils.c
[modify] https://crrev.com/902bc9190331343b2017211debcec8d2ab87e17a/src/dec/vp8li_dec.h
[modify] https://crrev.com/902bc9190331343b2017211debcec8d2ab87e17a/src/utils/huffman_utils.h


### am...@chromium.org (2023-09-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/2af26267cdfcb63a88e5c74a85927a12d6ca1d76

commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)

[modify] https://crrev.com/2af26267cdfcb63a88e5c74a85927a12d6ca1d76/src/dec/vp8l_dec.c
[modify] https://crrev.com/2af26267cdfcb63a88e5c74a85927a12d6ca1d76/src/utils/huffman_utils.c
[modify] https://crrev.com/2af26267cdfcb63a88e5c74a85927a12d6ca1d76/src/dec/vp8li_dec.h
[modify] https://crrev.com/2af26267cdfcb63a88e5c74a85927a12d6ca1d76/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c36406e679edd03a2bdbce49a5cb1e0fca0e620f

commit c36406e679edd03a2bdbce49a5cb1e0fca0e620f
Author: James Zern <jzern@chromium.org>
Date: Fri Sep 08 00:17:34 2023

Roll src/third_party/libwebp/src/ fd7bb21c0..2af26267c (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/fd7bb21c0cb5..2af26267cdfc

$ git log fd7bb21c0..2af26267c --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1479274
Change-Id: I95e24f3bbb9beacdf06447cf736d76e9c8e1c186
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852342
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Urvang Joshi <urvang@chromium.org>
Cr-Commit-Position: refs/branch-heads/5995@{#7}
Cr-Branched-From: 4db3cbc8d10bf9ecd5b838ed16edac25d0bc5818-refs/heads/main@{#1193498}

[modify] https://crrev.com/c36406e679edd03a2bdbce49a5cb1e0fca0e620f/third_party/libwebp/README.chromium
[modify] https://crrev.com/c36406e679edd03a2bdbce49a5cb1e0fca0e620f/third_party/libwebp/src
[modify] https://crrev.com/c36406e679edd03a2bdbce49a5cb1e0fca0e620f/DEPS


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/54d32e6513409152f500a244bea263ba9465116c

commit 54d32e6513409152f500a244bea263ba9465116c
Author: James Zern <jzern@chromium.org>
Date: Fri Sep 08 00:45:16 2023

Roll src/third_party/libwebp/src/ fd7bb21c0..2af26267c (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/fd7bb21c0cb5..2af26267cdfc

$ git log fd7bb21c0..2af26267c --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1479274
Change-Id: I56c712b561571518baa61dc41f414665281daf48
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852173
Commit-Queue: James Zern <jzern@google.com>
Reviewed-by: Urvang Joshi <urvang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1193867}

[modify] https://crrev.com/54d32e6513409152f500a244bea263ba9465116c/third_party/libwebp/README.chromium
[modify] https://crrev.com/54d32e6513409152f500a244bea263ba9465116c/third_party/libwebp/src
[modify] https://crrev.com/54d32e6513409152f500a244bea263ba9465116c/DEPS


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6f68ad62f8e6ae5a6402011549dfce192dc6efc4

commit 6f68ad62f8e6ae5a6402011549dfce192dc6efc4
Author: James Zern <jzern@chromium.org>
Date: Fri Sep 08 01:18:15 2023

Roll src/third_party/libwebp/src/ fd7bb21c0..2af26267c (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/fd7bb21c0cb5..2af26267cdfc

$ git log fd7bb21c0..2af26267c --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

(cherry picked from commit c36406e679edd03a2bdbce49a5cb1e0fca0e620f)

Bug: 1479274
Change-Id: I95e24f3bbb9beacdf06447cf736d76e9c8e1c186
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852342
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Urvang Joshi <urvang@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5995@{#7}
Cr-Original-Branched-From: 4db3cbc8d10bf9ecd5b838ed16edac25d0bc5818-refs/heads/main@{#1193498}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852215
Owners-Override: Krishna Govind <govind@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5994@{#4}
Cr-Branched-From: 533f23dd192f254f4625e01b963f8c4622a4447b-refs/heads/main@{#1193161}

[modify] https://crrev.com/6f68ad62f8e6ae5a6402011549dfce192dc6efc4/third_party/libwebp/README.chromium
[modify] https://crrev.com/6f68ad62f8e6ae5a6402011549dfce192dc6efc4/third_party/libwebp/src
[modify] https://crrev.com/6f68ad62f8e6ae5a6402011549dfce192dc6efc4/DEPS


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/8bacd63a6de1cc091f85a1692390401e7bbf55ac

commit 8bacd63a6de1cc091f85a1692390401e7bbf55ac
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/8bacd63a6de1cc091f85a1692390401e7bbf55ac/src/dec/vp8l_dec.c
[modify] https://crrev.com/8bacd63a6de1cc091f85a1692390401e7bbf55ac/src/utils/huffman_utils.c
[modify] https://crrev.com/8bacd63a6de1cc091f85a1692390401e7bbf55ac/src/dec/vp8li_dec.h
[modify] https://crrev.com/8bacd63a6de1cc091f85a1692390401e7bbf55ac/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/8d9916da9074535517481f9ccbdee706a89ac842

commit 8d9916da9074535517481f9ccbdee706a89ac842
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/8d9916da9074535517481f9ccbdee706a89ac842/src/dec/vp8l_dec.c
[modify] https://crrev.com/8d9916da9074535517481f9ccbdee706a89ac842/src/utils/huffman_utils.c
[modify] https://crrev.com/8d9916da9074535517481f9ccbdee706a89ac842/src/dec/vp8li_dec.h
[modify] https://crrev.com/8d9916da9074535517481f9ccbdee706a89ac842/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/50f60add5c547b8c9bc4462bd2fc2840d8fc4525

commit 50f60add5c547b8c9bc4462bd2fc2840d8fc4525
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/50f60add5c547b8c9bc4462bd2fc2840d8fc4525/src/dec/vp8l_dec.c
[modify] https://crrev.com/50f60add5c547b8c9bc4462bd2fc2840d8fc4525/src/utils/huffman_utils.c
[modify] https://crrev.com/50f60add5c547b8c9bc4462bd2fc2840d8fc4525/src/dec/vp8li_dec.h
[modify] https://crrev.com/50f60add5c547b8c9bc4462bd2fc2840d8fc4525/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/8d9916da9074535517481f9ccbdee706a89ac842

commit 8d9916da9074535517481f9ccbdee706a89ac842
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/8d9916da9074535517481f9ccbdee706a89ac842/src/dec/vp8l_dec.c
[modify] https://crrev.com/8d9916da9074535517481f9ccbdee706a89ac842/src/utils/huffman_utils.c
[modify] https://crrev.com/8d9916da9074535517481f9ccbdee706a89ac842/src/dec/vp8li_dec.h
[modify] https://crrev.com/8d9916da9074535517481f9ccbdee706a89ac842/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/4619a48fc3292743d7ce9658bee4245406734109

commit 4619a48fc3292743d7ce9658bee4245406734109
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/4619a48fc3292743d7ce9658bee4245406734109/src/dec/vp8l_dec.c
[modify] https://crrev.com/4619a48fc3292743d7ce9658bee4245406734109/src/utils/huffman_utils.c
[modify] https://crrev.com/4619a48fc3292743d7ce9658bee4245406734109/src/dec/vp8li_dec.h
[modify] https://crrev.com/4619a48fc3292743d7ce9658bee4245406734109/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/0aba549eb6c7e26a02d1f130d3c3f2b95b376a57

commit 0aba549eb6c7e26a02d1f130d3c3f2b95b376a57
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/0aba549eb6c7e26a02d1f130d3c3f2b95b376a57/src/dec/vp8l_dec.c
[modify] https://crrev.com/0aba549eb6c7e26a02d1f130d3c3f2b95b376a57/src/utils/huffman_utils.c
[modify] https://crrev.com/0aba549eb6c7e26a02d1f130d3c3f2b95b376a57/src/dec/vp8li_dec.h
[modify] https://crrev.com/0aba549eb6c7e26a02d1f130d3c3f2b95b376a57/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d6e3f821dacaa919bf3601aac5a026a7b3315b8d

commit d6e3f821dacaa919bf3601aac5a026a7b3315b8d
Author: James Zern <jzern@chromium.org>
Date: Fri Sep 08 04:04:32 2023

Roll src/third_party/libwebp/src/ fd7bb21c0..2af26267c (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/fd7bb21c0cb5..2af26267cdfc

$ git log fd7bb21c0..2af26267c --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

(cherry picked from commit 54d32e6513409152f500a244bea263ba9465116c)

Bug: 1479274
Change-Id: I56c712b561571518baa61dc41f414665281daf48
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852173
Commit-Queue: James Zern <jzern@google.com>
Reviewed-by: Urvang Joshi <urvang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1193867}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852965
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/5996@{#5}
Cr-Branched-From: 0a0fe9c5bc8a0873865121a2743a19fe1fafb7b0-refs/heads/main@{#1193789}

[modify] https://crrev.com/d6e3f821dacaa919bf3601aac5a026a7b3315b8d/third_party/libwebp/README.chromium
[modify] https://crrev.com/d6e3f821dacaa919bf3601aac5a026a7b3315b8d/third_party/libwebp/src
[modify] https://crrev.com/d6e3f821dacaa919bf3601aac5a026a7b3315b8d/DEPS


### jz...@chromium.org (2023-09-08)

[Empty comment from Monorail migration]

### gm...@google.com (2023-09-08)

[Empty comment from Monorail migration]

### jz...@chromium.org (2023-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-08)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-08)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-08)

Merge review required: a commit with DEPS changes was detected.

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
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-08)

Merge review required: a commit with DEPS changes was detected.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-08)

[Empty comment from Monorail migration]

### jz...@chromium.org (2023-09-08)

Re https://crbug.com/chromium/1479274#c44:

> This issue has been flagged as a merge candidate for Chrome OS' LTS channel.
> If selected, our merge team will handle any additional merges. To help us
> determine if this issue requires a merge to LTS, please answer this short
> questionnaire:
> 1. Was this issue a regression for the milestone it was found in?

No, the issue has existed since ~2014.

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### jz...@chromium.org (2023-09-08)

Re https://crbug.com/chromium/1479274#c45, https://crbug.com/chromium/1479274#c46 and https://crbug.com/chromium/1479274#c47:

> Please answer the following questions so that we can safely process your merge request:
> 1. Why does your merge fit within the merge criteria for these milestones?
> - Chrome Browser: https://chromiumdash.appspot.com/branches
> - Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

It's a fix for a 0-click exploit.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4852565 (M109)
https://chromium-review.googlesource.com/c/chromium/src/+/4853057 (M116)
https://chromium-review.googlesource.com/c/chromium/src/+/4852412 (M117)
https://chromium-review.googlesource.com/c/chromium/src/+/4852409 (M118)

> 3. Have the changes been released and tested on canary?

119.0.5996.2

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

No.

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Severe failures would manifest as a crash. Unexpected failures would result in
image decode failure.

### [Deleted User] (2023-09-08)

[Empty comment from Monorail migration]

### sr...@google.com (2023-09-08)

[Empty comment from Monorail migration]

### sr...@google.com (2023-09-08)

[Empty comment from Monorail migration]

### jz...@chromium.org (2023-09-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-08)

related: https://citizenlab.ca/2023/09/blastpass-nso-group-iphone-zero-click-zero-day-exploit-captured-in-the-wild/

### am...@chromium.org (2023-09-08)

canary data is good but quite limited at this time; based on jzern@'s testing, approving merges to M118 / branch 5993 and M117 / branch 5938 


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e40d2d9444730195a616691e5358202842b335b7

commit e40d2d9444730195a616691e5358202842b335b7
Author: James Zern <jzern@chromium.org>
Date: Fri Sep 08 19:56:43 2023

Roll src/third_party/libwebp/src/ fd7bb21c0..2af26267c (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/fd7bb21c0cb5..2af26267cdfc

$ git log fd7bb21c0..2af26267c --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1479274
Change-Id: I11b0d67ad950a33a097052e9ce7662b0ccfb461d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852412
Reviewed-by: Urvang Joshi <urvang@chromium.org>
Commit-Queue: James Zern <jzern@google.com>
Cr-Commit-Position: refs/branch-heads/5938@{#1137}
Cr-Branched-From: 2b50cb4bcc2318034581a816714d9535dc38966d-refs/heads/main@{#1181205}

[modify] https://crrev.com/e40d2d9444730195a616691e5358202842b335b7/third_party/libwebp/README.chromium
[modify] https://crrev.com/e40d2d9444730195a616691e5358202842b335b7/DEPS


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/134aac19655c2bc3af039ff33c6eebb93f41e2eb

commit 134aac19655c2bc3af039ff33c6eebb93f41e2eb
Author: James Zern <jzern@chromium.org>
Date: Fri Sep 08 19:58:31 2023

Roll src/third_party/libwebp/src/ fd7bb21c0..2af26267c (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/fd7bb21c0cb5..2af26267cdfc

$ git log fd7bb21c0..2af26267c --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1479274
Change-Id: I6c544c1f777229502eaa9975d7a699572a6642e3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852409
Reviewed-by: Urvang Joshi <urvang@chromium.org>
Commit-Queue: James Zern <jzern@google.com>
Cr-Commit-Position: refs/branch-heads/5993@{#73}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/134aac19655c2bc3af039ff33c6eebb93f41e2eb/third_party/libwebp/README.chromium
[modify] https://crrev.com/134aac19655c2bc3af039ff33c6eebb93f41e2eb/third_party/libwebp/src
[modify] https://crrev.com/134aac19655c2bc3af039ff33c6eebb93f41e2eb/DEPS


### jt...@google.com (2023-09-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-08)

merge approved for M116/ branch 5845

### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b2eab7500a18bd4d372f10149c6223fdfe48e3be

commit b2eab7500a18bd4d372f10149c6223fdfe48e3be
Author: James Zern <jzern@chromium.org>
Date: Fri Sep 08 20:57:18 2023

Roll src/third_party/libwebp/src/ 6a319d4da..4619a48fc (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/6a319d4da395..4619a48fc329

$ git log 6a319d4da..4619a48fc --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1479274
Change-Id: I0de56a278cfc64467d092ea0213bdf957b227ce1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4853057
Commit-Queue: James Zern <jzern@google.com>
Reviewed-by: Urvang Joshi <urvang@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#1779}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/b2eab7500a18bd4d372f10149c6223fdfe48e3be/third_party/libwebp/README.chromium
[modify] https://crrev.com/b2eab7500a18bd4d372f10149c6223fdfe48e3be/DEPS


### am...@chromium.org (2023-09-08)

acknowledgement for this issue to go to: Apple Security Engineering and Architecture (SEAR) and The Citizen Lab at The University of Torontoʼs Munk School 

### am...@chromium.org (2023-09-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4276f41d15741e4efd636a14414fb37dca632d77

commit 4276f41d15741e4efd636a14414fb37dca632d77
Author: James Zern <jzern@chromium.org>
Date: Fri Sep 08 23:46:57 2023

Roll src/third_party/libwebp/src/ 7366f7f39..0aba549eb (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/7366f7f394af..0aba549eb6c7

$ git log 7366f7f39..0aba549eb --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1479274
Change-Id: Id0b9e897c557b754de716633fd4035fcd8fdc846
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4852565
Commit-Queue: James Zern <jzern@google.com>
Reviewed-by: Urvang Joshi <urvang@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#1589}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/4276f41d15741e4efd636a14414fb37dca632d77/third_party/libwebp/README.chromium
[modify] https://crrev.com/4276f41d15741e4efd636a14414fb37dca632d77/DEPS


### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/904941b437ccc2f14de7cd791994f655c3583050

commit 904941b437ccc2f14de7cd791994f655c3583050
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/904941b437ccc2f14de7cd791994f655c3583050/src/dec/vp8l_dec.c
[modify] https://crrev.com/904941b437ccc2f14de7cd791994f655c3583050/src/utils/huffman_utils.c
[modify] https://crrev.com/904941b437ccc2f14de7cd791994f655c3583050/src/dec/vp8li_dec.h
[modify] https://crrev.com/904941b437ccc2f14de7cd791994f655c3583050/src/utils/huffman_utils.h


### [Deleted User] (2023-09-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/20ceff7eb3ccb679bd299f3d481309e10cbf2616

commit 20ceff7eb3ccb679bd299f3d481309e10cbf2616
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/20ceff7eb3ccb679bd299f3d481309e10cbf2616/src/dec/vp8l_dec.c
[modify] https://crrev.com/20ceff7eb3ccb679bd299f3d481309e10cbf2616/src/utils/huffman_utils.c
[modify] https://crrev.com/20ceff7eb3ccb679bd299f3d481309e10cbf2616/src/dec/vp8li_dec.h
[modify] https://crrev.com/20ceff7eb3ccb679bd299f3d481309e10cbf2616/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/801d2be12dba966233c21f850490203eb1acf014

commit 801d2be12dba966233c21f850490203eb1acf014
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/801d2be12dba966233c21f850490203eb1acf014/src/dec/vp8l_dec.c
[modify] https://crrev.com/801d2be12dba966233c21f850490203eb1acf014/src/utils/huffman_utils.c
[modify] https://crrev.com/801d2be12dba966233c21f850490203eb1acf014/src/dec/vp8li_dec.h
[modify] https://crrev.com/801d2be12dba966233c21f850490203eb1acf014/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/20ceff7eb3ccb679bd299f3d481309e10cbf2616

commit 20ceff7eb3ccb679bd299f3d481309e10cbf2616
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

Fix OOB write in BuildHuffmanTable.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)
(cherry picked from commit 2af26267cdfcb63a88e5c74a85927a12d6ca1d76)

[modify] https://crrev.com/20ceff7eb3ccb679bd299f3d481309e10cbf2616/src/dec/vp8l_dec.c
[modify] https://crrev.com/20ceff7eb3ccb679bd299f3d481309e10cbf2616/src/utils/huffman_utils.c
[modify] https://crrev.com/20ceff7eb3ccb679bd299f3d481309e10cbf2616/src/dec/vp8li_dec.h
[modify] https://crrev.com/20ceff7eb3ccb679bd299f3d481309e10cbf2616/src/utils/huffman_utils.h


### rz...@google.com (2023-09-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-11)

[Empty comment from Monorail migration]

### br...@google.com (2023-09-11)

[Empty comment from Monorail migration]

### bi...@google.com (2023-09-12)

Resolved in forthcoming Fuchsia F12.0.1 release via https://bugs.chromium.org/p/fuchsia/issues/detail?id=133453

### rz...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-09-12)

1. Just https://crrev.com/c/4858241
2. Low,  conflicts because 114 use assignments instead of calling setter methods for some values.
3. 116, 117, 118
4. Yes

### am...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### gm...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/a450afed44162f898ba5014e21efbad539fe3f0e

commit a450afed44162f898ba5014e21efbad539fe3f0e
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

[M114-LTS] Fix OOB write in BuildHuffmanTable.

M114 merge issues:
  dec/vp8l_dec.c:
    - Conflicting checks before ReadHuffmanCodeLengths() return statement;
    In 114, an assignment follows the check instead of a return.
    - ReadHuffmanCodes(): Conflict after the changed huffman_tables check,
    there's an assignment in 114 instead of the setter call.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)

[modify] https://crrev.com/a450afed44162f898ba5014e21efbad539fe3f0e/src/dec/vp8l_dec.c
[modify] https://crrev.com/a450afed44162f898ba5014e21efbad539fe3f0e/src/utils/huffman_utils.c
[modify] https://crrev.com/a450afed44162f898ba5014e21efbad539fe3f0e/src/dec/vp8li_dec.h
[modify] https://crrev.com/a450afed44162f898ba5014e21efbad539fe3f0e/src/utils/huffman_utils.h


### gi...@appspot.gserviceaccount.com (2023-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/webm/libwebp/+/a36ce6e442b170413d4fb18c5476bc2d2244c004

commit a36ce6e442b170413d4fb18c5476bc2d2244c004
Author: Vincent Rabaud <vrabaud@google.com>
Date: Thu Sep 07 19:16:03 2023

[M108-LTS] Fix OOB write in BuildHuffmanTable.

M108 merge issues:
  dec/vp8l_dec.c:
    - Conflicting checks before ReadHuffmanCodeLengths() return statement;
    In 114, an assignment follows the check instead of a return.
    - ReadHuffmanCodes(): Conflict after the changed huffman_tables check,
    there's an assignment in 114 instead of the setter call.

First, BuildHuffmanTable is called to check if the data is valid.
If it is and the table is not big enough, more memory is allocated.

This will make sure that valid (but unoptimized because of unbalanced
codes) streams are still decodable.

Bug: chromium:1479274
Change-Id: I31c36dbf3aa78d35ecf38706b50464fd3d375741
(cherry picked from commit 902bc9190331343b2017211debcec8d2ab87e17a)

[modify] https://crrev.com/a36ce6e442b170413d4fb18c5476bc2d2244c004/src/dec/vp8l_dec.c
[modify] https://crrev.com/a36ce6e442b170413d4fb18c5476bc2d2244c004/src/utils/huffman_utils.c
[modify] https://crrev.com/a36ce6e442b170413d4fb18c5476bc2d2244c004/src/dec/vp8li_dec.h
[modify] https://crrev.com/a36ce6e442b170413d4fb18c5476bc2d2244c004/src/utils/huffman_utils.h


### am...@chromium.org (2023-09-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-12)

^^ merge to 109 already completed, removing merge labels
all appropriate merges have been completed 

### rz...@google.com (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-09-13)

1. https://crrev.com/c/4859244 and a CL to roll DEPS in chromium
2. Low,  conflicts because 114 use assignments instead of calling setter methods for some values.
3. 116, 117, 118
4. Yes

### gm...@google.com (2023-09-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/356c4de1b73e14b4adf4590e1e6865725a02b7b3

commit 356c4de1b73e14b4adf4590e1e6865725a02b7b3
Author: Roger Zanoni <rzanoni@google.com>
Date: Wed Sep 13 11:02:36 2023

[M114-LTS] Roll src/third_party/libwebp/src/ fd7b5d484..a450afed4 (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/fd7b5d484644..a450afed4416

$ git log fd7b5d484..a450afed4 --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud [M114-LTS] Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: chromium:1479274
Change-Id: I8dfd1d68567f9ebb50ec395ec4eeb229e8bfd2cf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4862020
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1597}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/356c4de1b73e14b4adf4590e1e6865725a02b7b3/DEPS


### gi...@appspot.gserviceaccount.com (2023-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/130c12fcb7d1d1700882abd05b9fa10a81ccc85b

commit 130c12fcb7d1d1700882abd05b9fa10a81ccc85b
Author: Roger Zanoni <rzanoni@google.com>
Date: Wed Sep 13 12:00:43 2023

[M108-LTS] Roll src/third_party/libwebp/src/ 7366f7f39..a36ce6e44 (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/7366f7f394af..a36ce6e442b1

$ git log 7366f7f39..a36ce6e44 --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud [M108-LTS] Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: chromium:1479274
Change-Id: Ia30b95e4a894ec537da2158c0c29348d23de7dce
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4861960
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1515}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/130c12fcb7d1d1700882abd05b9fa10a81ccc85b/DEPS


### rz...@google.com (2023-09-13)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/321b33c9f528e2c84085a041afd6fcc4e3d88861

commit 321b33c9f528e2c84085a041afd6fcc4e3d88861
Author: James Zern <jzern@chromium.org>
Date: Wed Sep 13 17:53:59 2023

image_fetcher,ios/BUILD.gn: remove webp deps

These have been unnecessary since:
https://crrev.com/28ddb883d2d45db9edd9ec7342fdb62300e36afc
28ddb883d2d45 [iOS] WebPDecoder Cleanup

Bug: 1171745, 1129484, 1479274
Change-Id: Ida84b48e0b92e4c6e68c10086ee9119df8a29066
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4857236
Reviewed-by: Joemer Ramos <joemerramos@chromium.org>
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Commit-Queue: James Zern <jzern@google.com>
Cr-Commit-Position: refs/heads/main@{#1196124}

[modify] https://crrev.com/321b33c9f528e2c84085a041afd6fcc4e3d88861/components/image_fetcher/ios/BUILD.gn


### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

We greatly appreciate the work of Citizen Lab that lead to this discovery and them reporting this issue to Apple, who in turn, reported it to us. 
Due to their efforts, we have decided to award $10,000 to Citizen Lab for their efforts, which have benefitted all the billions of users of Apple and Google products.

We will be reaching out directly to Citizen Lab to convey this reward. 

### ad...@google.com (2023-09-14)

In https://crbug.com/chromium/1479274#c4 I did a little bit of analysis about whether this is likely to be reachable from outside the sandbox, which would dictate whether this was Critical or High severity.

I've dug a little deeper and I now believe this is High severity.

Of the two instances in https://crbug.com/chromium/1479274#c4 where it might have been accessible outside the sandbox, https://crbug.com/chromium/1479274#c15 and https://crbug.com/chromium/1479274#c17 say the iOS route is not a concern, so the remaining instance is the possible use of Skia image decoders via //ui/gfx from the browser or GPU process.

I was initially suspicious because of the use of libwebp within //media/gpu/vaapi tests, but it seems that this is used for comparing hardware vs software decoding and that the production vaapi code doesn't use the software decoder (that's kind of the whole point after all).

For image decoding in general, although //ui/gfx and Skia _could_ be used to decode images outside the sandbox, hopefully _they're not_. The Rule of 2 (https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/rule-of-2.md) is designed exactly to prevent this, and we provide the data decoder service as an alternative for folks who want to decode images outside the sandbox (https://source.chromium.org/chromium/chromium/src/+/main:services/data_decoder/public/cpp/data_decoder.h?q=data_decoder.h).

It is possible, of course, that we've missed places where images might be decoded outside the sandbox, but this bug doesn't provide any direct evidence of that, and so I think we should set this to High severity on the assumption that our most fundamental security design principles have worked in this case.

### [Deleted User] (2023-09-15)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f050718e4e17483487d9b2653574243245e6b011

commit f050718e4e17483487d9b2653574243245e6b011
Author: James Zern <jzern@chromium.org>
Date: Sat Sep 16 22:14:28 2023

Roll src/third_party/libwebp/src/ fd7b5d484..a450afed4 (1 commit)

https://chromium.googlesource.com/webm/libwebp.git/+log/fd7b5d484644..a450afed4416

$ git log fd7b5d484..a450afed4 --date=short --no-merges --format='%ad %ae %s'
2023-09-07 vrabaud [M114-LTS] Fix OOB write in BuildHuffmanTable.

Created with:
  roll-dep src/third_party/libwebp/src

Bug: 1479274
Change-Id: I792628f1fde29e7c1d6b34dd49bd9763620d395e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4869056
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#1464}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/f050718e4e17483487d9b2653574243245e6b011/DEPS


### am...@chromium.org (2023-09-17)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

There is ongoing confusion and consternation about the CVEs (Apple CVE + Chrome CVE + Google CVE) related to this issue, we trying to sort things out to best consolidate and potentially eliminate some duplicates here. We need more information to know in which direction we can potentially consolidate here, such as to potentially point to Apple's CVE and have Chrome's rejected as a duplicate or point to the Google CVE and reject the Chrome one as a duplicate. 

### au...@gmail.com (2023-09-28)

Thank you, Amy. We sent you an email to coordinate.

### jt...@google.com (2023-09-28)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-02)

[Empty comment from Monorail migration]

### jz...@chromium.org (2023-10-09)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### we...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1479274?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### tr...@yahoo.com (2024-05-16)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071416)*
