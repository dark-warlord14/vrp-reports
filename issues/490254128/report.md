# Use-after-free in MidiManagerAndroid due to incorrect member destruction order on Android

| Field | Value |
|-------|-------|
| **Issue ID** | [490254128](https://issues.chromium.org/issues/490254128) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebMIDI |
| **Platforms** | Android |
| **Reporter** | je...@gmail.com |
| **Assignee** | ho...@google.com |
| **Created** | 2026-03-06 |
| **Bounty** | $4,000.00 |

## Description

## Summary

On Android, `MidiManagerAndroid` destroys its `input_port_to_index_` hash map before closing MIDI input ports, allowing a concurrent Android MIDI system callback to call `find()` on the destroyed map. This is a use-after-destroy that executes directly in the browser process, reachable from any page that uses the Web MIDI API while a MIDI device is actively sending data. Because the vulnerable code runs in the browser process rather than a sandboxed renderer, successful exploitation would not require a sandbox escape; a compromised renderer or even a normal web page with MIDI access can trigger the bug to corrupt browser process memory. The platform affected is Android only.

## Bisect

Introducing Commit: `e8b2e7dee39f272747554f0b26451d15b786e06d`

- Date: 2015-09-17
- Author: yhirano
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/1346563>

This commit introduced `MidiManagerAndroid` with `input_port_to_index_` declared after `devices_` in the class definition, establishing the incorrect destruction order that has persisted ever since.

## Root Cause

C++ destroys class members in reverse declaration order. In `MidiManagerAndroid`, the members are declared as follows:

```
// media/midi/midi_manager_android.h:72-89
base::Lock lock_;
std::vector<std::unique_ptr<MidiDeviceAndroid>> devices_;
std::vector<raw_ptr<MidiInputPortAndroid, VectorExperimental>> all_input_ports_;
absl::flat_hash_map<MidiInputPortAndroid*, size_t> input_port_to_index_;
std::vector<raw_ptr<MidiOutputPortAndroid, VectorExperimental>> all_output_ports_;
absl::flat_hash_map<MidiOutputPortAndroid*, size_t> output_port_to_index_;
base::android::ScopedJavaGlobalRef<jobject> raw_manager_;

```

Because `input_port_to_index_` is declared after `devices_`, it is destroyed before `devices_`. When `devices_` is destroyed, each `MidiDeviceAndroid` destroys its owned `MidiInputPortAndroid` objects, and their destructors call `Close()`, which crosses JNI to set the Java-side port reference to null. Only after `Close()` does the Android MIDI system stop invoking the `onSend` callback for that port.

Between the destruction of `input_port_to_index_` and the `Close()` call on each port, the Android MIDI system thread may deliver data through a JNI callback that reaches `MidiManagerAndroid::OnReceivedData`:

```
// media/midi/midi_manager_android.cc:111-117
void MidiManagerAndroid::OnReceivedData(MidiInputPortAndroid* port,
                                        base::span<const uint8_t> data,
                                        base::TimeTicks timestamp) {
  const auto i = input_port_to_index_.find(port);
  DCHECK(input_port_to_index_.end() != i);
  ReceiveMidiData(i->second, data, timestamp);
}

```

The `find()` call operates on a destroyed `absl::flat_hash_map`. In HWASAN/ASAN builds, the Swiss table's internal `kDestroyed` sentinel catches this and produces a fatal abort. In production release builds, this sentinel is never set; the `find()` call silently reads memory belonging to the destroyed object, constituting undefined behavior that may corrupt state or produce incorrect port indices passed to `ReceiveMidiData`.

The Java-side `synchronized` block in `MidiInputPortAndroid.java` serializes `close()` and `onSend()` calls, but it cannot prevent `onSend()` from executing before `close()` is ever called. The `UnbindInstance()` call in `~MidiManagerAndroid()` only prevents `PostBoundTask` callbacks; it does not affect JNI callbacks arriving on the Android MIDI system thread. The `DCHECK` on the iterator result is compiled out in release builds.

When only a single MIDI port is connected, the `absl::flat_hash_map` uses Small Object Optimization (SOO), storing its single entry inline rather than in a separate heap allocation. In this configuration, `find()` reads stale but physically valid inline data from the still-allocated parent object. With two or more ports, the map allocates a heap-backed control and slot array; after destruction, `find()` follows the dangling internal pointer into freed heap memory, a conventional heap use-after-free.

## Reproduce

Tested on commit `89d6357f16ea4` on an Android arm64 device (Pixel 7 Pro, HWASAN userdebug build). The vulnerability is in the browser process and requires a connected MIDI device that is actively sending data.

To reproduce, first apply the patch that widens the race window. From the Chromium source root, run `git apply patch.diff` to add a 500ms sleep in `~MidiInputPortAndroid()`. This sleep delays port closure during `~MidiManagerAndroid()` member destruction, giving the Android MIDI callback thread time to invoke `OnReceivedData()` while `input_port_to_index_` is already destroyed.

Configure the HWASAN build with the following `args.gn` in `out/android`:

```
is_debug = false
dcheck_always_on = false
target_cpu = "arm64"
is_component_build = false
target_os = "android"
is_hwasan = true
android_static_analysis = "off"
incremental_install = false

```

Build with `autoninja -C out/android chrome_public_apk` and install the resulting APK on the device with `out/android/bin/chrome_public_apk install`.

A MIDI device that continuously sends data must be connected to the Android device. The included `VirtualMIDI.apk` is a virtual MIDI service that registers as an Android MIDI device and floods MIDI output data. Install it with `adb install VirtualMIDI.apk` and verify it appears in `adb shell dumpsys midi` before starting Chrome. Alternatively, a physical USB MIDI controller or BLE MIDI device that sends continuous data will work.

Serve the PoC from the Chromium source root by running `python3 -m http.server 8888` on the host, then forward the port with `adb reverse tcp:8888 tcp:8888`. Launch Chrome with `out/android/bin/chrome_public_apk launch --args='--enable-logging=stderr --disable-features=BlockMidiByDefault' http://localhost:8888/poc.html`. The `--disable-features=BlockMidiByDefault` flag bypasses the MIDI permission prompt so that `requestMIDIAccess()` succeeds without manual interaction; it is not required to trigger the vulnerability, which is equally reachable after a user grants MIDI permission through the normal prompt.

The page calls `navigator.requestMIDIAccess()`, waits two seconds for MIDI data to flow, then navigates to `about:blank`. This navigation tears down the MIDI session and triggers `~MidiManagerAndroid()`. During member destruction, the 500ms sleep in `~MidiInputPortAndroid()` holds the destructor thread while the MIDI callback thread continues to deliver data. The callback invokes `OnReceivedData()`, which calls `input_port_to_index_.find(port)` on the already-destroyed `absl::flat_hash_map`, producing a fatal abort with the message "Use of destroyed hash table." The tombstone or logcat will contain this message; check with `adb logcat -d | grep FATAL` or inspect `/data/tombstones/`.

The crash log from the Android tombstone, with native frames symbolized:

```
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
Build fingerprint: 'Android/aosp_cheetah_hwasan/cheetah:Baklava/MAIN/13282683:userdebug/test-keys'
Revision: 'MP1.0'
ABI: 'arm64'
Timestamp: 2026-03-06 21:28:06.704553922+0800
Process uptime: 25s
Cmdline: org.chromium.chrome
pid: 11051, tid: 11231, name: Thread-8  >>> org.chromium.chrome <<<
uid: 10136
tagged_addr_ctrl: 0000000000000001 (PR_TAGGED_ADDR_ENABLE)
signal 6 (SIGABRT), code -1 (SI_QUEUE), fault addr --------
Abort message: '[FATAL:raw_hash_set.h:3314] NOTREACHED hit. Use of destroyed hash table.

51 total frames
backtrace:
      #00 pc 000000000007bcf0  libc.so (abort+288)
      #01 pc 000000000bdd3a1c  libchrome.so (base::ImmediateCrash, base/immediate_crash.h:185)
      #02 pc 000000000bdd33b8  libchrome.so (logging::LogMessage::Flush, base/logging.cc:741)
      #03 pc 000000000bdd3c54  libchrome.so (logging::LogMessageFatal::~LogMessageFatal, base/logging.cc:1050)
      #04 pc 000000000bdd1e5c  libchrome.so (AbslAbortHook, base/logging.cc:630)
      #05 pc 0000000003e1d9f0  libchrome.so (absl::raw_log_internal::RawLog, raw_logging.cc:251)
      #06 pc 000000001042aa48  libchrome.so (raw_hash_set<...MidiInputPortAndroid*...>::AssertNotDebugCapacity, raw_hash_set.h:3314)
      #07 pc 000000001042aa94  libchrome.so (raw_hash_set::AssertOnFind, raw_hash_set.h:3295)
      #08 pc 0000000010429b28  libchrome.so (raw_hash_set::find, raw_hash_set.h:2805)
      #09 pc 0000000010429c64  libchrome.so (MidiManagerAndroid::OnReceivedData, midi_manager_android.cc:114)
      --- JNI bridge ---
      #10                      tr6.onSend (MidiInputPortAndroid JNI callback)
      #11                      android.media.midi.MidiReceiver.send (MidiReceiver.java:128)
      #12                      com.android.internal.midi.MidiDispatcher.onSend (MidiDispatcher.java:91)
      #13                      android.media.midi.MidiReceiver.send (MidiReceiver.java:128)
      #14                      android.media.midi.MidiOutputPort$1.run (MidiOutputPort.java:78)

```

The crashing thread (Thread-8) is the Android MIDI system callback thread, not an IO thread or renderer thread. The call chain starts from `MidiOutputPort$1.run`, dispatches through the MIDI framework, crosses JNI into native code at `MidiInputPortAndroid::OnData`, and reaches `MidiManagerAndroid::OnReceivedData` where `find()` on the destroyed map triggers the fatal abort.

The crash is caught by a Swiss table invariant that only exists in sanitizer and debug builds. The `absl::flat_hash_map` destructor sets a `kDestroyed` sentinel on the capacity field after tearing down the backing storage:

```
// third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:2310-2315
~raw_hash_set() {
    destructor_impl();
    if constexpr (SwisstableAssertAccessToDestroyedTable()) {
      common().set_capacity(InvalidCapacity::kDestroyed);
    }
}

```

The guard `SwisstableAssertAccessToDestroyedTable()` returns true only when a sanitizer is active or the build is non-NDEBUG:

```
// third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:276-281
constexpr bool SwisstableAssertAccessToDestroyedTable() {
#ifndef NDEBUG
  return true;
#endif
  return SwisstableGenerationsEnabled();
}

```

And `SwisstableGenerationsEnabled()` is controlled by `ABSL_SWISSTABLE_ENABLE_GENERATIONS`, which is only defined when ASAN, HWASAN, or MSAN is active:

```
// third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:234-244
#if (defined(ABSL_HAVE_ADDRESS_SANITIZER) ||   \
     defined(ABSL_HAVE_HWADDRESS_SANITIZER) || \
     defined(ABSL_HAVE_MEMORY_SANITIZER)) &&   \
    !defined(NDEBUG_SANITIZER)
#define ABSL_SWISSTABLE_ENABLE_GENERATIONS
#endif

```

When `find()` is called on a destroyed map in an HWASAN build, it enters `AssertOnFind`, which calls `AssertNotDebugCapacity`. This function detects the `kDestroyed` sentinel on the capacity field and issues the fatal abort:

```
// third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:3299-3315
void AssertNotDebugCapacity() const {
#ifdef NDEBUG
    if (!SwisstableGenerationsEnabled()) {
      return;                    // production release: returns immediately
    }
#endif
    if (ABSL_PREDICT_TRUE(capacity() < InvalidCapacity::kAboveMaxValidCapacity)) {
      return;
    }
    // ...
    if constexpr (SwisstableAssertAccessToDestroyedTable()) {
      if (capacity() == InvalidCapacity::kDestroyed) {
        ABSL_RAW_LOG(FATAL, "Use of destroyed hash table.");  // the crash we observe
      }
    }
}

```

In a production release build (NDEBUG, no sanitizer), this entire detection path is compiled out. `SwisstableGenerationsEnabled()` returns false, so `AssertNotDebugCapacity` returns at the first `#ifdef NDEBUG` guard without ever checking capacity. The destructor never sets `kDestroyed` either, so the capacity field retains its pre-destruction value. The `find()` call proceeds into the actual lookup logic.

For a single-port configuration, the map uses SOO (Small Object Optimization) because `sizeof(pair<MidiInputPortAndroid*, size_t>)` is 16 bytes, equal to `sizeof(HeapOrSoo)`. The `destructor_impl` handles SOO tables by destroying the single slot and returning early without calling `dealloc`:

```
// third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:3035-3050
void destructor_impl() {
    // ...
    if (is_small()) {
      if (!empty()) {
        destroy(single_slot());  // no-op for trivially destructible pair<ptr, size_t>
      }
      if constexpr (SooEnabled()) return;  // returns here; no dealloc, no metadata reset
    }
    // ...
}

```

After this destructor runs, the SOO inline storage still contains the original key-value pair, the capacity field still holds the SOO capacity, and the size field still indicates one element. When the concurrent callback thread calls `find(port)`, it takes the SOO path through `find_small`:

```
// third_party/abseil-cpp/absl/container/internal/raw_hash_set.h:2967-2970
iterator find_small(const key_arg<K>& key) {
    return empty() || !equal_to(key, single_slot()) ? end() : single_iterator();
}

```

Since `empty()` returns false (size was not zeroed) and the key still matches the stale inline slot, `find_small` returns a valid-looking iterator. The caller then reads `i->second` to obtain a port index and passes it to `ReceiveMidiData`. In this single-port scenario, the stale data happens to be correct, so the undefined behavior manifests silently without an immediate crash.

With two or more MIDI ports, the map exceeds SOO capacity and allocates a separate heap-backed array for control bytes and slots. The `destructor_impl` calls `dealloc()`, freeing that heap allocation, but the internal `ctrl_` pointer is not reset. In production, `find()` takes the `find_large` path, which reads freed heap memory through the dangling `ctrl_` pointer to probe control bytes, a conventional heap use-after-free.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.0 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 716 B)
- [VirtualMIDI.apk](attachments/VirtualMIDI.apk) (application/vnd.android.package-archive, 12.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 3.0 KB)
- [readme.md](attachments/readme.md) (text/markdown, 2.7 KB)

