# Security: UAF in indexed_db_cursor.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40050168](https://issues.chromium.org/issues/40050168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | pw...@chromium.org |
| **Created** | 2019-09-19 |
| **Bounty** | $20,500.00 |

## Description

Note: this is a bug which is triggered from a compromised render process to attack the privileged browser process

IndexDBTransaction contains a set of raw points of IndexedDBCursor, which are all open cursors in the transaction.

```c++
class CONTENT_EXPORT IndexedDBTransaction {
    ...
std::set<IndexedDBCursor*> open_cursors_;
    ...
}
```

The following executing flow will cause a UAF
Assuring we already have a transaction and a cursor. Close the cursor while Advancing it

```c++
leveldb::Status IndexedDBCursor::CursorAdvanceOperation(
    uint32_t count,
    base::WeakPtr<IndexedDBDispatcherHost> dispatcher_host,
    blink::mojom::IDBCursor::AdvanceCallback callback,
    IndexedDBTransaction* /*transaction*/) {
  IDB_TRACE("IndexedDBCursor::CursorAdvanceOperation");
  leveldb::Status s = leveldb::Status::OK();
  if (!dispatcher_host)
    return s;

  if (!cursor_ || !cursor_->Advance(count, &s)) {
    cursor_.reset();

    if (s.ok()) {
      std::move(callback).Run(blink::mojom::IDBCursorResult::NewEmpty(true));
      return s;
    }

    // CreateError() needs to be called before calling Close() so
    // |transaction_| is alive.
    auto error = CreateError(blink::kWebIDBDatabaseExceptionUnknownError,
                             "Error advancing cursor", transaction_);
    Close();   -----------------------------------> trigger this close to execute
    std::move(callback).Run(blink::mojom::IDBCursorResult::NewErrorResult(
        blink::mojom::IDBError::New(error.code(), error.message())));
    return s;  
  }
```

In the Close function, transaction_ will be reset. 
```c++
void IndexedDBCursor::Close() {
  if (closed_)
    return;
  IDB_ASYNC_TRACE_END("IndexedDBCursor::open", this);
  IDB_TRACE("IndexedDBCursor::Close");
  closed_ = true;
  cursor_.reset();
  saved_cursor_.reset();
  transaction_.reset();  --------------------->transaction_ is reset to null
}
```

and then try to release the cursor, for example, reset the cursor ptr in the render process

```c++
IndexedDBCursor::~IndexedDBCursor() {
  if (transaction_)
    transaction_->UnregisterOpenCursor(this); ---------------> because the cursor is closed once, transaction_ is reset to null, UnregisterOpenCursor will not be called, which leaves a Dangling poiner in the 'std::set<IndexedDBCursor*> open_cursors_'
  // Call to make sure we complete our lifetime trace.
  Close();
}
```

after that, we can free the transaction to trigger IndexedDBTransaction::CloseOpenCursors to be called,
The cursor will be close again in IndexedDBTransaction::CloseOpenCursors, which trigger a UAF
```c++
void IndexedDBTransaction::CloseOpenCursors() {
  IDB_TRACE1("IndexedDBTransaction::CloseOpenCursors", "txn.id", id());
  for (auto* cursor : open_cursors_)
    cursor->Close();
  open_cursors_.clear();
}
```

I'll try to provide the a PoC soon. 

## Attachments

- [reproduce.patch](attachments/reproduce.patch) (text/plain, 667 B)
- [patch.patch](attachments/patch.patch) (text/plain, 686 B)
- [poc.html](attachments/poc.html) (text/plain, 4.3 KB)

## Timeline

### rs...@chromium.org (2019-09-19)

Thanks for the report. What version of Chrome is this issue in?

dmurph: Can you take a look?

[Monorail components: Blink>Storage>IndexedDB]

### hi...@gmail.com (2019-09-20)

It exists in the latest stable channel 77.0.3865.90

### dm...@chromium.org (2019-09-21)

