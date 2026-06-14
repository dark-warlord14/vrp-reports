# Use-of-uninitialized-value in getNextNormalizedChar

| Field | Value |
|-------|-------|
| **Issue ID** | [40080867](https://issues.chromium.org/issues/40080867) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Editing, Blink>SVG, UI>Browser>FindInPage |
| **Reporter** | cl...@chromium.org |
| **Assignee** | js...@chromium.org |
| **Created** | 2014-11-17 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5449891764502528

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  getNextNormalizedChar
  ucol_prv_getSpecialCE_52
  ucol_IGetNextCE
  

Minimized Testcase (6.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Al_LEIYlSFNSfTBwMpVTrpg4-v_Wb0VVDpWWdk3MFE0EEobmwE5Lqcyiz9rUBJHMsWLhpkbq_w4KZqDQs5FSYvdJc1w-p0nZ1BKWNaoy1na6I6NaDctOFF5rXWQZatuMXtz-LInxjnDTQM3Tmh9Ojri_hyA

Filer: mbarbella

## Timeline

### mb...@chromium.org (2014-11-17)

This looks like an uninitialized pointer in icu. Could you take a look at this when you get a chance, jshin?

### mb...@chromium.org (2014-11-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-17)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-11-19)

Ok. I'll.

### js...@chromium.org (2014-11-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-11-19)

Hmm.. With an ASAN enabled build on Linux (64bit), I can't reproduce the problem with fuzz-88.html (minimized test case mentioned in https://crbug.com/chromium/433866#c0). 


For my record:

1. data in ucoll.cpp:2315 is of type |collIterate| defined in ucol_imp.h
   |fcdPosition|,  |pos| are two fields referenced.  

2. |collIterate| is a member of UCollationElement (defined in ucol_imp.h)

3. |textIter| (of type UCollationElement) is a member of struct UStringSearch

4. UStringSearch is created by Blink (TextIterator.cpp) and init'd with 
   a length-1 pattern(needle) and text (hay)

5. When UStringSearch is created, |textIter| is init'd 
   in usearch_openFromCollator (usearch.cpp) which calls ucol_openElements 
   (with pattern text/length) in ucoleitr.cpp

6. ucol_openElements() fills out various fields after creating UCollationElements. A bunch of initialization is done by uprv_init_collIterate (in ucol.cpp),
which in turn calls |IInit_collIterate|.  (ucol.cpp)

7. fcdPosition is set to 0, but only if initlaizeNFD() succeeds, but it should always succeed in our case. 

  The only scenario where fcPostion is not init'd is when initalizeNFD() fails.

### [Deleted User] (2014-11-20)

You need an MSan build, not an ASan one.

http://www.chromium.org/developers/testing/memorysanitizer

### js...@chromium.org (2014-11-20)

Thank you for the pointer (I was wondering how ASAN detects 'uninitialized memory') . I'm stuck with this: 

sudo third_party/instrumented_libraries/install-build-deps.sh

It fails on Goobuntu Trusty with libjack-dev:

Picking 'libxrender' as source package instead of 'libxrender1'
Picking 'libxss' as source package instead of 'libxss1'
Picking 'libxtst' as source package instead of 'libxtst6'
The following packages have unmet dependencies:
 libjack-dev : Depends: libjack0 (= 1:0.121.3+20120418git75e3e20b-2.1ubuntu1) but it is not going to be installed
E: Build-dependencies for pulseaudio could not be satisfied.


### js...@chromium.org (2014-11-20)

I installed libjack0 and the script is now running (through). 


### js...@chromium.org (2014-11-21)

Afaict, data->fcdPosition is initialized before use. I tried to use the same variable before it reaches where Msan crashed, but the crash happens always at the same position. My added code may have been optimized away (because it's no-op). Is it a good idea to build a Msan-enabled debug build ?  

 Msan build claimed that 'uninitialized value' was created by a heap allocation in line 2000 of TextIterator.cpp, but that's where wtf::Vector of UChar is created. 

 Uninitialized value was created by a heap allocation
    #0 0x7fb6d9896353 in __interceptor_malloc ??:0:0
    #1 0x7fb6dea4ac22 in partitionAllocGenericFlags /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:541:20
    #2 0x7fb6dea4ac22 in partitionAllocGeneric /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/wtf/PartitionAlloc.h:557:0
    #3 0x7fb6dea4ac22 in WTF::DefaultAllocator::backingAllocate(unsigned long) /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/wtf/DefaultAllocator.cpp:40:0
    #4 0x7fb6e1dbc5df in vectorBackingMalloc<unsigned short> /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/wtf/DefaultAllocator.h:68:37
    #5 0x7fb6e1dbc5df in allocateBuffer /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/wtf/Vector.h:294:0
    #6 0x7fb6e1dbc5df in reserveInitialCapacity /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/wtf/Vector.h:988:0
    #7 0x7fb6e1dbc5df in blink::SearchBuffer::SearchBuffer(WTF::String const&, unsigned int) /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/core/editing/TextIterator.cpp:2000:0
    #8 0x7fb6e1db3728 in blink::findPlainTextInternal(blink::CharacterIterator&, WTF::String const&, unsigned int, unsigned long&) /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/core/editing/TextIterator.cpp:2355:5
    #9 0x7fb6e1db537d in blink::findPlainText(blink::Position const&, blink::Position const&, WTF::String const&, unsigned int, blink::Position&, blink::Position&) /usr/local/google/w/cr/t/src/out/Release/../../third_party/WebKit/Source/core/editing/TextIterator.cpp:2431:23


### eu...@google.com (2014-11-21)

We don't have a regular build of msan+debug, and I've seen it fail once (due to code+data size overflowing the 2Gb limit on the default memory model).

You could use __msan_print_shadow to see what MSan thinks of a memory location at any point.
https://code.google.com/p/memory-sanitizer/wiki/MemorySanitizer#Interface

### js...@chromium.org (2014-11-21)

Thank you for the tips. 

Before doing anything further, I added an explicit initialization of TextIterator::m_buffer (of Vector<UChar>) in TextIterator.cpp  where msan claimed that the variable (used-before-init) was first allocated. With that, msan warning disappeared. 

So, this is kinda indirect proof that msan somehow mixes up two different variables, TextIterator::m_buffer and 'searcher' in TextIterator (of UStringSearch type).  

Is this convincing enough or do you think I need to do further investigation ?  



### kc...@chromium.org (2014-11-21)

(I haven't looked at the code)
Msan reports uses of uninitialized data, but not necessary the first load from 
uninitialized memory. 
I.e.  you may have
  int foo;  // uninitialized
  bar = foo;  // no bug report
  zab = bar;  // no bug report
  if (zab) {  // MSan barks here
     ... 
  }



### js...@chromium.org (2014-11-21)

I believe it's more like this:

int *foo = 0;
int *bar = (int *) malloc(10 * sizeof(int)); 
foo = bar;   // I haven't confirmed this connection in the case under investigation, but it's possible. 
                   // I hadn't thought of this connection before kcc's https://crbug.com/chromium/433866#c10. 

if (foo != 0) {   // MSan complains as if it's |*foo != 0|
   ... 
}



### kc...@chromium.org (2014-11-21)

This would be strange. 
In your case foo is fully initialized (but not "*foo" ), and msan should not complain. 

### eu...@google.com (2014-11-24)

When MSan points to
 getNextNormalizedChar(icu_52::collIterate*) src/third_party/icu/source/i18n/ucol.cpp:2315
it could actually be anything in the entire if() expression, not necessarily the fcdPosition member.

    if ((data->fcdPosition == NULL || data->fcdPosition < data->pos) &&
        (nextch >= NFC_ZERO_CC_BLOCK_LIMIT_ ||
         ch >= NFC_ZERO_CC_BLOCK_LIMIT_)) {

It could be "ch" or "nextch" that are uninitialized, and they could come from the uninitialized string buffer that the "created by a heap allocation" stack trace points to.

### js...@chromium.org (2014-11-24)

@eugenis, thanks. That makes a lot of sense. In that case, it's not an ICU bug, but a Blink bug which calls usearch_setText with an uninitialized buffer. 

    UStringSearch* searcher = blink::searcher();

    UErrorCode status = U_ZERO_ERROR;
    memset(m_buffer.data(), 0, size * sizeof(UChar));  // Added line 
    usearch_setText(searcher, m_buffer.data(), size, &status);
    ASSERT(status == U_ZERO_ERROR);

    usearch_setOffset(searcher, m_prefixLength, &status);
    ASSERT(status == U_ZERO_ERROR);

    int matchStart = usearch_next(searcher, &status);
    ASSERT(status == U_ZERO_ERROR);


### [Deleted User] (2014-11-24)

So, the bug seems to be somewhere in findPlainTextInternal(). Adding owners from Source/core/editing - please help triage this.

### js...@chromium.org (2014-11-24)

Actually, it's a bit more complicated. It may be still an ICU bug. 

At call site in TextIterator  : mbuffer_data, sizeof(UChar) * size (size = 4) 
Shadow map of [0x250000024000, 0x250000024008), 8 bytes:
0x250000024000: 00000000 00000000 ........ ........  |. . . .|

At the beginning of   getNextNormalizedChar in ICU  : data-pos
Shadow map of [0x250000024006, 0x25000002401a), 20 bytes:
0x250000024004: ....0000 ffffffff ffffffff ffffffff  |. A A A|
0x250000024014: ffffffff ffff.... ..

Right before the msan complaint in   getNextNormalizedChar() : data-pos

Shadow map of [0x250000024008, 0x25000002401c), 20 bytes:
0x250000024008: ffffffff ffffffff ffffffff ffffffff  |A A A A|
0x250000024018: ffffffff ........ ........ ........  |A . . .|

### js...@chromium.org (2014-11-24)

createTextNode is called with %u2b9b%u0c70%u0e4d%udb7e in the repro case. 

U+DB7E is a lone surrogate and invalid. We have to check what createTextNode is supposed to do per spec. I hope that the spec says that it should be turned into U+FFFD. 


### js...@chromium.org (2014-11-25)

https://dom.spec.whatwg.org/#dom-document-createtextnode : No check is performed that data consists of characters that match the Char production (it seems very intentional) .  Ick... So, Blink editor and/or ICU has to deal with this invalid input....  

### tk...@chromium.org (2014-11-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-11-25)

I got a patch for ICU.  It's up at https://codereview.chromium.org/751333003/




### bu...@chromium.org (2014-11-26)

------------------------------------------------------------------
r293126 | jshin@chromium.org | 2014-11-26T18:31:18.306291Z

Changed paths:
   A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu52/patches/col.patch?r1=293126&r2=293125&pathrev=293126
   M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu52/source/i18n/ucol.cpp?r1=293126&r2=293125&pathrev=293126
   M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu52/README.chromium?r1=293126&r2=293125&pathrev=293126

Apply a local patch to ucol.cpp


BUG=433866
TEST=See the bug.
R=mbarbella@google.com

Review URL: https://codereview.chromium.org/751333003
-----------------------------------------------------------------

### bu...@chromium.org (2014-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/87feb77547781a22b31c423bc0d57b7dca32d5b8

commit 87feb77547781a22b31c423bc0d57b7dca32d5b8
Author: Jungshik Shin (jungshik at google) <jshin@chromium.org>
Date: Wed Nov 26 19:17:21 2014

Roll src/third_party/icu dd72764:866ff69 (svn 292996:293126)

Summary of changes available at:
https://chromium.googlesource.com/chromium/deps/icu52/+log/dd72764..866ff69

BUG=433866
TEST=see the bug
TBR=mbarbella@chromium.org

Review URL: https://codereview.chromium.org/724233004

Cr-Commit-Position: refs/heads/master@{#305849}

[modify] http://crrev.com/87feb77547781a22b31c423bc0d57b7dca32d5b8/DEPS


### js...@chromium.org (2014-11-26)

Fixed in the trunk. 


### cl...@chromium.org (2014-11-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-12-01)

requesting to merge to M40. 

### js...@chromium.org (2014-12-03)

[Empty comment from Monorail migration]

### ma...@google.com (2014-12-03)

[Automated comment] Request affecting a post-stable build (M39), manual review required.

### ma...@google.com (2014-12-03)

Approved for M40 (branch: 2214)

### bu...@chromium.org (2014-12-04)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=65373

------------------------------------------------------------------
r65373 | jungshik@google.com | 2014-12-04T01:21:37.703910Z

-----------------------------------------------------------------

### js...@chromium.org (2014-12-05)

Per off-line discussion with amineer@ (he talked to the security team), we'll not merge this to M39. 


### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congratualtions - $1000 for this report. Notes from the reward panel: "$500 for the bug, +$500 ClusterFuzz bonus".

### cl...@chromium.org (2015-03-04)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/433866?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Editing, Blink>SVG, UI>Browser>FindInPage]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080867)*
