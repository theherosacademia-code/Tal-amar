import zipfile, re, shutil, sys, os

def add_outlines(src, dst, min_sz=2000):
    """Inject a black text outline on every white text run in a PPTX.
    min_sz: only runs at/above this size (hundredths of a point) get an outline."""
    shutil.copy(src, dst)
    zin = zipfile.ZipFile(src)
    names = zin.namelist()
    out = {}
    touched = 0
    for n in names:
        data = zin.read(n)
        if not re.match(r'ppt/slides/slide\d+\.xml$', n):
            out[n] = data
            continue
        x = data.decode('utf-8')

        def fix_run(m):
            nonlocal touched
            run = m.group(0)
            if '<a:ln' in run:
                return run
            # white fill?
            if not re.search(r'<a:solidFill>\s*<a:srgbClr val="FFFFFF"\s*/>\s*</a:solidFill>', run):
                return run
            rpr = re.search(r'<a:rPr\b[^>]*>', run)
            if not rpr:
                return run
            sz = re.search(r'\bsz="(\d+)"', rpr.group(0))
            size = int(sz.group(1)) if sz else 0
            if size < min_sz:
                return run
            w = int(size * 0.04 * 127)          # ~4% of the type size, in EMU
            ln = (f'<a:ln w="{w}" cap="rnd"><a:solidFill><a:srgbClr val="000000"/>'
                  f'</a:solidFill><a:round/></a:ln>')
            touched += 1
            return run.replace(rpr.group(0), rpr.group(0) + ln, 1)

        x = re.sub(r'<a:r>.*?</a:r>', fix_run, x, flags=re.S)
        out[n] = x.encode('utf-8')
    zin.close()
    zo = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
    for n in names:
        zo.writestr(n, out[n])
    zo.close()
    return touched

if __name__ == '__main__':
    n = add_outlines(sys.argv[1], sys.argv[2])
    print(f"outlined {n} runs -> {sys.argv[2]}")