Because I'm about to go OOO, unfortunately I have to assign this to you Chase.... oops! However, I do think I know how to fix this. We need to probably call the 

if (transaction_)
    transaction_->UnregisterOpenCursor(this); 

in the Close method instead of in the destructor (before the transaction is reset).

### rs...@chromium.org (2019-09-23)

[Empty comment from Monorail migration]

### hi...@gmail.com (2019-09-24)

Here is the poc files. you need a chrome asan build with version 77.0.3865.95
To reproduce the UAF easily, I patched  the function IndexedDBCursor::CursorAdvanceOperation to call Close directly, refer to the attached file reproduce.patch.
the poc.html is attached too.
after apply reproduce.patch, you can launch you asan chrome with the command "chrome-wrapper --user-data-dir="/tmp" --enable-blink-features=MojoJS http://x.x.x.x/poc.html"
you'll get the following asan crash log
=25158==ERROR: AddressSanitizer: heap-use-after-free on address 0x6070002c84b8 at pc 0x562c11b87604 bp 0x7fe1afd34a70 sp 0x7fe1afd34a68
READ of size 8 at 0x6070002c84b8 thread T4 (ThreadPoolForeg)
127.0.0.1 - - [24/Sep/2019 14:26:28] code 404, message File not found
127.0.0.1 - - [24/Sep/2019 14:26:28] "GET /favicon.ico HTTP/1.1" 404 -
    #0 0x562c11b87603  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xbfcc603)
    #1 0x562c11c4cccb  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xc091ccb)
    #2 0x562c11c4c443  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xc091443)
    #3 0x562c11b6c196  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xbfb1196)
    #4 0x562c11b6bcd0  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xbfb0cd0)
    #5 0x562c1035213d  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xa79713d)
    #6 0x562c184251e5  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1286a1e5)
    #7 0x562c1843b30e  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1288030e)
    #8 0x562c18439ab7  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1287eab7)
    #9 0x562c1841d7bb  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x128627bb)
    #10 0x562c1841f547  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x12864547)
    #11 0x562c1847ac2f  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x128bfc2f)
    #12 0x562c17fb4372  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x123f9372)
    #13 0x562c18008ca3  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244dca3)
    #14 0x562c18007764  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244c764)
    #15 0x562c1811a4eb  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1255f4eb)
    #16 0x562c180067c6  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244b7c6)
    #17 0x562c1802b03a  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1247003a)
    #18 0x562c1802a5dc  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1246f5dc)
    #19 0x562c1811bc81  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x12560c81)
    #20 0x7fe1c75246da  (/lib/x86_64-linux-gnu/libpthread.so.0+0x76da)

0x6070002c84b8 is located 40 bytes inside of 72-byte region [0x6070002c8490,0x6070002c84d8)
freed by thread T4 (ThreadPoolForeg) here:
    #0 0x562c0e5a9bbd  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x89eebbd)
    #1 0x562c11b1963e  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xbf5e63e)
    #2 0x562c11bd46f3  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xc0196f3)
    #3 0x562c18428a20  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1286da20)
    #4 0x562c1843cd86  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x12881d86)
    #5 0x562c1843716a  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1287c16a)
    #6 0x562c18439b12  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1287eb12)
    #7 0x562c1841d7bb  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x128627bb)
    #8 0x562c1841f547  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x12864547)
    #9 0x562c1847ac2f  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x128bfc2f)
    #10 0x562c17fb4372  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x123f9372)
    #11 0x562c18008ca3  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244dca3)
    #12 0x562c18007764  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244c764)
    #13 0x562c1811a4eb  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1255f4eb)
    #14 0x562c180067c6  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244b7c6)
    #15 0x562c1802b03a  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1247003a)
    #16 0x562c1802a5dc  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1246f5dc)
    #17 0x562c1811bc81  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x12560c81)
    #18 0x7fe1c75246da  (/lib/x86_64-linux-gnu/libpthread.so.0+0x76da)

