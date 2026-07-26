# XNNPACK Workspace Size Overflow — Heap Buffer Overflow from WebNN

| Field | Value |
|-------|-------|
| **Issue ID** | [498494630](https://issues.chromium.org/issues/498494630) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebML |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2026-04-01 |
| **Bounty** | $42,000.00 |

## Description

---

### Report description

XNNPACK Workspace Size Overflow — Heap Buffer Overflow from WebNN

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

third\_party/xnnpack/src/src/operators/convolution-nhwc.c

---

### The problem

#### Please describe the technical details of the vulnerability

XNNPACK's operator code computes workspace buffer sizes using `size_t` arithmetic
with no overflow checks. On 32-bit platforms (where `size_t` is 32 bits), the product
of tensor dimensions and kernel parameters wraps around, causing an undersized
allocation. The subsequent operator execution writes past the buffer, resulting in
a heap buffer overflow that crashes the GPU process.

This is reachable from JavaScript via the WebNN API.
The bug exists since XNNPACK's initial open-source release (September 27, 2019).

This vulnerability exclusively affects 32 bit builds. IIUC, this should apply to
standard Chrome shipping on most Android devices.

## Target Version

Chromium 148.0.7759.0 (commit 294ae18d736060977d16f6c5ca24ff2bf7de441d, 2026-03-27)

## Root Cause

XNNPACK operator reshape functions compute workspace sizes like:

```
// convolution-nhwc.c:2623-2625
const size_t tiled_output_size = round_up(output_size, mr);
const size_t indirection_buffer_size =
    sizeof(void*) * kernel_size * tiled_output_size;

```

On 32-bit: `sizeof(void*) = 4`, `size_t = uint32_t`.
With conv2d input `[1, 4700, 4700, 1]` and 7x7 kernel:

- `output_size` = 4694 \* 4694 = 22,033,636
- `tiled_output_size` = `round_up(22033636, mr)` (mr varies by CPU; mr=7 on AVX-512)
- `sizeof(void*) * 49 * tiled_output_size` exceeds `UINT32_MAX` and wraps

The ASAN-confirmed allocation: 23,626,340 bytes (~22.5 MiB).
The true indirection buffer needed: ~4.02 GiB.
Result: ~183x heap buffer overflow WRITE.

There are ZERO overflow checks in any XNNPACK operator file. Verified by searching
for `SIZE_MAX`, `overflow`, `__builtin_mul_overflow`, `checked_`, `safe_mul` across
all 26 files in `operators/` — zero results.

## Affected Code

The proven overflow is in `convolution-nhwc.c:2625` (confirmed by ASAN via poc.html).

The same pattern — `sizeof(void*) * kernel_or_pooling_size * output_size` computed
in `size_t` with no overflow check — exists in other XNNPACK operator reshape
functions, including deconvolution, resize-bilinear, max-pooling, and
average-pooling. These likely have the same vulnerability but have not been
individually confirmed.

## Reproduction

### A Note to the reviewers

Please bear with me, the following steps are admittedly a bit ugly. If you have an ASan build for 32 bit systems, there is probably a better solution. The following steps are what I did on my Linux server (64 bit) to make it run a 32 bit version of Chrome.

### Build

```
# Install i386 sysroot (required for 32-bit x86 cross-compile)
python3 build/linux/sysroot_scripts/install-sysroot.py --arch=i386

cd src

# Apply build patches (does not touch any code in the vulnerability path)
#   1. BUILD.gn: bypass assertion that blocks target_cpu="x86" on Linux
#   2. content_main_runner_impl.cc: fix ASAN build error (C++ modules issue)
git apply build_fix.patch

# Configure 32-bit x86 ASAN build
mkdir -p out/x86_asan
cat > out/x86_asan/args.gn << 'EOF'
target_cpu = "x86"
is_asan = true
is_debug = false
is_component_build = true
dcheck_always_on = false
use_siso = false
v8_use_external_startup_data = false
EOF
gn gen out/x86_asan
ninja -C out/x86_asan content_shell

```
### Run

```
Xvfb :77 -screen 0 1024x768x24 -ac &
sleep 2
DISPLAY=:77 ASAN_OPTIONS="detect_odr_violation=0:detect_leaks=0:allocator_may_return_null=1:halt_on_error=0" \
  ./out/x86_asan/content_shell \
  --no-sandbox \
  --enable-features=WebMachineLearningNeuralNetwork \
  file:///path/to/poc.html

```

See ASan report

#### Impact analysis

This vulnerability affects 32 bit builds of Chrome, which includes Android phones. Android phones use the TFLite+XNNPack backend for WebNN, which is exactly where this vulnerability lives. On Android, the GPU process is **unsandboxed**. The overflow writes pointer-valued data sequentially past the heap buffer, with attacker-controlled length (determined by conv2d parameters). This is suitable for heap corruption and potentially control flow hijacking. The vulnerability has existed in XNNPack since its initial release, albeit not very long reachable from Chrome since the WebNN API is new. Still, this could have gone unnoticed for a long time, even without a renderer compromise.

---

### The cause

#### What version of Chrome have you found the security issue in?

148.0.7759.0 dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tobias Wienand

## Attachments

- [asan_output.txt](attachments/asan_output.txt) (text/plain, 67.1 KB)
- [crash_report.txt](attachments/crash_report.txt) (text/plain, 31.2 KB)
- [build_fix.patch](attachments/build_fix.patch) (text/x-patch, 1.6 KB)
- [poc.html](attachments/poc.html) (text/html, 1.4 KB)
- [poc.html](attachments/poc_75260793.html) (text/html, 1.4 KB)
- [Dockerfile](attachments/Dockerfile) (application/octet-stream, 4.4 KB)

## Timeline

### da...@google.com (2026-04-01)

My x86\_asan build is taking a rather long time to complete. In the meantime, speculatively doing some of the triage prior to having repro:

- Looks like WebNN is not currently on so setting severity S1, but Security\_Impact-None
- Moving to the right component and adding CCs

For the next person who tries to repro this: I got the following error when trying to build for 32-bit x86 and ASan:

```
error: ../../third_party/libaom/source/libaom/av1/common/mvref_common.c:794:0: ran out of registers during register allocation in function 'av1_find_mv_refs'

```

Applying this patch to the file seems to clear that, but the rest of the build is still churning along.

```
diff --git a/av1/common/mvref_common.c b/av1/common/mvref_common.c
index fdb2c8d870..6fd6b69866 100644
--- a/av1/common/mvref_common.c
+++ b/av1/common/mvref_common.c
@@ -785,6 +785,7 @@ static inline void setup_ref_mv_list(
   }
 }
 
+[[clang::optnone]]
 void av1_find_mv_refs(const AV1_COMMON *cm, const MACROBLOCKD *xd,
                       MB_MODE_INFO *mi, MV_REFERENCE_FRAME ref_frame,
                       uint8_t ref_mv_count[MODE_CTX_REF_FRAMES],

```

### aj...@google.com (2026-04-02)

S0 as Android, Still None.

### to...@gmail.com (2026-04-07)

Hi, I've noticed the issue was fixed with [4d591b283646](https://chromium-review.googlesource.com/c/chromium/src/+/7726055). It appears to reference [bug 498736530](https://issues.chromium.org/issues/498736530). Is that a duplicate of this issue?

In the meantime, I wanted to follow up on the build complications. Here is a self-contained Dockerfile for the (now fixed) issue.

`docker build -t bug . && docker run -v $(pwd):/output bug && cat asan.*`

### to...@gmail.com (2026-04-08)

This report predates 498736530. Shouldn't it be the other way around?

### re...@chromium.org (2026-04-08)

For our tracking purposes it is helpful to keep the issue associated with the fix as the canonical one.

### aj...@chromium.org (2026-04-09)

The earlier issue should win in this case.

### to...@gmail.com (2026-04-16)

Hi, following the decision to keep this as the canonical report and given the fix is already referenced in the `Fixed By Code Changes` field, could the status be set to `Fixed` and the `reward-topanel` label added please?

### re...@chromium.org (2026-04-16)

I don't have permission to add the `reward-topanel` label but automation should take care of that momentarily.

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $42000.00 for this report.

Rationale for this decision:
Memory corruption in a highly privileged process (e.g. GPU, network processes). 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-25)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/498494630)*
