"Vim configuration file
"@author    jt_pritchett
"@copyright	ALAS LAB -- WPI

"No "vi" compatability
set nocompatible

"Basic vim settings
filetype plugin on
filetype indent on
set number
syntax on
set nowrap

"PEAR settings
set tabstop=2
set shiftwidth=2
set expandtab

"Prevent white space from being saved
autocmd BufWritePre *.* %s/\s\+$//e
