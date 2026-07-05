#!/bin/zsh
cd /Users/xsz/project/front-ai/interview || exit 1
omx team 3:executor "读取当前目录下的 resume.md ，生成技术面试准备材料。
worker-1 负责项目深挖题、简历风险点和参考回答；
worker-2 负责高频技术八股文、标准答案和追问点；
worker-3 负责高概率手写代码题、参考解法、常见错误，并汇总输出到 interview-prep.md。
要求内容贴合简历和岗位，按高概率排序，答案简洁、真实、可直接背诵。"
