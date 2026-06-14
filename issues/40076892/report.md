# Heap-buffer-overflow in WebCore::AudioBufferSourceNode::process

| Field | Value |
|-------|-------|
| **Issue ID** | [40076892](https://issues.chromium.org/issues/40076892) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Media>Audio |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-01-29 |
| **Bounty** | $1,000.00 |

## Description


Repro-file as attachment.

Tested on:

OS: Ubuntu 12.04
Chromium: ASAN 26.0.1398.0 (Developer Build 179318)

Test case is little unstable, but should crash if you wait some time.

ASAN-report:

==22680== ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7ffed93c27c8 at pc 0x7ffeed080213 bp 0x7ffed7025190 sp 0x7ffed7025188
WRITE of size 8 at 0x7ffed93c27c8 thread T102 (AudioOutputDevic)
    #0 0x7ffeed080212 in WebCore::AudioBufferSourceNode::process(unsigned long) ???:0
    #1 0x7ffeec2132fc in WebCore::AudioNode::processIfNecessary(unsigned long) ???:0
    #2 0x7ffeec218fa9 in WebCore::AudioNodeOutput::pull(WebCore::AudioBus*, unsigned long) ???:0
    #3 0x7ffeed084077 in WebCore::AudioDestinationNode::render(WebCore::AudioBus*, WebCore::AudioBus*, unsigned long) ???:0
    #4 0x7ffeef59d77d in WebCore::AudioPullFIFO::consume(WebCore::AudioBus*, unsigned long) ???:0
    #5 0x7ffeef39e456 in WebCore::AudioDestinationChromium::render(WebKit::WebVector<float*> const&, WebKit::WebVector<float*> const&, unsigned long) ???:0
.
.
.
allocated by thread T0 (chrome) here:
    #0 0x7ffee89f85c2 in operator new[](unsigned long) ??:0
    #1 0x7ffeed08157a in WebCore::AudioBufferSourceNode::setBuffer(WebCore::AudioBuffer*) ???:0
    #2 0x7ffef162882f in WebCore::V8AudioBufferSourceNode::bufferAccessorSetter(v8::Local<v8::String>, v8::Local<v8::Value>, v8::AccessorInfo const&) ???:0
    #3 0x7ffeefb0c69d in v8::internal::JSObject::SetPropertyWithCallback(v8::internal::Object*, v8::internal::String*, v8::internal::Object*, v8::internal::JSObject*, v8::internal::StrictModeFlag) ???:0
    #4 0x7ffeefb167a0 in v8::internal::JSObject::SetPropertyForResult(v8::internal::LookupResult*, v8::internal::String*, v8::internal::Object*, PropertyAttributes, v8::internal::StrictModeFlag, v8::internal::JSReceiver::StoreFromKeyed) ???:0
    #5 0x7ffeefb0b3e8 in v8::internal::JSReceiver::SetProperty(v8::internal::String*, v8::internal::Object*, PropertyAttributes, v8::internal::StrictModeFlag, v8::internal::JSReceiver::StoreFromKeyed) ???:0
.
.
.


## Attachments

- [chrome-heap-buffer-overflow-WebCoreAudioBufferSourceNodeprocess-213.html](attachments/chrome-heap-buffer-overflow-WebCoreAudioBufferSourceNodeprocess-213.html) (text/html; charset=us-ascii, 2.4 KB)

## Timeline

### sc...@gmail.com (2013-01-29)

Good job @attekett!
You seem to have hit a little nest of issues :-)

### at...@gmail.com (2013-01-29)

Thanks. :D I'll try to dig out few more. ;)

### [Deleted User] (2013-01-31)

I suspect that the offending code is 

        for (unsigned i = 0; i < outputBus->numberOfChannels(); ++i)
            m_destinationChannels[i] = outputBus->channel(i)->mutableData();

It seems like if the AudioBus can have more channels than the AudioBuffer passed in to AudioBufferSourceNode::setBuffer().

I haven't been able to get this to repro yet on Windows but it seems fairly straight forward.

crogers and james.wei looks like this was added by you guys, please take a look.





### [Deleted User] (2013-01-31)

cdn, thanks for reporting this issue. 

in AudioBufferSourceNode:: setBuffer(), if the channel of the buffer is not equal to that of AudioBus, the AudioBus should be reconfigured to have the same channel as the buffer. 

        output(0)->setNumberOfChannels(numberOfChannels);

void AudioNodeOutput::updateInternalBus()
{
    if (numberOfChannels() == m_internalBus->numberOfChannels())
        return;

    m_internalBus = adoptPtr(new AudioBus(numberOfChannels(), AudioNode::ProcessingSizeInFrames));

    // This may later be changed in pull() to point to an in-place bus with the same number of channels.
    m_actualDestinationBus = m_internalBus.get();
}


I will try to reproduce this issue and investigate it. thanks 

### [Deleted User] (2013-01-31)

I think I found the root cause of this issue. 

when setting the buffer to the AudioBufferSourceNode, the AudioContext will try to update the AudioOutputs and so re-configure AudioBus before rendering. 

But it is possible that AudioContext may fail to get the lock of the graph and renderring will start. 

So the channel number of m_buffer changed, but the AudioBus not re-configured and has different number of Channels. 



### [Deleted User] (2013-01-31)

it is by design that:
1. the audio thread should not be blocked with regular block. 
2. tryLock in audio thread may fail. 
3. AudioBus re-configuration happens in audio thread pre-rendering stage. 

should we change the design or just return if channel mis-match detected when rendering? 

Chris, what's your opinion? 
thanks 


### [Deleted User] (2013-01-31)

Thanks James. I did finally get this to reproduce on windows also although it took leaving it running overnight with a conditional breakpoint in the loop which hits when i >= the size of the m_destinationChannels[]. 

I also filed an upstream bug https://bugs.webkit.org/show_bug.cgi?id=108515

### [Deleted User] (2013-01-31)

cdn, I can upload a patch to WebKit for review. but I am not authorized to access the bugzilla item. could you grant the access to me? my webkit accout is also james.wei@intel.com 

thanks 


### in...@chromium.org (2013-01-31)

James, cced you.

### [Deleted User] (2013-02-01)

inferno, thanks. I can access it now. 

### [Deleted User] (2013-02-01)

patch uploaded to webkit and cc croger and kbr for review. 


### [Deleted User] (2013-02-01)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-11)

Hey James,

I'm following up on all the open high-severity security bugs since Pwnium/Pwn2Own (http://blog.chromium.org/2013/01/show-off-your-security-skills-pwn2own.html) is just around the corner (we're using M25).

How's this one going?

### cr...@google.com (2013-02-12)

This should be resolved in WebKit:
https://bugs.webkit.org/show_bug.cgi?id=108515

### sc...@gmail.com (2013-02-12)

Committed r141851: <http://trac.webkit.org/changeset/141851>

Thanks!

### sc...@gmail.com (2013-02-20)

M25: http://trac.webkit.org/changeset/143516

### sc...@gmail.com (2013-03-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-02)

$1000 !

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### da...@chromium.org (2013-03-14)

I believe this is a similar problem to https://crbug.com/chromium/188559.

### [Deleted User] (2013-03-14)

@dalecurtis, could you grant the acces to issue #188559 to me? I can have a look at it. thansk  

### da...@chromium.org (2013-03-14)

Done.

### [Deleted User] (2013-03-14)

thanks

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### at...@gmail.com (2013-07-22)

Can this issue be opened to the public?

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/172926?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Media>Audio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076892)*
