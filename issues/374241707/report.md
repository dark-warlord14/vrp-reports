# Security: [webkit] heap-use-after-free in WebCore::DOMWrapperWorld::~DOMWrapperWorld()+0x25b

| Field | Value |
|-------|-------|
| **Issue ID** | [374241707](https://issues.chromium.org/issues/374241707) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>iOSWeb |
| **Platforms** | iOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2024-10-18 |
| **Bounty** | $7,000.00 |

## Description

# Steps to reproduce the problem

## Test Environments

- WebKit : commit 6c794791a3396581d1b8184920f8694c23a55612 (HEAD -> main, origin/main, origin/HEAD)
- This could occur due to the string copying process in JavaScriptCore, making it a potential threat on iOS Chrome, which uses WebKit.

# Problem Description

## Details

- At [1], when the `makeStringByReplacing()` function replaces the text, the process of replacing the existing data and allocating new data leads to the previous text being freed from memory. Then at [2], during the execution of the `copyCharacters()` function, as it attempts to replace the existing string data and insert new data, a Use-After-Free occurs.
- [1] : <https://github.com/WebKit/WebKit/blob/4cb42b8c9386d435841b39b4864d920ee9416c03/Source/WebCore/inspector/InspectorStyleSheet.cpp#L1557>
- [2] : <https://github.com/WebKit/WebKit/blob/4cb42b8c9386d435841b39b4864d920ee9416c03/Source/WTF/wtf/text/StringImpl.cpp#L1142>

```
ExceptionOr<void> InspectorStyleSheet::setRuleStyleText(const InspectorCSSId& id, const String& newStyleDeclarationText, String* outOldStyleDeclarationText, const String* newRuleText, String* outOldRuleText)
{
    auto* cssStyleDeclaration = styleForId(id);
    if (!cssStyleDeclaration)
        return Exception { ExceptionCode::NotFoundError };

    auto* cssRule = ruleForId(id);
    if (!cssRule)
        return Exception { ExceptionCode::NotFoundError };

    RefPtr<CSSRuleSourceData> sourceData = ruleSourceDataFor(cssRule);
    if (!sourceData)
        return Exception { ExceptionCode::NotFoundError };

    RefPtr<CSSRuleSourceData> logicalContainingRuleSourceData = sourceData->isImplicitlyNested ? ruleSourceDataFor(cssRule->parentRule()) : sourceData;
    if (!logicalContainingRuleSourceData)
        return Exception { ExceptionCode::NotFoundError };

    unsigned bodyStart = logicalContainingRuleSourceData->ruleBodyRange.start;
    unsigned bodyEnd = logicalContainingRuleSourceData->ruleBodyRange.end;
    ASSERT(bodyStart <= bodyEnd);

    const String& styleSheetText = m_parsedStyleSheet->text();
    RELEASE_ASSERT_WITH_SECURITY_IMPLICATION(bodyEnd <= styleSheetText.length());

    if (outOldStyleDeclarationText)
        *outOldStyleDeclarationText = cssStyleDeclaration->cssText();

    if (outOldRuleText)
        *outOldRuleText = styleSheetText.substring(bodyStart, bodyEnd - bodyStart);

    cssStyleDeclaration->setCssText(newStyleDeclarationText);

    // Don't canonicalize the rule text if a `newRuleText` is provided, to allow for faithful undoing.
    StringView replacementBodyText = newRuleText ? *newRuleText : computeCanonicalRuleText(styleSheetText, newStyleDeclarationText, *logicalContainingRuleSourceData);

    m_parsedStyleSheet->setText(makeStringByReplacing(styleSheetText, bodyStart, bodyEnd - bodyStart, replacementBodyText));  //[ 1]
    m_pageStyleSheet->clearHadRulesMutation();
    fireStyleSheetChanged();

    return { };
}

```
```
Ref<StringImpl> StringImpl::replace(size_t position, size_t lengthToReplace, StringView string)
{
    position = std::min<size_t>(position, length());
    lengthToReplace = std::min(lengthToReplace, length() - position);
    size_t lengthToInsert = string.length();
    if (!lengthToReplace && !lengthToInsert)
        return *this;

    if ((length() - lengthToReplace) >= (MaxLength - lengthToInsert))
        CRASH();

    if (is8Bit() && (!string || string.is8Bit())) {
        LChar* data;
        auto newImpl = createUninitialized(length() - lengthToReplace + lengthToInsert, data);
        copyCharacters(data, { m_data8, position });
        if (string)
            copyCharacters(data + position, string.span8().first(lengthToInsert));  // [2]
        copyCharacters(data + position + lengthToInsert, { m_data8 + position + lengthToReplace, length() - position - lengthToReplace });
        return newImpl;
    }
    UChar* data;
    auto newImpl = createUninitialized(length() - lengthToReplace + lengthToInsert, data);
    if (is8Bit())
        copyCharacters(data, { m_data8, position });
    else
        copyCharacters(data, { m_data16, position });
    if (string) {
        if (string.is8Bit())
            copyCharacters(data + position, string.span8().first(lengthToInsert));
        else
            copyCharacters(data + position, string.span16().first(lengthToInsert));
    }
    if (is8Bit())
        copyCharacters(data + position + lengthToInsert, { m_data8 + position + lengthToReplace, length() - position - lengthToReplace });
    else
        copyCharacters(data + position + lengthToInsert, { m_data16 + position + lengthToReplace, length() - position - lengthToReplace });
    return newImpl;
}

```
# Summary

Use-After-Free in StringImpl::replace (JavaScriptCore)

# Custom Questions

#### Type of crash:

[tab]

#### Crash state:

See Reporting Crash Bugs, include the stack trace *with symbols*, registers, exception record]

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.0 KB)
- [patch_46d8803827ef233fd7572a5259097a95328ab007.diff](attachments/patch_46d8803827ef233fd7572a5259097a95328ab007.diff) (text/x-diff, 2.1 KB)