previously allocated by thread T4 (ThreadPoolForeg) here:
    #0 0x562c0e5a935d  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x89ee35d)
    #1 0x562c11ba8170  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xbfed170)
    #2 0x562c11bbd7ab  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xc0027ab)
    #3 0x562c11bb5c7f  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xbffac7f)
    #4 0x562c11bb5ea7  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xbffaea7)
    #5 0x562c11c4a17f  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xc08f17f)
    #6 0x562c17fb4372  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x123f9372)
    #7 0x562c18008ca3  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244dca3)
    #8 0x562c18007764  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244c764)
    #9 0x562c1811a4eb  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1255f4eb)
    #10 0x562c180067c6  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1244b7c6)
    #11 0x562c1802b03a  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1247003a)
    #12 0x562c1802a5dc  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1246f5dc)
    #13 0x562c1811bc81  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x12560c81)
    #14 0x7fe1c75246da  (/lib/x86_64-linux-gnu/libpthread.so.0+0x76da)

Thread T4 (ThreadPoolForeg) created by T0 (chrome) here:
    #0 0x562c0e56a56a  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x89af56a)
    #1 0x562c1811aeee  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1255feee)
    #2 0x562c18029a0b  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1246ea0b)
    #3 0x562c180185e4  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1245d5e4)
    #4 0x562c180108c8  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x124558c8)
    #5 0x562c18010727  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x12455727)
    #6 0x562c17ffc661  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x12441661)
    #7 0x562c12422417  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xc867417)
    #8 0x562c16f9434f  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x113d934f)
    #9 0x562c16f93e44  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x113d8e44)
    #10 0x562c1713185b  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x1157685b)
    #11 0x562c16f8ecb4  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x113d3cb4)
    #12 0x562c0e5abddd  (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0x89f0ddd)
    #13 0x7fe1c025ab96  (/lib/x86_64-linux-gnu/libc.so.6+0x21b96)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/test/ssd1/chromium/src/out/DesktopAsan/chrome+0xbfcc603) 
Shadow bytes around the buggy address:
  0x0c0e80051040: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
  0x0c0e80051050: fd fd fd fd fd fd fa fa fa fa fd fd fd fd fd fd
  0x0c0e80051060: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c0e80051070: fd fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c0e80051080: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa
=>0x0c0e80051090: fa fa fd fd fd fd fd[fd]fd fd fd fa fa fa fa fa
  0x0c0e800510a0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x0c0e800510b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0e800510c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0e800510d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c0e800510e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==25158==ABORTING

I think the fix in https://crbug.com/chromium/1005753#c3 is correct, and a fix patch is attached as fix.patch

### hi...@gmail.com (2019-09-24)

a fix patch is attached as patch.patch

### cm...@chromium.org (2019-09-24)

I have a fix out for review at https://crrev.com/c/1820837 that incorporates the change dmurph@ mentioned.

I'm also OOO atm, but will check in again Wed latest to check for review comments, dry run results, and to validate against the crash stack.  I let Victor know also to feel free to CQ+2 the patch if he's confident in it or if he (or someone) gets a chance before me to take a closer look.

### cm...@chromium.org (2019-09-24)

Victor has a WIP patch at https://crrev.com/c/1821675 to address this, over to him.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/23303e6f178ca2993bfde7114e6bdf48dd0eff9d

commit 23303e6f178ca2993bfde7114e6bdf48dd0eff9d
Author: Victor Costan <pwnall@chromium.org>
Date: Wed Sep 25 20:16:48 2019

IndexedDB: Unregister cursors from transactions more consistently.

IndexedDBCursor now calls IndexedDBTransaction::UnregisterOpenCursor()
in Close(), which is called by the destructor.

The previous setup missed an edge case where calling
IndexedDBCursor::Close() directly would not unregister the cursor. This
behavior was relied upon in IndexedDBTransaction::CloseOpenCursors(),
but was not intended at other callsites.

