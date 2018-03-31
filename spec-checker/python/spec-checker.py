#!/usr/bin/python3

from typed_ast.ast3 import *
from sys import argv, exit, exc_info
import builtins
import os
from collections import Iterable
from speclib_i import *

DEBUG_PRINT = True


def print(*args, **kwargs):
    if DEBUG_PRINT:
        builtins.print(*args, **kwargs)


class AstItem():
    def __init__(self, t, args=None):
        self.t = t
        self.args = []
        if args is not None:
            if isinstance(args, str):
                self.args.append(args)
            else:
                for a in args:
                    self.args.append(a)

    def __str__(self):
        return str(self.t) + ": " + str(self.args)

    def __repr__(self):
        return str(self)

    def get_function_signature(self):
        assert(self.t.__name__ == "FunctionDef")
        assert(isinstance(self.args[0], FunctionSignature))
        return self.args[0]

    def get_function_call(self):
        assert(self.t.__name__ == "Call")
        fun = self.args[0]
        # print(type(fun.args[0]))
        if type(fun.args[0]) == str:
            name = fun.args[0]
        elif type(fun.args[0]).__name__ == "AstName":
            name = fun.args[0].args[0]
        else:
            assert(False)
        args = self.args[1]
        assert(args.t.__name__ == "List")
        types = []
        for arg in args.args:
            # TODO: Arguments that are variables are names. We have to get the type
            # if arg.t.__name__ == "Name":
            #     print(arg.args[-1].t)
            #     print(arg.args[0].args[0])
            types.append(arg.t)
        class_ = ""
        if len(fun.args) > 1:
            class_ = fun.args[1].args[0]
        return (class_, name, types)


class AstName(AstItem):
    def __init__(self, name):
        super().__init__(str, [name])
        self.type = None

    def __str__(self):
        t = ""
        if self.type:
            t = ":" + str(self.type)
        return str(self.args[0]) + t

    def __repr__(self):
        return str(self)

    def set_type(self, t):
        if not (type(t) is type or type(t) is str):
            print("set_type only works with type or str ("+str(type(t))+")")
            exit(1)
        self.type = t

    def get_type(self):
        return self.type

    def get_name(self):
        return str(self.args[0])


class AstAttribute(AstItem):
    def __init__(self, name, cl):
        assert(type(name) == str)
        super().__init__(Attribute, [cl, AstName(name)])
        self.name = name
        self.class_ = cl

    def __str__(self):
        return str(self.class_) + "." + str(self.class_)

    def __repr__(self):
        return str(self)

    def get_function_name(self):
        return self.name

    def get_class_name(self):
        return self.class_

class Variable(AstItem):
    def __init__(self, t, name):
        assert(type(name) == str)
        super().__init__(t, [name])

    def __str__(self):
        return str(self.args[0]) + ": " + str(self.t)

    def __repr__(self):
        return str(self)

    def set_type(self, d):
        if type(d) is not FunctionSignature:
            print("set_type only works with FunctionSignature")
            exit(1)
        print(d)


class VariableTuple(AstItem):
    def __init__(self, names):
        assert(type(names) == list)
        super().__init__(Tuple, names)
        self.types = []

    def __str__(self):
        return str(self.args) + ": " + str(self.types)

    def __repr__(self):
        return str(self)

    def set_type(self, t):
        if type(t) is not list:
            print("Tuple.set_types type has to be a list.")
            exit(1)
        self.types = t

    def get_type(self):
        return self.types

    def get_name(self):
        return self.args


class VariableSubscript(AstName):
    def __init__(self, name, sl, slt):
        assert(type(name) == str)
        super().__init__(name)
        # TODO: verify slice
        self.slice = sl
        self.slice_type = slt

    def __str__(self):
        x = ""
        if self.slice_type is Slice:
            x = self.slice
        elif self.slice_type is Index:
            x = self.slice
        else:
            print("VariableSubscript has to be slice or index")
            assert(False)
        return str(self.args[0]) + " [" + str(x) + "]" + ": " + str(self.t)

    def __repr__(self):
        return str(self)


class FunctionCall(AstItem):
    def __init__(self, f):
        assert(type(f) == FunctionSignature)
        super().__init__(Call)
        self.fun = f

    def __str__(self):
        return str(self.fun)

    def __repr__(self):
        return str(self)

    def get_function_signature(self):
        return self.fun

