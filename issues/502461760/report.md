# Heap-use-after-free in `remoting::PamAuthorizer::GetNextMessage` / `OnMessageProcessed`

| Field | Value |
|-------|-------|
| **Issue ID** | [502461760](https://issues.chromium.org/issues/502461760) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Services (Use Subcomponents)>Chromoting |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | jo...@google.com |
| **Created** | 2026-04-14 |
| **Bounty** | $500.00 |

## Description

## Crash information

**Type of crash:** host process. `remoting_me2me_host` (Chrome Remote Desktop Linux host daemon). Not a browser tab or renderer crash. Reproduced inside the `remoting_unittests` ASAN binary, which links the production `pam_authorization_factory_posix.cc` source file unmodified.

**Crash State (symbolized stack trace from ASAN):**

```
==565990==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bf11023f138 at pc 0x55f20edd5719 bp 0x7ffe375e3a70 sp 0x7ffe375e3a68
READ of size 4 at 0x7bf11023f138 thread T0

  #0 remoting::(anonymous namespace)::PamAuthorizer::MaybeCheckLocalLogin()
       remoting/host/pam_authorization_factory_posix.cc:137:7
  #1 remoting::(anonymous namespace)::PamAuthorizer::GetNextMessage()
       remoting/host/pam_authorization_factory_posix.cc:119:3
  #2 remoting::PamAuthorizerUafTest_GetNextMessage_FreesThisDuringUnderlyingCall_Test::TestBody()
       remoting/host/pam_authorization_factory_posix_unittest.cc:167:26
  #3 testing::Test::Run()                       third_party/googletest/src/googletest/src/gtest.cc
  #4 testing::TestInfo::Run()                   third_party/googletest/src/googletest/src/gtest.cc:2892:11
  #5 testing::TestSuite::Run()                  third_party/googletest/src/googletest/src/gtest.cc:3070:30
  #6 testing::internal::UnitTestImpl::RunAllTests()
       third_party/googletest/src/googletest/src/gtest.cc:6062:44
  #7 testing::UnitTest::Run()                   third_party/googletest/src/googletest/src/gtest.cc
  #8 base::TestSuite::Run()                     base/test/test_suite.cc:440:16
  #9 base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*)
       base/functional/bind_internal.h:740:12
  #10 base::OnceCallback<int ()>::Run() &&      base/functional/callback.h:155:12
  #11 base::(anonymous namespace)::LaunchUnitTestsInternal(...)
       base/test/launcher/unit_test_launcher.cc:189:38
  #12 base::LaunchUnitTests(int, char**, base::OnceCallback<int ()>, unsigned long)
       base/test/launcher/unit_test_launcher.cc:337:10
  #13 main                                      remoting/base/run_all_unittests.cc:60:10

0x7bf11023f138 is located 40 bytes inside of 48-byte region [0x7bf11023f110,0x7bf11023f140)

freed by thread T0 here:
  #0 operator delete(void*, unsigned long)    (remoting_unittests+0xf7151a2)
  #1 base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*)
       gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
       (unique_ptr destructor chain, frees the PamAuthorizer wrapper)
  #2 base::OnceCallback<void ()>::Run() &&     base/functional/callback.h:155:12
  #3 remoting::(anonymous namespace)::TestUnderlyingAuthenticator::GetNextMessage()
       remoting/host/pam_authorization_factory_posix_unittest.cc:76:27
  #4 remoting::(anonymous namespace)::PamAuthorizer::GetNextMessage()
       remoting/host/pam_authorization_factory_posix.cc:117:46
  #5 remoting::PamAuthorizerUafTest_GetNextMessage_FreesThisDuringUnderlyingCall_Test::TestBody()
       remoting/host/pam_authorization_factory_posix_unittest.cc:167:26

previously allocated by thread T0 here:
  #0 operator new(unsigned long)              (remoting_unittests+0xf71459d)
  #1 remoting::PamAuthorizationFactory::CreateAuthenticator(
         const std::string& local_jid, const std::string& remote_jid)
       gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:26
       (PamAuthorizer constructed inside CreateAuthenticator)
  #2 remoting::PamAuthorizerUafTest_GetNextMessage_FreesThisDuringUnderlyingCall_Test::TestBody()
       remoting/host/pam_authorization_factory_posix_unittest.cc:156:19

SUMMARY: AddressSanitizer: heap-use-after-free
         remoting/host/pam_authorization_factory_posix.cc:137:7
         in remoting::(anonymous namespace)::PamAuthorizer::MaybeCheckLocalLogin()

```

Crash-state fingerprint (top three frames, standard ClusterFuzz-style notation):

```
remoting::PamAuthorizer::MaybeCheckLocalLogin
remoting::PamAuthorizer::GetNextMessage
remoting::PamAuthorizerUafTest_GetNextMessage_FreesThisDuringUnderlyingCall_Test::TestBody

```

Registers and exception record are not applicable. This is a sanitizer-detected memory safety violation on Linux, not a hardware exception. ASAN aborts the process after printing the report above. The full, unredacted report (with shadow memory map and all 14 frames of each stack) is attached as `asan-pam-uaf-20260414-152259.log`.

**Client ID:** Not applicable. This is not a crash from a running Chrome browser with uploaded crash reports, so there is no Client ID or crash/ hash. The crash is reproduced from source, locally, against tip-of-tree Chromium. Build configuration:

- Target: `remoting_unittests`
- Output dir: `out/fuzz_asan`
- GN args: `is_asan=true use_libfuzzer=true is_debug=false is_component_build=false optimize_for_fuzzing=true`
- Toolchain: bundled Chromium clang (`CR_CLANG_REVISION=llvmorg-23-init-10931-g20b6ec66-1`)
- Host: Linux x86\_64

---

## Executive summary

`PamAuthorizer` is a Linux-only authenticator wrapper used by the Chrome Remote Desktop host (`remoting_me2me_host`). It owns a child `underlying_` `std::unique_ptr<protocol::Authenticator>` and forwards calls to it. Two of its methods, `GetNextMessage()` and `OnMessageProcessed()`, dereference `this` after calling into `underlying_`, on the assumption that the child cannot cause `this` to be destroyed mid-call.

That assumption is wrong. Authenticators in this subsystem can synchronously cause their owning session (and therefore the wrapping `PamAuthorizer`) to be torn down from inside their own method bodies, via the `state_change_after_accepted` notification chain, or via any other synchronous state transition that the negotiating/session layer reacts to by destroying the `Authenticator`.

This is the same `base::Unretained(this)` plus "owned, so Unretained is safe" shape that [crbug.com/501376612](https://crbug.com/501376612) identified and fixed in five sibling files in commit `174583c9fcf83`:

- `remoting/protocol/negotiating_authenticator_base.cc`
- `remoting/protocol/negotiating_host_authenticator.cc`
- `remoting/protocol/validating_authenticator.cc`
- `remoting/protocol/pairing_authenticator_base.cc`
- `remoting/protocol/pairing_host_authenticator.cc`

The fix in that commit replaced `base::Unretained(this)` with `weak_factory_.GetWeakPtr()` and added a WeakPtr re-check after the underlying call returns. The same shape in `pam_authorization_factory_posix.cc` was missed, including the incorrect safety comment:

```
// |underlying_| is owned, so Unretained() is safe here.

```

I built `remoting_unittests` with ASAN against current HEAD, added a unit test that drives the production callsite (`PamAuthorizationFactory::CreateAuthenticator` then `PamAuthorizer::GetNextMessage` then `underlying_->GetNextMessage`), and had the test trigger synchronous destruction of the `PamAuthorizer` from inside the underlying's `GetNextMessage()`. ASAN fires with a heap-use-after-free pointing at line 137 of the production source file, called from line 119.

## Technical details

### The buggy code

`remoting/host/pam_authorization_factory_posix.cc`:

```
116: JingleAuthentication PamAuthorizer::GetNextMessage() {
117:   JingleAuthentication result = underlying_->GetNextMessage();
118:   // PAM check may be performed once the state has transitioned to ACCEPTED.
119:   MaybeCheckLocalLogin();            // UAF: `this` may be freed
120:   return result;                     //      by the line 117 call.
121: }

136: void PamAuthorizer::MaybeCheckLocalLogin() {
137:   if (local_login_status_ == NOT_CHECKED && state() == ACCEPTED) {  // read of freed `this`
...

```

And the same shape in the async path:

```
100: void PamAuthorizer::ProcessMessage(const JingleAuthentication& message,
101:                                    base::OnceClosure resume_callback) {
102:   // Always delegate to the underlying authenticator and let it manage its own
103:   // state machine.
104:   // |underlying_| is owned, so Unretained() is safe here.
105:   underlying_->ProcessMessage(
106:       message,
107:       base::BindOnce(&PamAuthorizer::OnMessageProcessed, base::Unretained(this),
108:                      std::move(resume_callback)));
109: }

111: void PamAuthorizer::OnMessageProcessed(base::OnceClosure resume_callback) {
112:   MaybeCheckLocalLogin();            // same UAF via BindOnce(Unretained(this))
113:   std::move(resume_callback).Run();
114: }

```

Compare with the parent fix in sibling files (commit `174583c9fcf83`), which removed the "owned, so Unretained() is safe here" comment and replaced `base::Unretained(this)` with `weak_factory_.GetWeakPtr()` plus an early-return check after the underlying call.

### Why `this` can die inside `underlying_->GetNextMessage()`

`Authenticator` instances can be destroyed synchronously from inside their own methods through the `NotifyStateChangeAfterAccepted` then `on_state_change_after_accepted_` callback chain. In production, that chain reaches the session / connection-manager layer, which reacts by tearing down the connection, destroying the top-level `Authenticator` it owns, which cascades into destroying the `PamAuthorizer` wrapper and, via its `std::unique_ptr`, the `underlying_` that is still on the stack. That is the failure mode the parent fix addressed in the sibling classes. `PamAuthorizer` sits in the same ownership position and uses the same shape.

### Proof

End-to-end ASAN reproduction built against tip-of-tree:

```
==565990==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bf11023f138
READ of size 4 at 0x7bf11023f138 thread T0
    #0 remoting::(anonymous namespace)::PamAuthorizer::MaybeCheckLocalLogin()
         remoting/host/pam_authorization_factory_posix.cc:137:7
    #1 remoting::(anonymous namespace)::PamAuthorizer::GetNextMessage()
         remoting/host/pam_authorization_factory_posix.cc:119:3
    #2 remoting::PamAuthorizerUafTest_GetNextMessage_FreesThisDuringUnderlyingCall_Test::TestBody()

freed by thread T0 here:
    #0 operator delete(void*, unsigned long)
    #1 ... unique_ptr destructor chain ...
    #3 remoting::(anonymous namespace)::TestUnderlyingAuthenticator::GetNextMessage()
    #4 remoting::(anonymous namespace)::PamAuthorizer::GetNextMessage()
         remoting/host/pam_authorization_factory_posix.cc:117:46

previously allocated by thread T0 here:
    #0 operator new(unsigned long)
    #1 remoting::PamAuthorizationFactory::CreateAuthenticator(...)

SUMMARY: AddressSanitizer: heap-use-after-free
         remoting/host/pam_authorization_factory_posix.cc:137:7
         in remoting::(anonymous namespace)::PamAuthorizer::MaybeCheckLocalLogin()

```

The `freed by` stack ends inside `underlying_->GetNextMessage()` (line 117). The `READ` stack is line 119, the next statement after that call returns. That is the temporal relationship that commit `174583c9fcf83` fixed in the sibling authenticators.

## Reproduction steps

Environment used: current Chromium HEAD (Linux x64), ASAN build (`is_asan=true`, `use_libfuzzer=true`, `is_debug=false`).

1. Apply the attached test (added to `remoting/host/BUILD.gn` `source_set("unit_tests")`, and `pam_authorization_factory_posix.cc` also added to that source\_set so its symbols are linked into `remoting_unittests`):
   
   `remoting/host/pam_authorization_factory_posix_unittest.cc` defines a `TestUnderlyingAuthenticator` whose `GetNextMessage()` runs a trigger that synchronously drops the only strong reference to the wrapping `PamAuthorizer` (a `std::unique_ptr<protocol::Authenticator>`). It then calls `pam->GetNextMessage()` through a saved raw pointer. This models what the `on_state_change_after_accepted_` chain does in production: the underlying authenticator's method runs a synchronous callback that tears down the owning session, destroying the wrapper.
   
   Full test source is attached as `pam_authorization_factory_posix_unittest.cc` in the submission package.
2. Build:
   
   ```
   autoninja -C out/fuzz_asan remoting_unittests
   
   ```
3. Run:
   
   ```
   out/fuzz_asan/remoting_unittests \
     --gtest_filter='PamAuthorizerUafTest.GetNextMessage_FreesThisDuringUnderlyingCall'
   
   ```
4. ASAN report (verbatim from my local run, see `asan-pam-uaf-20260414-152259.log`):

```
==565990==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bf11023f138 at pc 0x55f20edd5719
READ of size 4 at 0x7bf11023f138 thread T0
    #0 PamAuthorizer::MaybeCheckLocalLogin()
         remoting/host/pam_authorization_factory_posix.cc:137:7
    #1 PamAuthorizer::GetNextMessage()
         remoting/host/pam_authorization_factory_posix.cc:119:3
    #2 PamAuthorizerUafTest_GetNextMessage_FreesThisDuringUnderlyingCall_Test::TestBody()
         remoting/host/pam_authorization_factory_posix_unittest.cc:167:26

0x7bf11023f138 is located 40 bytes inside of 48-byte region [0x7bf11023f110,0x7bf11023f140)
freed by thread T0 here:
    #0 operator delete(void*, unsigned long)
    #3 TestUnderlyingAuthenticator::GetNextMessage()
         remoting/host/pam_authorization_factory_posix_unittest.cc:76:27
    #4 PamAuthorizer::GetNextMessage()
         remoting/host/pam_authorization_factory_posix.cc:117:46

previously allocated by thread T0 here:
    #0 operator new(unsigned long)
    #1 PamAuthorizationFactory::CreateAuthenticator(...)

SUMMARY: AddressSanitizer: heap-use-after-free
         remoting/host/pam_authorization_factory_posix.cc:137:7
         in PamAuthorizer::MaybeCheckLocalLogin()

```

5. Applying the analogous fix (replace `base::Unretained(this)` with `weak_factory_.GetWeakPtr()` in `ProcessMessage`, and add a WeakPtr self-check between lines 117 and 119 in `GetNextMessage`, paralleling the sibling fix in commit `174583c9fcf83`) causes the test to pass with no ASAN report.

## Impact

**Attack surface: the Chrome Remote Desktop host authentication handshake.**

`PamAuthorizer` wraps the top-level host authenticator for Linux CRD hosts. It processes authentication messages from the remote (attacker-controlled) client during the connection-initiation handshake, before PAM has authorized the user, i.e. pre-auth. The `GetNextMessage` / `OnMessageProcessed` entry points are driven by the XMPP/ICE signaling that a remote client sends. Any path that synchronously destroys the session's `Authenticator` from inside a state-change notification (connection rejection, policy failure, timeout racing with an accept, remote disconnect mid-handshake) can trip this UAF on the host process.

**Why this is exploitable and impactful:**

1. **Pre-authentication heap UAF in a host process.** The `remoting_me2me_host` daemon runs as the logged-in user (and, for curtain-mode / it2me flows, as a service process). A UAF on its heap during handshake is exploitable for control-flow hijack given a typical heap grooming setup. `PamAuthorizer` is a small (~48 byte) object allocated from the general heap, it holds a vtable pointer, and the freed region is reused by subsequent allocations triggered by the same handshake turn (strings, protobufs, callback state). Because the bug is on the read side of a vtable-dispatched virtual call path (`state()` at line 137 is a virtual call into the freed object), overwriting the freed region with attacker-shaped data before line 137 runs produces a controlled virtual dispatch.
2. **Reachable from the network by a remote peer.** The `GetNextMessage`/`ProcessMessage` chain is what the Chromoting signaling subsystem calls in response to `session-initiate` / `session-accept` / `session-info` stanzas received from the other end of the XMPP connection. The attacker controls message framing and can force the authenticator through its state machine, including the synchronous destroy path.
3. **Not mitigated by sandboxing.** The Chrome Remote Desktop host is not the renderer sandbox; it is a long-running host binary that holds PAM tokens, opens X11 sockets and writes remote input into the local session. A UAF here compromises the user's entire desktop session, not a sandboxed tab.
4. **No user interaction required after pairing.** Once a host has been registered for a user, incoming connection attempts drive this code path without any local confirmation for `me2me` mode. A prior-paired (or policy-permitted) remote endpoint that has been compromised becomes a stepping-stone to the host's heap.
5. **The bug class has recent precedent and a just-landed partial fix.** [crbug.com/501376612](https://crbug.com/501376612) (fixed by `174583c9fcf83` on 2026-04-11) acknowledged the shape of this vulnerability in five sibling files.

## Attachments

- `pam_authorization_factory_posix_unittest.cc`, the unit test that drives the production callsite
- `asan-pam-uaf-20260414-152259.log`, the verbatim ASAN report from the local run
- Reference: commit `174583c9fcf83` ("Fix more potential UaF instances", 2026-04-11), the parent fix that missed this file

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: David Bors, Catalin Iovita

## Attachments

- [pam_authorization_factory_posix_unittest.cc](attachments/pam_authorization_factory_posix_unittest.cc) (text/x-c++src, 6.5 KB)
- [asan-pam-uaf-report.log](attachments/asan-pam-uaf-report.log) (text/plain, 10.7 KB)

## Timeline

### da...@gmail.com (2026-04-14)

On second thought, this should be treated as a defense in depth hardening. After more careful review, the UAF is not pre-auth, so the uplift would be minimal.

### an...@chromium.org (2026-04-17)

Assigning S3 because this UAF occurs post auth (per comment 2).
joedow@, can you PTAL? Thanks.

### jo...@google.com (2026-04-17)

Thanks!  I'll whip up a fix.

### ch...@google.com (2026-04-18)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-04-20)

Project: chromium/src  

Branch:  main  

Author:  Joe Downing [joedow@google.com](mailto:joedow@google.com)  

Link:    <https://chromium-review.googlesource.com/7778216>

remoting: Fix UAF in PamAuthorizer

---


Expand for full commit details
```
     
    PamAuthorizer sits in a wrapper position where its child authenticator 
    can synchronously cause the PamAuthorizer to be destroyed. 
     
    This CL fixes the UAF by: 
    1. Replacing base::Unretained(this) with a WeakPtr in ProcessMessage. 
    2. Adding a WeakPtr self-check in GetNextMessage. 
     
    Bug: 502461760 
    Change-Id: Idd02da5b5326909d94b0b95f0f44b18858dbd3d7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7778216 
    Commit-Queue: Joe Downing <joedow@chromium.org> 
    Reviewed-by: Yuwei Huang <yuweih@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1617759}

```

---

Files:

- M `remoting/host/BUILD.gn`
- M `remoting/host/pam_authorization_factory_posix.cc`
- A `remoting/host/pam_authorization_factory_posix_unittest.cc`

---

Hash: [703791650ac6bd600dc5ab229a3271e69786f423](https://chromiumdash.appspot.com/commit/703791650ac6bd600dc5ab229a3271e69786f423)  

Date: Mon Apr 20 20:58:39 2026


---

### sp...@google.com (2026-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Low impact -- post auth in CRD host software not Chrome


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/502461760)*