## Timeline

### j6...@gmail.com (2024-10-18)

deleted

### ps...@google.com (2024-10-19)

Thank you for the report,

Were you able to produce this UAF on Chrome? Chrome uses V8 which should prevent this from happening. Without a chrome crash report and way to reproduce the issue within the Chrome code base I'd suggest you report this issue directly to the WebKit project so they credit you properly. You can do so here:

https://bugs.webkit.org/enter_bug.cgi?product=Security

### j6...@gmail.com (2024-10-19)

- This is a bit wrong with the Summary! It happens in WebCore, not JavaScriptCore.
- And I filed this in the WebKit Bugzilla!
  
  - <https://bugs.webkit.org/show_bug.cgi?id=281807>

### j6...@gmail.com (2024-10-19)

- Could you please change the description as follows?
  - Use-After-Free in WebCore::InspectorStyleSheet::setRuleStyleText

### j6...@gmail.com (2024-10-19)

## Update

```
ExceptionOr<void> InspectorStyleSheet::setRuleStyleText(const InspectorCSSId& id, const String& newStyleDeclarationText, String* outOldStyleDeclarationText, const String* newRuleText, String* outOldRuleText)
{
    auto* cssStyleDeclaration = styleForId(id);
    if (!cssStyleDeclaration)
        return Exception { ExceptionCode::NotFoundError };

    auto* cssRule = ruleForId(id);
    if (!cssRule)
        return Exception { ExceptionCode::NotFoundError };

    RefPtr<CSSRuleSourceData> sourceData = ruleSourceDataFor(cssRule);
    if (!sourceData)
        return Exception { ExceptionCode::NotFoundError };

    RefPtr<CSSRuleSourceData> logicalContainingRuleSourceData = sourceData->isImplicitlyNested ? ruleSourceDataFor(cssRule->parentRule()) : sourceData;
    if (!logicalContainingRuleSourceData)
        return Exception { ExceptionCode::NotFoundError };

    unsigned bodyStart = logicalContainingRuleSourceData->ruleBodyRange.start;
    unsigned bodyEnd = logicalContainingRuleSourceData->ruleBodyRange.end;
    ASSERT(bodyStart <= bodyEnd);

    const String& styleSheetText = m_parsedStyleSheet->text();
    RELEASE_ASSERT_WITH_SECURITY_IMPLICATION(bodyEnd <= styleSheetText.length());

    if (outOldStyleDeclarationText)
        *outOldStyleDeclarationText = cssStyleDeclaration->cssText();

    if (outOldRuleText)
        *outOldRuleText = styleSheetText.substring(bodyStart, bodyEnd - bodyStart);

    cssStyleDeclaration->setCssText(newStyleDeclarationText);

    // Don't canonicalize the rule text if a `newRuleText` is provided, to allow for faithful undoing.
    StringView replacementBodyText = newRuleText ? *newRuleText : computeCanonicalRuleText(styleSheetText, newStyleDeclarationText, *logicalContainingRuleSourceData);  // [1']

    m_parsedStyleSheet->setText(makeStringByReplacing(styleSheetText, bodyStart, bodyEnd - bodyStart, replacementBodyText));  // [2']
    m_pageStyleSheet->clearHadRulesMutation();
    fireStyleSheetChanged();

    return { };
}

```

- The `StringView` for the returned in [1'] refers to the freed `ComputeCanonicalRuleText`. During the usage in [2'], a use-after-free issue occurs.
- In this case, a `String` should be returned instead of a `StringView`.

### ps...@google.com (2024-10-19)

Thank you for the above clarification and submitting the bug to WebKit! For our end though, without a reproducible way to trigger this issue in Chrome there is not much our engineers can do as the issue is theoretical in the context for Chromium.  

### j6...@gmail.com (2024-10-20)

I am working on reproducing this issue. Since it was found in a WebKit beta version, I've been considering how I can trigger it effectively.

Has the chromium team tried triggering this?

### j6...@gmail.com (2024-10-20)