class AstReader():
    def __init__(self, ast):
        self.ast = ast
        self.objects = []

    def read_function_signature(self, f):
        fun_name = f.name
        if f.args.args is not None:
            arg_types = [x.annotation.id for x in f.args.args]
            arg_names = [x.arg for x in f.args.args]
        if f.returns is not None:
            if isinstance(f.returns, Name):
                rt = f.returns.id
            elif isinstance(f.returns, Subscript):
                rt = f.returns.slice.value
                if not isinstance(rt, Tuple):
                    print("Return types have to be simple types or tuples, not " + str(type(rt)) + ".")
                    exit(1)
                rt = [x.id for x in rt.elts]
        else:
            print("Functions must have a return type (use None for void functions).")
            exit(1)
        if len(f.decorator_list) != 0:
            print("Function argument decorators are not supported in hacspec.")
            exit(1)
        if len(f.args.defaults) != 0:
            print("Default arguments are not supported in hacspec.")
            exit(1)
        if f.type_comment is not None:
            print("Type comments on functions are not allowed in hacspec.")
            exit(1)
        if len(f.args.kwonlyargs) != 0:
            print("keyword only args are not allowed in hacspec.")
            exit(1)
        if f.args.vararg is not None:
            print("varargs are not allowed in hacspec")
            exit(1)
        if len(f.args.kw_defaults) != 0:
            print("keyword defaults are not allowed in hacspec")
            exit(1)
        if f.args.kwarg is not None:
            print("keyword args are not allowed in hacspec")
            exit(1)
        # TODO: be stricter and check everything.
        return FunctionSignature.create(fun_name, arg_types, arg_names, rt)

    def read(self, node):
        # FIXME: this shouldn't be allowed
        if node is None:
            print(" >>>>>>>>> none node in spec (something is probably wrong)")
            return

        if isinstance(node, Module):
            return AstItem(Module, [self.read(node.body)])

        if isinstance(node, ImportFrom):
            return AstItem(ImportFrom, [node.module])

        if isinstance(node, Tuple):
            tuples = []
            for e in node.elts:
                tuples.append(str(self.read(e)))
            return VariableTuple(tuples)

        # Normal assignments with types in comments
        if isinstance(node, Assign):
            args = [self.read(t) for t in node.targets]
            # testing
            # for a in args:
            #     print("Assign: "+str(type(a)))
            # TODO: infer type from node.value read result.
            # ass = Variable(None, args[0])
            # print(ass)
            args.append(self.read(node.value))
            if node.type_comment:
                print("Type comments are not supported by hacspec")
                exit(1)
            return AstItem(Assign, args)

        if isinstance(node, AugAssign):
            target = self.read(node.target)
            op = self.read(node.op)
            value = self.read(node.value)
            # print("AugAssign: " + str(target) + str(op) + " = " + str(value))
            return AstItem(AugAssign, [target, op, value])

        if isinstance(node, AnnAssign):
            args = [self.read(node.target)]
            if node.value:
                args.append(self.read(node.value))
            args.append(self.read(node.annotation))
            return AstItem(AnnAssign, args)

        if isinstance(node, List):
            l = []
            for elt in node.elts:
                l.append(self.read(elt))
            return AstItem(List, l)

        if isinstance(node, Attribute):
            return AstAttribute(node.attr, self.read(node.value))

        if isinstance(node, BinOp):
            left = self.read(node.left)
            op = self.read(node.op)
            right = self.read(node.right)
            return AstItem(BinOp, [left, op, right])

        # Primitive types
        if isinstance(node, Num):
            return AstItem(Num)

        if isinstance(node, Name):
            return AstName(node.id)

        if isinstance(node, Load):
            return AstItem(Load)
        if isinstance(node, Store):
            return AstItem(Store)
        if isinstance(node, AugStore):
            return AstItem(AugStore)
        if isinstance(node, AugLoad):
            return AstItem(AugLoad)

        # Loops
        if isinstance(node, For):
            args = [self.read(node.target)]
            if node.body:
                args.append(self.read(node.body))
            if node.orelse:
                args.append(self.read(node.orelse))
            if node.iter:
                args.append(self.read(node.iter))
            return AstItem(For, args)

        # Operators
        if isinstance(node, Pow):
            return AstItem(Pow)
        if isinstance(node, Sub):
            return AstItem(Sub)
        if isinstance(node, Mult):
            return AstItem(Mult)
        if isinstance(node, Add):
            return AstItem(Add)
        if isinstance(node, Mod):
            return AstItem(Mod)
        if isinstance(node, FloorDiv):
            return AstItem(FloorDiv)
        if isinstance(node, Div):
            return AstItem(FloorDiv)
        if isinstance(node, BitXor):
            return AstItem(BitXor)
        if isinstance(node, RShift):
            return AstItem(RShift)
        if isinstance(node, BitAnd):
            return AstItem(BitAnd)
        if isinstance(node, BitOr):
            return AstItem(BitOr)
        if isinstance(node, UnaryOp):
            return AstItem(UnaryOp)
        if isinstance(node, Compare):
            return AstItem(Compare)
        if isinstance(node, LShift):
            return AstItem(LShift)

        if isinstance(node, BoolOp):
            values = [node.op]
            for ex in node.values:
                values.append(self.read(ex, prev=previous))
            return AstItem(BoolOp, values)

        if isinstance(node, Subscript):
            r = VariableSubscript(str(self.read(node.value)), node.slice, type(node.slice))
            return r
            # return AstItem(Subscript, [self.read(node.value), AstItem(slice, [node.slice])])

        # Functions
        if isinstance(node, FunctionDef):
            sig = self.read_function_signature(node)
            body = self.read(node.body)
            return AstItem(FunctionDef, [sig, body])

        if isinstance(node, Return):
            return AstItem(Return, [self.read(node.value)])

        if isinstance(node, Call):
            args = [self.read(node.func)]
            if node.args:
                args.append(self.read(node.args))
            # build function signature
            name = args[0]
            cl = ""
            if isinstance(name, AstAttribute):
                cl = name.get_class_name()
                name = name.get_function_name()
            f = FunctionSignature.create(str(name), [], args[1:], None, cl)
            r = FunctionCall(f)
            return r
            # TODO: read keywords?
            # return AstItem(Call, args)

        if isinstance(node, Expr):
            return AstItem(Expr, [self.read(node.value)])

        if isinstance(node, If):
            test = self.read(node.test)
            body = self.read(node.body)
            orelse = self.read(node.orelse)
            return AstItem(If, [test, orelse, body])

        if isinstance(node, While):
            test = self.read(node.test)
            body = self.read(node.body)
            orelse = self.read(node.orelse)
            return AstItem(While, [test, orelse, body])

        if isinstance(node, Str):
            return AstItem(Str, [node.s])

        if isinstance(node, arguments):
            args = [self.read(a) for a in node.args]
            if len(node.defaults) != 0:
                print("Default arguments are not supported in hacspec.")
                exit(1)
            if len(node.kwonlyargs) != 0:
                print("keyword only args are not allowed in hacspec.")
                exit(1)
            if node.vararg is not None:
                print("varargs are not allowed in hacspec")
                exit(1)
            if len(node.kw_defaults) != 0:
                print("keyword defaults are not allowed in hacspec")
                exit(1)
            if node.kwarg is not None:
                print("keyword args are not allowed in hacspec")
                exit(1)
            return AstItem(arguments, args)

        if isinstance(node, arg):
            return AstItem(arg)

        # TODO: lambdas are only allowed in refine_t statements
        if isinstance(node, Lambda):
            args = self.read(node.args)
            body = self.read(node.body)
            return AstItem(Lambda, [args, body])

        # Explicitly disallowed statements
        if isinstance(node, With):
            print("With is not allowed in hacspec.")
            exit(1)
        if isinstance(node, AsyncWith):
            print("AsyncWith is not allowed in hacspec.")
            exit(1)
        if isinstance(node, AsyncFor):
            print("AsyncFor is not allowed in hacspec.")
            exit(1)
        if isinstance(node, ClassDef):
            print("Classes are not allowed in hacspec.")
            exit(1)
        if isinstance(node, AsyncFunctionDef):
            print("AsyncFunctionDef is not allowed in hacspec.")
            exit(1)
        if isinstance(node, Raise):
            print("Raise is not allowed in hacspec.")
            exit(1)
        if isinstance(node, Try):
            print("Try is not allowed in hacspec.")
            exit(1)
        if isinstance(node, Assert):
            print("Assert is not allowed in hacspec.")
            exit(1)
        if isinstance(node, Delete):
            print("Delete is not allowed in hacspec.")
            exit(1)
        if isinstance(node, Global):
            print("Global is not allowed in hacspec.")
            exit(1)
        if isinstance(node, Nonlocal):
            print("Global is not allowed in hacspec.")
            exit(1)
        if isinstance(node, Break):
            print("Break is not allowed in hacspec.")
            exit(1)
        if isinstance(node, Continue):
            print("Continue is not allowed in hacspec.")
            exit(1)

        # Disallowed expressions
        if isinstance(node, ListComp):
            print("List comprehensions are not allowed in hacspec.")
            exit(1)
        if isinstance(node, IfExp):
            print("If expressions are not allowed in hacspec.")
            exit(1)

        # List of nodes, read all of them.
        if isinstance(node, list):
            nodes = []
            for x in node:
                nodes.append(self.read(x))
            return AstItem(List, nodes)

        # If we get here, it's not valid.
        print("Spec is not valid using " + str(type(node)))
        exit(1)

    def filter(self, parsed, obj):
        filtered = []
        def rec(x, obj, item=None):
            if isinstance(x, AstItem):
                for y in x.args:
                    if isinstance(x.t, type) and x.t.__name__ == self.to_find:
                        if item not in filtered:
                            filtered.append(x)
                    rec(y, obj, x)
            elif isinstance(x, list):
                for y in x:
                    rec(y, obj)
            else:
                if isinstance(item.t, type) and item.t.__name__ == self.to_find:
                    if item not in filtered:
                        filtered.append(item)
        for a in parsed.args:
            rec(a, obj)
        return filtered

    def read_objects(self, obj):
        mod = self.ast.body
        if mod is None:
            # ast root has to be Module.
            return []
        if not isinstance(mod, list):
            # The ast module is a list of nodes.
            return []
        self.to_find = obj.__name__
        parsed = self.read(self.ast)
        filtered = self.filter(parsed, obj)
        return filtered


