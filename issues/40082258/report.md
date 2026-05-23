# Web MIDI performance crashes chrome canary

| Field | Value |
|-------|-------|
| **Issue ID** | [40082258](https://issues.chromium.org/issues/40082258) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebMIDI |
| **Platforms** | Windows |
| **Reporter** | j....@netcologne.de |
| **Assignee** | to...@chromium.org |
| **Created** | 2015-06-11 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2429.0 Safari/537.36

Steps to reproduce the problem:
1. Load the URL:http://james-ingram-act-two.de/open-source/assistantPerformer/assistantPerformer.html 
2. Select the score "Song Six (scroll) - annotated" from the drop-down menu in the middle.
3. Select "Microsoft GS Wavetable Synth" from the drop-down menu on the right  
3. Click the "Start" button that appears. The score appears with controls along the top.
4. Click the green Go button.

What is the expected behavior?
The score starts playing. A running marker appears, synchronized with the sound. Using the Microsoft Synth means that the sounds being heard are not those for which the score was designed -- but that is irrelevant here.

What went wrong?
Chrome crashes before the end of the score is reached.
It has crashed a couple of times near the end of bar 92, and sometimes earlier.

Crashed report ID: af79a3e1026c98a0, 27d156cbfecd46e2, e0f29462b8e52224, 4f8a273c3ea1a731, 75aa2a0add982d3a

How much crashed? Whole browser

Is it a problem with a plugin? No 

Did this work before? Yes It was working on 22. Jan 2014 when I made an mp3 recording of the piece. Possibly later too. It has never worked in Chrome 43.

Chrome version: 45.0.2429.0  Channel: canary
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 18.0 r0

My system is currently as simple as possible. In particular, the VirtualMIDISynth is not installed.
This is a large score, and my application is slowly leaking memory (I can see that in the task manager, and I'm working on the problem). I think Chrome is crashing, without warning, when the tab runs out of memory.

## Attachments

- [499279.mov](attachments/499279.mov) (application/octet-stream, 4.7 MB)
- [Step3.png](attachments/Step3.png) (image/png, 112.7 KB)
- [TaskManager15.06.2015.png](attachments/TaskManager15.06.2015.png) (image/png, 41.3 KB)
- [Song Six-(scroll)-annotated_2015-06-15.mid](attachments/Song Six-(scroll)-annotated_2015-06-15.mid) (application/octet-stream, 1000.1 KB)
- [499279.png](attachments/499279.png) (image/png, 86.3 KB)
- [Song Six-(scroll)-annotated(fromBar92)_2015-06-16.mid](attachments/Song Six-(scroll)-annotated(fromBar92)_2015-06-16.mid) (application/octet-stream, 268.6 KB)
- [ShortCrashSample.png](attachments/ShortCrashSample.png) (image/png, 38.3 KB)
- [ShortCrashSample.mid](attachments/ShortCrashSample.mid) (application/octet-stream, 2.7 KB)
- [LongCrashSample.png](attachments/LongCrashSample.png) (image/png, 38.1 KB)
- [LongCrashSample.mid](attachments/LongCrashSample.mid) (application/octet-stream, 30.5 KB)
- [penultimateChordBar92Channel2.png](attachments/penultimateChordBar92Channel2.png) (image/png, 38.7 KB)
- [penultimateChordBar92Channel2.mid](attachments/penultimateChordBar92Channel2.mid) (application/octet-stream, 119 B)
- [lastChordBar92Channel2.mid](attachments/lastChordBar92Channel2.mid) (application/octet-stream, 271 B)
- [lastTwoChordsBar92Channel2.png](attachments/lastTwoChordsBar92Channel2.png) (image/png, 38.6 KB)
- [lastTwoChordsBar92Channel2.mid](attachments/lastTwoChordsBar92Channel2.mid) (application/octet-stream, 362 B)
- [lastChordBar92Channel2.png](attachments/lastChordBar92Channel2.png) (image/png, 38.5 KB)

## Timeline

### pb...@chromium.org (2015-06-11)

Able to reproduce the issue on current Chrome Canary 45.0.2429.0,stable(43.0.2357.124) and Beta(44.0.2403.39) channel too on Win7, Win8.1

### rn...@chromium.org (2015-06-12)

@j.ingram: Unable to perform the Step 3 from the description, it is not displaying any options from the drop-down menu on the right.

Screen-recording is attached.

Could you please provide us URL which shows the options in the Step 3 to repro this issue from our end.

Thank you.

### j....@netcologne.de (2015-06-12)

Hi you seem to be on a Mac. The Microsoft GS Wavetable Synth is part of Windows.

I know that Macs have a similar default output device (its part of Quicktime), but I think it needs to be configured somehow. I'm not sure of the details -- but would really like to publish them on my web site! :-)

I think you will probably be able to reproduce the bug on a Mac, if you first set it up so that its default MIDI output device appears in the output device list.

Here's a screenshot showing step 3 on my system. The TS22 PCI MIDI is a hardware sound card.  

### tk...@chromium.org (2015-06-15)

[Empty comment from Monorail migration]

### to...@chromium.org (2015-06-15)

Three of the first five crash reports happen inside wdmaud.drv.

pbommana@
Can you take a crash ID on your case?

### j....@netcologne.de (2015-06-15)

I've been revising the local copy of my file
        ap/Sequence.js

That, if anywhere, is where I must be leaking memory.
There was some redundant code there, left over from previous versions of this application, but that has now been removed.

The simplification made no difference to the crash, which still happens as before.

To test where the memory leaks were happening, I then ran the performance with various lines commented out while watching the task manager.

A recording of the performance is being made in line 338:
        sequenceRecording.trackRecordings[currentMoment.messages[0].channel()].addLiveScoreMoment(currentMoment);
so that was the first line to be commented out. Memory is, of course, required for saving the growing recording.

With that done, I then commented out all calls to outputDevice.send(messageData, timeStamp).
The task manager now reports that memory is no longer leaking, and the score runs (silently) to completion. It seems to make no difference, whether I send a timestamp or not.

The performance also completes (silently) if I restore line 338, but then, of course, memory usage increases during the performance.

So the crash seems to be due to memory leaks on chrome's side of outputDevice.send(messageData, timeStamp).

I've committed the latest version of my ap/Sequence.js to my GitHub repository [1], but not yet to the URL we are testing.
Would you like me to upload the new, simplified, ap/Sequence.js to the URL we are testing?

[1] https://github.com/notator/assistant-performer

### to...@gmail.com (2015-06-15)

James:

It looks crashing inside the GS Wavetable Synth. Can you play back the song on another MIDI application with the GS Wavetable Synth?

Also, can you provide a minimized code that reproduce the issue?
It would be nice if it crashes in short time, and the page does not contain SVG graphics.

### j....@netcologne.de (2015-06-15)

I've now re-installed the VirtualMIDISynth.

At the first attempt to play Song Six with the VMS, Chrome froze after about 6 seconds, but with no crash report.
At the second attempt, the performance completed correctly, except for a moment where some notes hung for a short time. Probably some NoteOffs weren't sent for some reason.

There seemed to be the same memory leak as before: After a time, the memory in use seems to increment regularly at one second intervals. I ended up using much more memory in the tab than I've ever seen before, but there was no crash. See screen shot of the task manager at the completion of this performance.
Maybe its not just a memory leak after all?

I know that the graphics are not leaking. I've tried turning off the running cursor.

It should be quite easy to write a test without any graphics. Just make an long loop that sends a midi message every 2 milliseconds or so. I'll see what I can do.  

### j....@netcologne.de (2015-06-15)

@toyoshim: you asked
"Can you play back the song on another MIDI application with the GS Wavetable Synth?"

The 'save' button, which appears among the controls when an Assistant Performer performance ends, is supposed to save the performance as a Standard MIDI File.
So I tried using it to save a performance of Song Six on Chrome+VMS.
Rather to my surprise, it actually worked! :-) I haven't used/tested saving for some time...
I attach the resulting SMF file. [1]

Windows Media Player plays this SMF to its end on the VirtualMIDISynth, but crashes at the beginning of bar 93 when playing on the Microsoft GS Wavetable Synth.(That is where it has often crashed in previous tests using the MSGSSynth.)
Could it be that the MSGSSynth is leaking memory? Maybe it just wasn't built for this rate of data input. I suspect, however, that this is a memory problem, since the MSGSSynth plays Study 2 and other, shorter scores without any problem - even though the data rate is just as high.

Could you try the playing the score (and/or SMF) on a Mac?

[1] This SMF needs treating with caution. It was created using _my_, possibly buggy/optimisable, code for creating SMFs...  :-)
Playing the SMF back on WMP+VMS (with the correct SoundFont) does _not_ sound exactly like the original performance, as it should. The timing seems a bit wrong (the word samples are getting clipped slightly, and there are occasional mixups, as if data is getting lost). The performance does not, however, crash. Most of the score, including the final bars, sound more or less as they should (on WMP+VMS)!





 

