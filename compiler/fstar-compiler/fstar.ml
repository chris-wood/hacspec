open Hacs.Core
open Hacs.Location
open Hacs.Syntax
open Hacs.Ast

module T = Hacs.Typing

let fstar_of_uniop u = 
  match u with
  | `Not -> "not"
  | `Neg -> "-"
  | `BNot -> "~"

let fstar_of_binop b = 
  match b with
  | `Add -> "+."
  | `Sub -> "-."
  | `Mul -> "*."
  | `Div -> "/."
  | `IDiv -> "/."
  | `Mod -> "%"
  | `Pow -> "**."
  | `BAnd -> "&."
  | `BOr -> "|."
  | `BXor -> "^."
  | `And -> "&&"
  | `Or -> "||"
  | `Lt -> "<."
  | `Gt -> ">."
  | `Le -> "<=."
  | `Ge -> ">=."
  | `LSL -> "<<."
  | `LSR -> ">>."
  
let fstar_of_assop b = 
  match b with
  | `Add -> "+."
  | `Sub -> "-."
  | `Mul -> "*."
  | `Div -> "/."
  | `IDiv -> "/."
  | `Mod -> "%"
  | `Pow -> "**."
  | `BAnd -> "&."
  | `BOr -> "|."
  | `BXor -> "^."
  | `Plain -> ""

let paren b s =
  if b then "("^s^")"
  else s
  
let rec fstar_of_expr b e =
  match e with
  | EVar v -> Ident.to_string v 
  | EUnit -> "()"
  | EBool b -> string_of_bool b 
  | EUInt u -> Big_int.string_of_big_int u
  | EString s -> "\""^s^"\""
  | ETuple el -> "("^String.concat "," (List.map (fstar_of_expr false) el)^")"
  | EArray el -> paren b ("array_createL ["^String.concat "; " (List.map (fstar_of_expr false) el)^"]")
  | ECall (i,[e]) when Ident.to_string i = "uint32" -> paren b ("uint32 "^fstar_of_hoexpr true e)
  | ECall (i,el) -> paren b (Ident.to_string i^" "^(String.concat " " (List.map (fstar_of_hoexpr true) el)))
  | EUniOp (u,e) -> paren b (fstar_of_uniop u ^ " " ^ (fstar_of_expr false e))
  | EBinOp (op,(e1,e2)) -> paren b (fstar_of_expr true e1 ^ " " ^ fstar_of_binop op ^ " " ^ fstar_of_expr true e2)
  | EEq (false,(e1,e2)) -> fstar_of_expr true e1 ^ " = " ^ fstar_of_expr true e2
  | EEq (true,(e1,e2)) -> fstar_of_expr true e1 ^ " <> " ^ fstar_of_expr true e2
  | EGet(e1,`One e2) -> (fstar_of_expr true e1)^".["^(fstar_of_expr false e2)^"]"
  | EGet(e1,`Slice (e2,e3)) -> paren b ("array_slice "^(fstar_of_expr true e1)^" "^(fstar_of_expr true e2)^" "^(fstar_of_expr true e3))
  | EFun(xl,e) -> "(fun "^String.concat " " (List.map Ident.to_string xl)^" -> "^fstar_of_expr false e^")"
  | _ -> ("not an f* expr:")

and fstar_of_hoexpr b e =
  match e with
  | `Expr e -> fstar_of_expr b e
  | `Proc p -> Ident.to_string p

let rec fstar_of_lvalue b e =
  match e with
  | LVar v -> let e = Ident.to_string v in e,e
  | LTuple el -> let l1,e1 = List.split (List.map (fstar_of_lvalue false) el) in
                 let e = "("^String.concat "," l1^")" in e,e
  | LGet(e1,`One e2) -> let l1,e1 = fstar_of_lvalue true e1 in
                        let e = e1^".["^(fstar_of_expr false e2)^"]" in
                        (l1,e)
  | LGet(e1,`Slice (e2,e3)) ->
                        let l1,e1 = fstar_of_lvalue true e1 in
                        let e = "slice "^e1^" "^(fstar_of_expr true e2)^" "^(fstar_of_expr true e3) in
                        (l1,e)

let rec fstar_of_type b ty =
  match ty with
  | TUnit    -> "unit"
  | TBool    -> "bool"
  | TInt `Int  -> "int"
  | TInt `Nat  -> "nat"
  | TInt `Pos  -> "pos"
  | TInt (`Natm x)  -> "natmod_t "^ (fstar_of_expr true x)
  | TString  -> "string"
  | TWord sz -> begin
      let sizes = 
        [(  1, "bit_t"  );
         (  8, "uint8_t");
         ( 16, "uint8_t");
         ( 32, "uint8_t");
         ( 64, "uint8_t");
         (128, "uint8_t")] in

      Option.default_delayed
        (fun () -> Format.sprintf "uintn_t %s" (Big_int.string_of_big_int sz))
        (List.Exceptionless.find_map
           (fun (i, name) ->
             if Big_int.eq_big_int (Big_int.big_int_of_int i) sz then
               Some name
             else None) sizes)
    end

  | TTuple tys ->
        "("^(String.concat " * " (List.map (fstar_of_type false) tys))^")"

  | TArray (ty, None) ->
       if b then Format.sprintf "(vlarray_t %s)" (fstar_of_type true ty)
       else Format.sprintf "vlarray_t %s" (fstar_of_type true ty) 
 
      
  | TArray (ty, Some i) ->
       if b then
        Format.sprintf "(array_t %s %s)"
        (fstar_of_type true ty) (Big_int.string_of_big_int i)
       else 
        Format.sprintf "array_t %s %s"
        (fstar_of_type true ty) (Big_int.string_of_big_int i)

  | TRange (i, j) ->
      Format.sprintf "range_t %s %s"
        (Big_int.string_of_big_int i)
        (Big_int.string_of_big_int j)

  | TRefined (ty, EFun([x],e)) ->
      Format.sprintf "(%s:%s{%s})" (Ident.to_string x) (fstar_of_type false ty) (fstar_of_expr false e)

  | TNamed name ->
      Format.sprintf "%s" (QSymbol.to_string name)

  | TResult ty ->
      Format.sprintf "result_t %s" (fstar_of_type true ty)

  | _ -> "TODO TYPE ******"