class FileReader():
    def __init__(self, filename):
        self.filename = filename

    def read_functions(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as py_file:
                code = py_file.read()
                ast = parse(source=code, filename=self.filename)
                reader = AstReader(ast)
                functions = reader.read_objects(FunctionDef)
                return functions
        except:
            print("File is not a valid hacspec. Import is not a local spec.")
            return []
        return []


class FunctionSignature():
    def __init__(self):
        self.fun_name = ""
        self.argtypes = []
        self.argnames = []
        self.returntype = None
        self.class_ = ""

    def __str__(self) -> str:
        return self.fun_name + str(self.argtypes) + " -> " + str(self.returntype)

    @staticmethod
    def create(fun_name, arg_names, arg_types, rt, cl = ""):
        fs = FunctionSignature()
        fs.argnames = arg_types
        fs.argtypes = arg_names
        fs.returntype = rt
        fs.fun_name = fun_name
        fs.class_ = cl
        return fs

    def add_arg(self, arg):
        self.argnames.append(arg)

    def set_return_type(self, t):
        self.returntype = t

    def get_args(self):
        return self.argnames

    def get_arg_types(self):
        return self.argtypes

    def get_return_type(self):
        return self.returntype

    def get_fun_name(self):
        name = ""
        if self.class_:
            name += str(self.class_) + "."
        name += self.fun_name
        return name

    def get_class_name(self):
        return str(self.class_)


class Imported():
    def __init__(self, file_dir, reader):
        self.file_dir = file_dir
        self.fsigs = {}
        self.fun_list = []
        self.reader = reader
        self.read_modules()
        self.parse_functions()
        self.read_speclib()

    def read_speclib(self):
        for f in speclib:
            self.fsigs[f] = FunctionSignature.create(f, speclib[f][0], [], speclib[f][1])

    def parse_hacspec_file(self, filename):
        if filename == "speclib":
            # speclib is more complex to parse and it's not a valid hacspec.
            # TODO: We import those functions statically.
            return True
        filename = os.path.join(self.file_dir, filename + ".py")
        reader = FileReader(filename)
        functions = reader.read_functions()
        if len(functions) == 0:
            return False
        self.fun_list += functions
        return True

    def read_modules(self):
        imports = self.reader.read_objects(ImportFrom)
        for imp in imports:
            print("reading functions from import " + imp.args[0])
            if not self.parse_hacspec_file(imp.args[0]):
                print("Only other hacspecs can be imported")
                exit(1)

    def parse_functions(self):
        for f in self.fun_list:
            f = f.get_function_signature()
            self.fsigs[f.get_fun_name()] = f

    def get_function(self, fun):
        try:
            fs = self.fsigs[fun]
        except:
            print(fun + " is not a known hacspec function.")
            exit(1)
        return fs

    def check_function(self, fun, variables):
        fun_name = fun.get_fun_name()
        fs = None
        try:
            fs = self.fsigs[fun_name]
        except:
            print(fun_name + " is not a known hacspec function.")

        tas = []
        if fs is not None:
            fun_args = fun.get_args()
            return_type = fs.get_return_type()
            types = fs.get_arg_types()
            for (t, a) in zip(types, fun_args):
                a = a.args[0]
                ta = None
                if type(a) is FunctionCall:
                    arg_fsig = a.get_function_signature()
                    ta, variables = self.check_function(arg_fsig, variables)
                else:
                    ta = variables[str(a)]
                if t == ta:
                    print("type checked function argument")
                elif t == speclib_classes[ta]:
                    print("type checked function argument (inherited)")
                else:
                    print("Wrong type. Got " + str(t) + " expected " + str(ta))
                    exit(1)
                tas.append(ta)
        else:
            print("\"" + fun_name + "\" is not a defined function.")
            exit(1)
        return return_type, variables

class SpecChecker():
    def __init__(self, file_dir, reader):
        imported = Imported(file_dir, reader)
        # TODO: get types and constants from imports
        self.fun_sigs = imported.fsigs
        self.reader = reader
        spec_functions = self.reader.read_objects(FunctionDef)
        for fun in spec_functions:
            sig = fun.args[0]
            self.fun_sigs[sig.get_fun_name()] = sig

    def check_function(self, fun, variables):
        fun_name = fun.get_fun_name()
        fs = None
        try:
            fs = self.fun_sigs[fun_name]
        except:
            print(fun_name + " is not a known hacspec function.")

        tas = []
        if fs is not None:
            fun_args = fun.get_args()
            return_type = fs.get_return_type()
            types = fs.get_arg_types()
            for (t, a) in zip(types, fun_args):
                a = a.args[0]
                ta = None
                if type(a) is FunctionCall:
                    arg_fsig = a.get_function_signature()
                    ta, variables = self.check_function(arg_fsig, variables)
                else:
                    if a.t is Num:
                        ta = Num
                    else:
                        ta = variables[str(a)]
                class_ = None
                try:
                    class_ = speclib_classes[ta]
                except:
                    pass
                if t == ta:
                    print("type checked function argument")
                elif class_ is not None and t == class_:
                    print("type checked function argument (inherited)")
                else:
                    print("Wrong type. Got " + str(t) + " expected " + str(ta))
                    exit(1)
                tas.append(ta)
        else:
            print("\"" + fun_name + "\" is not a defined function.")
            exit(1)
        return return_type, variables


    def check_functions(self):
        functions = self.reader.read_objects(FunctionDef)
        for fun in functions:
            sig = fun.args[0]
            variables = {}
            print("processing " + sig.get_fun_name() + " ...")
            for (arg, arg_type) in zip(sig.get_args(), sig.get_arg_types()):
                variables[arg] = arg_type
            args = sig.get_args()
            body = fun.args[1:]
            for l in body[0].args:
                print("processing " + str(l))
                if l.t is Assign:
                    right = l.args[1]
                    return_type = None
                    if type(right) is FunctionCall:
                        #Get return type from function and check argument types
                        fsig = right.get_function_signature()
                        fun_name = fsig.get_fun_name()
                        fun_args = fsig.get_args()
                        return_type, variables = self.check_function(fsig, variables)
                        if return_type is None or fun_name in functions:
                            print("foooo")
                            exit(1)
                        elif return_type is None:
                            print("\"" + fun_name + "\" is not a defined function.")
                            exit(1)
                    elif type(right) is AstItem:
                        if right.t is BinOp:
                            # TODO: check math ops. We assume all these are nums for now
                            return_type = Num
                    elif type(right) is AstName:
                        # Assign type of right variable to left variable
                        return_type = right.get_type()
                        if return_type is None:
                            return_type = variables[str(right)]
                    elif type(right) is VariableSubscript:
                        if right.slice_type is Slice:
                            return_type = right.get_type()
                            if return_type is None:
                                # TODO: this isn't correct (lengths don't fit), we need to take the base type.
                                return_type = variables[right.get_name()]
                        else:
                            print("TODO: handle this slice type " + str(right.slice_type))
                            exit(1)
                    else:
                        print("TODO: process " + str(type(right)))
                    if return_type is None:
                        print("Couldn't determine variable type. Called " + str(l.t))
                        exit(1)
                    # Check variable type and set
                    var_type = l.args[0].get_type()
                    if not (var_type is None or var_type is return_type or type(var_type) is list):
                        print("Type error in assign. Got " + str(return_type) + " but expected " + str(var_type))
                        exit(1)
                    l.args[0].set_type(return_type)
                    var_name = l.args[0].get_name()
                    if type(var_name) is not list:
                        variables[var_name] = return_type
                    elif type(var_name) is list:
                        for (name, t) in zip(var_name, return_type):
                            variables[name] = t
                    else:
                        print("Error storing types (" + str(return_type) + ") for " + str(var_name))
                    print(variables)
                else:
                    print("TODO: process " + str(l.t))

# def check_function_calls(reader, imported):
#     # Take all function calls and check that they are properly typed.
#     calls = reader.read_objects(Call)
#     # FIXME: we have function twice in here.
#     for c in calls:
#         fc = c.get_function_call()
#         # print(fc)

# def get_variables(reader, imported):
#     # Make a list of all variables in the spec and their types
#     assigns = reader.read_objects(Assign)
#     assigns += reader.read_objects(AnnAssign)
#     assigns += reader.read_objects(AugAssign)
#     def get_return_value(fc):
#         if type(fc) is FunctionCall:
#             fsig = fc.get_function_signature()
#             fun = fsig.get_fun_name()
#             class_ = fsig.get_class_name()
#             if class_:
#                 print(class_+"."+fun)
#             else:
#                 expected_args = speclib[fun][0]
#                 expected_return = speclib[fun][1]
#                 # check arg types
#                 args = fsig.get_arg_types()[0].args
#                 if len(args) is not len(expected_args):
#                     print("Wrong arguments")
#                     print("expected: " + str(expected_args) + " -> " + str(expected_return))
#                     print("got: " + str(fsig))
#                     exit(1)
#                 for (expected, got) in zip(expected_args, args):
#                     if expected is not got.t:
#                         print("Wrong arguments")
#                         print("expected: " + str(expected_args) + " -> " + str(expected_return))
#                         print("got: " + str(fsig))
#                         exit(1)
#                 return expected_return

#         else:
#             # TODO: handle these
#             print("check " + str(fc))

#     for ass in assigns:
#         a = ass.args[0]
#         v = ass.args[1]
#         if type(a) is AstName:
#             t = get_return_value(v)
#         elif type(a) is VariableSubscript:
#             t = get_return_value(v)
#         elif type(a) is VariableTuple:
#             t = get_return_value(v)
#         else:
#             print("Error reading file. Didn't recognise this assign.")
#             assert(False)


def main(filename):
    with open(filename, 'r', encoding='utf-8') as py_file:
        file_dir = os.path.dirname(os.path.abspath(filename))
        code = py_file.read()
        ast = parse(source=code, filename=filename)

        # Get reader for ast
        reader = AstReader(ast)

        # Init spec checker
        checker = SpecChecker(file_dir, reader)
        checker.check_functions()
        # Read and process all functions in file
        # functions = reader.read_objects(FunctionDef)
        # process_function(functions, imported)

        # get_variables(reader, imported)
        # check_function_calls(reader, imported)
        # imported.get_function("chacha20_counter_mode")


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: spec-checker.py <your-hacpsec.py>")
        exit(1)
    main(argv[1])