## Timeline

### je...@gmail.com (2026-03-06)

This vulnerability is not easy to reproduce, but the underlying principle should be clear. If you need any assistance, please feel free to contact me.

### jd...@chromium.org (2026-03-06)

Setting a VERY TENTATIVE severity to aid in subsequent triage. Marking as High as a potential memory corruption in the browser process, heavily mitigated by being so racy and requiring a connected and active midi device.

### me...@google.com (2026-03-06)

Reporter: This commit and the review don't seem to exist?

> Introducing Commit: e8b2e7dee39f272747554f0b26451d15b786e06d

> Date: 2015-09-17
> Author: yhirano
> Review: <https://chromium-review.googlesource.com/c/chromium/src/+/1346563>

### je...@gmail.com (2026-03-07)

Thank you for catching that. The commit hash e8b2e7dee39f272747554f0b26451d15b786e06d is correct -- it is the commit that first introduced MidiManagerAndroid with `devices_` declared before `input_port_to_index_`, establishing the incorrect destruction order. I apologize for the wrong review URL; this 2015 commit predates the migration to Gerrit and used the old Rietveld code review system. The correct review URL is:

<https://codereview.chromium.org/1177973003>

For completeness, here is the history of changes relevant to this destruction-order bug:

1. e8b2e7dee39f2 (2015-09-17, yhirano) -- Bug introduced. The destructor was empty, relying entirely on automatic member destruction. Because `devices_` is declared before `input_port_to_index_`, the map is destroyed first, and then `devices_` destruction triggers port Close() calls via JNI. The race window between map destruction and port closure has existed since this commit.
2. 8d3e6e645dc73 (2017-09-25, toyoshim) -- Partially mitigated. A Finalize() method was added that explicitly calls `devices_.clear()` before `input_port_to_index_.clear()`, which is the correct order. This was only effective when Finalize() was called in the dynamic instantiation path.
3. 9151f22fca5ac (2018-10-03, toyoshim) -- Mitigation removed. Finalize() was deleted and the destructor was reduced to just calling UnbindInstance(), returning to automatic member destruction in the wrong order.
4. aa649e688dd4b (2019-02-05, yhirano) -- Incomplete fix attempt. Added a Java\_MidiManagerAndroid\_stop() call in the destructor, but stop() only sets mStopped=true on the Java MidiManagerAndroid object. The onSend callback in MidiInputPortAndroid.java does not check mStopped -- it only checks mPort==null, which is set by close(). So MIDI data callbacks on the Android MIDI system thread are unaffected by stop(), and the race remains.

