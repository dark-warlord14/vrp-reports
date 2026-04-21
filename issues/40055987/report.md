# Security: expat vulnerable to CVE-2013-0340?

| Field | Value |
|-------|-------|
| **Issue ID** | [40055987](https://issues.chromium.org/issues/40055987) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>XML |
| **Platforms** | Android, Linux, Mac, Windows |
| **CVE IDs** | CVE-2013-0340 |
| **Reporter** | se...@pipping.org |
| **Assignee** | bu...@chromium.org |
| **Created** | 2021-05-24 |
| **Bounty** | $500.00 |

## Description

Reported by Sebastian Pipping:

I believe ... this vulnerability affect Chromium:

  CVE-2013-0340 "Billion Laughs" fixed in Expat 2.4.0

https://blog.hartwork.org/posts/cve-2013-0340-billion-laughs-fixed-in-expat-2-4-0/

## Timeline

### [Deleted User] (2021-05-24)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2021-05-24)

Every user of expat (afaik) uses XML_SetEntityDeclHandler to simply halt parsing (as invalid) on any xml entity expansion. It's like step three of any expat use. Good to see that they're mitigating upstream though. Should probably pick that up.

### bu...@chromium.org (2021-05-24)

Roll at https://chromium-review.googlesource.com/c/chromium/src/+/2915493 .

### bu...@chromium.org (2021-05-24)

Well, at least, I thought it was well known to always set XML_SetEntityDeclHandler and disable entity expansion when using expat. However, outside of Skia I don't see any code actually doing so. So it looks like libjingle_xmpp, the parser in the wayland support code, and the one fontconfig could be vulnerable to this. The fontconfig and wayland parsers appear to be only using xml from the system, so it would only be someone DoS'ing themselves. Not sure about libjingle though. Note that there are two more uses, one in perl and one in libprotobuf-mutator, but these don't appear to ship.

### gi...@appspot.gserviceaccount.com (2021-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7217f03fbf9a14dff84acd71770335e44b5e38ac

commit 7217f03fbf9a14dff84acd71770335e44b5e38ac
Author: Ben Wagner <bungeman@chromium.org>
Date: Tue May 25 14:26:03 2021

Roll src/third_party/expat/src/ e976867fb..a28238bde (182 commits)

https://chromium.googlesource.com/external/github.com/libexpat/libexpat.git/+log/e976867fb57a..a28238bdeebc

$ git log e976867fb..a28238bde --date=short --no-merges --format='%ad %ae %s'
2021-05-23 sebastian Set expected release date for 2.4.1
2021-05-23 sebastian Bump version info from 9:0:8 to 9:1:8
2021-05-23 sebastian Bump version to 2.4.1
2021-05-23 sebastian Keep macro SIZEOF_VOID_P out of expat_config.h(.in) for multilib support
2021-05-23 sebastian Actions: Avoid error "would clobber existing tag" when pushing new tags
2021-05-11 sebastian Set expected release date for 2.4.0
2021-05-11 sebastian Bump version info from 8:0:7 to 9:0:8
2021-05-11 sebastian Bump version to 2.4.0
2021-05-11 sebastian Changes: Extend section on upcoming release 2.4.0
2021-05-21 sebastian Changes: Document new XML_FEATURE_ constants
2021-05-21 sebastian Changes: Combine notes on billion laughs attack protection
2021-05-22 sebastian README.md: Mention Windos binaries zip download option
2021-05-22 sebastian README.md: Fix a URL for some markdown interpreters
2021-05-22 sebastian README.md: Document where generated CMake files need >=2.4.0 to work
2021-05-22 sebastian README.md: Make CMake config mode example more clear
2021-05-20 sebastian Changes: Document Autotools CMake file fixes
2021-05-20 sebastian autotools-cmake.yml: Cover macOS and MinGW
2021-05-20 sebastian cmake/autotools: Fix generated expat-noconfig.cmake for macOS and MinGW
2021-05-20 sebastian cmake/autotools: Use AC_CHECK_SIZEOF to fix 32bit support
2021-05-14 sebastian expat.iss: Use URLs with SSL
2021-05-13 sebastian Increase precision in existing MIT headers based on Git history
2021-05-13 sebastian doc/xmlwf.xml: Drop two XML comments of little value
2021-05-13 sebastian doc/xmlwf.xml: Add GNU FDL 1.1 copyright header
2021-05-14 sebastian expat.iss: Add MIT header
2021-05-13 sebastian CMake: Streamline existing copyright header
2021-05-14 sebastian tests: Cover accounting of CDATA sections inside of general entities
2021-05-14 sebastian lib: Fix accounting of CDATA sections inside of general entities
2021-05-13 sebastian README.md: Add total download count badges
2021-05-13 sebastian Revert ".github/workflows: Re-add repo ppa:ondrej/php(!) to fix wine32 installation"
2021-05-12 sebastian Changes: Document support for CMake variable BUILD_SHARED_LIBS
2021-05-12 sebastian CMake: Support standard variable BUILD_SHARED_LIBS
2021-05-08 sebastian doc/reference.html: Upgrade to OK.css 1.0.3
2021-04-19 sebastian Changes: Document protection against billion laughs attacks
2021-04-26 sebastian tests: Cover helper unsignedCharToPrintable
2021-04-26 sebastian tests: Cover billion laughs attack protection API
2021-04-25 sebastian doc/reference.html: Document billion laughs attack protection API
2021-04-25 sebastian xmlwf.1: Document arguments -a and -b
2021-04-17 sebastian xmlwf: Add support for custom attack protection parameters
2021-04-18 sebastian xmlwf: Include expat_config.h so we can check for macro XML_DTD
2021-04-21 sebastian tests: Cover accounting
2021-04-19 sebastian lib: Make EXPAT_ENTROPY_DEBUG consistent with other EXPAT_*_DEBUG variables
2021-04-14 sebastian lib: Add prefix "expat: " to EXPAT_ENTROPY_DEBUG=1 stderr output
2021-04-19 sebastian lib: Allow test suite to access raw accounting values
2021-04-20 sebastian lib: Address Cppcheck 2.4.1 warning "uninitvar"
2021-04-19 sebastian lib: Protect against billion laughs attacks (approach 3.0.21)
2021-04-20 sebastian Autotools|CMake: Suppress -Wpedantic-ms-format false positives
2021-04-20 sebastian mass-cppcheck.sh: Suppress warning "unknownMacro"
2021-05-07 sebastian Actions: Ensure well-formed and valid XML
2021-05-07 sebastian doc/reference.html: Fix XML validity
2021-05-07 sebastian xmlwf.1: Fix DocBook validity
(...)
2021-03-16 Alexander.Richardson CMake: Only set CMAKE_CXX_FLAGS after enable_language(CXX)
2021-03-10 sebastian fuzzers: Address Clang warning -Wunused-parameter
2021-02-24 sebastian .travis.yml: Install llvm-11 for llvm-symbolizer
2021-02-23 sebastian .travis.yml: Upgrade to Ubuntu Bionic 18.04.x LTS and Clang 11
2021-02-23 sebastian apply-clang-format.sh: Report on clang-format version
2021-02-24 sebastian xmlparse.c: Reject missing call to XML_GetBuffer in XML_ParseBuffer
2020-12-29 sebastian configure.ac: Drop obsolescent macro AC_HEADER_STDC (#436)
2020-12-29 sebastian Actions: Cover list of symbols exported by installed expat_config.h
2020-12-27 sebastian Use GitHub Actions to run current macOS Travis CI tasks
2020-12-27 tc Detect unsupported VS at configure time (and not at compile time)
2020-12-17 tim.gates docs: fix simple typo, wtihout -> without
2020-10-30 sebastian Changes: Document #382 and #428
2020-10-25 sebastian tests: Show failure location for normal mode output as well
2020-10-25 sebastian Travis: Add CTEST_OUTPUT_ON_FAILURE=1 where missing
2020-10-25 sebastian tests: Make argument -v more useful
2020-10-25 sebastian tests: Report actual failure location
2020-10-25 sebastian tests: Make check for silence explain itself better
2020-10-03 sebastian Drop remaining support for Visual Studio 2008, 2010, 2012 (#422)
2020-10-03 sebastian Revert "AppVeyor: Be explicit about build script to support msbuild 3.5"
2020-10-03 sebastian Revert "AppVeyor: Cover 32bit Visual Studio 9 2008 using MSBuild 3.5"
2020-10-03 sebastian CMake: Remove unused variable
2020-10-03 sebastian Set release date for 2.2.10
2020-10-02 sebastian Bump version info from 7:11:6 to 7:12:6
2020-10-02 sebastian Bump version from 2.2.9 to 2.2.10
2020-10-02 sebastian Changes: Document #405 #356 #359 #394 #366 #412 #368 #369
2020-10-02 sebastian CMake: Turn endif(..) into endif(), and else(..) into else()
2020-10-03 sebastian tests: Add missing static to address compiler warning
2020-10-01 sebastian Changes: Document #424
2020-09-30 sebastian CMake: Support "make package" based on CPack
2020-09-26 sebastian Changes: Document #419
2019-08-03 sebastian qa.sh: Enable LeakSanitizer
2020-09-15 sebastian AppVeyor: Cover Visual Studio 16 2019
2020-09-18 gulliver added "new" behaviour for Policy CMP0077 which allows to control the build options by variables if lib is used by FetchContent of a super project
2020-09-09 sebastian installer: Add missing file to fix build from installed sources (#409)
2020-08-20 sebastian readme: Sync list of CMake options
2020-08-20 sebastian CMake: Introduce option EXPAT_BUILD_PKGCONFIG (#413)
2020-08-12 boris Get rid of unsigned integer overflow in column calculation
2020-07-16 sebastian CMake: Consider use of CMAKE_{EXE,MODULE,SHARED}_LINKER_FLAGS
2020-07-16 sebastian Be more correct about const correctness on the inside
2020-07-15 sebastian Changes: Document #408
2020-07-10 sebastian CMake: Get expat target name back to constant "expat"
2020-06-22 sebastian Changes: Document #406
2020-06-22 klebertarcisio xmlwf: Checks value after calling malloc
2020-05-28 sebastian Travis: Limit Cppcheck to macOS
2020-05-27 sebastian xmlparse.c: Fix reading uninitialized variable (#404)
2020-05-12 sebastian Travis: Improve call to cppcheck
2020-05-12 sebastian Travis: Install a find(1) better than that of macOS
2020-05-13 sebastian Changes: Document #403
2020-05-13 jorton Update xmlwf to exit with 3 if an output file could not be opened. Update xmlwf exit code docs per review.
2020-05-12 jorton Document the exit codes for xmlwf.

Created with:
  roll-dep src/third_party/expat/src
R=bungeman@chromium.org,dcheng@chromium.org

Bug: chromium:1212733
Change-Id: Ia8acd0e3b7efe9fd7225c7760016d9c3dc67655c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915493
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Ben Wagner <bungeman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#886278}

[modify] https://crrev.com/7217f03fbf9a14dff84acd71770335e44b5e38ac/DEPS
[modify] https://crrev.com/7217f03fbf9a14dff84acd71770335e44b5e38ac/third_party/expat/README.chromium
[modify] https://crrev.com/7217f03fbf9a14dff84acd71770335e44b5e38ac/third_party/expat/include/expat_config/expat_config.h
[modify] https://crrev.com/7217f03fbf9a14dff84acd71770335e44b5e38ac/third_party/expat/roll-expat.sh


### bu...@chromium.org (2021-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-25)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and Security_Impact labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues Impact guidelines: https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2021-05-25)

Of the shipping users of expat in Chromium, the only one I can find that seems could be impacted by this is libjingle. From a cursory glance it looks like this may be involved in XMPP, though I haven't looked too hard. It does seem that an attacker could send an XMPP request which could cause a tab in the recipient (who would already need to be connected to the attacker) to crash when it runs into memory limits, but is limited to this sort of DoS. Someone from the security team could take a closer look and verify if they so wish (and change the Security_Severity label as appropriate), but this has been a generally known thing for the past eight years now so doesn't seem overly urgent.

### ad...@google.com (2021-05-25)

Thanks! Adjusting Impact to mark the earliest affected branch (i.e. forever) but severity sounds good. If it's denial of service technically it's not a security bug at all according to Chrome guidelines, but as it's got a CVE we'll keep it in the security queue to reduce confusion.

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-05)

The VRP Panel has decided to award $500 for reporting this issue and https://crbug.com/chromium/1212694. We appreciate you bringing this to our attention! 

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-12-13)

considering the roll of https://crbug.com/chromium/1212733#c7 to be the final fix

### pg...@google.com (2023-01-18)

removing relnotes_update_needed since the fix was upstream and this bug tracks the roll only

### is...@google.com (2023-01-18)

This issue was migrated from crbug.com/chromium/1212733?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055987)*
