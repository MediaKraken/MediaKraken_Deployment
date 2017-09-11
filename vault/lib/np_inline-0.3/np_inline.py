# Copyright (c) 2011 J. David Lee. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are
# met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

import os
import numpy as np
import multiprocessing 
import imp

###############################################################################
# Compilation lock for multiprocessing.                                       #
###############################################################################
_COMP_LOCK = multiprocessing.Lock()

###############################################################################
# C-code skeleton.                                                            #
###############################################################################
_SKEL = r'''
#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>

// Forward declarations of our function.
static PyObject *function(PyObject *self, PyObject *args); 


// Boilerplate: function list.
static PyMethodDef methods[] = {
    { "function", function, METH_VARARGS, "Doc string."},
    { NULL, NULL, 0, NULL } /* Sentinel */
};

// Boilerplate: Module initialization.
PyMODINIT_FUNC init__MODULE_NAME__(void) {
        (void) Py_InitModule("__MODULE_NAME__", methods);
        import_array();
}


/*****************************************************************************
 * Array access macros.                                                      *
 *****************************************************************************/
__NUMPY_ARRAY_MACROS__


/*****************************************************************************
 * Support code.                                                             *
 *****************************************************************************/
__SUPPORT_CODE__


/*****************************************************************************
 * The function.                                                             *
 *****************************************************************************/
PyObject *function(PyObject *self, PyObject *args) {


/***************************************
 * Variable declarations.              *
 ***************************************/
__FUNC_VAR_DECLARATIONS__


/***************************************
 * Parse variables.                    *
 ***************************************/
if (!PyArg_ParseTuple(args, "__PARSE_ARG_TYPES__", __PARSE_ARG_LIST__)) {
    return NULL;
} 


/***************************************
 * User code.                          *
 ***************************************/
__USER_CODE__


/***************************************
 * Return value.                       *
 ***************************************/
__RETURN_VAL__

} // End of function(self, args).

'''

###############################################################################
# Module setup.                                                               #
###############################################################################
_PATH = os.path.expanduser('~/.np_inline')

if not os.path.exists(_PATH):
    os.makedirs(_PATH)


###############################################################################
# Code generation.                                                            #
###############################################################################
_TYPE_CONV_DICT = {
    float : 'double',
    int   : 'long'
}


_RETURN_FUNC_DICT = {
    float : 'PyFloat_FromDouble',
    int   : 'PyLong_FromLong'
}


_TYPE_PARSE_SPEC_DICT = {
    float : 'd',
    int   : 'i'
}


_NP_TYPE_CONV_DICT = {
    np.uint8    : 'npy_uint8',
    np.uint16   : 'npy_uint16',
    np.uint32   : 'npy_uint32',
    np.uint64   : 'npy_uint64',
    np.int8     : 'npy_int8',
    np.int16    : 'npy_int16',
    np.int32    : 'npy_int32',
    np.int64    : 'npy_int64',
    np.float32  : 'npy_float32',
    np.float64  : 'npy_float64',
}

# The numpy floating point 128 bit type isn't available on all systems it 
# turns out. 
try:
    _NP_TYPE_CONV_DICT[np.float128] = 'npy_float128'
except:
    print('Numpy float128 not available.')


def _gen_var_decls(py_types, np_types, return_type):
    """py_types should be a list with elements of the form
    (python_object, python_type, c_code_name)
    
    np_types should be a list with elements of the form 
    (numpy_object, numpy_type, num_dims, c_code_name)
    """
    str_list = []
    for py_type, c_name in py_types:
        c_type = _TYPE_CONV_DICT[py_type]
        str_list.append('{0} {1};'.format(c_type, c_name))

    for np_type, dims, c_name in np_types:
        str_list.append('PyArrayObject *py_{0};'.format(c_name))

    if return_type is not None:
        c_type = _TYPE_CONV_DICT[return_type]
        str_list.append('{0} return_val;'.format(c_type))

    return '\n'.join(str_list)


def _gen_parse_arg_types(py_types, np_types):
    str_list = []
    for py_type, c_name in py_types:
        str_list.append(_TYPE_PARSE_SPEC_DICT[py_type])

    for np_type, dims, c_name in np_types:
        str_list.append('O')
        
    return ''.join(str_list)