### to...@chromium.org (2015-06-16)

Marked as Restrict-View-Google just in case for potential security risk.

### to...@chromium.org (2015-06-16)

For memory, these crashes are not for out of memory. It isn't easy to observe memory leak in the system using GC. I guess you just see the sending ArrayBuffer data are collected lazily since they are passed outside the local scope.

### tk...@chromium.org (2015-06-16)

Able to repro the issue on win8 chrome version 45.0.2433.0 canary,44.0.2403.39 and 43.0.2357.124	 - crashed with crash Ids 423ef2f57011d68b 423ef2f57011d68b 

Previous builds from M40 displayed the empty drop downs as shown in the screenshot
Hence removing the Needs-Bisect label for now. Plaese feel free to tag the label if needed.

Stack Trace:
Thread 2 CRASHED [EXCEPTION_ACCESS_VIOLATION_WRITE @ 0x00000000 ]MAGIC SIGNATURE THREAD
0x00007ffba9997eaf	[nvwgf2umx.dll + 0x00ac7eaf ]	
0x00007ffba937653f	[nvwgf2umx.dll + 0x004a653f ]





### to...@chromium.org (2015-06-16)

tkonchada:
Thanks.

We launched this feature at M43. If you want to try it with previous versions, you need to enable the feature from chrome://flags/#enable-web-midi. But, yes, this won't need bisect.

