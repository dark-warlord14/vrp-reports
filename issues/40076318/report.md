# IndexedDB causes V8 heap corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40076318](https://issues.chromium.org/issues/40076318) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Blink>Storage>IndexedDB |
| **Reporter** | in...@chromium.org |
| **Assignee** | dc...@chromium.org |
| **Created** | 2012-09-19 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=110791598

Fuzzer: Inferno_layout_test_unmodified

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  void v8::internal::String::WriteToFlat<unsigned short>
  v8::internal::String::SlowTryFlatten
  v8::internal::FlattenGetString
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=157275:157317

Minimized Testcase (7.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94GG04k-97NkbgKEBnPyuvzuM-TVvolFHQdgEvR1Nkflrx9GVwyhg8M3Bl_TOVdZouO1l0mXRq5LWb-w_MZaP6HQn4GE0__CO5A3aqAOpzC2pdKYbiMk1sr8p1AOjChyOWAKsbf9FC_921FfXP0khXZvDhRr_xNLK62Lr0MOTGxka5seXg

## Attachments

- [v8_context_null_ptr_trace.txt](attachments/v8_context_null_ptr_trace.txt) (text/x-c++; charset=us-ascii, 2.9 KB)
- [tov8context_0ptr_repro.html](attachments/tov8context_0ptr_repro.html) (text/html; charset=us-ascii, 951 B)
- [tov8context_0ptr_improved_repro_linux_trace.txt](attachments/tov8context_0ptr_improved_repro_linux_trace.txt) (text/plain; charset=us-ascii, 1.3 KB)
- [tov8context_0ptr_improved_repro.html](attachments/tov8context_0ptr_improved_repro.html) (text/plain; charset=us-ascii, 599 B)
- [minimal.html](attachments/minimal.html) (text/html; charset=us-ascii, 498 B)

## Timeline

### in...@chromium.org (2012-09-19)

This one crashes on different addresses at different times, and reproduces on CF by running unmodified version of storage/indexeddb/structured-clone.html layout test using DumpRenderTree.

### ms...@chromium.org (2012-09-19)

I cannot get this to repro. Neither with the linked testcase nor with the unmodified storage/indexeddb/structured-clone.html. I tried both x64.debug and x64.release builds. Do you have further information on this?

### in...@chromium.org (2012-09-19)

The testcase reproduces beautifully for me (1 day old trunk), did you pass absolute path to DumpRenderTree. i ran asanified drt as - ./out/Release/DumpRenderTree /absolute_path_to_my_chrome/chrome-asan/src/third_party/WebKit/LayoutTests/storage/indexeddb/structured-clone.html

### cl...@chromium.org (2012-09-20)

ClusterFuzz has detected this issue as fixed in range 157666:157677.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=110791598

Fuzzer: Inferno_layout_test_unmodified

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  void v8::internal::String::WriteToFlat<unsigned short>
  v8::internal::String::SlowTryFlatten
  v8::internal::FlattenGetString
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=157275:157317
Fixed: https://cluster-fuzz.appspot.com/revisions?range=157666:157677

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94GG04k-97NkbgKEBnPyuvzuM-TVvolFHQdgEvR1Nkflrx9GVwyhg8M3Bl_TOVdZouO1l0mXRq5LWb-w_MZaP6HQn4GE0__CO5A3aqAOpzC2pdKYbiMk1sr8p1AOjChyOWAKsbf9FC_921FfXP0khXZvDhRr_xNLK62Lr0MOTGxka5seXg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-09-21)

from fixed range - https://trac.webkit.org/log/?verbose=on&stop_rev=129011&rev=129048&limit=1000, this looks be to fixed by the idb changes.

David, can you please tell what fixed it and also merge it to the m23 branch. it branched before these changes could get in.

### dg...@chromium.org (2012-09-24)

I can't reproduce this locally at either the first affected revision (cr157318 / wk128849) or the last (cr157665 / wk129011).  I tried both an asan-ified DRT and content_shell --single-process.

I'm not sure what else I can do.  I'd say that the fix, if we do ever find it, will not make today's dev cut.

### in...@chromium.org (2012-09-24)

It did reproduce locally for me, I am working with David on chat.

### dg...@chromium.org (2012-09-25)

While testing this I sometimes get this that looks like a separate v8 problem, not sure though.

AddressSanitizer global-buffer-overflow on address 0x000006e7e880 at pc 0x22f7190 bp 0x7fff88cf5bb0 sp 0x7fff88cf5ba8
READ of size 8 at 0x000006e7e880 thread T0
    #0 0x22f718f in v8::internal::VisitorDispatchTable<void (*)(v8::internal::Map*, v8::internal::HeapObject*)>::GetVisitor(v8::internal::Map*) /src/chrome/1/src/out_asan/Release/../../v8/src/objects-visiting.h:164
    #1 0x2375c8b in v8::internal::StaticMarkingVisitor<v8::internal::MarkCompactMarkingVisitor>::IterateBody(v8::internal::Map*, v8::internal::HeapObject*) /src/chrome/1/src/out_asan/Release/../../v8/src/objects-visiting.h:386
    #2 0x2374dda in v8::internal::MarkCompactCollector::EmptyMarkingDeque() /src/chrome/1/src/out_asan/Release/../../v8/src/mark-compact.cc:2206
    #3 0x238a6dd in v8::internal::RootMarkingVisitor::MarkObjectByPointer(v8::internal::Object**) /src/chrome/1/src/out_asan/Release/../../v8/src/mark-compact.cc:1821
    #4 0x2253bf1 in v8::internal::GlobalHandles::IterateWeakRoots(v8::internal::ObjectVisitor*) /src/chrome/1/src/out_asan/Release/../../v8/src/global-handles.cc:468
    #5 0x236fa95 in v8::internal::MarkCompactCollector::MarkLiveObjects() /src/chrome/1/src/out_asan/Release/../../v8/src/mark-compact.cc:2370
    #6 0x236f48e in v8::internal::MarkCompactCollector::CollectGarbage() /src/chrome/1/src/out_asan/Release/../../v8/src/mark-compact.cc:374
    #7 0x226c2bc in v8::internal::Heap::MarkCompact(v8::internal::GCTracer*) /src/chrome/1/src/out_asan/Release/../../v8/src/heap.cc:985
    #8 0x226af4e in v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer*) /src/chrome/1/src/out_asan/Release/../../v8/src/heap.cc:868
    #9 0x226aa13 in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const*, char const*) /src/chrome/1/src/out_asan/Release/../../v8/src/heap.cc:606
    #10 0x2224a0f in v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, char const*) /src/chrome/1/src/out_asan/Release/../../v8/src/heap-inl.h:440
    #11 0x226a60e in v8::internal::Heap::CollectAllGarbage(int, char const*) /src/chrome/1/src/out_asan/Release/../../v8/src/heap.cc:516
    #12 0x221f5ea in v8::internal::GCExtension::GC(v8::Arguments const&) /src/chrome/1/src/out_asan/Release/../../v8/src/extensions/gc-extension.cc:43
    #13 0x21cf7aa in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) /src/chrome/1/src/out_asan/Release/../../v8/src/builtins.cc:1146
    #14 0x2acda890618d in  
    #15 0x2acda8953948 in  
    #16 0x2acda8924006 in  
    #17 0x2acda89112d6 in  
    #18 0x221883b in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /src/chrome/1/src/out_asan/Release/../../v8/src/execution.cc:118
    #19 0x21885bb in v8::Script::Run() /src/chrome/1/src/out_asan/Release/../../v8/src/api.cc:1615
    #20 0x8cf737 in WebCore::V8GCController::collectGarbage() /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8GCController.cpp:507
    #21 0x56a1f2 in main /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Tools/DumpRenderTree/chromium/DumpRenderTree.cpp:252
    #22 0x7f742493b76c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226


