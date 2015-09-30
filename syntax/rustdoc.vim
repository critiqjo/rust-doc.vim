syntax include @rust syntax/rust.vim
syntax region rustSnip matchgroup=Snip start="\[code\]" end="\[/code\]" contains=@rust
syntax region rustSnip matchgroup=Snip start="`" end="`" contains=@rust
syntax match rustdocHead /^#\+ .\+/ contains=ALL

hi link Snip SpecialComment
hi link rustdocHead Title