I think this should be triggered on iOS. It crashes WebKit rendering engine, not the JS Engine.

However, since this occurred in a beta commit, I'm having trouble reproducing it on iOS Chrome.

This crash uses `com.apple.WebKit.WebContent`, and iOS Chrome also uses `com.apple.WebKit.WebContent`.

### j6...@gmail.com (2024-10-20)

But I'm curious, is V8 used instead of JSC on iOS? I remember that JSC was used when I tested it before. Has this changed?

### j6...@gmail.com (2024-10-21)

Hello?

### j6...@gmail.com (2024-10-21)

This affects iOS Chrome, not macOS Chrome. iOS Chrome uses WebKit.

### pe...@google.com (2024-10-21)

Thank you for providing more feedback. Adding the requester to the CC list.

### j6...@gmail.com (2024-10-21)

Thanks! I'm building in the simulator to reproduce this on iOS!

### ps...@google.com (2024-10-21)

Thanks for the back and forth on this with the added context. 

Setting severity to S2 and priority to P2, placing found in at 133, but that is a little tough as the webkit issue has not been seen in Chrome yet. Assigning to ajuma@ feel free to adjust severity as you see fit. 

webkit bug: https://bugs.webkit.org/show_bug.cgi?id=281807

### j6...@gmail.com (2024-10-21)

If you need a CC for the WebKit Bug Tracker, please let me know! I'm ready to add it.

### aj...@google.com (2024-10-21)

For clarity, when you say "beta commit" do you mean this commit is available in an iOS beta (e.g., iOS 18.1 beta)? Or do you just mean it has landed on WebKit trunk?

### j6...@gmail.com (2024-10-21)

This is caused by commit 227d5b5 to the webkit repo main on September 20th!

- <https://github.com/WebKit/WebKit/commit/227d5b5816c0493843f5ec63f3aaa869c631e2b8>

I'm using the following commit for webkit with the latest macOS Beta:

```
commit 6c794791a3396581d1b8184920f8694c23a55612 (HEAD -> main, origin/main, origin/HEAD)
Author: Carlos Alberto Lopez Perez <clopez@igalia.com>
Date:   Wed Oct 16 03:14:23 2024 -0700

```

### j6...@gmail.com (2024-10-23)

Hello,

These issues were patched in the following commit, and according to WebKit developers, the nature of the bugs is clear, so the behavior of the vulnerabilities should not differ between macOS and iOS.

Therefore, these bugs can be triggered in Safari/Chrome on iOS, which uses WebKit.

The following patches will apply to macOS as well as iOS.

<https://github.com/WebKit/WebKit/pull/35530>

### pe...@google.com (2024-10-23)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### aj...@google.com (2024-10-23)

Setting "Found in" to 1 since this bug is independent of Chrome milestone (in reality it's not found in any Chrome milestone since the WebKit logic never shipped).

### pe...@google.com (2024-10-24)

Setting milestone because of s2 severity.

### pe...@google.com (2024-10-24)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [131].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### aj...@google.com (2024-10-24)

There's nothing to merge here -- this is a bug in trunk WebKit that was fixed in trunk WebKit, and Apple is responsible for shipping WebKit on iOS.

### pg...@google.com (2024-10-24)

thanks for the info! removing merge labels here

### j6...@gmail.com (2024-10-26)

According to an additional note from the WebKit developer, they got the same results as this report when testing on iOS with ASan enabled, so this works on iOS Chrome.

### am...@chromium.org (2024-11-20)

Thank you for the report. Since this issue does not provide evidence or demonstration of exploitability in Chrome, this report is unfortunately not eligible for a Chrome VRP reward.

### j6...@gmail.com (2024-11-23)

This happened in WebKit Beta, so it wasn't actually in stable. We patched this before it reached stable. If it were in WebKit Stable, it would definitely be reachable in Chrome.

the previously reported [Issue 40061108](https://issues.chromium.org/issues/40061108) was also found in WebKit Beta, and Chrome was using WebKit Stable, so it was the same situation.

I would like to request a re-evaluation of this matter.

In fact, we've worked with the developers of WebKit to verify that this works on iOS, so if it ever reaches Stable, it should work on Chrome too.

### am...@chromium.org (2024-11-24)

Hello, as conveyed both on and off bug, VRP eligible reports must demonstrate the issue is reachable and triggerable in Chrome. You have provided no such demonstration.

> the previously reported [Issue 40061108](https://issues.chromium.org/issues/40061108) was also found in WebKit Beta, and Chrome was using WebKit Stable, so it was the same situation.

That issue provided a test case (poc.html) that reproduced and was confirmed to reproduce the issue on a active release channel of Chrome at that time. You have provided no such test case or demonstration.
The information in your reassessment request in c#28 does not provide this nor is providing any information we may have missed in our assessment, so unfortunately there is nothing to re-evaluate at this time.

If you are able to demonstrate how this was reachable in Chrome, that would be something we could re-evaluate.

### pe...@google.com (2025-01-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/374241707)*
