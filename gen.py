

# script to generate a tileset from a spritesheet

w = 208 // 8
h = 152 // 8

with open("gen.txt", "w") as f:
    for j in range(h):
        for i in range(w):
            f.write(f"""{{
                "tid": {i + j * w + 1},
                "offset": [{i * 8}, {j * 8}]
            }},""")