### dg...@chromium.org (2012-09-25)

This is "fixed" by wk129037.  It really doesn't fix anything, just hides whatever the problem is.  I haven't narrowed down what revision introduced the problem, will do that tomorrow.

It would be glorious if someone from the v8 team could look at the stacktrace in https://crbug.com/chromium/150737#c8 and offer their opinion - is it a bug in v8's gc?

### da...@chromium.org (2012-09-25)

This might be a GC problem, Michael, care to comment on the GC crash with ASAN?

### gl...@chromium.org (2012-09-25)

Could https://crbug.com/chromium/151888 be related?
MarkCompactCollector seems to access random memory, so the report type (global buffer overflow or unknown crash) should not matter.

### ms...@chromium.org (2012-09-25)

About the stacktrace in https://crbug.com/chromium/150737#c8: This is most likely some sort of heap corruption. Without a repro or a minidump it is hard to tell what's causing the corruption. Let me know if you keep seeing this so I can look into it.

@glider: It is most likely not related to the issue you mentioned. The GC touches all of the V8 heap, so it basically is a big consistency checker for the heap and crashes whenever there is heap corruption of any sort.

### dg...@chromium.org (2012-09-25)

This started after http://trac.webkit.org/changeset/128789.

I'd like to know if this only affects DRT or also multi-process chrome. The issue doesn't show up in single-process chrome, which indicates that it doesn't affect multi-process chrome, but doesn't prove such a thing.

Running in an asan-ified chrome spews a million of the lines below before the renderer crashes.
Running in an asan-ified chrome --single-process works fine, no asan error.
Running in an asan-ified content_shell --single-process works fine, no asan error.
Running in an asan-ified content_shell spews a million of the lines below before the page stops loading even though it's blank.

==17731== AddressSanitizer CHECK failed: /usr/local/google/chrome/src/third_party/llvm/projects/compiler-rt/lib/sanitizer_common/sanitizer_linux.cc:168 "((proc_self_maps_buff_len_)) > ((0))" (0x0, 0x0)

inferno, is asan in multi-process chrome/content_shell unsupported?

### in...@chromium.org (2012-09-26)

dgrogan, you need to do two things. Upgrade binutils to ftp://sourceware.org/pub/binutils/snapshots/binutils.tar.bz2. this will fix the DWARF4 errors causing millions of lines.

For the CHECK failed, just run chrome with --no-sandbox, see also the flags in the ClusterFuzz report.

### dg...@chromium.org (2012-09-26)

I'm not getting any DWARF4 errors, just the CHECK. --no-sandbox fixed it.  I don't see any flags in https://cluster-fuzz.appspot.com/testcase?key=110791598.

When running chrome with --no-sandbox, structured-clone.html runs fine, no errors. So we can not worry about this issue, as it seems to be DRT-only, correct?

### in...@chromium.org (2012-09-26)

this is reproducing in drt because of use of eventsender. that should reproduce in the real world with Chrome in most cases with e.g. with real drag and drop.  I don't see anything else in testcase which might indicate a drt false positive.

if (self.eventSender) {
    var fileRect = fileInput.getClientRects()[0];
    var targetX = fileRect.left + fileRect.width / 2;
    var targetY = fileRect.top + fileRect.height / 2;
    eventSender.beginDragWithFiles(['resources/test-data.html', 'resources/test-data.txt']);
    eventSender.mouseMoveTo(targetX, targetY);
    eventSender.mouseUp();
}



### gl...@chromium.org (2012-09-26)

@mstarzinger: I wonder then whether ASan is actually right about the heap corruptions. How does the V8 garbage collector walk the heap? Can it somehow hit a freed memory region (e.g. by stepping on a dangling pointer) or read a global out of bounds?

### ms...@chromium.org (2012-09-26)

@glider: Yes, both is true. It can either follow a pointer that was corrupted or not updated (e.g. missing write barrier) or it could interpret an object incorrectly because it's hidden class got corrupted. Those are just two simple examples which we haven't seen in a long time, usually it's a little bit more intricate.

### dg...@chromium.org (2012-09-26)

[Empty comment from Monorail migration]

### dg...@chromium.org (2012-09-26)

[Empty comment from Monorail migration]

### dg...@chromium.org (2012-09-27)

I duped https://crbug.com/chromium/151744 and https://crbug.com/chromium/150667 against this bug.  More details forthcoming.

### dg...@chromium.org (2012-09-27)

We've gotten quite a few IDB crash reports[A] since http://trac.webkit.org/changeset/128789 landed. alecflett@ and I have looked at this for a few days and need some help.

haraken@ and abarth@, one suspect is the use of "any" in IDB{Cursor,ObjectStore}.idl. Could you look at the generated code and see if anything catches your eye?

V8 team, https://crbug.com/chromium/150737#c12 indicates that the minidumps in the crash reports could be helpful to you. Could someone take a look at them [A] and let us know what you think? Either if it's a v8 problem or some hints about where we should be looking.  mstarzinger@ wasn't too successful in reproducing this with an asan build, but there's now an alternate repro, provided by therealholden.

I've been able to reproduce crashes two ways. They both require syncing to cr157296 / wk128789.

1. Use the file and follow the directions from http://code.google.com/p/chromium/issues/detail?id=150667#c3.  Note that the breakpoint has to be on the request.onsuccess = function line, not on the document.write line. A regular, non-asan, static_library, debug content_shell crashes, you don't need full chrome.  Using an asanified content_shell gives the output at [B].
$ out/Debug/content_shell file:///$(readlink -f idb_onupgradeneeded_debug_crash.html)

2. Run an asan-enabled DRT as specified by cluterfuzz [C].  I had a tough time reproducing this with my usual local gyp variables. I had to change enable_svg from 0 to 1 and component from shared_library to static_library.
$ out_asan/Release/DumpRenderTree /src/chrome/1/src/third_party/WebKit/LayoutTests/storage/indexeddb/structured-clone.html

I've noticed that structured-clone.html is pretty robust against causing an asan error, slight changes make it not crash.  I've gotten a few different v8-y asan errors from it though [D].

Thanks for your help, we're a bit out of our element.

A. (sorry non-googlers, these probably won't work for you)
http://go/crash/reportdetail?reportid=3a89b05c59228c6d
http://go/crash/reportdetail?reportid=4404a1199eeff13c
http://go/crash/reportdetail?reportid=f546f471bfe9cdd1

B. http://www/~dgrogan/asan_debug_crash.txt

C. https://cluster-fuzz.appspot.com/testcase?key=110791598

D.
http://www/~dgrogan/asan-structured-clone1.txt
http://www/~dgrogan/asan-structured-clone2.txt
http://www/~dgrogan/asan-structured-clone3.txt
http://www/~dgrogan/asan-structured-clone4.txt

### ha...@chromium.org (2012-09-27)

> http://go/crash/reportdetail?reportid=4404a1199eeff13c
> http://go/crash/reportdetail?reportid=f546f471bfe9cdd1

These are crashing at adjustedContext(). I posted a (not so much helpful) comment here (http://code.google.com/p/chromium/issues/detail?id=150667#c9).

Taking a look...

### ha...@chromium.org (2012-09-27)

> haraken@ and abarth@, one suspect is the use of "any" in IDB{Cursor,ObjectStore}.idl. Could you look at the generated code and see if anything catches your eye?

- The generated code looks sane.
- http://trac.webkit.org/changeset/128789 is the culprit.
- I've not succeeded in reproducing the crash.
- I would guess that it might be a bug around V8Context, but I have no specific idea.



0x7fdc071e4c7e	 [chrome]	 - third_party/WebKit/Source/WebCore/bindings/v8/ScopedPersistent.h:55]	WebCore::WorldContextHandle::adjustedContext
0x7fdc071d0968	 [chrome]	 - third_party/WebKit/Source/WebCore/bindings/v8/V8Binding.cpp:301]	WebCore::toV8Context