### j....@netcologne.de (2015-06-16)

The bug can be reproduced more quickly by doing steps 1-4 as before:
1. Load the URL:http://james-ingram-act-two.de/open-source/assistantPerformer/assistantPerformer.html 
2. Select the score "Song Six (scroll) - annotated" from the drop-down menu in the middle.
3. Select "Microsoft GS Wavetable Synth" from the drop-down menu on the right  
4. Click the "Start" button that appears. The score appears with controls along the top.
Then:
5. Scroll down to bar 92.
6. Select the Set Start tool (Click the button with the vertical green bar)
7. Click on the score near the first chord in the top staff in bar 92.
8. Unselect the Set Start tool, by clicking on its button again.
9. Click the Go button.

The MSGSSynth crashes as before. Sometimes at the beginning of bar 93, sometimes later.
The VirtualMIDISynth does not crash, but plays correctly to the end of the score.

Crash IDs: 678300812c2d27ef, 4316655452d5c250




### j....@netcologne.de (2015-06-16)

Attached is a new SMF containing the VirtualMIDISynth's performance from bar 92 to the end of the piece.
Windows Media Player has no problem playing this SMF on the VirtualMIIDISynth, but crashes when using the MSGSSynth. The crashes dont happen where they do when using Chrome to play the MSGSSynth.

### to...@chromium.org (2015-06-16)

I'm asking security team since this could be serious security issue not only on Chrome, but also on all Windows application.
Please do not discuss this problem in public for a while.

### to...@chromium.org (2015-06-16)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-06-16)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-06-16)

Punting this to the security queue. This looks like a heap corruption in the browser process accessible from the open web.

### pb...@chromium.org (2015-06-16)

toyoshim@  Please find the crash_id and stack trace which I got from my machine :

Crash_id : ede9c1c7e7835d10