### pe...@google.com (2026-03-07)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@google.com (2026-03-07)

Setting milestone because of s0/s1 severity.

### to...@chromium.org (2026-03-10)

pass to Michael who is the current owner.

### mj...@chromium.org (2026-03-10)

I'm getting flooded with security issues recently but will try to look at this by the end of the week.

### mj...@chromium.org (2026-03-10)

Also, thank you for the report! I am happy that we are uncovering these problems it will just take me some time to work through them.

### ho...@google.com (2026-03-11)

I have written a fix for this Use-After-Free issue locally by moving the declaration of `devices_` to the end of the `MidiManagerAndroid` class member list in `media/midi/midi_manager_android.h`. This enforces that `devices_` is destroyed first during class teardown, correctly closing ports and unbinding Java callbacks before the underlying `absl::flat_hash_map` port maps are destroyed.

I've verified the fix compiles and the basic tests pass. The UAF timing behavior will be verified by ClusterFuzz/Security Sheriffs after landing using the reporter's excellent PoC.

Comment created using go/buganizer-mcp-server

### ho...@google.com (2026-03-11)

jdeblasio@

Since this relies heavily on Android MIDI hardware and timing, standard CI cannot reliably verify this race. Could you or the Security Sheriff rotation please verify the fix on an Android HWASAN device using the reporter's PoC?