At the very least, I'd like to know which of the following two lines (A or B) leads to the crash (I cannot judge it from the stack trace of the reported crashes):

  v8::Local<v8::Context> WorldContextHandle::adjustedContext(ScriptController* script) const
{
    ASSERT(m_worldToUse != UseWorkerWorld);
    if (m_worldToUse == UseMainWorld)
        return script->mainWorldContext();  /* (A) */

    ASSERT(!m_context->get().IsEmpty());  /* (B) */
    return v8::Local<v8::Context>::New(m_context->get());
  }


### [Deleted User] (2012-09-27)

I should also add that when we started using "any" (an alias for "DOMObject") we became the first users of 'any' without a custom binding - if you look through all the IDL in webkit, every single use of 'any' is also [Custom]

So at the very least it's probably worth investigating the generated code, since it was more or less previously untested. It's very possible that the heap corruption starts here, but is tickled by later accesses. it's worth thinking about all the different scenarios for how these methods could be called in the wild too - i.e. put(), put(value), put(NaN), put(value, key), etc.


Here it is for:

        [CallWith=ScriptExecutionContext] IDBRequest put(in any value, in [Optional] IDBKey key)
            raises (IDBDatabaseException);

static v8::Handle<v8::Value> putCallback(const v8::Arguments& args)
{
    INC_STATS("DOM.IDBObjectStore.put");
    if (args.Length() < 1)
        return throwNotEnoughArgumentsError(args.GetIsolate());
    IDBObjectStore* imp = V8IDBObjectStore::toNative(args.Holder());
    ExceptionCode ec = 0;
    {
    EXCEPTION_BLOCK(ScriptValue, value, ScriptValue(MAYBE_MISSING_PARAMETER(args, 0, DefaultIsUndefined)));
    if (args.Length() <= 1) {
        ScriptExecutionContext* scriptContext = getScriptExecutionContext();
        RefPtr<IDBRequest> result = imp->put(scriptContext, value, ec);
        if (UNLIKELY(ec))
            goto fail;
        return toV8(result.release(), args.Holder(), args.GetIsolate());
    }
    EXCEPTION_BLOCK(RefPtr<IDBKey>, key, createIDBKeyFromValue(MAYBE_MISSING_PARAMETER(args, 1, DefaultIsUndefined)));
    ScriptExecutionContext* scriptContext = getScriptExecutionContext();
    RefPtr<IDBRequest> result = imp->put(scriptContext, value, key.get(), ec);
    if (UNLIKELY(ec))
        goto fail;
    return toV8(result.release(), args.Holder(), args.GetIsolate());
    }
    fail:
    return setDOMException(ec, args.GetIsolate());
}


### ha...@chromium.org (2012-09-28)

> I should also add that when we started using "any" (an alias for "DOMObject") we became the first users of 'any' without a custom binding - if you look through all the IDL in webkit, every single use of 'any' is also [Custom]

Yes. (As far as I see the generate code, it looks sane though.)

Another big change of http://trac.webkit.org/changeset/128789 is that it starts using toV8Context() in the call path. As far as I look at the stack trace of the crashes, they are crashing at toV8Context(). So it would be helpful to investigate how toV8Context() is used in the patch. That's why I want to know which line of WorldContextHandle::adjustedContext() leads to the crashes. (Sorry, I'm failing reproducing the bug in my local machine.)


### dg...@chromium.org (2012-09-28)

When I run in Debug, the assertion at (C) fails.

v8::Local<v8::Context> WorldContextHandle::adjustedContext(ScriptController* script) const
{
    ASSERT(m_worldToUse != UseWorkerWorld);  /* (C) */
    if (m_worldToUse == UseMainWorld)
        return script->mainWorldContext();  /* (A) */

    ASSERT(!m_context->get().IsEmpty());  /* (B) */
    return v8::Local<v8::Context>::New(m_context->get());
  }

### ha...@chromium.org (2012-09-28)

[Empty comment from Monorail migration]

### dc...@google.com (2012-09-28)

I added the failing assertion recently while tracking down a strange error.  Those changes were not intended to change any functionality, and I don't believe that they do (except for triggering the assertion).  

### ha...@chromium.org (2012-09-29)

Yes. I think the assertion makes sense. The problem is not that you added the assertion but that we are hitting the assertion. (I'll look at it on Monday but I'm happy if anyone could also take a look.)

### dc...@google.com (2012-09-29)

Okay, so I reviewed my patch, and there is a slight change in behaviour.  Originally, a js callback from a worker could finish execution in the main world, and my change triggers an ASSERT in debug mode, but does a null dereference in non debug mode instead of allowing the execution in the main world, which I figured was a mild form of security violation.

### ha...@chromium.org (2012-10-01)

dcarney: Thanks. Let me confirm one thing. WorldContextHandle::adjustedContext() should not be called by a worker, and thus, the ASSERT(m_worldToUse != UseWorkerWorld) is needed, right? I mean, the bug is not that the assertion is there but that we are hitting the assertion. Am I understanding things correctly?

dgrogan, alecflett: If my understanding is correct, the bug would be that IDBDatabase::scriptExecutionContext() returns a wrong ScriptExecutionContext for a Worker.

Look at the following code:

// IDBDatabase.cpp
ScriptExecutionContext* IDBDatabase::scriptExecutionContext() const {
  return ActiveDOMObject::scriptExecutionContext();
}

// IDBRequest.cpp
void IDBRequest::onSuccess(...) {
  deserializeIDBValue(scriptExecutionContext(), serializedValue);
}

// IDBBindingUtilities.cpp
ScriptValue deserializeIDBValue(ScriptExecutionContext* scriptContext, PassRefPtr<SerializedScriptValue> prpValue) {
  v8::Context::Scope contextScope(toV8Context(scriptContext, UseCurrentWorld));
  ...;
}

// V8Binding.cpp
v8::Local<v8::Context> toV8Context(ScriptExecutionContext* context, const WorldContextHandle& worldContext) {
  if (context->isDocument()) { // For a worker, this branch should not be hit. However, actually, this branch is being hit by a worker. I think that this is the bug.
    if (Frame* frame = static_cast<Document*>(context)->frame())
      return worldContext.adjustedContext(frame->script());  // This method should not be called by a worker.
  } else if (context->isWorkerContext()) { // A worker should hit this branch.
    if (WorkerContextExecutionProxy* proxy = static_cast<WorkerContext*>(context)->script()->proxy())
      return proxy->context();
  }
}

dgrogan, alecflett: Would you check if IDBDatabase::scriptExecutionContext() returns a correct ScriptExecutionContext?

### dg...@chromium.org (2012-10-01)

The script that triggers the assertion at (C) from https://crbug.com/chromium/150737#c27, the script from http://code.google.com/p/chromium/issues/detail?id=150667#c3, doesn't run in a worker, or start one up at all.

### dc...@google.com (2012-10-01)

haraken: that's correct, adjustedContext must be called from a non worker ScriptExecutionContext.  toV8Context is designed to take care of that.

### dc...@google.com (2012-10-01)

haraken: also, that assertion indicates that the WorldContextHandle constructor was from a worker thread and the callback occurred in a non worker thread.

### dc...@google.com (2012-10-01)

