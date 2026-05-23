# Security: Out-of-bounds access in WebAudio

| Field | Value |
|-------|-------|
| **Issue ID** | [40055614](https://issues.chromium.org/issues/40055614) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kk...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2021-04-21 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webaudio/audio_worklet_processor.cc;drc=7f5a8953f42e12194870ec6f0bf6d41c66663a36;l=173>

```
bool AudioWorkletProcessor::PortTopologyMatches(  
    v8::Isolate\* isolate,  
    v8::Local<v8::Context> context,  
    const Vector<scoped_refptr<AudioBus>>& audio_port_1,  
    const TraceWrapperV8Reference<v8::Array>& audio_port_2) {  
  TRACE_EVENT0(TRACE_DISABLED_BY_DEFAULT("audio-worklet"),  
               "AudioWorkletProcessor::Process (compare topology)");  
  if (audio_port_2.IsEmpty())  
    return false;  
  
  // Two AudioPorts are supposed to have the same length because the number of  
  // inputs and outputs of AudioNode cannot change after construction.  
  v8::Local<v8::Array> port_2_local = audio_port_2.NewLocal(isolate);  
  DCHECK(port_2_local->IsArray());  
  DCHECK_EQ(audio_port_1.size(), port_2_local->Length());  
  
  v8::TryCatch try_catch(isolate);  
  
  v8::Local<v8::Value> value;  
  uint32_t bus_index_counter = 0;  
  for (const auto& audio_bus_1 : audio_port_1) {  
    if (!port_2_local->Get(context, bus_index_counter).ToLocal(&value) ||        // \*\*\* 1 \*\*\*  
        !value->IsArray())  
      return false;  
  
    // Compare the length of AudioBus1[i] from AudioPort1 and AudioBus2[i] from  
    // AudioPort2.  
    unsigned number_of_channels =  
        audio_bus_1 ? audio_bus_1->NumberOfChannels() : 0;  
    v8::Local<v8::Array> audio_bus_2 = value.As<v8::Array>();  
    if (number_of_channels != audio_bus_2->Length())                             // \*\*\* 2 \*\*\*  
      return false;  
  
    // If the channel count of AudioBus1[i] and AudioBus2[i] matches, then  
    // iterate all the channels in AudioBus1[i] and see if any AudioChannel  
    // is detached. (i.e. transferred to a different thread)  
    for (uint32_t channel_index = 0; channel_index < audio_bus_2->Length();  
         ++channel_index) {  
      if (!audio_bus_2->Get(context, channel_index).ToLocal(&value) ||  
          !value->IsFloat32Array())                                             // \*\*\* 3 \*\*\*  
        return false;  
      v8::Local<v8::Float32Array> float32_array = value.As<v8::Float32Array>();  
  
      // If any array is transferred, we need to rebuild them.  
      if (float32_array->ByteLength() == 0)                                     // \*\*\* 4 \*\*\*  
        return false;  
    }  
  
    bus_index_counter++;  
  }  
  
  return true;  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webaudio/audio_worklet_processor.cc;l=61;drc=cb83c85e1025099b2888bc29e24dac4ab49b02c7>

```
bool AudioWorkletProcessor::Process(  
    const Vector<scoped_refptr<AudioBus>>& inputs,  
    Vector<scoped_refptr<AudioBus>>& outputs,  
    const HashMap<String, std::unique_ptr<AudioFloatArray>>& param_value_map) {  
  TRACE_EVENT0(TRACE_DISABLED_BY_DEFAULT("audio-worklet"),  
               "AudioWorkletProcessor::Process");  
  
  DCHECK(global_scope_->IsContextThread());  
  DCHECK(!hasErrorOccurred());  
  
  ScriptState\* script_state =  
      global_scope_->ScriptController()->GetScriptState();  
  ScriptState::Scope scope(script_state);  
  v8::Isolate\* isolate = script_state->GetIsolate();  
  v8::Local<v8::Context> context = script_state->GetContext();  
  AudioWorkletProcessorDefinition\* definition =  
      global_scope_->FindDefinition(Name());  
  
  // 1st JS arg |inputs_|. Compare |inputs| and |inputs_|. Then allocates the  
  // data container if necessary.  
  if (!PortTopologyMatches(isolate, context, inputs, inputs_)) {                  // \*\*\* 5 \*\*\*  

```

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webaudio/audio_worklet_processor.cc;drc=7f5a8953f42e12194870ec6f0bf6d41c66663a36;l=314>

```
void AudioWorkletProcessor::CopyPortToArrayBuffers(  
      v8::Isolate\* isolate,  
      const Vector<scoped_refptr<AudioBus>>& audio_port,  
      BackingArrayBuffers& array_buffers) {  
  DCHECK_EQ(audio_port.size(), array_buffers.size());  
  
  for (uint32_t bus_index = 0; bus_index < audio_port.size(); ++bus_index) {  
    const scoped_refptr<AudioBus>& audio_bus = audio_port[bus_index];  
    size_t bus_length = audio_bus ? audio_bus->length() : 0;  
    unsigned number_of_channels = audio_bus ? audio_bus->NumberOfChannels() : 0;  
    for (uint32_t channel_index = 0; channel_index < number_of_channels;  
         ++channel_index) {  
      auto backing_store = array_buffers[bus_index][channel_index]               // \*\*\* 6 \*\*\*  
                               .NewLocal(isolate)  
                               ->GetBackingStore();  
      memcpy(backing_store->Data(), audio_bus->Channel(channel_index)->Data(),  // \*\*\* 7 \*\*\*  
             bus_length \* sizeof(float));  
    }  
  }  
}  

```

The root cause of this vulnerability is JavaScript callback from [1].

In `AudioWorkletProcessor::PortTopologyMatches`, `audio_port_1` is the parameter variable `inputs` in `AudioWorkletProcessor::Process` [5].  

The size of `audio_port_1` is the same as the length of `audio_bus_2` in most cases.  

The variable `audio_bus_2` is determined by `audio_port_1` in `AudioWorkletProcessor::ClonePortTopology` function.  

After `audio_bus_2` is set, `audio_bus_2` is not changed before `AudioWorkletProcessor::PortTopologyMatches` returns `false`.

When the user makes two `AudioWorkletNode`s using singleton pattern, `AudioWorkletNode`s have the same `AudioWorkletProcessor`.  

Then, `AudioWorkletProcessor::PortTopologyMatches` can have different sizes of `audio_port_1`.  

Because we can pass the different sizes of `inputs` using different `AudioWorkletNode`s.  

It means that the length of `port_2_local` less than `bus_index_counter` which is an index of `audio_port_1`'s size.  

In this case, we can make a JavaScript callback using `__defineGetter__`, and it will be called in [1].

Using the JavaScript callback, we can control the variable `value` which is the return value of the callback.  

Then, we can bypass the check routine [2] because we can control the size of the array using the callback.  

Also, we can bypass the check routines [3], and [4] in the same manner.  

Bypassing the check routines, `AudioWorkletProcessor::PortTopologyMatches` always returns `true`.  

It means the variable `audio_bus_2` is never changed, and also the variable `array_buffers`, which is explained as follows, is not changed too.

In `AudioWorkletProcessor::CopyPortToArrayBuffers`, `audio_port` is the same variable above `audio_port_1`.  

The variable `array_buffers` is `Vector` type, and the size of `array_buffers` is also determined by `audio_port_1` from `AudioWorkletProcessor::ClonePortTopology`.  

It means that the size of `audio_port_1` can be bigger than the size of `array_buffers` (using singleton pattern and bypassing check routines).  

So we can access `array_buffers` out of bounds in [6].  

Also, if we detach one of `ArrayBuffer` in `array_buffers` from `AudioWorkletProcessor::PortTopologyMatches` after bypassing check routines (TOCTOU),  

We can access the detached backing store of `ArrayBuffer` in [7].

**VERSION**  

Chrome Version: 90.0.4430.72 (latest stable version)  

Operating System: Windows, Linux, MacOS, Android

**REPRODUCTION CASE**

I attached two JavaScript codes. One is Out-of-Bounds `Vector` access. The other is accessing the detached `ArrayBuffer`'s backing store.  

Please see the attachments.

## Attachments

- [arraybuffer.html](attachments/arraybuffer.html) (text/plain, 1.4 KB)
- [oob.html](attachments/oob.html) (text/plain, 1.3 KB)
- [oob.log](attachments/oob.log) (text/plain, 10.9 KB)
- [arraybuffer.log](attachments/arraybuffer.log) (text/plain, 5.9 KB)

## Timeline

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5667300636950528.

### cl...@chromium.org (2021-04-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5079857089019904.

### ca...@chromium.org (2021-04-23)

It looks like CF was not able to reproduce this with either poc, and I was also not able to reproduce by hand. Could you attach the crash log you get? Thanks

### kk...@gmail.com (2021-04-26)

I attach the crash logs. And, you have to run the PoCs with web server for reproducing it.

### [Deleted User] (2021-04-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2021-04-27)

rtoy: Can you please help triage this one too? Thanks

[Monorail components: Blink>WebAudio]

### rt...@chromium.org (2021-04-27)

See also https://crbug.com/chromium/1202060, which is probably a duplicate where DCHECK is enabled to catch the unexpected state which looks as if it can actually happen.

This probably happens for all OSes.

### [Deleted User] (2021-04-27)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-05)

hongchan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2021-05-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f1e277f1b586e0be0cc7f3b4f6462fa4982b7b49

commit f1e277f1b586e0be0cc7f3b4f6462fa4982b7b49
Author: Hongchan Choi <hongchan@chromium.org>
Date: Thu May 06 00:20:54 2021

Return false when the size of audio_port_1 and audio_port_2 is different

The current code assumes the size of audio ports is identical because
the number of inputs and outputs cannot change after construction. This
assumption is broken when multiple AudioWorkletNodes share a singleton
AudioWorkletProcessor instance.

This patch removes the assumption and explicitly returns false when the
number of inputs and outputs does not match.

Bug: 1201033, 120260
Test: 3 repro cases submitted do not crash on ASAN.
Change-Id: I4065e7970b9b7b54468fc82558509a3238ff28e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2875846
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#879631}

[modify] https://crrev.com/f1e277f1b586e0be0cc7f3b4f6462fa4982b7b49/third_party/blink/renderer/modules/webaudio/audio_worklet_processor.cc


### ho...@chromium.org (2021-05-07)

kkwondotnet@

Could you check with 92.0.4500.0?

### [Deleted User] (2021-05-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-08)

Requesting merge to beta M91 because latest trunk commit (879631) appears to be after beta branch point (738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-08)

This bug requires manual review: M91's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kk...@gmail.com (2021-05-09)

hongchan@

I checked it, and it seems to be fixed very well.

### ho...@chromium.org (2021-05-10)

1. Yes.
2. https://crrev.com/c/2875846
3. Yes.
4. Yes.
5. This is a security issue.
6. No.
7. No.

### ad...@google.com (2021-05-10)

Approving merge to M91, branch 4472.

### ad...@chromium.org (2021-05-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bce03b43e222a2e659809ae909674a242bdccdde

commit bce03b43e222a2e659809ae909674a242bdccdde
Author: Hongchan Choi <hongchan@chromium.org>
Date: Tue May 11 16:50:26 2021

Return false when the size of audio_port_1 and audio_port_2 is different

The current code assumes the size of audio ports is identical because
the number of inputs and outputs cannot change after construction. This
assumption is broken when multiple AudioWorkletNodes share a singleton
AudioWorkletProcessor instance.

This patch removes the assumption and explicitly returns false when the
number of inputs and outputs does not match.

(cherry picked from commit f1e277f1b586e0be0cc7f3b4f6462fa4982b7b49)

Bug: 1201033, 120260
Test: 3 repro cases submitted do not crash on ASAN.
Change-Id: I4065e7970b9b7b54468fc82558509a3238ff28e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2875846
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#879631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2885639
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4472@{#935}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/bce03b43e222a2e659809ae909674a242bdccdde/third_party/blink/renderer/modules/webaudio/audio_worklet_processor.cc


### am...@google.com (2021-05-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-20)

Congratulations, the VRP Panel has decided to award you $7500 for this report! Nice work! 

### am...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-06-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e80c2769e463f2795afa72fe36a66c02ba1f2a14

commit e80c2769e463f2795afa72fe36a66c02ba1f2a14
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Jun 02 18:34:26 2021

Return false when the size of audio_port_1 and audio_port_2 is different

The current code assumes the size of audio ports is identical because
the number of inputs and outputs cannot change after construction. This
assumption is broken when multiple AudioWorkletNodes share a singleton
AudioWorkletProcessor instance.

This patch removes the assumption and explicitly returns false when the
number of inputs and outputs does not match.

(cherry picked from commit f1e277f1b586e0be0cc7f3b4f6462fa4982b7b49)

Bug: 1201033, 120260
Test: 3 repro cases submitted do not crash on ASAN.
Change-Id: I4065e7970b9b7b54468fc82558509a3238ff28e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2875846
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#879631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2922863
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1659}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/e80c2769e463f2795afa72fe36a66c02ba1f2a14/third_party/blink/renderer/modules/webaudio/audio_worklet_processor.cc


### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/32bfec158a82ae94fb62efdd5dc2cd616f7c0891

commit 32bfec158a82ae94fb62efdd5dc2cd616f7c0891
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Jun 16 12:57:57 2021

[M90-LTS] Return false when the size of audio_port_1 and audio_port_2 is different

The current code assumes the size of audio ports is identical because
the number of inputs and outputs cannot change after construction. This
assumption is broken when multiple AudioWorkletNodes share a singleton
AudioWorkletProcessor instance.

This patch removes the assumption and explicitly returns false when the
number of inputs and outputs does not match.

(cherry picked from commit f1e277f1b586e0be0cc7f3b4f6462fa4982b7b49)

(cherry picked from commit bce03b43e222a2e659809ae909674a242bdccdde)

Bug: 1201033, 120260
Test: 3 repro cases submitted do not crash on ASAN.
Change-Id: I4065e7970b9b7b54468fc82558509a3238ff28e4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2875846
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#879631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2885639
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#935}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2961288
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1525}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/32bfec158a82ae94fb62efdd5dc2cd616f7c0891/third_party/blink/renderer/modules/webaudio/audio_worklet_processor.cc


### vs...@google.com (2021-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-09-22)

Hello- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1201033?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1202060]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055614)*
