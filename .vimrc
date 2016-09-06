"Vim configuration file
"@author	Joshua T. Prtchett
"@copyright	ALAS LAB -- WPI

"No "vi" compatability
set nocompatible

"Basic vim settings
filetype plugin on
filetype indent on
set numbers
syntax on
set nowrap

"PEAR settings
set tabstop=2
set shiftwidth=2
set expandtab=2

"Prevent white space from being saved
autocmd BufWritePre *.* %s/\s\+$//e