def _gen_parse_arg_list(py_types, np_types):
    str_list = []

    for py_type, c_name in py_types:
        str_list.append('&{0}'.format(c_name))

    for np_type, dims, c_name in np_types:
        str_list.append('&py_{0}'.format(c_name))
        
    return ', '.join(str_list)


def _gen_numpy_array_index_macro(np_type, dims, c_name):
    c_type = _NP_TYPE_CONV_DICT[np_type]

    # First we generate the list of arguments for the macro. 
    # These have the form x0, x1, ...
    arg_list = ', '.join(['x{0}'.format(i) for i in range(dims)])

    # Next, we want to create the indexing code. This looks like:
    # *(type *)((data + i*array->strides[0] + j*array->strides[1]))
    strides = ''
    for i in range(dims):
        strides += ' + (x{0}) * py_{1}->strides[{0}]'.format(i, c_name)
    
    return '#define {0}({1}) *({2} *)((py_{0}->data {3}))'.format(
        c_name, arg_list, c_type, strides)
    
    
def _gen_numpy_array_macros(np_types):
    str_list = []
    for np_type, dims, c_name in np_types:
        str_list.append(_gen_numpy_array_index_macro(np_type, dims, c_name))
        s = '#define {0}_shape(i) (py_{0}->dimensions[(i)])'.format(c_name)
        str_list.append(s)
        s = '#define {0}_ndim (py_arr->nd)'.format(c_name)
        str_list.append(s)
    return '\n'.join(str_list)


def _gen_return_val(return_type):
    if return_type is None:
        return 'Py_RETURN_NONE;'
    return 'return {0}(return_val);'.format(_RETURN_FUNC_DICT[return_type])


def _gen_code(name, user_code, py_types, np_types, support_code, return_type):
    """Return a string containing the generated C code."""
    s = _SKEL.replace('__MODULE_NAME__', 
                     name)
    s = s.replace('__NUMPY_ARRAY_MACROS__', 
                  _gen_numpy_array_macros(np_types))
    s = s.replace('__SUPPORT_CODE__', 
                  support_code)
    s = s.replace('__FUNC_VAR_DECLARATIONS__', 
                  _gen_var_decls(py_types, np_types, return_type))
    s = s.replace('__PARSE_ARG_TYPES__',
                  _gen_parse_arg_types(py_types, np_types))
    s = s.replace('__PARSE_ARG_LIST__', 
                  _gen_parse_arg_list(py_types, np_types))
    s = s.replace('__USER_CODE__', 
                  user_code)
    s = s.replace('__RETURN_VAL__', 
                  _gen_return_val(return_type))
    return s
    

###############################################################################
# Building and installation.                                                  #
###############################################################################
def _build_install_module(c_code, mod_name, extension_kwargs={}):
    # Save the current path so we can reset at the end of this function.
    curpath = os.getcwd() 
    mod_name_c = '{0}.c'.format(mod_name)

    try:
        from distutils.core import setup, Extension
        
        # Write out the code.
        with open(os.path.join(_PATH, mod_name_c), 'wb') as f:
            f.write(c_code)

        # Make sure numpy headers are included. 
        if 'include_dirs' not in extension_kwargs:
            extension_kwargs['include_dirs'] = []
        extension_kwargs['include_dirs'].append(np.get_include())
            
        # Change to the code directory.
        os.chdir(_PATH)

        # Create the extension module object. 
        ext = Extension(mod_name, [mod_name_c], **extension_kwargs)

        # Clean.
        setup(ext_modules=[ext], script_args=['clean'])

        # Build and install the module here. 
        setup(ext_modules=[ext], 
              script_args=['install', '--install-lib={0}'.format(_PATH)])

    finally:
        os.chdir(curpath)


###############################################################################
# Helper functions.                                                           #
###############################################################################
def _string_or_path(code_str, code_path):
    """Return either code_str if it is not None, or the contents in 
    code_path.
    """
    if code_str is not None:
        return code_str
    
    if code_path is not None:
        with open(code_path, 'rb') as f:
            return f.read()

    return ''


###############################################################################
# Importing and running.                                                      #
###############################################################################

# This is a dictionary mapping unique names to their functions. 
_FUNCS = {}


def _mod_path(mod_name):
    return os.path.join(_PATH, '{0}.so'.format(mod_name))


def _import(mod_name):
    mod = imp.load_dynamic(mod_name, _mod_path(mod_name))
    _FUNCS[mod_name] = mod.function

                  