Bug: 1005753
Change-Id: I91944138d05faa2d91ecc03b1040ec16ca1a7e5f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1821675
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#699937}

[modify] https://crrev.com/23303e6f178ca2993bfde7114e6bdf48dd0eff9d/content/browser/indexed_db/indexed_db_cursor.cc
[modify] https://crrev.com/23303e6f178ca2993bfde7114e6bdf48dd0eff9d/content/browser/indexed_db/indexed_db_transaction.cc


### pw...@chromium.org (2019-09-26)

I was able to reproduce on Chrome 77, and verify that the fix makes the ASAN crash go away. I was not able to reproduce on Chrome 78 or master -- I suspect that poc.html needs to be updated to match changes in the IndexedDB mojo interface.

In a successful run, the DevTools console has the following output:
upgradeNeeded
success key is called
successCursor called
AssociatedInterfacePtrInfo

Repro notes: poc.html needs to be copied in the build directory, as it relies on mojo JS files. The http:// server seems unnecessary -- serving the file from file:// also works. In other words...
autoninja -C out/Asan
cp ~/Downloads/poc.html out/Asan/poc.html
cd out/Asan
./chrome-wrapper --user-data-dir=/tmp/crbug1005753 --enable-blink-features=MojoJS ./poc.html

### pw...@chromium.org (2019-09-26)

awhalley@: Should this fix be merged into M77 as well?

Requesting merge into M78, as this is tagged as a high severity security bug.

### sh...@chromium.org (2019-09-26)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2019-09-26)

+adetaylor@ who frields such questions these days.

But yes, we should get this into 77 once it's had some more time in dev or beta.

### sr...@google.com (2019-09-26)

merge approved for M78, branch:3904

### ad...@chromium.org (2019-09-26)

Adding merge request for 77, and we can decide whether to put it into the upcoming security respin based on how much time it's had in dev/beta by then.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dd0d2d4c8f904da421b1dca81aff5ae70a1eb051

commit dd0d2d4c8f904da421b1dca81aff5ae70a1eb051
Author: Victor Costan <pwnall@chromium.org>
Date: Thu Sep 26 16:50:58 2019

IndexedDB: Unregister cursors from transactions more consistently.

IndexedDBCursor now calls IndexedDBTransaction::UnregisterOpenCursor()
in Close(), which is called by the destructor.

The previous setup missed an edge case where calling
IndexedDBCursor::Close() directly would not unregister the cursor. This
behavior was relied upon in IndexedDBTransaction::CloseOpenCursors(),
but was not intended at other callsites.

(cherry picked from commit 23303e6f178ca2993bfde7114e6bdf48dd0eff9d)

Bug: 1005753
Change-Id: I91944138d05faa2d91ecc03b1040ec16ca1a7e5f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1821675
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#699937}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1827481
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/branch-heads/3904@{#474}
Cr-Branched-From: 675968a8c657a3bd9c1c2c20c5d2935577bbc5e6-refs/heads/master@{#693954}

[modify] https://crrev.com/dd0d2d4c8f904da421b1dca81aff5ae70a1eb051/content/browser/indexed_db/indexed_db_cursor.cc
[modify] https://crrev.com/dd0d2d4c8f904da421b1dca81aff5ae70a1eb051/content/browser/indexed_db/indexed_db_transaction.cc


### sh...@chromium.org (2019-09-27)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-27)

We will take this for M77 Security respin after it soaks in M78 Beta next week.

### la...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### la...@google.com (2019-10-04)

merge approved for M77 branch 3865. please merge today as we are planning an M77 respin for 10/07.

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

 Congrats! The Panel decided to reward $20,000 for this report + a $500 fuzzing bonus :) 

### pw...@chromium.org (2019-10-04)

The CL has been merged to M77: https://crrev.com/c/1842038



### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-03)

pwnall@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-01-02)

This issue was migrated from crbug.com/chromium/1005753?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050168)*