Perhaps the problematic line is:

            if (UNLIKELY(!V8DOMWrapper::isWrapperOfType(toInnerGlobalObject(context), &V8DOMWindow::info))) {

in WorldContextHandle::WorldContextHandle.

This assumes that a context with innerGlobalObject of type != V8DOMWindow is a worker and marks the handle as a worker at that point.  If there is another option here for innerGlobalObject for a context, then this is definitely an issue.  I copied this check from somewhere else, so I just assumed it was correct.



### dg...@chromium.org (2012-10-01)

We create some other context objects here, are those getting confused with worker objects?

http://code.google.com/searchframe#OAMlx_jo-ck/src/third_party/WebKit/Source/WebCore/bindings/v8/IDBBindingUtilities.cpp&exact_package=chromium&q=deserializeidbvalue&type=cs&l=213

ScriptValue deserializeIDBValue(ScriptExecutionContext* scriptContext, PassRefPtr<SerializedScriptValue> prpValue)
{
    v8::HandleScope handleScope;
    v8::Context::Scope contextScope(toV8Context(scriptContext, UseCurrentWorld));
    return ScriptValue(prpValue->deserialize());
}

### dg...@chromium.org (2012-10-01)

deserializeIDBValue (from https://crbug.com/chromium/150737#c37) is on the call stack when that assertion fails:

    #0 0x7fc6492f424b in WebCore::WorldContextHandle::adjustedContext(WebCore::ScriptController*) const ???:0
    #1 0x7fc6491692ca in WebCore::toV8Context(WebCore::ScriptExecutionContext*, WebCore::WorldContextHandle const&) ???:0
    #2 0x7fc648f07b61 in WebCore::deserializeIDBValue(WebCore::ScriptExecutionContext*, WTF::PassRefPtr<WebCore::SerializedScriptValue>) ???:0
    #3 0x7fc64885bb34 in WebCore::IDBRequest::onSuccess(WTF::PassRefPtr<WebCore::SerializedScriptValue>) ???:0
    #4 0x7fc643761d5c in WebKit::WebIDBCallbacksImpl::onSuccess(WebKit::WebSerializedScriptValue const&) /src/chrome/1/src/out_asan/Debug/../../third_party/WebKit/Source/WebKit/chromium/src/WebIDBCallbacksImpl.cpp:95
...
...

### dc...@google.com (2012-10-02)

Created potential patch to fix the problem:

https://bugs.webkit.org/show_bug.cgi?id=98108

The use of toV8Context(scriptContext, UseCurrentWorld) in deserializeIDBValue is quit unusual to begin with.  Depending on where it's called from, it's totally possible that v8::Context::GetCurrent() should be used there instead.

### ha...@chromium.org (2012-10-02)

Thanks dcarney!

dgrogan, alecflett: Would you check if the patch (https://bugs.webkit.org/show_bug.cgi?id=98108) fixes the crash?

### bu...@chromium.org (2012-10-02)

https://bugs.webkit.org/show_bug.cgi?id=98108

### dg...@chromium.org (2012-10-03)

That patch fixes the crash I get via the repro at http://code.google.com/p/chromium/issues/detail?id=150667#c3 but the asan DRT crash remains, with this stack:

==22576== ERROR: AddressSanitizer crashed on unknown address 0x000000000027 (pc 0x7f807f58b7d8 sp 0x7fff5ec64f30 bp 0x7fff5ec64f30 T0)
AddressSanitizer can not provide additional info.
    #0 0x7f807f58b7d7 in v8::internal::FixedArray::get(int) /src/chrome/1/src/out_asan/Release/../../v8/src/objects-inl.h:1692
    #1 0x7f807f778c3f in v8::internal::Isolate::native_context() /src/chrome/1/src/out_asan/Release/../../v8/src/isolate.cc:1346
    #2 0x7f807f5b2671 in v8::Context::GetCurrent() /src/chrome/1/src/out_asan/Release/../../v8/src/api.cc:4498
    #3 0x7f8079e179b0 in WebCore::WorldContextHandle::WorldContextHandle(WebCore::WorldToUse) ???:0
    #4 0x7f8079d7414a in WebCore::deserializeIDBValue(WebCore::ScriptExecutionContext*, WTF::PassRefPtr<WebCore::SerializedScriptValue>) ???:0
    #5 0x7f8079c2c2e5 in WebCore::IDBRequest::onSuccess(WTF::PassRefPtr<WebCore::SerializedScriptValue>) ???:0


### dc...@google.com (2012-10-03)

There was a slight issue with that patch. I can fix that, but knowing the correct context for the call to deserializeIDBValue would be a better fix.  The current call to find a context is quite expensive.  Since I don't know the IDB code, there's not much I can do here.  I notice that V8PerIsolateData::current()->ensureAuxiliaryContext(), which might be the context causing the issue.  If that is always being used, for instance, it would be much faster to just use that.

### dc...@google.com (2012-10-03)

I've submitted a corrected patch which I expect will stop the errors if someone wants to try it.

### [Deleted User] (2012-10-03)

taking a look now


### [Deleted User] (2012-10-03)

ok, I tried the patch and I'm still pretty consistently crashing both with and without it.

The way to reproduce with an ASAN build:

1) build an ASAN build as per http://www.chromium.org/developers/testing/addresssanitizer
2) copy down fuzz-lyt-structured-clone1347969945.15.html from the fuzz linked above into LayoutTests/storage/indexeddb/
3) run layout tests against this file:
new-run-webkit-tests --chromium storage/indexeddb/fuzz-lyt-structured-clone1347969945.15.html --no-retry

You'll pretty consistently crash. The stack is a little different every time. Usually the first 8 frames are garbage:
STDERR:     #0 0x840e6651201 in  
STDERR:     #1 0x840e6650ff7 in  
STDERR:     #2 0x840e660a74d in  
STDERR:     #3 0x840e6643c96 in  
STDERR:     #4 0x840e660a74d in  
STDERR:     #5 0x840e664fb8f in  
STDERR:     #6 0x840e664a734 in  
STDERR:     #7 0x840e6624006 in  
STDERR:     #8 0x840e66112d6 in  

Then frame #9 is somewhere in v8, often in Invoke:
STDERR:     #9 0x22a00db in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /usr/local/google/home/alecflett/chrome/src/out/Release/../../v8/src/execution.cc:118
STDERR:     #10 0x221e4bf in v8::Function::Call(v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /usr/local/google/home/alecflett/chrome/src/out/Release/../../v8/src/api.cc:3662

but the stack is of varying depth.

### ka...@google.com (2012-10-04)

[Empty comment from Monorail migration]

### ka...@google.com (2012-10-04)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-10-04)

Status: Started, but by whom? :) alecflett?

### ka...@google.com (2012-10-04)

can't assign to dcarney@google.com since he's not a project member but i assume he's the one who's been workig on it.

### jk...@chromium.org (2012-10-04)

@https://crbug.com/chromium/150737#c46: Those "garbage" frames are generated code. I can take a look at what's going on there (could be a real bug in V8, or could be the generated code stumbling over a broken object that got passed in via the API or got corrupted later on; either way it potentially provides some leads). Which version of Chromium do I need to build? Do I need to apply any patches or non-standard WebKit/V8 revisions?


### [Deleted User] (2012-10-04)

jkummerow@ - nope, standard ToT of chromium + webkit build will get you this crash. (See https://crbug.com/chromium/150737#c46)



### jk...@chromium.org (2012-10-05)

I'm not seeing any crashes (tried a handful of times). Instead, the test times out, without any CPU load. Here's what I did:

- updated Chrome (that pulled r160341, according to DEPS WebKit is at r130452 and V8 at r12514)
- built a Release build of DumpRenderTree following the instructions at http://www.chromium.org/developers/testing/addresssanitizer
- copied the test file as per #46 and ran third_party/WebKit/Tools/Scripts/new-run-webkit-tests --chromium storage/indexeddb/fuzz-lyt-structured-clone1347969945.15.html --no-retry

### [Deleted User] (2012-10-05)

jkummerow@ - please keep trying - we haven't changed anything on our end, but now I can't reproduce the crash either - but I could yesterday very reliably - one thing that I messed around with was --time-out-ms=60000 - I think ASAN slows the build down significantly.

dgrogan was also finding that the test was incredibly sensitive to slight changes in code - i.e. he'd remove one random line or add one random line of JS and it would drastically change the probability that it would fail.. can you try messing with the test itself - just adding or removing one line to see if you can get it to crash (if I come up with something that makes it crash again.



### dg...@chromium.org (2012-10-08)

Three separate points.

1) dcarney, you say "knowing the correct context for the call to deserializeIDBValue would be a better fix" - how would we do that?  Is it something that would be changed in IDB code or V8 code?  I.e. something that should be changed in an IDB file from http://trac.webkit.org/changeset/128789 or would one of the V8 files from http://wkb.ug/98108 be changed?