def inline(unique_name, args=(), py_types=(), np_types=(), code=None, 
           code_path=None, support_code=None, support_code_path=None, 
           extension_kwargs={}, return_type=None):
    """Inline C code in your python code. 
    
    Parameters:
    unique_name : string
        A unique string identifying this bit of code. This should be valid
        to use as a filename.
    args : typle
        The arguments passed to the C function. Currently the code can
        accept python ints and floats, as well as numpy numeric arrays 
        of all types. Numpy objects should always be after other 
        objects, and types should correspond with the definitions given
        in py_types and np_types respectively. 
    py_types : typle of tuples (python_type, c_name)
        Type specifications for non-numpy arguments. Currently only int 
        and float are valid types. Default is empty tuple.
    np_types : typle of tuples (numpy_type, dims, c_name)
        Type specifications for numpy-type arguments. Most numeric numpy 
        types are valid. dims is the integer number of dimensions of the 
        corresponding array. Default is empty tuple.
    code : string, optional 
        C-code. One of code and code_path must be given. 
    code_path : string, optional
        Full path to c-code. One of code or code_path should be given.
    support_code : string, optional 
        C support code. This code will be inserted before the function 
        containing the c-code above. This can include any valid C code 
        including #includes and #defines.
    support_code_path : string, optional
        Full path to support code. 
    extension_kwargs : dictionary, optiona
        Keyword arguments to pass to the distutils.Extension constructor.
    return_type : python primitive type
        Either int or float.
    """
    # We first just try to run the code. This makes calling the code the 
    # second time the fastest thing we do. 
    try:
        return _FUNCS[unique_name](*args)
    except:
        pass
        
    # Next, we try to import the module and inline it again. This will make
    # calling the code the first time reasonably fast. 
    try:
        _import(unique_name)
        return _FUNCS[unique_name](*args)
    except:
        pass

    # Now we can be as slow as we'd like. We either have an error or the 
    # code isn't compiled. We'll try to compile the code and call the function
    # again.
    # Note that we are generating the code here if the module isn't found,
    # but we don't try to see if the code is already written to disk. This 
    # allows the debug inline code to easily delete the module code. 
    with _COMP_LOCK:
        code_str = _string_or_path(code, code_path)
        support_code_str = _string_or_path(support_code, support_code_path)
        c_code = _gen_code(unique_name, code_str, py_types, np_types, 
                           support_code_str, return_type)
        _build_install_module(c_code, unique_name, extension_kwargs)
        _import(unique_name)

    return _FUNCS[unique_name](*args)
    

def inline_debug(unique_name, args=(), py_types=(), np_types=(), code=None, 
                 code_path=None, support_code=None, support_code_path=None,
                 extension_kwargs={}, return_type=None):
    """Same as inline, but the types of each argument are checked, and 
    the code is recompiled the first time this function is called. 
    """
    # Check args, py_types and np_types for iterability.
    assert(np.iterable(args))
    assert(np.iterable(py_types))
    assert(np.iterable(np_types))

    # Check that code and code path aren't both None, or not None.
    assert code is not None or code_path is not None
    assert not (code is not None and code_path is not None)

    # Check support_code and support_code_path aren't both given.
    assert not (support_code is not None and support_code_path is not None)

    # Check paths if they are used. 
    if code_path is not None:
        assert(os.path.exists(code_path))
        
    if support_code_path is not None:
        assert(os.path.exists(support_code_path))

    # Type check python arguments.
    for py_obj, (py_type, c_name) in zip(args[:len(py_types)], py_types):
        assert isinstance(py_obj, py_type), 'Type err: {0}'.format(c_name)
        assert py_type in (int, float), 'Bad type: {0}'.format(py_type)
        
    # Type check numpy arguments. 
    for np_obj, (np_type, ndim, c_name) in zip(args[len(py_types):], np_types):
        assert np_obj.dtype == np_type, 'Type err: {0}'.format(c_name)
        assert np_obj.ndim == ndim, 'Bad dims: {0}'.format(c_name)

    # Type check the return type. 
    assert return_type in (None, int, float)

    # If this is the first call to this function, delete the module to force
    # a recompilation. 
    if unique_name not in _FUNCS and os.path.exists(_mod_path(unique_name)):
        os.unlink(_mod_path(unique_name))
    
    return inline(unique_name, args, py_types, np_types, code, code_path, 
                  support_code, support_code_path, extension_kwargs, 
                  return_type)
