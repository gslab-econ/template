import os, SCons.Script


###
### Edits for lyx
###

def namelyxtarget(target, source, env):
    '''The name of the output tex file is the same as the input.'''
    assert len(source) == 1, 'Lyx is single_srouce only.'
    s = str(source[0])
    if s.endswith('.lyx'): 
        target[0] = s[0:-4] +'.tex'
    return target, source

env = Environment(ENV=dict(PATH='/usr/texbin:/bin:/usr/bin'), IMPLICIT_COMMAND_DEPENDENCIES = 0)

env.lyx = SCons.Script.Builder( action = 'lyx --export pdflatex $SOURCE', 
                                suffix = '.tex', src_suffix='.lyx', 
                                single_source=True, # file by file
                                emitter = namelyxtarget )
env.Append(BUILDERS = {'Lyx' : env.lyx})

# Teach PDF to understand lyx
env['BUILDERS']['PDF'].add_src_builder(env.lyx)

###
###
###


if env['PLATFORM'] == "darwin":
    env.PrependENVPath( 'PATH', '/Applications/LyX.app/Contents/MacOS')

env.Decider('MD5-timestamp') # Only computes hash if time-stamp changed
Export('env')

SConscript('source/data/SConscript')
SConscript('source/analysis/SConscript')
SConscript('source/paper/SConscript')
SConscript('source/talk/SConscript')