2) I can only reproduce the asan error when synced to cr157296/wk128789/v812514 - not at ToT.  I also had to reset most of my ~/.gyp/include.gypi.  It is now as follows.  I think you need to specify 'component': 'static_library' explicitly; only commenting the shared_library line is probably insufficient.
{
  'variables': {
    'component': 'static_library',
#    'component': 'shared_library',
#    'remove_webcore_debug_symbols': 1,
#    'disable_nacl': 1,
#    'enable_svg': 0,
#    'enable_webrtc': 0,
  },
}

My out_asan/Release/build.ninja is at http://www/~dgrogan/build.ninja.  Differences in yours and mine might explain why you can't reproduce.

3) Patch 166888 from https://bugs.webkit.org/show_bug.cgi?id=98108 again fixes the content_shell crash, but not the asan error:
$ out_asan/Release/DumpRenderTree /src/chrome/1/src/third_party/WebKit/LayoutTests/storage/indexeddb/structured-clone.html 2>&1 | tools/valgrind/asan/asan_symbolize.py `pwd`/  | c++filt

==26197== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x27cfd464e4a2 sp 0x7fff5a9f4230 bp 0x7fff5a9f4248 T0)
AddressSanitizer can not provide additional info.
    #0 0x27cfd464e4a1 in  
    #1 0x27cfd464e297 in  
    #2 0x27cfd460a74d in  
    #3 0x27cfd4640fb6 in  
    #4 0x27cfd460a74d in  
    #5 0x27cfd464ce2f in  
    #6 0x27cfd4647af4 in  
    #7 0x27cfd4624006 in  
    #8 0x27cfd46112d6 in  
    #9 0x2219a1b in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /src/chrome/1/src/out_asan/Release/../../v8/src/execution.cc:118
    #10 0x2197b2f in v8::Function::Call(v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /src/chrome/1/src/out_asan/Release/../../v8/src/api.cc:3662
    #11 0x880b76 in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext*, v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:235
    #12 0x8806ac in WebCore::ScriptController::callFunction(v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:188
    #13 0x8cdde2 in WebCore::V8EventListener::callListenerFunction(WebCore::ScriptExecutionContext*, v8::Handle<v8::Value>, WebCore::Event*) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8EventListener.cpp:95
    #14 0xe3293f in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext*, WebCore::Event*, v8::Handle<v8::Value>) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:142
    #15 0xe32504 in WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext*, WebCore::Event*) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:102
    #16 0x157e1d6 in WebCore::EventTarget::fireEventListeners(WebCore::Event*, WebCore::EventTargetData*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/dom/EventTarget.cpp:231
    #17 0x157dd76 in WebCore::EventTarget::fireEventListeners(WebCore::Event*) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/dom/EventTarget.cpp:198
    #18 0x10357fb in WebCore::IDBEventDispatcher::dispatch(WebCore::Event*, WTF::Vector<WTF::RefPtr<WebCore::EventTarget>, 0ul>&) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/Modules/indexeddb/IDBEventDispatcher.cpp:54
    #19 0x104f6f1 in WebCore::IDBRequest::dispatchEvent(WTF::PassRefPtr<WebCore::Event>) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/Modules/indexeddb/IDBRequest.cpp:476
    #20 0x104fcfc in non-virtual thunk to WebCore::IDBRequest::dispatchEvent(WTF::PassRefPtr<WebCore::Event>) ???:0
    #21 0x15534db in WebCore::DocumentEventQueue::dispatchEvent(WTF::PassRefPtr<WebCore::Event>) /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/dom/DocumentEventQueue.cpp:165
    #22 0x1552f0c in WebCore::DocumentEventQueue::pendingEventTimerFired() /src/chrome/1/src/out_asan/Release/../../third_party/WebKit/Source/WebCore/dom/DocumentEventQueue.cpp:155


### dg...@chromium.org (2012-10-08)

[Empty comment from Monorail migration]

### th...@chromium.org (2012-10-10)

Also seeing this on 24.0.1284.2 - top renderer crasher on Linux. e.g. http://go/crash/reportdetail?reportid=f47cc53ef743ff6d

### dg...@chromium.org (2012-10-10)

http://go/crash/reportdetail?reportid=f47cc53ef743ff6d doesn't show IDB anywhere in the stack trace, I'm not sure it's the same issue.

### dh...@chromium.org (2012-10-11)

v8::internal::Isolate::MayNamedAccess crash spiked up in 1290.1 Mac dev channel build. All the crashes are from docs.google.com. 

https://crash.corp.google.com/reportdetail?reportid=6975eb707d833354#crashing_thread

### dg...@chromium.org (2012-10-12)

I posted a tiny change that makes both reproduction cases no longer reproduce for me.  I think this is what dcarney@ was talking about.

https://bugs.webkit.org/show_bug.cgi?id=99131


### js...@chromium.org (2012-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2012-10-12)

I really thought this was assigned to someone on v8... everything looks kosher on the IDB side. I'm going to start with haraken, and if everything looks right in bindings, less pass this on...

### ha...@chromium.org (2012-10-14)

dcarney: I thought you're making a patch for the fix. How is it going?

### th...@gmail.com (2012-10-17)

The (duplicate?) https://crbug.com/chromium/154867 (similar WorldContextHandle::adjustedContext trace) has a script that looks like the first repro of https://crbug.com/chromium/150667 (https://crbug.com/chromium/150737#c22).

### la...@google.com (2012-10-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-18)

[Empty comment from Monorail migration]

### ka...@google.com (2012-10-19)

is there a fix for this? we're still seeing this very high in m23 mac.



### js...@chromium.org (2012-10-19)

[Empty comment from Monorail migration]

### dc...@chromium.org (2012-10-22)

I've uploaded a patch that removes all calls to auxilliaryContext, which is the underlying problem. I can't repro this issue locally. Could someone who can please test this?  https://bugs.webkit.org/show_bug.cgi?id=99975

### db...@google.com (2012-10-22)

Thanks for the patch!  With this issue generally you're unlikely to get a definitive fixed/not fixed - the issues are too intermittent.  Suggest that your default practice be to introduce new instrumentation with each fix like this, so it can be 'tested in production'.  Known problem areas should end up crammed with it.  This is what we do in docs for hard to pin down issues.  It's frustrating and the turnaround time is slow, but it's the only thing that's eventually going to convince you that the issue is really gone.  People don't typically hit forums or whatever when our webapps break, they vote with their feet.

### ka...@google.com (2012-10-26)

[Empty comment from Monorail migration]

### dh...@google.com (2012-10-27)

In 24.0.1305.3 dev channel for Mac, 'v8::internal::Isolate::MayNamedAccess' is #1 renderer crash. Is there anything we could do to fix this?

https://chromecrash.corp.google.com/browse?q=product.name%3D'Chrome_Mac'%20AND%20product.version%3D'24.0.1305.3'%20AND%20custom_data.ChromeCrashProto.ptype%3D'renderer'%20AND%20custom_data.ChromeCrashProto.magic_signature_1.name%3D'v8%3A%3Ainternal%3A%3AIsolate%3A%3AMayNamedAccess'

### js...@chromium.org (2012-10-27)

Fixes are being discussed in the linked WebKit bug. 

### js...@chromium.org (2012-10-29)

Root cause is two WebKit patches that landed in M23 and on which significant refactoring has been done since:

