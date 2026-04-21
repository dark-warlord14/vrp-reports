#  TALOS-2021-1352: Google Chrome Blink setBaseAndExtent use after free vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40056812](https://issues.chromium.org/issues/40056812) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Editing>Selection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | vm...@chromium.org |
| **Created** | 2021-08-06 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55

Steps to reproduce the problem:
### Summary

A use after free vulnerability exists in the Selection API of Blink rendering engine in Google Chrome 92.0.4515.131 (Stable) and 94.0.4597.1 (Canary). A specially-crafted web page can trigger reuse of previously freed memory which can lead to arbitrary code execution. Victim would need to visit a malicious website to trigger this vulnerability.

### Tested Versions

Google Chrome 92.0.4515.131 (Stable)   
Google Chrome 94.0.4597.1 (Canary)   

### Product URLs

[https://www.google.com/chrome/](https://www.google.com/chrome/)

### CVSSv3 Score

8.3 - CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L

### CWE

CWE-416 - Use After Free

### Details

Google Chrome is a cross-platform web browser, developed by Google.

A use after free vulnerability exists in Selection API in Blink, which is a main DOM parsing and rendering engine used as core of chromium. More specifically, the vulnerability is manifasted in implementation of `setBaseAndExtent` method. 

While executing the supplied POC, Chromium browser crashes inside `blink::LayoutObject::LayoutObjectBitfields::IsBox()` at line 17. Snippet of this function is as follows:

     1:  LayoutObjectBitfields(Node* node)
     2:      : self_needs_layout_for_style_(false),
     3:        self_needs_layout_for_available_space_(false),
     4:        needs_positioned_movement_layout_(false),
     5:        normal_child_needs_layout_(false),
     6:        pos_child_needs_layout_(false),
     7:        needs_simplified_normal_flow_layout_(false),
     8:        self_needs_layout_overflow_recalc_(false), {...} background_paint_location_(kBackgroundPaintInGraphicsLayer),
     9:        overflow_clip_axes_(kNoOverflowClip) {}
    10:  {...}
    11:  // This boolean is the cached value of 'float'
    12:  // (see ComputedStyle::isFloating).
    13:  ADD_BOOLEAN_BITFIELD(floating_, Floating);
    14:  
    15:  ADD_BOOLEAN_BITFIELD(is_anonymous_, IsAnonymous);
    16:  ADD_BOOLEAN_BITFIELD(is_text_, IsText);
    17:  ADD_BOOLEAN_BITFIELD(is_box_, IsBox);
    18:  {...}

Function that is necessary for triggering vulnerability is "setBaseAndExtent" from "Selection" interface which is responsible for selecting all nodes between two nodes that are provided as arguments to the function. Prototype of this function looks like this:
`setBaseAndExtent(Node anchorNode, unsigned long anchorOffset, Node focusNode, unsigned long focusOffset);`

To be able to trigger this vulnerability the provided arguments must have a meaningful hierarchy: anchorNode needs to be parent to the focusNode and parameter anchorOffset must be equal or lower than focusOffset.

Looking down the stack trace there is function that is responsible for ComputeVisibleSelectionInDOMTree.

     1:  VisibleSelection SelectionEditor::ComputeVisibleSelectionInDOMTree() const {
     2:    DCHECK_EQ(GetFrame()->GetDocument(), GetDocument());
     3:    DCHECK_EQ(GetFrame(), GetDocument().GetFrame());
     4:    UpdateCachedVisibleSelectionIfNeeded();
     5:    if (cached_visible_selection_in_dom_tree_.IsNone())
     6:      return cached_visible_selection_in_dom_tree_;
     7:    DCHECK_EQ(cached_visible_selection_in_dom_tree_.Base().GetDocument(),
     8:              GetDocument());
     9:    return cached_visible_selection_in_dom_tree_;
    10:  }

At line 4 function UpdateCachedVisibleSelectionIfNeeded is responsible for checking if all nodes are visible. However statement in style element says otherwise because it marks all nodes as "content-visibility: hidden;" which results in engine not properly recognizing visibility of nodes inside "DOMSelection::setBaseAndExtent" function, which finally leads to a use after free vulnerability.

With proper manipulation of node elements this vulnerability could lead to control over freed memory and can ultimately result in remote code execution.

What is the expected behavior?

What went wrong?
### Crash Information

Command Line: chrome.exe --no-sandbox poc.html

    =================================================================
    ==11880==ERROR: AddressSanitizer: heap-use-after-free on address 0x1200e3f5c35c at pc 0x7ff7a8b769a6 bp 0x00d9686fcba0 sp 0x00d9686fcbe8
    READ of size 4 at 0x1200e3f5c35c thread T26
    ==11880==WARNING: Failed to use and restart external symbolizer!
    [11880:9520:0804/084012.801:ERROR:service_worker_storage.cc(1899)] Failed to delete the database: Database IO error
        #0 0x7ff7a8b769a5 in blink::To<blink::LayoutBox,blink::LayoutObject> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\casting.h:127
        #1 0x7ff7ad6c018c in blink::EndsOfNodeAreVisuallyDistinctPositions C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_units.cc:530
        #2 0x7ff7ad6c1191 in blink::MostBackwardCaretPosition<blink::EditingAlgorithm<blink::FlatTreeTraversal> > C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_units.cc:669
        #3 0x7ff7ad6c060d in blink::MostBackwardOrForwardCaretPosition<blink::PositionTemplate<blink::EditingInFlatTreeStrategy> (*)(const blink::PositionTemplate<blink::EditingInFlatTreeStrategy> &, blink::EditingBoundaryCrossingRule)> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_units.cc:567
        #4 0x7ff7ad6b9078 in blink::CanonicalPositionOf C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_units.cc:159
        #5 0x7ff7ad6c94db in blink::VisiblePositionTemplate<blink::EditingAlgorithm<blink::NodeTraversal> >::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_position.cc:121
        #6 0x7ff7ad6cbd6a in blink::CreateVisiblePosition C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_position.cc:218
        #7 0x7ff7ad57da1d in blink::VisibleSelectionTemplate<blink::EditingAlgorithm<blink::NodeTraversal> >::Creator::ComputeVisibleSelection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_selection.cc:75
        #8 0x7ff7ad581a12 in blink::CreateVisibleSelection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_selection.cc:100
        #9 0x7ff7ad8a1c58 in blink::SelectionEditor::UpdateCachedVisibleSelectionIfNeeded C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\selection_editor.cc:423
        #10 0x7ff7ad8a1ad0 in blink::SelectionEditor::ComputeVisibleSelectionInDOMTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\selection_editor.cc:79
        #11 0x7ff7aa5e286b in blink::FrameSelection::SetFocusedNodeIfNeeded C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:938
        #12 0x7ff7aa5e1dd8 in blink::FrameSelection::DidSetSelectionDeprecated C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:293
        #13 0x7ff7ad7314f6 in blink::DOMSelection::UpdateFrameSelection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\dom_selection.cc:89
        #14 0x7ff7ad73643f in blink::DOMSelection::setBaseAndExtent C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\dom_selection.cc:385
        #15 0x7ff7b0c57b6d in blink::`anonymous namespace'::v8_selection::SetBaseAndExtentOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_selection.cc:818
        #16 0x7ff7a4053ced in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:156
        #17 0x7ff7a4050dfd in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
        #18 0x7ff7a404e231 in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
        #19 0x7ff7a404d52e in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
        #20 0x7ee8000b81db  (<unknown module>)

    0x1200e3f5c35c is located 28 bytes inside of 296-byte region [0x1200e3f5c340,0x1200e3f5c468)
    freed by thread T26 here:
        #0 0x7ff7a8db642b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
        #1 0x7ff7ae20e62b in blink::LayoutNGTableCell::~LayoutNGTableCell C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\ng\table\layout_ng_table_cell.h:18
        #2 0x7ff7aaa9d27a in blink::LayoutObject::Destroy C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_object.cc:3881
        #3 0x7ff7aaa9cf29 in blink::LayoutObject::DestroyAndCleanupAnonymousWrappers C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_object.cc:3867
        #4 0x7ff7aa55408a in blink::Node::DetachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\node.cc:1726
        #5 0x7ff7aa4cb4ae in blink::Element::DetachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:2822
        #6 0x7ff7acff4b76 in blink::ContainerNode::DetachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1015
        #7 0x7ff7aa4cb49d in blink::Element::DetachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:2819
        #8 0x7ff7aa553d0c in blink::Node::ReattachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\node.cc:1690
        #9 0x7ff7aa4d446d in blink::Element::RebuildLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3175
        #10 0x7ff7acffabc1 in blink::ContainerNode::RebuildLayoutTreeForChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1381
        #11 0x7ff7acffaf86 in blink::ContainerNode::RebuildChildrenLayoutTrees C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1403
        #12 0x7ff7aa4d4894 in blink::Element::RebuildLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3203
        #13 0x7ff7ace1aa4c in blink::StyleEngine::RebuildLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2076
        #14 0x7ff7ace1bf94 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2115
        #15 0x7ff7aa3ef2c2 in blink::Document::UpdateStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2185
        #16 0x7ff7aa3ed9c2 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2134
        #17 0x7ff7aa3e41ed in blink::Document::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2054
        #18 0x7ff7aa3f0a04 in blink::Document::UpdateStyleAndLayoutTreeForNode C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2286
        #19 0x7ff7b05c70e7 in blink::HTMLMeterElement::CanContainRangeEndPoint C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\html_meter_element.cc:223
        #20 0x7ff7ad6c0178 in blink::EndsOfNodeAreVisuallyDistinctPositions C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_units.cc:529
        #21 0x7ff7ad6c1191 in blink::MostBackwardCaretPosition<blink::EditingAlgorithm<blink::FlatTreeTraversal> > C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_units.cc:669
        #22 0x7ff7ad6c060d in blink::MostBackwardOrForwardCaretPosition<blink::PositionTemplate<blink::EditingInFlatTreeStrategy> (*)(const blink::PositionTemplate<blink::EditingInFlatTreeStrategy> &, blink::EditingBoundaryCrossingRule)> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_units.cc:567
        #23 0x7ff7ad6b9078 in blink::CanonicalPositionOf C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_units.cc:159
        #24 0x7ff7ad6c94db in blink::VisiblePositionTemplate<blink::EditingAlgorithm<blink::NodeTraversal> >::Create C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_position.cc:121
        #25 0x7ff7ad6cbd6a in blink::CreateVisiblePosition C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_position.cc:218
        #26 0x7ff7ad57da1d in blink::VisibleSelectionTemplate<blink::EditingAlgorithm<blink::NodeTraversal> >::Creator::ComputeVisibleSelection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_selection.cc:75
        #27 0x7ff7ad581a12 in blink::CreateVisibleSelection C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\visible_selection.cc:100

    previously allocated by thread T26 here:
        #0 0x7ff7a8db651b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
        #1 0x7ff7aaa6674d in blink::LayoutObject::operator new C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_object.cc:237
        #2 0x7ff7adf4584c in blink::LayoutObjectFactory::CreateBlockFlow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_object_factory.cc:119
        #3 0x7ff7aaa66dea in blink::LayoutObject::CreateObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\layout\layout_object.cc:288
        #4 0x7ff7ad4ddf4b in blink::LayoutTreeBuilderForElement::CreateLayoutObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\layout_tree_builder.cc:84
        #5 0x7ff7aa4c849f in blink::Element::AttachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:2729
        #6 0x7ff7acff4985 in blink::ContainerNode::AttachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1008
        #7 0x7ff7aa4c8b4b in blink::Element::AttachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:2762
        #8 0x7ff7acff4985 in blink::ContainerNode::AttachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1008
        #9 0x7ff7aa4c8b4b in blink::Element::AttachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:2762
        #10 0x7ff7ad557cc4 in blink::HTMLHtmlElement::AttachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\html_html_element.cc:184
        #11 0x7ff7aa553d41 in blink::Node::ReattachLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\node.cc:1691
        #12 0x7ff7aa4d446d in blink::Element::RebuildLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3175
        #13 0x7ff7ace1aa4c in blink::StyleEngine::RebuildLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2076
        #14 0x7ff7ace1bf94 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2115
        #15 0x7ff7aa3ef2c2 in blink::Document::UpdateStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2185
        #16 0x7ff7aa3ed9c2 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2134
        #17 0x7ff7aa3e41ed in blink::Document::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2054
        #18 0x7ff7aa3e41dc in blink::Document::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2052
        #19 0x7ff7aa430c09 in blink::Document::FinishedParsing C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:6646
        #20 0x7ff7ad2a4303 in blink::HTMLDocumentParser::end C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1422
        #21 0x7ff7ad291ae2 in blink::HTMLDocumentParser::PrepareToStopParsing C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:567
        #22 0x7ff7ad29527c in blink::HTMLDocumentParser::AttemptToEnd C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1459
        #23 0x7ff7ad2a4a78 in blink::HTMLDocumentParser::Finish C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:1522
        #24 0x7ff7ad0fbef0 in blink::DocumentLoader::FinishedLoading C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:1047
        #25 0x7ff7ad103a92 in blink::DocumentLoader::StartLoadingResponse C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:1631
        #26 0x7ff7ad10c35e in blink::DocumentLoader::CommitNavigation C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\document_loader.cc:2370
        #27 0x7ff7acfb7188 in blink::FrameLoader::CommitDocumentLoader C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\loader\frame_loader.cc:1227

    Thread T26 created by T0 here:
        #0 0x7ff7a8dc0c52 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
        #1 0x7ff7a8fb7bae in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
        #2 0x7ff7a8f4472a in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:200
        #3 0x7ff7a7d2d52f in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1967
        #4 0x7ff7a7d107b2 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2814
        #5 0x7ff7a7d07e1b in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3053
        #6 0x7ff7a7d05b4e in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1060
        #7 0x7ff7a7d046f6 in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:815
        #8 0x7ff7a7a8a579 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:531
        #9 0x7ff7a7c423dd in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:595
        #10 0x7ff7a7bb6cf3 in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3302
        #11 0x7ff7a7bb5ecc in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1136
        #12 0x7ff7aed1c47d in content::Shell::LoadURLForFrame C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell.cc:250
        #13 0x7ff7aed1c128 in content::Shell::LoadURL C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell.cc:238
        #14 0x7ff7aed1be2c in content::Shell::CreateNewWindow C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell.cc:228
        #15 0x7ff7aed6358a in content::ShellBrowserMainParts::InitializeMessageLoopContext C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell_browser_main_parts.cc:156
        #16 0x7ff7aed63b64 in content::ShellBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell_browser_main_parts.cc:197
        #17 0x7ff7a725a478 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:949
        #18 0x7ff7a7fdb9ab in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
        #19 0x7ff7a725997e in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:857
        #20 0x7ff7a72613ad in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
        #21 0x7ff7a7255f90 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
        #22 0x7ff7a3e44814 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:597
        #23 0x7ff7a3e471fd in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1080
        #24 0x7ff7a3e4640c in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:955
        #25 0x7ff7a3e43687 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:380
        #26 0x7ff7a3e43c6e in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:406
        #27 0x7ff7a0cf11d2 in main C:\b\s\w\ir\cache\builder\src\content\shell\app\shell_main.cc:33
        #28 0x7ff7b66c3093 in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
        #29 0x7ff8dabd7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
        #30 0x7ff8dc122650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

    SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\casting.h:127 in blink::To<blink::LayoutBox,blink::LayoutObject>
    Shadow bytes around the buggy address:
      0x041d006eb810: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
      0x041d006eb820: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
      0x041d006eb830: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
      0x041d006eb840: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
      0x041d006eb850: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
    =>0x041d006eb860: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd
      0x041d006eb870: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
      0x041d006eb880: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
      0x041d006eb890: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
      0x041d006eb8a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
      0x041d006eb8b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa
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
    ==11880==ABORTING

Did this work before? N/A 

Chrome version: 94.0.4597.1  Channel: canary
OS Version: 10.0

### Credit

Discovered by Marcin Towalski of Cisco Talos.

https://talosintelligence.com/vulnerability_reports/

## Attachments

- [TALOS-2021-1352 - Google_Chrome_Blink_setBaseAndExtent_use_after_free_vulnerability.txt](attachments/TALOS-2021-1352 - Google_Chrome_Blink_setBaseAndExtent_use_after_free_vulnerability.txt) (text/plain, 23.5 KB)
- [TALOS-2021-1352-poc.html](attachments/TALOS-2021-1352-poc.html) (text/plain, 431 B)

## Timeline

### vu...@sourcefire.com (2021-08-06)

Label: reward_to-marcin.towalski_at_gmail.com

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-08-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4951115500945408.

### cl...@chromium.org (2021-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-08-09)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-08-09)

Thank you for the report. Clusterfuzz is still trying to find a regression range but it doesn't appear to be recent.

yosin@: Can you PTAL at this security bug?

[Monorail components: Blink>Editing>Selection]

### [Deleted User] (2021-08-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-08-10)

Detailed Report: https://clusterfuzz.com/testcase?key=4951115500945408

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 12
Crash Address: 0x61300000cd54
Crash State:
  blink::LayoutBox& blink::To<blink::LayoutBox, blink::LayoutObject>
  blink::EndsOfNodeAreVisuallyDistinctPositions
  blink::PositionTemplate<blink::EditingAlgorithm<blink::FlatTreeTraversal> > blin
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=832702:832706

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4951115500945408

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/4951115500945408 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### yo...@chromium.org (2021-08-10)

It seems this is caused by Display Locking (content-visibility)

I got DCHECK()

[document_lifecycle.cc(363)] Check failed: CanRewindTo(state). Cannot rewind document lifecycle from "kLayoutClean" to "kVisualUpdatePending"


# Stack Trace on ToT
DocumentLifecycle::EnsureStateAtMost()
Document::ScheduleLayoutTreeUpdate()
Document::ScheduleLayoutTreeUpdateIfNeeded()
Node::MarkAncestorsWithChildNeedsStyleRecalc()
Node::SetNeedsStyleRecalc()
DisplayLockContext::MarkForStyleRecalcIfNeeded()
DisplayLockContext::NotifyForcedUpdateScopeStarted()
DisplayLockUtilities::ScopedForcedUpdate::Impl::Impl()
MakeGarbageCollectedTrait<blink::DisplayLockUtilities::ScopedForcedUpdate::Impl>::Call<const blink::Node *&,bool &>()
MakeGarbageCollected<blink::DisplayLockUtilities::ScopedForcedUpdate::Impl,const blink::Node *&,bool &>()
DisplayLockUtilities::ScopedForcedUpdate::ScopedForcedUpdate()
Document::UpdateStyleAndLayoutTreeForNode()
HTMLMeterElement::CanContainRangeEndPoint()
CanHaveChildrenForEditing()
EndsOfNodeAreVisuallyDistinctPositions()
MostBackwardCaretPosition<blink::EditingAlgorithm<blink::FlatTreeTraversal>>()
MostBackwardOrForwardCaretPosition<blink::PositionTemplate<blink::EditingAlgorithm<blink::FlatTreeTraversal>> ()
MostBackwardCaretPosition()
CanonicalPosition<blink::PositionTemplate<blink::EditingAlgorithm<blink::NodeTraversal>>>()
CanonicalPositionOf()
VisiblePositionTemplate<blink::EditingAlgorithm<blink::NodeTraversal>>::Create()
CreateVisiblePosition()
CanonicalizeSelection<blink::EditingAlgorithm<blink::NodeTraversal>>()
VisibleSelectionTemplate<blink::EditingAlgorithm<blink::NodeTraversal>>::Creator::ComputeVisibleSelection()
VisibleSelectionTemplate<blink::EditingAlgorithm<blink::NodeTraversal>>::Creator::CreateWithGranularity()
CreateVisibleSelection()
SelectionEditor::UpdateCachedVisibleSelectionIfNeeded()
SelectionEditor::ComputeVisibleSelectionInDOMTree()
FrameSelection::ComputeVisibleSelectionInDOMTree()
FrameSelection::ComputeVisibleSelectionInDOMTreeDeprecated()
FrameSelection::SetFocusedNodeIfNeeded()
FrameSelection::DidSetSelectionDeprecated()
DOMSelection::UpdateFrameSelection()
DOMSelection::setBaseAndExtent()
`anonymous namespace'::v8_selection::SetBaseAndExtentOperationCallback()
v8.dll!v8::internal::FunctionCallbackArguments::Call()
v8.dll!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>()
v8.dll!v8::internal::Builtin_Impl_HandleApiCall()
v8.dll!v8::internal::Builtin_HandleApiCall()


### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-21)

vmpstr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2021-08-21)

ClusterFuzz testcase 4951115500945408 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=910752:913964

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-22)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M93. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M94. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-22)

This bug requires manual review: We are only 8 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vm...@chromium.org (2021-08-23)

It's hard for me to trace through the whole selection code here, so I'm hoping to get some help :)

The underlying issue seems to be that content-visibility: hidden elements are not updated until it's too late in the stack. Note that we can't simply skip them since I believe that content-visibility: auto, which should still participate in selection, would have the same problem.

In FrameSelection::ComputeVisibleSelectionInDOMTreeDeprecated(), we update style and layout tree for the document. Much deeper in the stack, in HTMLMeterElement::CanContainRangeEndPoint(), we call UpdateStyleAndLayoutTreeForNode, which forces any ancestor display locks and does the update again. This causes the DCHECK that yosin@ saw, and possibly other issues reported here.

Ideally, what we want is to gather all DOM nodes that participate in this selection in FrameSelection::ComputeVisibleSelectionInDOMTreeDeprecated(), force them to unlock by DisplayLockUtilities::ScopedForcedUpdate, and then call UpdateStyleAndLayoutTree for the document.

The part that I am not familiar with is how, if possible, to get all of the DOM nodes that participate in this selection. There's a selection_editor_ that is available, which may contain this information. 

yosin@, do you by any chance know how to gather all of these nodes? Or do you know someone who can answer this?


### am...@chromium.org (2021-08-23)

[Comment Deleted]

### am...@chromium.org (2021-08-23)

removing merge labels as this issue has been re-opened and/or verification of ClusterFuzz reporting fixed in quite large regression range 

### vm...@chromium.org (2021-08-23)

It is possible that the underlying crash has disappeared in the fixed range, but I can still get the DCHECK that yosin@ found, I'm working on a fix now. 

### gi...@appspot.gserviceaccount.com (2021-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/484bc1abffcdee33648695244c86daca15ab6539

commit 484bc1abffcdee33648695244c86daca15ab6539
Author: Vladimir Levin <vmpstr@chromium.org>
Date: Tue Aug 24 05:19:07 2021

content-visibility: Force range base/extent when computing visual selection.

Some of the code that does visual selection ends up updating style and
layout for node. This means that it will temporarily unlock c-v nodes
and may cause a state rewind from layout clean to visual update pending.

That's not an operation we support, verified by DCHECKs. So, instead
we should unlock any c-v nodes prior to getting to layout clean.

R=chrishtr@chromium.org, yosin@chromium.org

Bug: 1237533
Change-Id: Ib30036c4536bea3da2ae4fa54c19ad5684829597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114230
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#914631}

[modify] https://crrev.com/484bc1abffcdee33648695244c86daca15ab6539/third_party/blink/renderer/core/display_lock/display_lock_utilities.cc
[modify] https://crrev.com/484bc1abffcdee33648695244c86daca15ab6539/third_party/blink/renderer/core/display_lock/display_lock_utilities.h
[modify] https://crrev.com/484bc1abffcdee33648695244c86daca15ab6539/third_party/blink/renderer/core/editing/frame_selection.cc
[add] https://crrev.com/484bc1abffcdee33648695244c86daca15ab6539/third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/meter-selection-crash.html


### vm...@chromium.org (2021-08-24)

I'd like the change to be in Canary for a day or two, and then merge into M94.

### vu...@sourcefire.com (2021-08-24)

Is there an estimated public release date for this issue? As a release date is determined, please let us know. 

### [Deleted User] (2021-08-25)

Your change meets the bar and is auto-approved for M94. Please go ahead and merge the CL to branch 4606 (refs/branch-heads/4606) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2021-08-25)

Please merge your change to M94 branch 4606 ASAP. Thank you.

### gi...@appspot.gserviceaccount.com (2021-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e2f1a09b9ea955912194c4dd4610b00b873efa4

commit 2e2f1a09b9ea955912194c4dd4610b00b873efa4
Author: Vladimir Levin <vmpstr@chromium.org>
Date: Wed Aug 25 20:50:40 2021

content-visibility: Force range base/extent when computing visual selection.

Some of the code that does visual selection ends up updating style and
layout for node. This means that it will temporarily unlock c-v nodes
and may cause a state rewind from layout clean to visual update pending.

That's not an operation we support, verified by DCHECKs. So, instead
we should unlock any c-v nodes prior to getting to layout clean.

R=​chrishtr@chromium.org, yosin@chromium.org

(cherry picked from commit 484bc1abffcdee33648695244c86daca15ab6539)

Bug: 1237533
Change-Id: Ib30036c4536bea3da2ae4fa54c19ad5684829597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114230
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#914631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3119866
Commit-Queue: vmpstr <vmpstr@chromium.org>
Commit-Queue: Chris Harrelson <chrishtr@chromium.org>
Auto-Submit: vmpstr <vmpstr@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#323}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/2e2f1a09b9ea955912194c4dd4610b00b873efa4/third_party/blink/renderer/core/display_lock/display_lock_utilities.cc
[modify] https://crrev.com/2e2f1a09b9ea955912194c4dd4610b00b873efa4/third_party/blink/renderer/core/display_lock/display_lock_utilities.h
[modify] https://crrev.com/2e2f1a09b9ea955912194c4dd4610b00b873efa4/third_party/blink/renderer/core/editing/frame_selection.cc
[add] https://crrev.com/2e2f1a09b9ea955912194c4dd4610b00b873efa4/third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/meter-selection-crash.html


### am...@chromium.org (2021-09-01)

re-adding merge labels now that full fix has been landed and is in M94/beta; to re-kickoff of the full merge review process 

### am...@google.com (2021-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-01)

Congratulations, Marcin! The VRP Panel has decided to award you $7500 for this report. Nice work! 

### am...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-07)

merge approved for M93, please go ahead merge to branch 4577 at your earliest convenience so this fix can be included in next week's stable refresh. 
Also, merge approved for M92, so this can be included in the Extended Stable release as we move to the 4W stable channel release cycle, please merge to branch 4515. Thank you! 

### vm...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6bf424362b615b227edf1d564555663b24bbccaf

commit 6bf424362b615b227edf1d564555663b24bbccaf
Author: Vladimir Levin <vmpstr@chromium.org>
Date: Tue Sep 07 21:21:46 2021

content-visibility: Force range base/extent when computing visual selection.

Some of the code that does visual selection ends up updating style and
layout for node. This means that it will temporarily unlock c-v nodes
and may cause a state rewind from layout clean to visual update pending.

That's not an operation we support, verified by DCHECKs. So, instead
we should unlock any c-v nodes prior to getting to layout clean.

R=​chrishtr@chromium.org, yosin@chromium.org

(cherry picked from commit 484bc1abffcdee33648695244c86daca15ab6539)

Bug: 1237533
Change-Id: Ib30036c4536bea3da2ae4fa54c19ad5684829597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114230
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#914631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3139666
Auto-Submit: vmpstr <vmpstr@chromium.org>
Commit-Queue: Chris Harrelson <chrishtr@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#1193}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/6bf424362b615b227edf1d564555663b24bbccaf/third_party/blink/renderer/core/display_lock/display_lock_utilities.cc
[modify] https://crrev.com/6bf424362b615b227edf1d564555663b24bbccaf/third_party/blink/renderer/core/display_lock/display_lock_utilities.h
[modify] https://crrev.com/6bf424362b615b227edf1d564555663b24bbccaf/third_party/blink/renderer/core/editing/frame_selection.cc
[add] https://crrev.com/6bf424362b615b227edf1d564555663b24bbccaf/third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/meter-selection-crash.html


### gi...@appspot.gserviceaccount.com (2021-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9723e3c13c8c3e72e0dfeacef00abc97e4a9e3b7

commit 9723e3c13c8c3e72e0dfeacef00abc97e4a9e3b7
Author: Vladimir Levin <vmpstr@chromium.org>
Date: Tue Sep 07 21:32:03 2021

content-visibility: Force range base/extent when computing visual selection.

Some of the code that does visual selection ends up updating style and
layout for node. This means that it will temporarily unlock c-v nodes
and may cause a state rewind from layout clean to visual update pending.

That's not an operation we support, verified by DCHECKs. So, instead
we should unlock any c-v nodes prior to getting to layout clean.

R=​chrishtr@chromium.org, yosin@chromium.org

(cherry picked from commit 484bc1abffcdee33648695244c86daca15ab6539)

Bug: 1237533
Change-Id: Ib30036c4536bea3da2ae4fa54c19ad5684829597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114230
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#914631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3145452
Auto-Submit: vmpstr <vmpstr@chromium.org>
Commit-Queue: Chris Harrelson <chrishtr@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#2115}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/9723e3c13c8c3e72e0dfeacef00abc97e4a9e3b7/third_party/blink/renderer/core/display_lock/display_lock_utilities.cc
[modify] https://crrev.com/9723e3c13c8c3e72e0dfeacef00abc97e4a9e3b7/third_party/blink/renderer/core/display_lock/display_lock_utilities.h
[modify] https://crrev.com/9723e3c13c8c3e72e0dfeacef00abc97e4a9e3b7/third_party/blink/renderer/core/editing/frame_selection.cc
[add] https://crrev.com/9723e3c13c8c3e72e0dfeacef00abc97e4a9e3b7/third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/meter-selection-crash.html


### am...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-13)

[Empty comment from Monorail migration]

### rz...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/11ff9feda46c2d569bbf84f0e0614ed31e7a1df9

commit 11ff9feda46c2d569bbf84f0e0614ed31e7a1df9
Author: Vladimir Levin <vmpstr@chromium.org>
Date: Wed Sep 29 08:26:47 2021

[M90-LTS] content-visibility: Force range base/extent when computing visual selection.

Some of the code that does visual selection ends up updating style and
layout for node. This means that it will temporarily unlock c-v nodes
and may cause a state rewind from layout clean to visual update pending.

That's not an operation we support, verified by DCHECKs. So, instead
we should unlock any c-v nodes prior to getting to layout clean.

R=chrishtr@chromium.org, yosin@chromium.org

(cherry picked from commit 484bc1abffcdee33648695244c86daca15ab6539)

Bug: 1237533
Change-Id: Ib30036c4536bea3da2ae4fa54c19ad5684829597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114230
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#914631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3162069
Reviewed-by: vmpstr <vmpstr@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Chris Harrelson <chrishtr@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1625}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/11ff9feda46c2d569bbf84f0e0614ed31e7a1df9/third_party/blink/renderer/core/display_lock/display_lock_utilities.h
[add] https://crrev.com/11ff9feda46c2d569bbf84f0e0614ed31e7a1df9/third_party/blink/web_tests/external/wpt/css/css-contain/content-visibility/meter-selection-crash.html
[modify] https://crrev.com/11ff9feda46c2d569bbf84f0e0614ed31e7a1df9/third_party/blink/renderer/core/editing/frame_selection.cc
[modify] https://crrev.com/11ff9feda46c2d569bbf84f0e0614ed31e7a1df9/third_party/blink/renderer/core/display_lock/display_lock_utilities.cc


### rz...@google.com (2021-09-29)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2021-10-04)

Is there a release date for this issue? 


### am...@chromium.org (2021-10-04)

Hi vulndiscovery@ - the fix for this issue was released in the first security refresh of M93 on 13 September 2021: https://chromereleases.googleblog.com/2021/09/stable-channel-update-for-desktop.html



### vu...@sourcefire.com (2021-10-04)

Thanks. Just want to confirm this is good for public disclosure as well. Please advise

### am...@chromium.org (2021-10-04)

No worries! We would greatly appreciate it if y'all could hold off on public disclosure until this bug is made allpublic, which should be on or about 30 November 2021, as it was fixed on 24 August. 

### vu...@sourcefire.com (2021-10-04)

Thanks, will make note on our end.

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2021-11-29)

Can you provide CVE assigned to this issue?


### [Deleted User] (2021-11-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1237533?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056812)*
