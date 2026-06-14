# Arbitrary Read in swiftshader

| Field | Value |
|-------|-------|
| **Issue ID** | [40094236](https://issues.chromium.org/issues/40094236) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2019-03-07 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36

Steps to reproduce the problem:
Simplest PoC:

#version 300 es
layout(location=0x86868686u

* the value in "location" must be greater than 0x7fffffff and should be ended with "u".
----------------------------------------

1. Compile PoC above with newest swiftshader.

   You can just simply modify the code of VertexRoutineFuzzer.cpp in swiftshader project to call the compile() method.

	const char * szPoC = R"(#version 300 es
layout(location=0x86868686u
)";
	std::unique_ptr<TranslatorASM> glslCompiler(new TranslatorASM(fakeVS.get(), GL_VERTEX_SHADER));
         ...................
	glslCompiler->compile(szPoC, 1, SH_OBJECT_CODE);

2. You should got a SIGSEGV/Access violation error.

        attachment [0xC0000005.jpg]

What is the expected behavior?

What went wrong?
Swiftshader treat 0x86868686u as an buffer pointer of TString object, and when Swiftshader tries to report error that location couldn't be a negative value（>0x7fffffff）, it will tries to read the string in 0x86868686u. 

On 32-bit platform, seems like there's a high chance that an attacker could read arbitrary memory.

----------------------------------------------------------

TLayoutQualifier TParseContext::parseLayoutQualifier(const TString &qualifierType, const TSourceLoc& qualifierTypeLine, const TString &intValueString, int intValue, const TSourceLoc& intValueLine)
{
.....
	if (qualifierType != "location")
	{
......
	}
	else
	{
		// must check that location is non-negative
		if (intValue < 0)
		{
			error(intValueLine, "out of range:", intValueString.c_str(), "location must be non-negative");  

                   <<<<<<< intValueString is not correct (_Buf=0x8686868e)
......

}

-		[Original Viwe]	{_Myval1={allocator=??? } _Myval2={_Bx={_Buf=0x8686868e  _Ptr=??? _Alias=0x8686868e  } ...} }	std::_Compressed_pair<pool_allocator<char>,std::_String_val<std::_Simple_types<char> >,0>
+		_Myval1	{allocator=??? }	pool_allocator<char>
+		_Myval2	{_Bx={_Buf=0x8686868e _Ptr=??? _Alias=0x8686868e  } _Mysize=??? _Myres=??? }	std::_String_val<std::_Simple_types<char> >

It is incorrectly converted to TString object here:

  case 154:  // unsigned int

    {
        (yyval.interm.layoutQualifier) = context->parseLayoutQualifier(*(yyvsp[-2].lex).string, (yylsp[-2]), *(yyvsp[0].lex).string, (yyvsp[0].lex).i, (yylsp[0]));
    }

which 
		   yyvsp - 2  -->  "location"
		   yyvsp - 1  -->  =
		   yyvsp + 0  -->  0x86868686u

and 0x86868686 is being used to construct a TString object which is not correct.

Fix Advice:
yyvsp[0] should be a Integer but not String. Do not convert it to TString here.

Did this work before? No 

Chrome version: 72.0.3626.109  Channel: n/a
OS Version: 10.0
Flash Version: 

Sorry if I post this at wrong place.

The problem is: If I try to compile this code directly in swiftshader project. Things works as I expected.

Seems like chromium shares the same code, but seems like in WebGL, Angle will translate first and cause a translate error, thus PoC will not be passed to swiftshader compiler.

I don't know if there's some method to trigger this in chrome. But still I try to report it here because the detail of security problem in this issue board will not be revealed to public before it is fixed.

Regards,
Wenxiang Qian of Tencent Blade Team

## Attachments

- [0xc0000005.jpg](attachments/0xc0000005.jpg) (image/jpeg, 296.8 KB)

## Timeline

### oc...@chromium.org (2019-03-07)

capn, could you please take a look at this?

(also not sure about platform impact here -- assuming desktop platforms).

[Monorail components: Internals>GPU>SwiftShader]

### sh...@chromium.org (2019-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-07)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-03-07)

I was able to reproduce it with an end-to-end test as well, so yes this looks legit and scary.

Might affect ANGLE as well.

### ca...@chromium.org (2019-03-07)

Actually ANGLE seems fine, but I'll let Geoff confirm.

SwiftShader fix for review: https://swiftshader-review.googlesource.com/26428

### oc...@chromium.org (2019-03-08)

Thanks capn! Would you mind uploading the end-to-end test here so CF can confirm? 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-08)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader.git/+/d2b1d2f936eec56edf753735dc8d6d024ce841d6

commit d2b1d2f936eec56edf753735dc8d6d024ce841d6
Author: Nicolas Capens <capn@google.com>
Date: Fri Mar 08 16:43:47 2019

Remove literal string from error message.

The lexer doesn't actually keep the string for literals.

https://crbug.com/chromium/939239

Change-Id: Ib8b28e75e36d1c6beff8afa580fc4c29c23b6eb0
Reviewed-on: https://swiftshader-review.googlesource.com/c/SwiftShader/+/26428
Tested-by: Nicolas Capens <nicolascapens@google.com>
Reviewed-by: Alexis Hétu <sugoi@google.com>

[modify] https://crrev.com/d2b1d2f936eec56edf753735dc8d6d024ce841d6/src/OpenGL/compiler/ParseHelper.cpp
[modify] https://crrev.com/d2b1d2f936eec56edf753735dc8d6d024ce841d6/src/OpenGL/compiler/ParseHelper.h
[modify] https://crrev.com/d2b1d2f936eec56edf753735dc8d6d024ce841d6/src/OpenGL/compiler/glslang.y
[modify] https://crrev.com/d2b1d2f936eec56edf753735dc8d6d024ce841d6/src/OpenGL/compiler/glslang_tab.cpp
[modify] https://crrev.com/d2b1d2f936eec56edf753735dc8d6d024ce841d6/tests/GLESUnitTests/unittests.cpp


### ca...@chromium.org (2019-03-08)

#8 is the quick fix. Should roll into Chromium in a few hours.

Ideally unsigned literals should be handled separately as they can't be negative: https://swiftshader-review.googlesource.com/c/SwiftShader/+/26428/1/tests/GLESUnitTests/unittests.cpp#825 But that's a much lower priority issue, and will be obsolete when we replace our OpenGL ES front-end with ANGLE.

### ca...@chromium.org (2019-03-08)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-03-08)

Roll landed: https://chromium-review.googlesource.com/c/chromium/src/+/1512152

https://crbug.com/swiftshader/126 for potential follow-up.

### sh...@chromium.org (2019-03-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-11)

[Empty comment from Monorail migration]

### aa...@google.com (2019-03-14)

Flipping severity to medium, since only a read.

### na...@google.com (2019-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-14)

Congrats! The Panel decided to reward $1,000 for this report :) 

### le...@gmail.com (2019-03-15)

Thank you! BTW, is there a CVE number assigned to this issue now?

### aw...@chromium.org (2019-03-15)

A CVE will be assigned when M73 gets to Stable, is that OK?

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### le...@gmail.com (2019-03-16)

OK, thank you :).

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-03-25)

branch:3729

### sh...@chromium.org (2019-03-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-04-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-04-17)

Rejecting merge to M74 now since this hasn't been merged and we're less than a week away. 

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/939239?no_tracker_redirect=1

[Monorail blocking: crbug.com/swiftshader/126]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094236)*