http://trac.webkit.org/changeset/128379
http://trac.webkit.org/changeset/128789

Now that we understand the issue, dcarney@ has posted a patch in https://bugs.webkit.org/show_bug.cgi?id=99975 that looks like it's headed in the right direction.

Once we're happy with that patch it should be possible to apply to M23. 

Alternately, we can explore reverting the above two changesets from M23. omahaproxy.appspot.com reports that the branch point was webkit r128938 and I don't see any other patches that would need to be reverted.


### ka...@google.com (2012-10-29)

being that we're cuttng m23 stable today/tomrorow, can we revert those two CLs on m23 without any negative side effects?

### ka...@google.com (2012-10-29)

so for m23, we went with a revert of both patches.

### ka...@google.com (2012-10-29)

moving to m24 since it's still an issue for m24.

### sc...@gmail.com (2012-10-29)

Ok. Re-flagging as M24.

### js...@chromium.org (2012-10-30)

dharani@ - http://trac.webkit.org/changeset/132922 should be merged to M24 if it didn't make the cut.


### dh...@google.com (2012-10-30)

M24 was cut at webkit r132834. We need to merge r132922 to M24. Please wait until I branch webkit.

### dh...@google.com (2012-10-30)

Karen merged the webkit change at r132934

### ka...@google.com (2012-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2012-10-31)

so if I'm looking at http://trac.webkit.org/changeset/132934 correctly, M24 is good to go here - no extra merge requests or anything?

### ke...@chromium.org (2012-11-02)

[Empty comment from Monorail migration]

### dg...@chromium.org (2012-11-07)

I think this is fixed. Objections?

### dh...@chromium.org (2012-11-07)

Though the crashes from worker process is gone, we still have these crashes in renderer process which were happening in http://docs.google.com

https://crash.corp.google.com/reportdetail?reportid=0f8e446a33dbfba6#crashing_thread

### dh...@chromium.org (2012-11-07)

Oops.. we still have similar crash in worker process but its very low.

### dh...@google.com (2012-11-20)

13% of Mac renderer crashes are due to this. Is there a simple fix to reduce the crash volume?

https://chromecrash.corp.google.com/browse?q=product.name%3D'Chrome_Mac'%20AND%20product.version%3D'24.0.1312.14'%20AND%20custom_data.ChromeCrashProto.ptype%3D'renderer'%20AND%20custom_data.ChromeCrashProto.magic_signature_1.name%3D'v8%3A%3Ainternal%3A%3AIsolate%3A%3AMayNamedAccess'

### ab...@chromium.org (2012-11-20)

On which branch?  This bug should be fixed on trunk.

### dh...@google.com (2012-11-20)

This is M24 beta which has webkit r132922 fix merged at r132934.

### dh...@google.com (2012-11-20)

This crash isn't completely gone in trunk too. In 25.0.1330.0, which is latest canary, has this crash - https://crash.corp.google.com/reportdetail?reportid=23570bca8eb7e8d8#crashing_thread

### [Deleted User] (2012-11-20)

one observation here: 100% of crashes for this is docs.google.com - and docs.google.com is one of the few properties that we're aware of that use workers + idb.

We've double-checked that, especially on trunk, that IDB is "doing the right thing" at least as far as honoring the world/scriptexecutioncontext that we're supposed to. I'm beginning to suspect something is wrong with worker's event queues or something.

### [Deleted User] (2012-11-20)

More observations after looking at the data deeper.
1) documents spans stuff both inside (/a/google.com) outside (/a/otherdomains.com) and public (no /a/) documents. 
2) most urls tend to crash at most once
3) most users tend to crash at most once.

Or to think of it another way, out of ~200 reports, only a few (<10) users and a few (<10) urls crash more than once.

My intuition is that this crash is semi-random - meaning it's not a reproducable, do-this-and-crash case - that there is some kind of gradual transition to a bad state - I would expect that if your doc crashed, and you got the sad tab page, you'd hit reload immediately... so assuming users are doing this, they aren't crashing again. If that doc or that user was doing something that tended to crash, then we'd likely see more 

The other thing: I only see a single crash on linux due to this, and I'm kind of assuming that the product.name="Chrome" crashes are windows. Assuming that's the case, we're seeing about 60% mac, and the windows crashes tend not to even have IDB in the stack. (in fact out of 10 windows crashes that I spot checked, only 1 had IDB in the stack like the others)

I'm more and more thinking we're looking at a v8 crash of some kind... and one that only manifests itself on Mac.. do we have fuzzers on mac?


### [Deleted User] (2012-11-20)

oh and one last bit: the crashes are always using the DocumentEventQueue, so what I said with workers may not be entirely correct. 

### dg...@chromium.org (2012-11-21)

dbk, what does docs do with IDB in the renderer process?  I thought docs only used IDB in the worker process.

### dc...@chromium.org (2012-11-21)

This may be same problem I describe in: https://bugs.webkit.org/show_bug.cgi?id=101725, but it's impossible to say from the stacktraces alone.

