(* -------------------------------------------------------------------- *)
open Core

(* -------------------------------------------------------------------- *)
module Ident : sig
  type ident = private string

  val make : string -> ident
  val to_string : ident -> string

  module C : Interfaces.OrderedType with type t = ident
end = struct
  type ident = string

  module H = Weak.Make(struct
    type t = string

    let equal   = ((=) : t -> t -> bool)
    let compare = (compare : t -> t -> int)
    let hash    = (Hashtbl.hash : t -> int)
  end)

  let table = H.create 0

  let make (s : string) : ident =
    H.merge table s

  let to_string (i:ident) : string =
    i

  module C : Interfaces.OrderedType with type t = ident = struct
    type t = ident

    let compare = String.compare
  end
end

module IdentMap = Map.Make(Ident.C)
module IdentSet = Set.Make(Ident.C)

(* -------------------------------------------------------------------- *)
type symbol  = string
type qsymbol = (string list * string)
type ident   = Ident.ident
type wsize   = Big_int.big_int

(* ------------------------------------------------------------------- *)
module QSymbol : sig
  val to_string : qsymbol -> string
  val equal     : qsymbol -> qsymbol -> bool
end = struct
  let to_string ((nm, x) : qsymbol) =
    String.concat "." (nm @ [x])

  let equal = ((=) : qsymbol -> qsymbol -> bool)
end

(* -------------------------------------------------------------------- *)
type uniop = Syntax.puniop
type binop = Syntax.pbinop
type assop = Syntax.passop

(* -------------------------------------------------------------------- *)
type refined = private unit
type raw     = private unit

type type_ =
  | TUnit
  | TBool
  | TInt     of [`Int | `Nat | `Pos | `Natm of expr]
  | TString
  | TWord    of wsize
  | TTuple   of type_ list
  | TArray   of type_ * Big_int.big_int option
  | TRange   of Big_int.big_int * Big_int.big_int
  | TRefined of type_ * expr
  | TResult  of type_
  | TNamed   of qsymbol

and hotype = type_ list * type_

(* -------------------------------------------------------------------- *)
and expr =
  | EVar    of ident
  | EUnit
  | EBool   of bool
  | EUInt   of Big_int.big_int
  | EString of string
  | ETuple  of expr list
  | EArray  of expr list
  | ERange  of expr
  | EEq     of bool * (expr * expr)
  | EUniOp  of uniop * expr
  | EBinOp  of binop * (expr * expr)
  | ECall   of ident * hoexpr list
  | EGet    of expr * slice
  | EFun    of ident list * expr

and slice  = [ `One of expr | `Slice of expr * expr ]
and hoexpr = [`Expr of expr | `Proc of ident]

(* -------------------------------------------------------------------- *)
type tyexpr = expr * type_

(* -------------------------------------------------------------------- *)
let twordi (i : int) = TWord (Big_int.of_int i)

let tword1   = twordi   1
let tword8   = twordi   8
let tword16  = twordi  16
let tword32  = twordi  32
let tword64  = twordi  64
let tword128 = twordi 128
let tword256 = twordi 256

(* -------------------------------------------------------------------- *)
let hotype1 (ty : type_) : hotype = ([], ty)

(* -------------------------------------------------------------------- *)
let rec string_of_type (ty : type_) =
  match ty with
  | TUnit    -> "unit"
  | TBool    -> "bool"
  | TInt _   -> "int[.]"
  | TString  -> "string"
  | TWord _  -> "word[.]"

  | TTuple tys ->
      Format.sprintf "tuple[%s]"
        (String.concat ", " (List.map string_of_type tys))

  | TArray (ty, None) ->
      Format.sprintf "array[%s]" (string_of_type ty)

  | TArray (ty, Some i) ->
      Format.sprintf "array[%s, %s]"
        (string_of_type ty) (Big_int.string_of_big_int i)

  | TRange (i, j) ->
      Format.sprintf "range[%s, %s]"
        (Big_int.string_of_big_int i)
        (Big_int.string_of_big_int j)

  | TRefined (ty, _) ->
      Format.sprintf "refine[%s]" (string_of_type ty)

  | TResult (ty) ->
      Format.sprintf "result[%s]" (string_of_type ty)

  | TNamed name ->
      Format.sprintf "named[%s]" (QSymbol.to_string name)

(* -------------------------------------------------------------------- *)
module Type : sig
  val eq : type_ -> type_ -> bool
  val compat : type_ -> type_ -> bool

  val is_unit    : type_ -> bool
  val is_bool    : type_ -> bool
  val is_int     : type_ -> bool
  val is_string  : type_ -> bool
  val is_word    : type_ -> bool
  val is_tuple   : type_ -> bool
  val is_array   : type_ -> bool
  val is_refined : type_ -> bool
  val is_range   : type_ -> bool

  val as_word  : type_ -> wsize
  val as_tuple : type_ -> type_ list
  val as_array : type_ -> type_

  val strip : type_ -> type_
end = struct
  let eq = ((=) : type_ -> type_ -> bool)

  let is_unit    = function TUnit      -> true | _ -> false
  let is_bool    = function TBool      -> true | _ -> false
  let is_int     = function TInt _     -> true | _ -> false
  let is_string  = function TString    -> true | _ -> false
  let is_word    = function TWord    _ -> true | _ -> false
  let is_tuple   = function TTuple   _ -> true | _ -> false
  let is_array   = function TArray   _ -> true | _ -> false
  let is_refined = function TRefined _ -> true | _ -> false
  let is_range   = function TRange   _ -> true | _ -> false

  let as_word  = function TWord  ws      -> ws  | _ -> assert false
  let as_tuple = function TTuple tys     -> tys | _ -> assert false
  let as_array = function TArray (ty, _) -> ty  | _ -> assert false

  let rec strip (ty : type_) : type_ =
    match ty with
    | TUnit           -> TUnit
    | TBool           -> TBool
    | TInt _          -> TInt `Int
    | TString         -> TString
    | TWord    ws     -> TWord ws
    | TTuple   t      -> TTuple (List.map strip t)
    | TArray   (t, _) -> TArray (strip t, None)
    | TRefined (t, _) -> strip t  
    | TResult  (t)    -> TResult(strip t)
    | TRange   _      -> TInt `Int
    | TNamed   _      -> ty

  let compat (ty1 : type_) (ty2 : type_) =
    eq (strip ty1) (strip ty2)
end

(* -------------------------------------------------------------------- *)
type instr =
  | IFail   of tyexpr
  | IReturn of tyexpr option
  | IAssign of (lvalue * assop) option * tyexpr
  | IIf     of (expr * block) * (expr * block) list * block option
  | IWhile  of (expr * block) * block option
  | IFor    of (ident * range * block) * block option

and block  = instr list
and range  = expr option * expr

and lvalue =
  | LVar   of ident
  | LTuple of lvalue list
  | LGet   of lvalue * slice

(* -------------------------------------------------------------------- *)
type tydecl  = { tyd_name : ident; tyd_body : type_; }
type vardecl = { vrd_name : ident; vrd_type : type_; vrd_init : expr; }

type 'env procdef = {
  prd_name : ident;
  prd_att  : (ident * hoexpr list) list;
  prd_args : (ident * hotype) list;
  prd_ret  : type_;
  prd_body : 'env * block;
  prd_subs : ('env procdef) list;
}

(* -------------------------------------------------------------------- *)
type 'env topdecl1 =
  | TD_TyDecl  of tydecl
  | TD_VarDecl of vardecl
  | TD_ProcDef of 'env procdef

(* -------------------------------------------------------------------- *)
type 'env program = ('env topdecl1) list
