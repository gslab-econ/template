""" Converts some lyx files to the latex format.

Note: everything in the file is thrown away until a section or the workd "stopskip" is found.
This way, all the preamble added by lyx is removed.
"""
from waflib import Logs
from waflib import TaskGen,Task
from waflib import Utils
from waflib.Configure import conf

def postprocess_lyx(src, tgt):
  Logs.debug("post-processing %s into %s" % (src,tgt))
  f_src = open(src,'r')
  f_tgt = open(tgt,'w')
  toks = ['\\documentclass','\\usepackage','\\begin{document}','\\end{document}','\\geometry','\\PassOptionsToPackage']
  keep = False
  for l in f_src:
    this_keep = ("stopskip" in l) or ("\\section" in l) or ("\\chapter" in l)
    if this_keep:
      print "start to keep"
    keep = keep or this_keep
    local_skip = False
    for tok in toks:
      local_skip = local_skip or l.startswith(tok)
    local_keep = False if local_skip else keep
    if local_keep:
      f_tgt.write(l)
  f_src.close()
  f_tgt.close()
  return 0

def process_lyx(task):
  input0 = task.inputs[0]
  src = input0.abspath()
  input1 = input0.change_ext("_tmp.lyx")
  output0 =task.outputs[0] 
  tgt = output0.abspath()
  print "processing lyx file %s" % src
  t = task.exec_command("cp %s %s" % (input0.abspath(), input1.abspath()))
  if t != 0:
    return t
  t = task.exec_command("%s --export pdflatex %s" % (task.env.LYX, input1.abspath()))
  if t != 0:
    return t
  t = postprocess_lyx(input1.change_ext(".tex").abspath(),output0.abspath())
  return t

class PostprocessLyx(Task.Task):
  def run(self):
    #Logs.debug("in post process")
    return postprocess_lyx(self.inputs[0].abspath(),self.outputs[0].abspath())

@conf
def lyx2tex(bld, lyx_file):
  lyx_files = Utils.to_list(lyx_file)
  for a in lyx_files:
    b = a.change_ext("_tmp.lyx")
    c = a.change_ext("_tmp.tex") 
    d = a.change_ext(".tex") 
    bld(rule="cp ${SRC} ${TGT}",source=a,target=b)
    tsk0 = bld(rule="${LYX} --export pdflatex ${SRC}",source=b,target=c)
    tsk = tsk0.create_task("PostprocessLyx")
    tsk.set_inputs(c)
    tsk.set_outputs(d)

def configure(conf):
  conf.find_program('lyx',var='LYX')