At the moment, there is a bug (https://bugs.webkit.org/show_bug.cgi?id=101573) which I can't land because of 101725 which stops WorldContextHandle from choosing the main world in the absence of a v8 context. It should call CRASH(), as this behaviour is very wrong.

The only place I can find which could generate this issue is in ExecutableWithDatabase::start in the InspectorIndexedDBAgent. But there may be others. If we add the CRASH(), we can at least figure out whether this is the problem and where it is starting rather than trying to figure it out way downstream.

### dc...@chromium.org (2012-11-23)

[Empty comment from Monorail migration]

### dc...@chromium.org (2012-11-23)

I've added the CRASH to enable early detection of the problem, do in so doing I had to introduce a hack in inspector which works around that CRASH. I'm hoping we'll see the CRASHes now instead of v8::MayNamedAccess in the crash reports, but if we continue to see v8 code in the stack, then my theory is that the problem is coming from the inspector hack.

### yu...@chromium.org (2012-11-26)

[Empty comment from Monorail migration]

### db...@google.com (2012-11-26)

In answer to dgrogan@, we do plenty of IDB work in the render process.  On online-start, the render process syncs the document.  On offline-start, it reads the document model.  During editing while offline it writes incoming mutations to a queue.  In both cases it maintains a lock, regularly writing a record to keep the shared worker and other tabs showing the same document from interfering.  The 'bulk syncer' (which runs in a shared worker, kept active by a background page) only synchronizes documents which aren't currently opened in a tab.

### in...@chromium.org (2012-12-05)

Is the security problem resolved by https://bugs.webkit.org/show_bug.cgi?id=101573 ? Can we close this bug now ?

### js...@chromium.org (2012-12-06)

I see a few more crashes which look like they come after dcarney's change. All from docs, on mac, identical stacks:

https://crash.corp.google.com/reportdetail?reportid=c5f1dd4ddc5ff2c3 25.0.1350.0
https://crash.corp.google.com/reportdetail?reportid=bd7962e7bddffaf4 25.0.1338.0
https://crash.corp.google.com/reportdetail?reportid=778da5f3790a20ee 25.0.1337.0
https://crash.corp.google.com/reportdetail?reportid=327d64ef95d0ba93 25.0.1337.0 



### in...@chromium.org (2012-12-12)

Will http://trac.webkit.org/changeset/135513 fix anything ? Does it make sense to merge this to m24 ? Do we want to file a new bug for crashes in c#102, if we know the regressing changeset, we should probably revert for m24.

### dc...@chromium.org (2012-12-12)

http://trac.webkit.org/changeset/135513 doesn't fix any problems. It should just crash earlier in a secure way if we have certain bugs (which we had earlier). It's still possible that these crashes originate in the inspector, but it's impossible to tell from the stack traces.  If so, I had to introduce the new crashes (which would look the same as the old ones) in https://bugs.webkit.org/show_bug.cgi?id=101725.  The only way to tell would be to revert 101725, but that would almost certainly cause inspector crashes (albeit non security hole crashes).

### in...@chromium.org (2012-12-12)

We don't want to ship this security regression into stable. Null or non-security crashes are better than shipping with a security hole. Why don't we give reverting 101725 a shot and monitor the crash metrics. These security crashes are also hit by user, so I don't we are saving user from crashing as well.

### th...@gmail.com (2012-12-14)

I was working on a simple repro of a different (webworker related to https://crbug.com/chromium/153913) crash when a 0-ptr "toV8Context" renderer crash popped up. Somehow this may be related to the changeset mentioned in #104. If it isn't, it is just a small new non-security renderer issue.

It seems to repro reliably with the inspector open.

### th...@gmail.com (2012-12-15)

Tested with ToT Version 25.0.1359.0 (172836) and also reproduces without the JavaScript debugger.

The crash seems to be timing related, so if it does repro reliably, some tweaking may be necessary. Also removing the "createIndex" part will make the crash disappear (like with https://crbug.com/chromium/150667).



### js...@chromium.org (2012-12-15)

[Comment Deleted]

### js...@chromium.org (2012-12-15)

[Comment Deleted]

### th...@gmail.com (2012-12-15)

[Comment Deleted]

### th...@gmail.com (2012-12-16)

[Empty comment from Monorail migration]

### dc...@chromium.org (2012-12-17)

The stack trace in #111 indicates that this is a new non-security issue.

### rb...@chromium.org (2012-12-17)

[Empty comment from Monorail migration]

### yu...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-01-06)

Please use this bug to discuss the security problem(memory corruption) issue. For the null ptr functional crashes, please file a separate functional bug. Also, it will be great if we can prioritize on the security vulnerability.

### th...@gmail.com (2013-01-06)

Ok, I filed the 0-ptr crash as https://crbug.com/chromium/168503. 

I only posted it here, because the c#23 (ASAN corruption) repro resembles the 0-ptr repro very closely (IDB createIndex triggers it) and is also a regression that started somewhere after the current stable version.


### ke...@google.com (2013-01-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-01-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2013-01-15)

[Empty comment from Monorail migration]

### ze...@chromium.org (2013-01-17)

this is now top extension process crash on ChromeOS (M25):

https://chromecrash.corp.google.com/browse?q=product.name%3D'Chrome_ChromeOS'%20AND%20product.version%3D'25.0.1364.33'%20AND%20custom_data.ChromeCrashProto.ptype%3D'extension'

### rs...@chromium.org (2013-01-22)

[Empty comment from Monorail migration]

### ke...@google.com (2013-01-25)

Updates here?

### db...@google.com (2013-01-25)

Crashes and corrupted databases are still routinely being reported by docs offline users.  We really need this thing stable ASAP, our plans call for document loading from IDB to get a lot more popular this year.  If there's anything we can do to help gather data from failures observed in the field please say so.

### [Deleted User] (2013-01-25)

this really has nothing to do with disk corruption - this is heap corruption in the V8 engine. dcarney@ is still working on this, I thin jsbell just pinged him recently...

jsbell also recently found a crash (https://crbug.com/chromium/168503) in dispatchEvent - in that case we had a guaranteed null pointer but the root of the problem was that events were getting dispatched after shutdown began. (i.e. the request got told to stop, but then the message queue kept pumping its events)

This could be related to that - at least in the previous case we were guaranteed that stop() was called, which nulled out a pointer. But the message queue might still be feeding us event, or maybe stop() hasn't *yet* been called? [Up until this point we have reduced frequency of this and similar crashes by fixing up the ScriptExecutionContext/CurrentWorld -> v8::Context binding)

### sc...@gmail.com (2013-01-25)

I wonder if the heap corruption bugs in our database code might leak to the disk corruption events ;-)

### mi...@chromium.org (2013-01-25)

> I wonder if the heap corruption bugs in our database code might leak to the disk corruption events ;-)

Definitely could for WebSQL but should not be the case for IDB where the process with the busted heap is not responsible for writing data to disk. Could get invalid data in there, but not database corruption.

### dc...@chromium.org (2013-01-25)

We've recently tried to inject some intentional crashes in v8 in order to stop the issue from being a security bug, so it might not show up in the canaries anyway (I haven't checked recently), but with no reliable repro, we've gotten nowhere trying to track the cause of this bug down.

### rs...@chromium.org (2013-01-28)

[Empty comment from Monorail migration]

### dg...@chromium.org (2013-01-29)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-29)

[Empty comment from Monorail migration]

### dh...@chromium.org (2013-01-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-01-30)

To consolidate a bit of data, which probably isn't valuable but maybe will catch someone's eye.

The bug therealholden@ noted in #111 was fixed over in https://crbug.com/chromium/168503 and turned out to be due to a race condition during Worker shutdown. The specific stack was unrelated to the root cause. Since v8's not involved at all it's unlikely (but not inconceivable) that it's related, except for general heap stomping potential.

Per private email, therealholden@ also filed 172240 with a related repro/different stack. I don't have permission to view. From email discussion, also relates to Worker lifecycle edge cases. Ditto to likelihood of being involved.

Closer to v8 (but NOT workers), I've been struggling to repro https://crbug.com/chromium/165671 which shows up as wkbug.com/105363 - the limited data (see the WebKit bug) points to something wonky with the binding code, but I can't force it to repro outside the bots. The bug that occasionally triggers the failure on the bots does not appear to be unique in what it does other than exercising the v8 heap and binding/wrapper code a little more than other tests.


### ke...@google.com (2013-02-05)

What's left to do here for 25?

### in...@chromium.org (2013-02-11)

what is the point of keeping this open when we have other tracking bugs like 172240 ?

### ha...@chromium.org (2013-02-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-02-26)

dcarney, jsbell: This looks like a centi-thread for https://crbug.com/chromium/178151. What is the current status?

(Would you cc me on https://crbug.com/chromium/172240? It looks like this bug was marked as WONTFIX due to 172240.)


### dc...@chromium.org (2013-02-26)

haraken: I'm currently trying to fix a known issue where indexdb causes heap corruption.  With any luck, this bug will go away with that fix, but it's completely impossible to say, since it's almost certainly gc-dependent.

### js...@chromium.org (2013-02-26)

dcarney@ - is there anything anyone can do to help with the investigation? 

### ha...@chromium.org (2013-02-26)

Thanks, Dan. I discussed with jsbell just right now. Our guess is that:

- The bug has existed for a long time.
- Half a year ago, Dan refactored V8 binding, which exposed the bug.
- M25 was launched. We observed the bug.
- Two month ago, Tomas added the security check. This hid the bug.
- M26 was launched. We didn't observe the bug, although the bug still exists potentially.


### ms...@chromium.org (2013-02-26)

jsbell: I have recently added zapping of disposed persistent handles to V8 in debug mode that flushes out use-after-dispose situations for those handles. Unfortunately the zapping is disabled because several IndexedDB test cases fail with this. This is also what dcarney@ is currently looking into. So for investigative purposes I strongly suggest to turn on the zapping manually (i.e. by removing the "_TODO" postfix in the ifdex). I'm gonna enabled the zapping as soon as dcarney@ was able to fix all issues that make the IndexedDB tests fail.

https://code.google.com/p/v8/source/detail?r=13680

### dc...@chromium.org (2013-02-26)

haraken: I think the bug was introduced in http://trac.webkit.org/changeset/128789, and that's what i'm fixing now. I don't see any similar traces before that although I may be wrong about that.  It is the use after free problem mstarzinger describes. Was the bug really hidden by the introduction of the security check?

### ha...@chromium.org (2013-02-26)

> Was the bug really hidden by the introduction of the security check?

This is just our guess. The security check ensures that a freed wrapper or a realloced wrapper is not returned to V8. (i.e. if a wrapper we are about to return has a wrong type, we return an empty wrapper to V8.) So it might have hidden the bug, though I'm not sure.

Either way it would be best if we can reproduce the bug by enabling the zapping.


### sc...@gmail.com (2013-02-26)

I though the security check did a CRASH() if it detects a bad object? This might accentuate, and not hide the bug.

### la...@google.com (2013-02-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-02-26)

> I though the security check did a CRASH() if it detects a bad object? This might accentuate, and not hide the bug.

Good point. You're right.

### ha...@chromium.org (2013-02-26)

> I though the security check did a CRASH() if it detects a bad object? This might accentuate, and not hide the bug.

Good point. You're right.

### js...@chromium.org (2013-02-27)

mstarzinger: awesome, thanks.

### js...@chromium.org (2013-02-27)

Attached a minimal repro that exhibits the crash with global handle zapping enabled.

It's the IDBRequest.release access with a ScriptValue as the IDBAny type that seems to do it. I'm suddenly hopeful that it's the same root cause as the elusive http://crbug.com/165671 crash that haraken@ and I were trying to debug yesterday.

### dc...@chromium.org (2013-02-27)

Any call to IDBAny that returns a scriptvalue returns a disposed handle, which causes heap corruption when a gc occurs before it's used. This flaw is fixed in https://bugs.webkit.org/show_bug.cgi?id=110206 which i can't get in until i land some patches in chrome.  I hope to get it relanded by Friday.

### js...@chromium.org (2013-02-27)

That's great news. We weren't aware of https://bugs.webkit.org/show_bug.cgi?id=110206 but bogisity in ScriptValue copying matches the conclusion we were coming to here. alecflett@ was working on a patch that eliminates ScriptValue copies made by IDBAny which resolves most of the crashes, but it sounds like you have the more fundamental fixes in flight.

This is also exactly the behavior I was seeing with http://crbug.com/165671	http://wkbug.com/105363 when I could briefly repro it - a GC at exactly the right time after an IDBAny/ScriptValue access would lead to use-after-free.


### [Deleted User] (2013-02-27)

Also see http://wkb.ug/111002 which adds some cleanup to IDB that ends up avoiding most of the ScriptValue copying in IDB altogether.

### js...@chromium.org (2013-02-27)

[Empty comment from Monorail migration]

### dc...@chromium.org (2013-02-27)

@alecflett: I was actually going to make the change that you are making in http://wkb.ug/111002, but it turns out that that is only a partial solution and the problem will still exist just in a less likely to appear form.  After my change is in, copying a scriptvalue just has the cost of reffing a refptr, so if you're at all uneasy about passing back references to scriptvalue , you can just wait for my patch to land instead.  References to scriptvalue are relatively safe unless clear() is called on them anywhere.

### js...@chromium.org (2013-02-27)

IMHO we should not land wkbug.com/111002 until wkbug.com/110206 is in, so we don't accidentally hide some aspect of the 110206 fix.

### [Deleted User] (2013-02-27)

@dcarney / @jsbell - agreed on all counts. Marking as a dependent.

### bu...@chromium.org (2013-02-27)

https://bugs.webkit.org/show_bug.cgi?id=110206
http://trac.webkit.org/changeset/143441
https://bugs.webkit.org/show_bug.cgi?id=111002
http://trac.webkit.org/changeset/143503


### bu...@chromium.org (2013-03-01)

https://bugs.webkit.org/show_bug.cgi?id=110206
http://trac.webkit.org/changeset/144458


### bu...@chromium.org (2013-03-02)

https://bugs.webkit.org/show_bug.cgi?id=111002
http://trac.webkit.org/changeset/144517


### js...@chromium.org (2013-03-04)

dcarney@ - anything left to land for this?

Is it feasible to merge the WebKit/chromium patches to 26?


### dc...@chromium.org (2013-03-04)

@jsbell - i don't see why not.  I doubt the affected code has changed much.  Would just need 

https://chromiumcodereview.appspot.com/12335006/
https://chromiumcodereview.appspot.com/12390008/
and
https://bugs.webkit.org/show_bug.cgi?id=110206


### sc...@gmail.com (2013-03-05)

Can we now mark the bug as "Fixed"?

### dh...@chromium.org (2013-03-07)

This crash doesn't seem to happen after M26 was branched (1410). So I'm removing the blocker label for now.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-03-12)

Dan - pinging again - can we resolve this as Fixed?


### dc...@chromium.org (2013-03-13)

Marking as fixed as it's not showing up in any crash logs anymore.

### js...@chromium.org (2013-03-13)

It's really hard to tell from the history how we should handle this on the security end. Is there anything we should merge to stable or beta, or was that taken care of in the various other bugs?

### ta...@google.com (2013-03-18)

To merge or not to merge - that is the question :-)?

