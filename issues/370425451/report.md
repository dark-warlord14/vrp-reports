# UAF in gl::ErrorSet::handleError(ANGLE for Metal)

| Field | Value |
|-------|-------|
| **Issue ID** | [370425451](https://issues.chromium.org/issues/370425451) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Mac |
| **Reporter** | em...@gmail.com |
| **Assignee** | kb...@chromium.org |
| **Created** | 2024-09-30 |
| **Bounty** | $2,000.00 |

## Description

## Vulnerability Overview

Within the Chromium project, the `gl::ErrorSet::handleError` function contains a **Use-After-Free (UAF)** vulnerability. This flaw arises from improper handling of error messages in the ANGLE for Metal implementation, potentially allowing malicious actors to execute arbitrary code through specially crafted shader code, thereby compromising system security.

## Affected Environment

- **Operating System**: macOS 14.0
- **Chromium Version**: 129.0.6658.0

## Steps to Reproduce

1. **Compile Chromium**:
   
   Use the following `args.gn` configuration for compilation:
   
   ```
   is_asan = true
   is_debug = false
   enable_nacl = false
   treat_warnings_as_errors = false
   is_component_build = true
   dcheck_always_on = false
   
   ```
2. **Run Chromium with ASAN Enabled**:
   
   Execute the following command to start Chromium and visit the page that triggers the crash:
   
   ```
   ~/chromium/src/out/release/Chromium.app/Contents/MacOS/Chromium \
   --password-store=basic --use-mock-keychain \
   --user-data-dir=/tmp/ff1 \
   http://localhost:8880/crash.html
   
   ```

## Vulnerability Analysis

### 1. Local Variable Lifetime Issue

In the `CreateMslShaderLib` function, `std::ostringstream ss`[0] is used to construct the error message string. The relevant code is as follows:

```
angle::Result CreateMslShaderLib(mtl::Context *context,
                                 gl::InfoLog &infoLog,
                                 mtl::TranslatedShaderInfo *translatedMslInfo,
                                 const std::map<std::string, std::string> &substitutionMacros)
{
    ANGLE_MTL_OBJC_SCOPE
    {
        mtl::LibraryCache &libraryCache = context->getDisplay()->getLibraryCache();

        // Convert to actual binary shader
        mtl::AutoObjCPtr<NSError *> err = nil;
        const bool disableFastMath =
            context->getDisplay()->getFeatures().intelDisableFastMath.enabled ||
            translatedMslInfo->hasIsnanOrIsinf;
        const bool usesInvariance       = translatedMslInfo->hasInvariant;
        translatedMslInfo->metalLibrary = libraryCache.getOrCompileShaderLibrary(
            context->getDisplay(), translatedMslInfo->metalShaderSource, substitutionMacros,
            disableFastMath, usesInvariance, &err);
        if (err && !translatedMslInfo->metalLibrary)
        {
            std::ostringstream ss;  // [0]
            ss << "Internal error compiling shader with Metal backend.\n";
            ss << err.get().localizedDescription.UTF8String << "\n";
            ss << "-----\n";
            ss << *(translatedMslInfo->metalShaderSource);
            ss << "-----\n";

            infoLog << ss.str();

            ANGLE_MTL_HANDLE_ERROR(context, ss.str().c_str(), GL_INVALID_OPERATION); // [1]
            return angle::Result::Stop;
        } // [2] End of ss scope

        return angle::Result::Continue;
    }
}

```

**Source Code Link**: [CreateMslShaderLib - ProgramExecutableMtl.mm:344](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/ProgramExecutableMtl.mm;l=344)

In the above code, `ss` is a local variable whose `c_str()` method returns a pointer that becomes invalid once the function scope ends. This pointer is subsequently passed to `ANGLE_MTL_HANDLE_ERROR`[1] and stored in `mErrorMessage`[3].

### 2. Issue in the Error Handling Function

The `handleError` function is defined as follows:

```
void handleError(GLenum glErrorCode,
                 const char *message,
                 const char *file,
                 const char *function,
                 unsigned int line) override
{
    mErrorCode     = glErrorCode;
    mErrorMessage  = message;        // [3]
    mErrorFile     = file;
    mErrorFunction = function;
    mErrorLine     = line;
}

```

**Source Code Link**: [handleError - ProgramMtl.mm:125](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/ProgramMtl.mm;l=125)

In this function, `mErrorMessage` is assigned the address returned by `ss.str().c_str()`. However, since `ss` is a local variable, its lifetime is limited to the scope of the `CreateMslShaderLib` function[2]. Once the function exits, `ss` is destroyed, and `mErrorMessage` points to a memory address that has been freed.

### 3. Asynchronous Call Leading to UAF

The `getResult` function is defined as follows:

```
angle::Result getResult(const gl::Context *context, gl::InfoLog &infoLog) override
{
    if (mErrorCode != GL_NO_ERROR)
    {
        mtl::GetImpl(context)->handleError(mErrorCode, mErrorMessage, mErrorFile, 
                                           mErrorFunction, mErrorLine); // [4]
        return angle::Result::Stop;
    }

    return mResult;
}

```

**Source Code Link**: [getResult - ProgramMtl.mm:104](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/metal/ProgramMtl.mm;l=104)

Since `getResult` is invoked asynchronously, by the time it is called, `mErrorMessage` points to memory that has already been freed, resulting in a **Use-After-Free (UAF)** condition.

## Key ASAN Logs

Below are the critical sections of the AddressSanitizer (ASAN) report, highlighting the heap use-after-free details:

```
==3713==ERROR: AddressSanitizer: heap-use-after-free on address 0x623000147500 at pc 0x0001010e0b94 bp 0x00016fc18710 sp 0x00016fc17ee0
READ of size 4 at 0x623000147500 thread T0
...
Freed by thread T16 here:
    #0 0x0001010e0b90 in __asan_after_dynamic_init ??:0:0
    #1 0x00017ae50234 in gl::ErrorSet::handleError(unsigned int, char const*, char const*, char const*, unsigned int) ??:0:0
    #2 0x00017b2d15b8 in non-virtual thunk to rx::ProgramMtl::LinkTaskMtl::getResult(gl::Context const*, gl::InfoLog&) ??:0:0
    #3 0x00017af23a1c in gl::Program::MainLinkLoadEvent::wait(gl::Context const*) ??:0:0
    ...
previously allocated by thread T16 here:
    #0 0x00010112bff8 in __sanitizer_finish_switch_fiber ??:0:0
    #1 0x00017aa9d81c in std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> std::__Cr::basic_stringbuf<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>::str<std::__Cr::allocator<char>>(std::__Cr::allocator<char> const&) const ??:0:0
    #2 0x00017b2aa9a8 in rx::CreateMslShaderLib(rx::mtl::Context*, gl::InfoLog&, rx::mtl::TranslatedShaderInfo*, std::__Cr::map<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::less<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>, std::__Cr::allocator<std::__Cr::pair<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>> const&) ??:0:0
    ...
SUMMARY: AddressSanitizer: heap-use-after-free in gl::ErrorSet::handleError(unsigned int, char const*, char const*, char const*, unsigned int) [ProgramExecutableMtl.mm:XXX]

```

## Attachments

- [crash.html](attachments/crash.html) (text/html, 1.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 43.0 KB)

## Timeline

### mp...@google.com (2024-10-01)

Maybe introduced in <https://chromium-review.googlesource.com/c/angle/angle/+/5701902>?

Marking as only medium severity since the UAF-ed data only gets copied into a log.

### am...@chromium.org (2024-10-01)

in c#2 priority was set rather than severity; setting s2 (medium severity) and adjusting priority accordingly

### pe...@google.com (2024-10-02)

Setting milestone because of s2 severity.

### kb...@chromium.org (2024-10-02)

Alexey, do you think you might be able to rethink the allocation of this error string? Please take the bug from Geoff if so. Thanks.

### kb...@chromium.org (2024-10-03)

Talked with Alexey; will try a fix later.

### kb...@chromium.org (2024-10-16)

<https://chromium-review.googlesource.com/c/angle/angle/+/5938484> up for review.

### ap...@google.com (2024-10-17)

Project: angle/angle  

Branch: main  

Author: Kenneth Russell <[kbr@chromium.org](mailto:kbr@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5938484>

Hold on to error message in LinkTaskMtl as C++ string.

---


Expand for full commit details
```
Hold on to error message in LinkTaskMtl as C++ string.

Make a copy of the incoming C string because the error message might
be dynamically allocated and deallocated by the caller.

Bug: angleproject:370425451
Change-Id: If4aaa93a90a1da8bc60f7839e29b705b0d2864e5
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/5938484
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
Auto-Submit: Kenneth Russell <kbr@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/metal/ProgramMtl.mm`

---

Hash: 831a52f2dc592ec7dda48d2129dacfc4511f9bb1  

Date:  Wed Oct 16 13:46:04 2024


---

### kb...@chromium.org (2024-10-17)

I think the above change fixes this; please reopen if not.

### em...@gmail.com (2024-10-17)

I tested the above CL and did not reproduce the problem again.

### sp...@google.com (2024-11-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower impact information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-20)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2025-01-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/370425451)*
