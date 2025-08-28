#!/usr/bin/env python3
# fix_nullable_unions.py
import json, sys, copy

NULL = {"type": "null"}

def infer_type(sch: dict):
    """If no explicit 'type', try to infer (object/array) from keywords."""
    if "type" in sch:
        return sch["type"]
    if "properties" in sch or "required" in sch or "additionalProperties" in sch:
        return "object"
    if "items" in sch:
        return "array"
    return None  # unknown

def merge_nullable(node):
    """
    If node has anyOf/oneOf with exactly one null-branch and one non-null branch,
    collapse to {type:[nonNullTypes..., "null"], ...nonNullKeywords...}.
    """
    if not isinstance(node, dict):
        return

    # Recurse first
    for k, v in list(node.items()):
        if isinstance(v, dict):
            merge_nullable(v)
        elif isinstance(v, list):
            for it in v:
                if isinstance(it, dict):
                    merge_nullable(it)

    for key in ("anyOf", "oneOf"):
        alts = node.get(key)
        if not isinstance(alts, list) or len(alts) != 2:
            continue

        # Partition into null vs non-null
        null_branches = [a for a in alts if isinstance(a, dict) and a.get("type") == "null"]
        nonnull = [a for a in alts if isinstance(a, dict) and a.get("type") != "null"]

        # Also handle cases where non-null has no explicit type but is clearly object/array
        if not nonnull:
            candidates = [a for a in alts if isinstance(a, dict)]
            if candidates:
                t = infer_type(candidates[0])
                if t:
                    nonnull = [copy.deepcopy(candidates[0])]
                    nonnull[0]["type"] = t

        if len(null_branches) == 1 and len(nonnull) == 1:
            nn = copy.deepcopy(nonnull[0])

            # Collect non-null types as list
            nn_type = nn.get("type")
            if isinstance(nn_type, list):
                types = list(dict.fromkeys([*nn_type, "null"]))  # dedupe preserve order
            elif nn_type is None:
                types = ["null"]  # fallback (shouldn’t happen after infer)
            else:
                types = [nn_type, "null"]

            # Build the replacement: start with nn’s keys, then set 'type'
            replacement = {k: v for k, v in nn.items() if k != "type"}
            replacement["type"] = types

            # If parent had a default:null (common), keep it; otherwise don’t force defaults
            if node.get("default", None) is None and "default" in node:
                replacement["default"] = None
            elif "default" in node and node["default"] is not None:
                replacement["default"] = node["default"]

            # Preserve parent-level descriptive keys if present
            for meta in ("title", "description", "examples", "deprecated", "readOnly", "writeOnly"):
                if meta in node and meta not in replacement:
                    replacement[meta] = node[meta]

            # Replace node in-place
            node.clear()
            node.update(replacement)
            break  # done with this node

def main():
    data = json.load(sys.stdin)
    merge_nullable(data)
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