Patch: [crrev.com/c/7659363](https://crrev.com/c/7659363)

jerrylulu7@

Thanks for your detailed report. Could you help us verify the fix with the patch above?

### je...@gmail.com (2026-03-11)

No problem, I can help you with patch verification and will provide you with an update today.

### je...@gmail.com (2026-03-12)

Verification Results for crrev.com/c/7659363

Device: Pixel 7 Pro (cheetah), HWASAN userdebug build (Android/aosp_cheetah_hwasan/cheetah:Baklava/MAIN/13282683)
Chromium HEAD: 457566e1c0b41 (2026-03-12)
Instrumentation: patch.diff (500ms sleep in ~MidiInputPortAndroid() to widen race window)
MIDI source: VirtualMIDI APK (virtual MIDI service flooding output data)

=== Before fix (baseline) ===

Applied only patch.diff (race window widener). Launched Chrome with --disable-features=BlockMidiByDefault, loaded poc.html which calls requestMIDIAccess(), waits 2s for MIDI data to flow, then navigates to about:blank to trigger ~MidiManagerAndroid().

Result: CRASH on first attempt.

  pid: 24490, tid: 24692, name: Thread-8  >>> org.chromium.chrome <<<
  signal 6 (SIGABRT), code -1 (SI_QUEUE)
  Abort message: '[FATAL:raw_hash_set.h:3336] NOTREACHED hit. Use of destroyed hash table.'

  Java stack:
    at py6.onSend(chromium-ChromePublic.apk:30)
    at android.media.midi.MidiReceiver.send(MidiReceiver.java:128)
    at com.android.internal.midi.MidiDispatcher.onSend(MidiDispatcher.java:91)
    at android.media.midi.MidiReceiver.send(MidiReceiver.java:128)
    at android.media.midi.MidiOutputPort$1.run(MidiOutputPort.java:78)

  Tombstone: tombstone_41 generated at 2026-03-12 10:10:12

=== After fix (crrev.com/c/7659363) ===

Applied the fix (moved devices_ declaration after port index maps in midi_manager_android.h) in addition to patch.diff. Ran the same PoC 4 consecutive times.

  Run 1: Chrome survived (pid 24817), 0 tombstones, 0 FATAL messages
  Run 2: Chrome survived (pid 25114), 0 tombstones, 0 FATAL messages
  Run 3: Chrome survived (pid 25388), 0 tombstones, 0 FATAL messages
  Run 4: Chrome survived (pid 25663), 0 tombstones, 0 FATAL messages

Result: NO CRASH across all 4 runs.

=== Conclusion ===

The fix correctly resolves the Use-After-Free. By declaring devices_ after the port index maps, C++ reverse-order member destruction now destroys devices_ first, closing ports and stopping JNI callbacks before the absl::flat_hash_map members are destroyed. The Android MIDI callback thread can no longer invoke OnReceivedData() on a destroyed hash table.


### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  Hongchan Choi [hongchan@chromium.org](mailto:hongchan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7659363>

[WebMIDI/Android] Fix destruction order n MidiManagerAndroid

---


Expand for full commit details
```
     
    Moving the `devices_` declaration to the end of the class ensures 
    it is destroyed first, safely closing ports before the hash maps 
    are destroyed. 
     
    Bug: 490254128 
    Change-Id: I1a7857ef3f0f58772cd300f603dc74720ac49964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7659363 
    Commit-Queue: Hongchan Choi <hongchan@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1598579}

```

---

Files:

- M `media/midi/midi_manager_android.h`

---

Hash: [ab92725b0824c9fd98aea65a5b4c7fb1a27fcc5e](https://chromiumdash.appspot.com/commit/ab92725b0824c9fd98aea65a5b4c7fb1a27fcc5e)  

Date: Thu Mar 12 18:37:09 2026


---

### ho...@google.com (2026-03-12)

Per [comment#14](https://issues.chromium.org/issues/490254128#comment14), updating this as Fixed (Verified).

I'll wait for 2~3 days and start merge requests.

### ch...@google.com (2026-03-13)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1598579) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1598579) appears to be after beta branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-13)

**Merge approved:** your change passed merge requirements and is auto-approved for M147. Please go ahead and merge the CL to branch 7727 (refs/branch-heads/7727) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-13)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ho...@google.com (2026-03-17)

M147 merge in progress: [crrev.com/c/7674785](https://crrev.com/c/7674785)

### ho...@google.com (2026-03-17)

Responding to [comment#19](https://issues.chromium.org/issues/490254128#comment19):

1. The fix is for a P1/S1 security issue.
2. [crrev.com/c/7659363](https://crrev.com/c/7659363)
3. Yes. The merge to M147 is already in progress.
4. No.
5. The fix is already verified by the reporter, but the manual verification from the test team would also be appreciated. The reproduction instruction can be found in the bug description.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Hongchan Choi [hongchan@chromium.org](mailto:hongchan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7674785>

[WebMIDI/Android] Fix destruction order n MidiManagerAndroid

---


Expand for full commit details
```
     
    Moving the `devices_` declaration to the end of the class ensures 
    it is destroyed first, safely closing ports before the hash maps 
    are destroyed. 
     
    (cherry picked from commit ab92725b0824c9fd98aea65a5b4c7fb1a27fcc5e) 
     
    Bug: 490254128 
    Change-Id: I1a7857ef3f0f58772cd300f603dc74720ac49964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7659363 
    Commit-Queue: Hongchan Choi <hongchan@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1598579} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7674785 
    Cr-Commit-Position: refs/branch-heads/7727@{#644} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `media/midi/midi_manager_android.h`

---

Hash: [878002d1ca10eddb3eb5cad272b12f84bf6abc0c](https://chromiumdash.appspot.com/commit/878002d1ca10eddb3eb5cad272b12f84bf6abc0c)  

Date: Tue Mar 17 21:40:18 2026


---

### dr...@chromium.org (2026-03-25)

Sorry about the delay here. Approved to merge to M146.

### dx...@google.com (2026-03-28)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Hongchan Choi [hongchan@chromium.org](mailto:hongchan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705635>

[WebMIDI/Android] Fix destruction order n MidiManagerAndroid

---


Expand for full commit details
```
     
    Moving the `devices_` declaration to the end of the class ensures 
    it is destroyed first, safely closing ports before the hash maps 
    are destroyed. 
     
    (cherry picked from commit ab92725b0824c9fd98aea65a5b4c7fb1a27fcc5e) 
     
    (cherry picked from commit 878002d1ca10eddb3eb5cad272b12f84bf6abc0c) 
     
    Bug: 490254128 
    Change-Id: I1a7857ef3f0f58772cd300f603dc74720ac49964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7659363 
    Commit-Queue: Hongchan Choi <hongchan@chromium.org> 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1598579} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7674785 
    Cr-Original-Commit-Position: refs/branch-heads/7727@{#644} 
    Cr-Original-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705635 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Jordan Bayles <jophba@chromium.org> 
    Reviewed-by: Jordan Bayles <jophba@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3385} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `media/midi/midi_manager_android.h`

---

Hash: [4b865179d7883b7561648c63e51a68a0d9b7175e](https://chromiumdash.appspot.com/commit/4b865179d7883b7561648c63e51a68a0d9b7175e)  

Date: Sat Mar 28 06:21:47 2026


---

### sp...@google.com (2026-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Moderately mitigated (non-sandboxed) wit bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490254128)*