and fstar_of_hotype b (sg, ty) =
  String.concat " -> " (List.map (fstar_of_type b) (sg @ [ty]))
       
module IdentSet = Set.Make(String)
let rec lvars il =
  match il with
  | [] -> IdentSet.empty
  | IFail te :: r -> IdentSet.empty
  | IReturn None :: r -> IdentSet.empty
  | IReturn (Some (e,t)) :: r -> IdentSet.empty
  | IAssign (None,(e,t)) :: r -> lvars r
  | IAssign (Some(LVar v as p,op),(e,t)) :: r -> IdentSet.add (Ident.to_string v) (lvars r)
  | IAssign (Some(LTuple tl as p,op),(e,t)) :: r -> List.fold_left (fun s v -> match v with LVar v -> IdentSet.add (Ident.to_string v) s | _ -> s) (lvars r) tl
  | IAssign (Some(LGet(LVar v,sl) as p,op),(e,t)) :: r -> IdentSet.add (Ident.to_string v) (lvars r)
  | IIf ((e,b),ebl,bo) :: r ->
     let else_b = match bo with | None -> IdentSet.empty | Some b -> lvars b in
     List.fold_left (fun s (e,b) -> IdentSet.union (lvars b) s)
                                   (IdentSet.union else_b (IdentSet.union (lvars b) (lvars r))) ebl
  | IFor ((i,rg,b),None) :: r -> IdentSet.union (IdentSet.remove (Ident.to_string i) (lvars b)) (lvars r)
  | _ -> IdentSet.empty


let rec fstar_of_instrs il fin =
  match il with
  | [] -> fin
  | IFail te :: [] when fin = "" -> "failwith \"\""
  | IReturn None :: [] when fin = "" -> "()"
  | IReturn (Some (e,t)) :: [] when fin = "" -> fstar_of_expr false e
  | IAssign (None,(e,t)) :: r -> "let _ = "^fstar_of_expr false e^" in \n"^fstar_of_instrs r fin
  | IAssign (Some(LVar _ as p,op),(e,t)) :: r 
  | IAssign (Some(LTuple _ as p,op),(e,t)) :: r ->
     assign p None op e r fin
  | IAssign (Some(LGet(LVar v,sl) as p,op),(e,t)) :: r ->
     assign p (Some sl) op e r fin
  | IIf ((e,b),[],bo) as i :: r ->
     let lvs = IdentSet.elements (lvars [i]) in
     let tup = match lvs with [] -> "()" | [x] -> x | tl -> "("^String.concat "," tl^")" in
     let else_b = match bo with None -> tup | Some b -> fstar_of_instrs b tup in
     let ife = "if "^fstar_of_expr false e^" then "^fstar_of_instrs b tup^" else " ^ else_b in
     if r = [] && tup = fin then ife
     else "let "^tup^" = "^ife^" in \n"^fstar_of_instrs r fin
  | IFor ((v,(None,e),b),None) as i :: r ->
     let lvs = IdentSet.elements (IdentSet.remove (Ident.to_string v) (lvars b)) in
     let tup = match lvs with [] -> "()" | [x] -> x | tl -> "("^String.concat "," tl^")" in
     let fore = "repeati "^fstar_of_expr true e^" (fun "^Ident.to_string v^" "^tup^" -> "^fstar_of_instrs b tup^") "^tup in
     if r = [] && tup = fin then fore
     else "let "^tup^" = "^fore^" in \n"^fstar_of_instrs r fin
  | _ -> "TODO: fstar_of_instrs ****"

and assign p slo op e r fin =
  let l,le = fstar_of_lvalue false p in
  let e = 
    match op with
    | `Plain -> fstar_of_expr false e
    | _ -> le ^ " " ^ fstar_of_assop op ^ " " ^ fstar_of_expr false e
  in
  let e =
    match slo with
    | None -> e
    | Some (`One _) -> le ^" <- "^e
    | Some (`Slice _) -> "array_update_"^le^" ("^e^")"
  in
  if (r = [] && l = fin) then e
  else "let "^l^" = "^e^" in \n"^fstar_of_instrs r fin
    
  
let fstar_of_topdecl d =
    match d with
    | TD_TyDecl td ->  "let "^Ident.to_string td.tyd_name^" : Type0 = "^fstar_of_type false td.tyd_body
    | TD_VarDecl vd -> "let "^Ident.to_string vd.vrd_name^" : "^fstar_of_type false vd.vrd_type^" = "^fstar_of_expr false vd.vrd_init
    | TD_ProcDef pd -> "let "^Ident.to_string pd.prd_name^" "^(String.concat " " (List.map (fun (v,t) -> "(" ^ Ident.to_string v ^ " : " ^ fstar_of_hotype false t ^ ")") pd.prd_args)) ^" : " ^(fstar_of_type false pd.prd_ret)^" = \n"^fstar_of_instrs (snd pd.prd_body) ""
let fstar_of_program (n:string) (p: T.Env.env * T.Env.env program) : string =
    let e,dl = p in
    "module " ^(String.capitalize_ascii n)^"\n"^
    "open Speclib\n"^
    "#reset-options \"--z3rlimit 60\""^
    String.concat "\n" (List.map fstar_of_topdecl dl) ^"\n"


