import re
import sys

header = """
========================================
         METÁSTASIS v0.0.0.2
     Larax experimental interpreter
  Now with variable support!  (x = 5)
========================================
"""
print(header)

# Regex para línea de asignación  <identificador> = <expr>
ASSIGN_RE = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$')
VALID_ID  = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

# Tabla de símbolos
env = {}

def eval_expr(expr: str):
    """Evalúa una expresión usando el entorno env, con seguridad básica."""
    # Reemplazá cada ident por su valor en env, si existe
    tokens = re.split(r'(\W)', expr)   # separa por no‑palabras
    resolved = []
    for tok in tokens:
        if VALID_ID.fullmatch(tok) and tok in env:
            resolved.append(str(env[tok]))
        else:
            resolved.append(tok)
    safe_expr = ''.join(resolved)
    return eval(safe_expr)

while True:
    try:
        line = input("» ").strip()
        if line in ("exit", "quit"):      # salir
            sys.exit(0)
        if not line:
            continue

        # ¿Asignación?
        m = ASSIGN_RE.match(line)
        if m:
            ident, expr = m.groups()
            if ident in ("print", "exit"):   # palabras reservadas mínimas
                print(f"❌ '{ident}' is a reserved keyword")
                continue
            try:
                value = eval_expr(expr)
                env[ident] = value
                print(f"✅ {ident} = {value}")
            except Exception as e:
                print("❌ Error evaluating expression:", e)
        # ¿Comando print?
        elif line.startswith("print"):
            try:
                inside = line[len("print"):].strip()
                result = eval_expr(inside)
                print(result)
            except Exception as e:
                print("❌ Error in print:", e)
        # Expresión suelta
        else:
            try:
                result = eval_expr(line)
                print(result)
            except NameError as e:
                print("❌ Undefined variable:", e)
            except Exception as e:
                print("❌ Error:", e)

    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
        break
