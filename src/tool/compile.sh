#!/bin/sh

case "$1" in
    "elf" ) # 生成可执行文件
        gcc $2 -o $3
        ;;
    "link" ) # 生成链接 .o.
        nasm -f elf$4 $2 -o $3
        ;;
    "bin" ) # 生成bin文件.
        # nasm -f 
        echo "bin文件生成:" $1,$2,$3
        ;;
    esac    