So, nothing to merge to M26?

### js...@chromium.org (2013-03-18)

(Sorry, I've been out sick.)

The fix we want is WK 110206. Per dcarney@'s https://crbug.com/chromium/150737#c160 this would require merging two chromium revisions (r184024 and r185510) and WebKit revision http://trac.webkit.org/changeset/144458 - none of those are tracked by Chromium bugs other than this one.


### ta...@google.com (2013-03-18)

Ok, thanks for the update! Let me know when the fix makes it to Chrome trunk and once it's validated there I will approve the merge.

### js...@chromium.org (2013-03-18)

They hit trunk more than a week (two weeks?) ago. dcarney@ verified in c#165 that the crashes are gone from the logs as of 5 days ago. (yay!).

### sc...@gmail.com (2013-03-18)

I'll merge it.


### sc...@gmail.com (2013-03-19)

Note to self: also need http://src.chromium.org/viewvc/chrome?view=rev&revision=183544

### bu...@chromium.org (2013-03-19)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=188905

------------------------------------------------------------------------
r188905 | cevans@chromium.org | 2013-03-19T01:41:18.364454Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/chrome/renderer/searchbox/searchbox_extension.cc?r1=188905&r2=188904&pathrev=188905
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/chrome/renderer/translate_helper.cc?r1=188905&r2=188904&pathrev=188905
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/content/public/test/render_view_test.cc?r1=188905&r2=188904&pathrev=188905
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/content/renderer/browser_plugin/browser_plugin_browsertest.cc?r1=188905&r2=188904&pathrev=188905
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/content/renderer/render_view_impl.cc?r1=188905&r2=188904&pathrev=188905

Merge r183544, r184024, r185510

BUG=150737
Review URL: https://codereview.chromium.org/12833012
------------------------------------------------------------------------

### sc...@gmail.com (2013-03-19)

Chromium parts on M26 at crrev.com/188905.
WebKit M26: http://trac.webkit.org/changeset/146169

Looks like it took so long to track down that it affects Chrome 25 stable? Adding labels appropriately. Also tagging reward-topanel because it looks like https://code.google.com/p/chromium/issues/detail?id=150667 might have been the first report.

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-29)

Argh. Freeing up some labels and adding
release-0
release-private

This went out in M26, but wasn't adequately considered for release notes / reward.

Not much can be done about the release notes but for sure we'll sort out the reward.

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-04-02)

@therealholden: sorry again for dropping the ball.

The rewards panel has issued you a $1000 Chromium Security Reward for your extensive help here. This was a really hard issue to track down, so your energy and enthusiasm in providing lots of test cases is really appreciated.

### th...@gmail.com (2013-04-02)

Thanks!

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-04-26)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-10)

[Empty comment from Monorail migration]

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/150737?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Blink>Storage>IndexedDB]
[Monorail mergedwith: crbug.com/chromium/150667, crbug.com/chromium/151744, crbug.com/chromium/156114, crbug.com/chromium/156115, crbug.com/chromium/158083, crbug.com/chromium/165671, crbug.com/chromium/171190, crbug.com/chromium/172471, crbug.com/chromium/187888]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076318)*