Stack Trace :
Thread 44 CRASHED [EXCEPTION_ACCESS_VIOLATION_READ @ 0x0000013f000000f1 ]MAGIC SIGNATURE THREAD
0x000007fef83a2e41	[winmm.dll + 0x00002e41 ]	ValidateHandle
0x000007fef83bd0cd	[winmm.dll + 0x0001d0cd ]	midiOutShortMsg
0x000007fedd882682	[chrome.dll -midi_manager_win.cc:931 ]	media::midi::`anonymous namespace'::MidiServiceWinImpl::SendOnSenderThread(unsigned int,unsigned __int64,std::vector<unsigned char,std::allocator<unsigned char> > const &,base::TimeTicks)
0x000007fedd881ec6	[chrome.dll -bind_internal.h:346 ]	base::internal::Invoker<base::IndexSequence<0,1,2,3,4>,base::internal::BindState<base::internal::RunnableAdapter<void ( media::midi::`anonymous namespace'::MidiServiceWinImpl::*)(unsigned int,unsigned __int64,std::vector<unsigned char,std::allocator<unsigned char> > const &,base::TimeTicks)>,void ,base::internal::TypeList<base::internal::UnretainedWrapper<media::midi::`anonymous namespace'::MidiServiceWinImpl>,unsigned int,unsigned __int64,std::vector<unsigned char,std::allocator<unsigned char> >,base::TimeTicks> >,base::internal::TypeList<base::internal::UnwrapTraits<base::internal::UnretainedWrapper<media::midi::`anonymous namespace'::MidiServiceWinImpl> >,base::internal::UnwrapTraits<unsigned int>,base::internal::UnwrapTraits<unsigned __int64>,base::internal::UnwrapTraits<std::vector<unsigned char,std::allocator<unsigned char> > >,base::internal::UnwrapTraits<base::TimeTicks> >,base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void ( media::midi::`anonymous namespace'::MidiServiceWinImpl::*)(unsigned int,unsigned __int64,std::vector<unsigned char,std::allocator<unsigned char> > const &,base::TimeTicks)>,base::internal::TypeList<media::midi::`anonymous namespace'::MidiServiceWinImpl *,unsigned int const &,unsigned __int64 const &,std::vector<unsigned char,std::allocator<unsigned char> > const &,base::TimeTicks const &> >,void >::Run(base::internal::BindStateBase *)
0x000007fedbb6cba9	[chrome.dll -task_annotator.cc:62 ]	base::debug::TaskAnnotator::RunTask(char const *,char const *,base::PendingTask const &)
0x000007fedbb08e38	[chrome.dll -message_loop.cc:459 ]	base::MessageLoop::RunTask(base::PendingTask const &)
0x000007fedbb098d0	[chrome.dll -message_loop.cc:580 ]	base::MessageLoop::DoWork()
0x000007fedbb69c4d	[chrome.dll -message_pump_default.cc:34 ]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x000007fedbb089e9	[chrome.dll -message_loop.cc:424 ]	base::MessageLoop::RunHandler()
0x000007fedbb441fd	[chrome.dll -run_loop.cc:55 ]	base::RunLoop::Run()
0x000007fedbb082b5	[chrome.dll -message_loop.cc:286 ]	base::MessageLoop::Run()
0x000007fedbb31472	[chrome.dll -thread.cc:251 ]	base::Thread::ThreadMain()
0x000007fedbb469ba	[chrome.dll -platform_thread_win.cc:78 ]	base::`anonymous namespace'::ThreadFunc(void *)
0x772559ec	[kernel32.dll + 0x000159ec ]	BaseThreadInitThunk
0x7738c540	[ntdll.dll + 0x0002c540 ]	RtlUserThreadStart

### cl...@chromium.org (2015-06-16)

[Empty comment from Monorail migration]

### fo...@chromium.org (2015-06-16)

With the .mid from #15 the crash is pretty much reliably inside wdmaud.drv with wmplayer as well as in my build of Chrome so I think it's pretty good chance it isn't a specific issue with Chrome's usage of the APIs but a probable bug in the MS Synth. 

From the crash it tends to manifest as a OOB read, over the end of a heap allocation but I've also seem it kill the process due to "terminate on heap corruption" so could be fairly bad. This might be something which needs sending to MS, but before that we might need to try and reduce the MIDI file down to the absolute minimum necessary to reproduce.

Crash from windbg/wmplayer on Win8.1 32 bit, similar exhibited in my Chrome and on 64 bit platforms:

0:024> r
eax=6f27fa4a ebx=00fdd500 ecx=0000021a edx=00000002 esi=09b768ee edi=0006f27f
eip=71a0e749 esp=0908f6d8 ebp=0908f72c iopl=0         nv up ei pl nz na po cy
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010203
wdmaud!CDigitalAudio::Mix16X+0x117:
71a0e749 0f6e3e          movd    mm7,dword ptr [esi]  ds:0023:09b768ee=????????
0:024> kb
ChildEBP RetAddr  Args to Child              
0908f72c 71a24803 00000520 00000004 00000000 wdmaud!CDigitalAudio::Mix16X+0x117
0908f818 71a2503a 0908f85c 00000001 00000001 wdmaud!CDigitalAudio::Mix+0x420
0908fa44 71a20f94 0908fae8 00000001 0000089d wdmaud!CVoice::Mix+0x577
0908fa8c 71a1ffc8 0908fae8 0908fac4 0908facc wdmaud!CSynth::Mix+0x127
0908fadc 71a20603 087acf88 09ae4bb0 0000089d wdmaud!CUserModeSynth::Render+0x88
0908fb2c 71a206b8 71a206a0 0908fb74 76f37fb0 wdmaud!CDSLink::SynthProc+0x97
0908fb38 76f37fb0 09ae4b40 987ba5d2 76f380b0 wdmaud!CDSLink::SynthThread+0x18
0908fb74 76f380f5 0908fb90 770c4198 04985700 msvcrt!_callthreadstartex+0x25
0908fb7c 770c4198 04985700 770c4170 999be4db msvcrt!_threadstartex+0x61
0908fb90 779732b1 04985700 9923ffe7 00000000 KERNEL32!BaseThreadInitThunk+0x24
0908fbd8 7797327f ffffffff 7799f077 00000000 ntdll!__RtlUserThreadStart+0x2b
0908fbe8 00000000 76f380b0 04985700 00000000 ntdll!_RtlUserThreadStart+0x1b


### j....@netcologne.de (2015-06-17)

Attached are two screenshots and two corresponding Standard MIDI files.

ShortCrashSample.png shows the really problematic section of the score.
ShortCrashSample.mid is a recording of this section, made using my Standard MIDI File writer (with the VirtualMIDISynth).

Here, the crashes don't always happen the first time the samples are played, but always happen after a couple of runs. The behaviour is similar in both Chrome (using the score) and in Windows Media Player (using the MIDI file).

Crash IDs 1cb6a98aaeda9ac1, 567b481a6d6f4933

There is similar behaviour if I just play the second half of bar 92.

The crash *always* seems to happen first time if the whole of bar 92 is played.
LongCrashSample.png
LongCrashSample.mid

Crash IDs: b4c42b13eb4c334a, 15bbefb38a757421

Both MIDI files play without a problem using Windows Media Player and the VirtualMIDSynth.

### wf...@chromium.org (2015-06-17)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-06-17)

marking as P0 as this is a memory corruption in the browser process with no user interaction.

### wf...@chromium.org (2015-06-17)

cwilso -> can you take a look at this.  in particular, are there any mitigations we can put in place to prevent this type of vulnerability being exposed to the web?

### yu...@chromium.org (2015-06-17)

Possible mitigations are:

A. Ban "Microsoft GS Wavetable Synth" in the browser process.  My current understanding is that we can reliably detect whether the target MIDI output is "Microsoft GS Wavetable Synth" or not.  Here is my related commit.
  https://code.google.com/p/chromium/issues/detail?id=472341#c1
Blacklisting that MIDI device in the browser process would be the easiest mitigation.

B. Ban certain MIDI stream pattern in the browser process.  If there was a chance that we could fail to detect whether the target MIDI output is "Microsoft GS Wavetable Synth" or not, alternatively we can ban certain MIDI stream pattern in the browser process before the stream date is passed to the OS (then the driver).
The best place to do that is probably media/midi/midi_message_queue.cc.
https://chromium.googlesource.com/chromium/src/+/78b9d632216a85390766a1fa04f321954e4a1da2/media/midi/midi_message_queue.cc




### cl...@chromium.org (2015-06-17)

[Empty comment from Monorail migration]

### cw...@chromium.org (2015-06-17)

I think the first mitigation (Ban the GS wavetable synth) is a reasonable one unless we can identify why it's crashing.  My guess is the GS synth is simply flaky; we'll probably need to delegate to Microsoft.

### to...@chromium.org (2015-06-18)

Yep, +1 to ban the GS synth for now.

It would not be easy to strip the malicious sequence since the pattern would depend on the internal states of GS synth since MIDI is just a event data stream that triggers internal complicated sound synthesis.

For other platforms, e.g., Core MIDI service on OS X, we do not support software MIDI so to avoid such a problem. But we didn't on Windows because the API does not provide a scheme to detect device type, e.g., hardware vs software emulated.

I'll take the ownership to prepare a patch to ban it.

Security team: Can you report this problem to Microsoft in proper way?

### yu...@chromium.org (2015-06-18)

Re #30:
> But we didn't on Windows because the API does not provide a scheme to detect device type, e.g., hardware vs software emulated.

Just for your reference, perhaps we might be able to use MOD_SWSYNTH or KSMUSIC_TECHNOLOGY_SWSYNTH to ban all the software synth MIDI devices that report themselves software synth correctly.
- https://msdn.microsoft.com/en-us/library/windows/hardware/ff537580.aspx
- https://msdn.microsoft.com/en-us/library/windows/desktop/dd798467.aspx



### to...@chromium.org (2015-06-18)

+yhirano@ for review.
patch under the review is here; https://codereview.chromium.org/1178793007/

#31
Permanently disabling all software synths would be controversial. But could be a solution.

We will have some choice.

1) Support all synths, but all software synths should run in a separate process.
2) Support "Microsoft GS Wavetable Synth" once this critical bug is fixed. But this is the only software synth we support, and ban others.
3) Ban all software synths.

But, we may want to file a separate bug to discuss it?

### bu...@chromium.org (2015-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/133b995ac61440832fe1b91d2180eb0da182aced

commit 133b995ac61440832fe1b91d2180eb0da182aced
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Thu Jun 18 05:12:28 2015

Web MIDI: disable unsupported devices on Windows

BUG=499279
R=yukawa@chromium.org

Review URL: https://codereview.chromium.org/1178793007.

Cr-Commit-Position: refs/heads/master@{#334994}

[modify] http://crrev.com/133b995ac61440832fe1b91d2180eb0da182aced/media/midi/midi_manager_win.cc


### to...@chromium.org (2015-06-18)

Set merge requests for all branches. It isn't usual way, but did it at once since this is p0. If it does not work, let me know.

### to...@chromium.org (2015-06-18)

oops, request for 45 is not needed.

### cl...@chromium.org (2015-06-18)

[Empty comment from Monorail migration]

### j....@netcologne.de (2015-06-18)

I've been looking at the score's XML to see if I did something I shouldn't have in the critical section.

The MIDI definition for the final chord in staff 3 (=channel 2) of bar 92 (~7) is:
           <score:midiChord
               pitchWheelDeviation="101">
              <basicChords>
                <basicChord
                   msDuration="34"
                   patch="74"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="49"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="47"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="50"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="50"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="50"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="47"
                   pitches="92 100"
                   velocities="36 36" />
              </basicChords>
              <sliders
                 pitchWheel="64 64 100 64"
                 pan="107" />
            </score:midiChord>

The pitch bend range (pitchWheelDeviation) is being set to 101 semitones, and there is a pitch Wheel envelope (in the <sliders>) having a peak at 100, which takes the pitch into astronomical heights.
There are lots of pitchWheelDeviation settings earlier in the score, but nothing quite so extreme.

I suspect that the MS Synth is failing to cope with this situation.

Hope that helps,
James

### to...@chromium.org (2015-06-18)

James, thank you for looking details. Can you create a minimized SMF file that can make WMP crash with minimum MIDI messages?

### j....@netcologne.de (2015-06-18)

Its the combination of the last two chords in channel 2 (staff3) that crashes.
Attached are the last two chords, separately and together. I have been unable to get either of the separate chords to crash the MS Synth, even after multiple runs.

The combination (lastTwoChordsBar92Channel2.mid) crashes WMP immediately.

The penultimate chord's MIDI XML looks like this:
             <score:midiChord
               pitchWheelDeviation="100">
              <basicChords>
                <basicChord
                   msDuration="65"
                   patch="117"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="74"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="75"
                   pitches="92 100"
                   velocities="36 36" />
                <basicChord
                   msDuration="61"
                   pitches="92 100"
                   velocities="36 36" />
              </basicChords>
              <sliders
                 pan="107" />
            </score:midiChord>

The pitchWheelDeviation is being set, but there is no pitchWheel envelope in the sliders (!).


### to...@chromium.org (2015-06-18)

Thanks! It's surprising that such a small MIDI sequence can crash it, and it has not been found for a long time.

Security team: Can you send lastTwoChordsBar92Channel2.mid to Microsoft for further investigation?

### wf...@chromium.org (2015-06-18)

yes - forshaw@ will handle the disclosure to microsoft via project zero channels, giving credit to j.ingram@netcologne.de (please confirm you wish to be credited for this).

I still think there is a risk to the exposure of other MIDI drivers here - I like the suggestions in #32 but have we also considered a permission prompt similar to geolocation?  Adding Security-UX tag for more input on this.

### j....@netcologne.de (2015-06-18)

Giving me credit is fine. :-)

Apropos the suggestions in #32: I think it would be a disaster if all software Synths were banned. We are trying to put MIDI on the web, and want websites to work even if their users have no MIDI hardware attached.

Obviously this whole subject needs discussing more fully. Probably at the Web MIDI API GitHub site. There's the beginnings of such a discussion in
https://github.com/WebAudio/web-midi-api/issues/124

I don't understand: "a permssion prompt similar to geolocation".

I suspect that software synths are going to have to be vetted somehow...

All the best,
James

### fo...@chromium.org (2015-06-18)

Okay I've sent the example MIDI off to MS with a basic write up of the issue. Let's see whether they feel it's a security or a reliability issue. 


### ti...@google.com (2015-06-18)

+laforge@ for M-43
+pennymac for M-44

@#34 - For critical bugs, we ask for at least 24 hours on trunk before merging to beta or stable.

@laforge - I understand that you have a release of M43 cutting today at 4PM. Can we sneak this in?




### fo...@chromium.org (2015-06-18)

Also for information the link to the Project Zero tracker for this issue is https://code.google.com/p/google-security-research/issues/detail?id=454. Note that this is under the standard PZ 90 day disclosure deadline. 

### ti...@google.com (2015-06-18)

@j.ingram - what name would you like to use for credit in our release notes? We'll go with "James Ingram" unless you let us know otherwise.

### la...@google.com (2015-06-18)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-06-18)

Re #32: Another option is to allow software synths, but move this API behind a chooser where the user is asked to choose which MIDI output device to connect to. When we did the security review I was told that users would have to have a physical device plugged in which would be rare, so it seemed like a very low risk API that didn't need a permission. We should probably consider that given the fact that software synths are allowed and provided by default on some OSes.

### ti...@google.com (2015-06-18)

asked pennymac@ via chat to approve the beta merge.

wfh@ - Providing that pennymac approves, please merge to both beta (2403) and stable (2357). Merging to stable first is okay in the circumstances due to the pending stable branch cut. I'll be accountable to making sure this ends up in beta if you don't get an approval to merge to beta.

### pe...@chromium.org (2015-06-18)

Yup.  M44 branch 2403.

### bu...@chromium.org (2015-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/953b7b015a2c283057c539a447816aeed56b2d99

commit 953b7b015a2c283057c539a447816aeed56b2d99
Author: Will Harris <wfh@chromium.org>
Date: Thu Jun 18 18:09:12 2015

Merge M44: Web MIDI: disable unsupported devices on Windows

BUG=499279
R=yukawa@chromium.org

Review URL: https://codereview.chromium.org/1178793007.

Cr-Commit-Position: refs/heads/master@{#334994}
(cherry picked from commit 133b995ac61440832fe1b91d2180eb0da182aced)

Review URL: https://codereview.chromium.org/1189113003.

Cr-Commit-Position: refs/branch-heads/2403@{#350}
Cr-Branched-From: f54b8097a9c45ed4ad308133d49f05325d6c5070-refs/heads/master@{#330231}

[modify] http://crrev.com/953b7b015a2c283057c539a447816aeed56b2d99/media/midi/midi_manager_win.cc


### bu...@chromium.org (2015-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b30110acb142ab5f2d57b85cdf8dcde32d2ce022

commit b30110acb142ab5f2d57b85cdf8dcde32d2ce022
Author: Will Harris <wfh@chromium.org>
Date: Thu Jun 18 18:14:40 2015

Merge M43: Web MIDI: disable unsupported devices on Windows

BUG=499279
R=yukawa@chromium.org

Review URL: https://codereview.chromium.org/1178793007.

Cr-Commit-Position: refs/heads/master@{#334994}
(cherry picked from commit 133b995ac61440832fe1b91d2180eb0da182aced)

Review URL: https://codereview.chromium.org/1182913007.

Cr-Commit-Position: refs/branch-heads/2357@{#476}
Cr-Branched-From: 59d4494849b405682265ed5d3f5164573b9a939b-refs/heads/master@{#323860}

[modify] http://crrev.com/b30110acb142ab5f2d57b85cdf8dcde32d2ce022/media/midi/midi_manager_win.cc


### ti...@google.com (2015-06-18)

Great - thanks wfh!

@toyoshim: thanks for the quick patch and testing in https://codereview.chromium.org/1178793007#msg2 . This should ship with the next update to stable.

### j....@netcologne.de (2015-06-18)

@timwil... in #46 'James Ingram' is fine thanks.

@f... in #48: I can imagine other options (maybe this discussion belongs somewhere else):
Ideally, I would like there to be an online software MIDI output device, stored next to my application, into which I (as website author) could load sounds of my own choosing. The Assistant Performer application would not then give the user a choice of software synths, it would simply target the exact sounds the score is designed for. In other words, the software synth would be invisible to the user. Presumably, in that scenario, the whole application would have to ask the user for enhanced permission. Is there some way that I, as an application developer, can ask for such permission for my application?


### fe...@chromium.org (2015-06-18)

toyoshim, do you want to start a separate bug to discuss what we can do about this moving forwards? I don't know enough about MIDI & the needs of MIDI developers to move the discussion along.

### to...@chromium.org (2015-06-19)

https://code.google.com/p/chromium/issues/detail?id=502127

Here is a new thread for the topic, how to handle native software synths in the Web MIDI.

### to...@chromium.org (2015-06-19)

Thank you for your helps to merge this to stable and beta.

#41 wfh:
We show a prompt when JavaScript requests using privilege operations over the Web API. But now, the problem happens in a non-privilege operations. Maybe we have two choses. 1) Prompt always, 2) Add an option to request using software synths, then prompt for it. Let me discuss it at crbug.com/502127.

#48 felt:
The Web MIDI API is not an API to playback a song with one synth, but an API to allow communicating with all connected music devices. So the chooser idea does not match with the API model, and prompt would match well.

I relied to questions asked in this bug. But let's use the new bug crbug.com/502127 if you have thoughts on this topic.

Thanks.

### bu...@chromium.org (2015-06-19)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/953b7b015a2c283057c539a447816aeed56b2d99

commit 953b7b015a2c283057c539a447816aeed56b2d99
Author: Will Harris <wfh@chromium.org>
Date: Thu Jun 18 18:09:12 2015


### pb...@chromium.org (2015-06-19)

Verified the issue using latest Chrome stable i.e.,  where the option "Microsoft GS Wavetable Synth" is not available as expected, checked on Win7 and 8.1.

Marking the bug as verified.

### ti...@google.com (2015-06-19)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-19)

Note that although this fix will ship in the next stable release, I won't add this bug to the release notes until we hear back from Microsoft (which means that your acknowledgement for reporting this bug will likely go out with Chrome version 44).

I'll assign a CVE for tracking on our end.

### to...@chromium.org (2015-06-24)

Security team:
This is very sad, but James disclosed this security incident in public.
https://github.com/WebAudio/web-midi-api/issues/151

### in...@chromium.org (2015-06-24)

[Empty comment from Monorail migration]

### j....@netcologne.de (2015-06-24)

[Comment Deleted]

### j....@netcologne.de (2015-06-24)

[Comment Deleted]

### in...@chromium.org (2015-06-24)

---- Sorry, shall I delete it?

Please mark it private or delete it for now. This is a critical severity bug, not yet shipped to users. We would appreciate you holding on this until we release a fix to all of our users.

### j....@netcologne.de (2015-06-24)

I've deleted the text, but can't see how to delete the issue itself, which was my answer to the thread in GitHub issue #150.

The text originally in https://github.com/WebAudio/web-midi-api/issues/151 was as follows:

========================================================
Recent developments mean that web app authors, like myself, urgently need to be able to use web-based softsynths as output devices. (See 'Background:' below.)
IMHO, this issue is crucial to the continued use of the Web MIDI API on the web, and its solution should have a high priority.

As we now realize, there is no way to be certain that a softsynth won't crash.

In #150, @toyoshim said:
>The best design to save the browser from software synths' crashes is that browser launches an isolated service process to host software synths, and just communicates with it to control synths. Under this design, if the service process crashes, the browser could restart it.

It would be useful if the browser could send an exception to the host web app if/when the softsynth crashes. That's not absolutely necessary, but would be helpful while developing the app. Would that be possible?

----
Background:
Recently, I discovered that a particular sequence of MIDI messages sent to the Microsoft GS Wavetable Synth (part of the Windows OS), would cause it to crash in such a way as to crash Chrome.
This has led to the realization that all software synthesizers are a potential security problem, and to proposal #150: Add softwaresynth to MIDIOptions to prompt for user permissions.

It now looks as if it may be impossible to use OS-based softsynths safely (i.e. in a way that is guaranteed not to crash the browser), so their use may have to be disallowed permanently by the Web MIDI API.

My web app sends MIDI messages to a MIDI output device, and I want it to work without its users having to install any special hardware or additional software. If OS-based softsynths are not allowed, then the app has no choice (on the web) but to send its MIDI messages to a web-based software synth. That would be a better solution anyway, since the app would then work on _any_ operating system, and I would get to choose which softsynth the app should use (so have greater control over the sounds being produced).

----
This issue relates to #45, #124,  #150
==========================================================================-


Should I open this issue here instead?

### wf...@chromium.org (2015-06-24)

Thanks for deleting the post, did you link to the midi file that was causing the crash? Do you know how many people might have downloadded it?

The midi fix to block MS software synth actually went out in 43.0.2357.130 which was on Monday 22 June, but would not have reached all of our users yet and was not in the release notes.  The VRP rules [1] specifies that rewards may be ineligible if the vulnerability is disclosed early.

The VRP panel will make a determination when we decide the next set of rewards whether this disclosure will preclude a reward from happening.

[1] https://www.google.com/about/appsecurity/chrome-rewards/index.html

### j....@netcologne.de (2015-06-24)

[Comment Deleted]

### j....@netcologne.de (2015-06-24)

No, I didn't say anything about the specific file or where to find the critical chords in it.

I think it very unlikely that anyone should have downloaded the score. Its difficult to access, except via my app, and it can't be downloaded from there. Also, its not possible to have saved a Standard MIDI File of the piece without sitting through a performance of the whole piece using a third party MIDI output device and then hitting the Save button. Highly unlikely, I think.

I have now made the score temporarily inaccessible from my app. When it goes back, the offending chords will have been changed/corrected.

### to...@chromium.org (2015-06-25)

I got another crash report from a security bounty hunter who got CVE prize sometimes, and the crash in the report happened at the James's site. So people who are interested in security bugs had monitored this thread before we marked this as restrict-view-*, and knew the magic sequence.

So, we should not say "we found a serious bug on MS synth" in public as possible. If an attacker is interested in this, he could find the sequence by running random stress test. The sequence could cause crashes on IE and other applications that contain IE's rendering engine, e.g., Outlook. Also Flash, Java applet, silverlight, and so on could have the same risk, IIUC. Off course, Firefox with Jazz plugin have the same issue. This is not a problem only for Chrome.

### j....@netcologne.de (2015-06-26)

I'm going away from my computer for a while tomorrow, so I took some more precautions yesterday, just in case:

1. The score at
http://james-ingram-act-two.de/compositions/songSix/setting1Score/Song%20Six.html
has been re-compiled so that its chords no longer contain MIDI information. (The link provides a recording of the piece made using the VirtualMIDISynth, a custom SoundFont and Audacity.)

2. I completely deleted all other copies of the score from my site. There is now no way at all to access them there.

Its interesting to note that Song Six was online and playable by the MS Synth for over a year (on both Chrome and Firefox) and nobody reported a problem. My traffic is just not very high. :-)

Best wishes with the Web MIDI API spec and implementation!
James

### wf...@chromium.org (2015-09-17)

https://code.google.com/p/google-security-research/issues/detail?id=454 was the tracking bug for reporting this vulnerability to Microsoft.

They have since replied and confirmed that this is a denial of service only, so no further action is required on this bug.

### j....@netcologne.de (2015-09-17)

I can still crash the Microsoft Synth (on an up-to-date Windows 10), so can verify that the bug has not been fixed.

Since Microsoft thinks its all right to use it in this state with WMP, and seem to think that the bug is not exploitable, can you reconsider the descision to ban the Synth from Chrome?

### wf...@chromium.org (2015-09-17)

The MS wavetable synth code is very old code and this denial of service crash is likely to be just the tip of the iceberg of potentially exploitable issues with it.

Given this, we simply cannot risk the safety of our users by allowing this code to be exposed on the open-web, unsandboxed from within the browser process. Therefore, I do not think we will be un-restricting this functionality for now.

If we have strong evidence that MS have done a significant clean up of the code based on the issue reported by Project Zero, we might reconsider this decision.

### cl...@chromium.org (2015-09-24)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-30)

We found some old bugs that weren't voted on and took them to the reward panel last week. This was one of them.

Our reward panel decided to award you $2,000 for this report. 

Our finance team should be in touch within 7 days. If that doesn't happen, please contact me directly at timwillis@

Thanks for your report!

### ti...@google.com (2016-06-30)

[Empty comment from Monorail migration]

### j....@netcologne.de (2016-06-30)

Wow! Thanks! :-)


### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### is...@google.com (2016-12-09)

This issue was migrated from crbug.com/chromium/499279?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/499654]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082258)*
