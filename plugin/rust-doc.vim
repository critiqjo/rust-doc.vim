if (exists('g:loaded_rust_doc') && g:loaded_rust_doc) || &cp
    finish
endif

command! -nargs=+ -complete=customlist,rust_doc#complete_cmd RustDoc call rust_doc#open(<f-args>)
command! -nargs=1 RustDocFuzzy call rust_doc#open_fuzzy(<f-args>)

let g:loaded_rust_doc = 1

""" Options
let s:dir = expand('<sfile>:p:h:h')
if !exists('g:viewdoc_rust_cmd')
  let g:viewdoc_rust_cmd='python ' . s:dir . '/rustdoc2text.py'
endif

""" Interface
" - command
command -bar -bang -nargs=1 -complete=customlist,rust_doc#complete_cmd ViewDocRust
  \ call ViewDoc('<bang>'=='' ? 'new' : 'doc', <q-args>, 'rust')
" - abbrev
if !exists('g:no_plugin_abbrev') && !exists('g:no_viewdoc_abbrev')
  cnoreabbrev <expr> rustdoc      getcmdtype()==':' && getcmdline()=='rustdoc'  ? 'ViewDocRust'  : 'rustdoc'
  cnoreabbrev <expr> rustdoc!     getcmdtype()==':' && getcmdline()=='rustdoc!' ? 'ViewDocRust'  : 'rustdoc!'
endif

""" Handlers
function s:ViewDoc_rust(topic, ...)
  let parts = split(a:topic)
  if len(parts) > 1
    let path = rust_doc#get_path(parts[0], parts[1])
  else
    let path = rust_doc#get_path(parts[0])
  endif

  return  { 'cmd': printf('%s %s', g:viewdoc_rust_cmd, shellescape(path)),
          \ 'ft':  'rustdoc',
          \ }
endfunction

let g:ViewDoc_rust = function('s:ViewDoc_rust')
let g:ViewDoc_rustdoc = function('s:ViewDoc_rust')
