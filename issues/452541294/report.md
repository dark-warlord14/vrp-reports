# Type confusion in v8 caused by incorrect unregistration of prototype users

| Field | Value |
|-------|-------|
| **Issue ID** | [452541294](https://issues.chromium.org/issues/452541294) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2025-10-16 |
| **Bounty** | $10,000.00 |

## Description

Security Bug

Vulnerability details

When a prototype object changes its map, it'll call [`UpdatePrototypeUserRegistration`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/js-objects.cc;l=3082;drc=1fb4c56b03b105b03c45627871b15b8933ed8a11?q=js-objects.cc&ss=chromium%2Fchromium%2Fsrc) to transfer the prototype user information from the old map to the new map:

```
void JSObject::NotifyMapChange(DirectHandle<Map> old_map,
                               DirectHandle<Map> new_map, Isolate* isolate) {
  if (!old_map->is_prototype_map()) return;

  InvalidatePrototypeChains(*old_map);

  // If the map was registered with its prototype before, ensure that it
  // registers with its new prototype now. This preserves the invariant that
  // when a map on a prototype chain is registered with its prototype, then
  // all prototypes further up the chain are also registered with their
  // respective prototypes.
  UpdatePrototypeUserRegistration(old_map, new_map, isolate);
}

```

Prototype users are maps that has this object as their prototypes and are used in inline cache to ensure optimized inline cache handlers are used on the correct prototype object. Whenever there is a map change in a prototype object, its users along the prototype chains are tracked down, and their [`PrototypeValidityCell` gets invalidated](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/js-objects.cc;l=5232;drc=9d6f972e353f541f4f3261fa971d20fa61d839bd?q=js-objects.cc&ss=chromium%2Fchromium%2Fsrc) so that any inline cache handlers using these users get invalidated.

When transferring the user information from the old prototype map to a new prototype map, if the old prototype object has a `WasmObject` as its prototype, then `UnregisterPrototypeUser` will skip removing the old prototype map from the users of its prototype (`user` below is the old prototype map):

```
bool JSObject::UnregisterPrototypeUser(DirectHandle<Map> user,
                                       Isolate* isolate) {
  ...
  if (!IsJSObject(user->prototype())) {
    Tagged<Object> users =
        Cast<PrototypeInfo>(user->prototype_info())->prototype_users();
    return IsWeakArrayList(users);
  }
  ...

```

Moreover, if the old prototype map does not have any user itself, then `UnregisterPrototypeUser` will return `false`:

```
void JSObject::UpdatePrototypeUserRegistration(DirectHandle<Map> old_map,
                                               DirectHandle<Map> new_map,
                                               Isolate* isolate) {
  ...
  bool was_registered = JSObject::UnregisterPrototypeUser(old_map, isolate);
  new_map->set_prototype_info(old_map->prototype_info(), kReleaseStore);
  old_map->set_prototype_info(Smi::zero(), kReleaseStore);
  ...
  if (was_registered) {
    if (new_map->has_prototype_info()) {
      // The new map isn't registered with its prototype yet; reflect this fact
      // in the PrototypeInfo it just inherited from the old map.
      Cast<PrototypeInfo>(new_map->prototype_info())
          ->set_registry_slot(PrototypeInfo::UNREGISTERED);
    }
    JSObject::LazyRegisterPrototypeUser(new_map, isolate);
  }
}

```

This then skips setting the `registry_slot` of `new_map` to `PrototypeInfo::UNREGISTERED` and registering `new_map` as the user of its prototype.

Consider the following scenario, where each arrow indicates a prototype:

```
old_map->wasm_obj->proto2->...

```

In this case, `proto2` is the prototype of `wasm_obj` and `wasm_obj` is the prototype of `old_map`, while `old_map` is a user of `wasm_obj` and `wasm_obj` is a user of `proto2`, and `wasm_obj` is a `WasmObject`.

When the object with `old_map` migrates to a new map, because `old_map` has `wasm_obj`, a `WasmObject` as its prototype and has no user, the `prototype_users` of `old_map` gets transferred directly to `new_map`, however,
the the registration of `new_map` in `proto2` is skipped, while `old_map` is not unregistered`from`proto2`. This means that:

1. `prototype_users` of `proto2` is not updated and still contains a reference to `old_map`, and it also does not contain a reference to `new_map`.
2. `registry_slot` in the new map is not `UNREGISTERED`.

Point 2. in particular, means that `new_map` will never be registered as a user of `wasm_obj`, because `LazyRegisterPrototypeUser` bails out once it sees a set `registry_slot` in the prototype chain:

```
void JSObject::LazyRegisterPrototypeUser(DirectHandle<Map> user,
                                         Isolate* isolate) {
  ...
  DirectHandle<Map> current_user = user;
  DirectHandle<PrototypeInfo> current_user_info =
      Map::GetOrCreatePrototypeInfo(user, isolate);
  for (PrototypeIterator iter(isolate, user); !iter.IsAtEnd(); iter.Advance()) {
    // Walk up the prototype chain as far as links haven't been registered yet.
    if (current_user_info->registry_slot() != PrototypeInfo::UNREGISTERED) {
      break;
    }
    ...

```

If an inline cache handler is now created to read a field from `proto2` via an object that has `new_map` as its prototype, `LazyRegisterPrototypeUser` will be called in an attempt to register `new_map` as a user of `wasm_obj`, which will fail. This means that if the map of `proto2` is changed after the creation of the inline cache handler, the `PrototypeValidityCell` of `new_map` will not be invalidated because it cannot be found amongst the chain of users of `proto2`.

This then results in a type confusion.

As there is currently an [origin trial](https://developer.chrome.com/origintrials/?hl=uk#/view_trial/619807898716864513) for the Webassembly custom descriptors, which allows prototypes to be set on `WasmObject`, anyone can register for the origin trial and host a website that can trigger this bug.

Thank you very much for your help and please let me know if there is anything I can help.

REPRODUCTION CASE

To test locally, run the `poc.js` with the `--experimental-wasm-custom-descriptors` flag and the `--allow-natives-syntax` flag to print out debug message. The flag `--experimental-wasm-custom-descriptors` is only needed for local testing to emulate the origin trial. It should cause an OOB access which then loads an object from outside of the boundary of `proto` (A heap number map in my case).

I've also included a `cage_rw.js` poc to demonstrate arbitrary read and write within the v8 heap sandbox using this bug.

VERSION

v8 commit 172e05b
OS: Ubuntu 24.04 LTS

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

Reporter credit: Man Yue Mo of GitHub Security Lab

## Attachments

- poc.js (text/javascript, 1.2 KB)
- cage_rw.js (text/javascript, 2.8 KB)
- wasm-module-builder.js (text/javascript, 76.5 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-10-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5460541317251072.

### 24...@project.gserviceaccount.com (2025-10-16)

Testcase 5460541317251072 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5460541317251072.

### ja...@chromium.org (2025-10-17)

[security shepherd]
I was able to reproduce this manually. Sending to the v8 shepherd for a closer look. I'll try to run clusterfuzz one more time.

### ja...@chromium.org (2025-10-17)

[security shepherd]
Here was the output I got:

```
$ ../Extended-140/d8 --experimental-wasm-custom-descriptors --allow-natives-syntax ./poc.js 
V8 is running with experimental features enabled. Stability and security will suffer.
0x6bc800000011 <undefined>

```

Also:

```
$ ../Canary_asan-143_Canary-143/d8 --experimental-wasm-custom-descriptors --allow-natives-syntax ./poc.js 
V8 is running with experimental features enabled. Stability and security will suffer.
0x7e9400000515 <Map[12](HEAP_NUMBER_TYPE)>

```

### ja...@chromium.org (2025-10-17)

Provisionally assigning High (S1). And found in to extended stable

### cl...@appspot.gserviceaccount.com (2025-10-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4507095353196544.

### ch...@google.com (2025-10-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-10-18)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cl...@chromium.org (2025-10-20)

Jakob, is this a duplicate of <https://crbug.com/447613211>? Seems at least related.

### jk...@chromium.org (2025-10-20)

#1: Thanks for the report! FYI, the Origin Trial is currently disabled, so this isn't impacting users.

#5: This is not in stable/140. `undefined` is perfectly safe.

#10: Not a dupe. Valid issue. Will fix.

### dx...@google.com (2025-10-20)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7062032>

[wasm-custom-desc] Fix UnregisterPrototypeUser for mixed chains

---


Expand for full commit details
```
     
    The recent fix crrev.com/c/7003558 fixed registration but not 
    deregistration; this follow-up addresses that. 
     
    Fixed: 452541294 
    Change-Id: I1796947424289ac8221efde88d338780be12bf8c 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7062032 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#103204}

```

---

Files:

- M `src/objects/js-objects.cc`
- A `test/mjsunit/regress/wasm/regress-452541294.js`

---

Hash: [5ac3b7e20bec233ea90439a811d8ad9bfadf0ca4](https://chromiumdash.appspot.com/commit/5ac3b7e20bec233ea90439a811d8ad9bfadf0ca4)  

Date: Mon Oct 20 09:42:08 2025


---

### ch...@google.com (2025-10-29)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge approved:** your change passed merge requirements and is auto-approved for M143. Please go ahead and merge the CL to branch 7499 (refs/branch-heads/7499) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [143].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2025-10-30)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### jk...@chromium.org (2025-10-30)

#13: Fix landed before branch.

### ct...@chromium.org (2025-11-13)

Quick followup question to [Comment #11](https://issues.chromium.org/issues/452541294#comment11): Are existing OT tokens invalidated? It appears that the feature is still enable-able via OT as it is specified in runtime\_enabled\_features.json5 <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/runtime_enabled_features.json5;l=5563;drc=b967fb8ce7fde4202959ab603bde78742088748e>, although new signups for the OT do appear to be disabled on the dashboard (<https://developer.chrome.com/origintrials/#/view_trial/619807898716864513>).

### jk...@chromium.org (2025-11-13)

#16: Yes. Only four OT tokens had been registered when we disabled new signups (on Sep 23), and the process to disable the existing four tokens was kicked off on Oct 6 (internal [b/449782934](https://issues.chromium.org/issues/449782934)).

### ct...@chromium.org (2025-11-13)

Excellent, thank you for confirming!

### sp...@google.com (2025-11-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality memory corruption in a sandboxed process. the panel thanks you in particular for going the extra mile and noticing this issue might be exposed to users via origin trial.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### my...@gmail.com (2025-11-17)

Thanks. I'd like to donate the reward to charity. I've included a poc in the report to demonstrate arbitrary read and write within the v8 heap sandbox using this bug. (`cage_rw.js`) Does that affect the decision? Thanks.

### ch...@google.com (2026-01-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality memory corruption in a sandboxed process. the panel thanks you in particular for going the extra mile and noticing this issue might be exposed to users via origin trial.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/452541294)*
