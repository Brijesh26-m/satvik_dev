import fitz
import os

doc = fitz.open('Satvik Roots breif and prompts.pdf')
os.makedirs('test_output/pdf_images', exist_ok=True)
count = 0
for i, page in enumerate(doc):
    for j, img in enumerate(page.get_images()):
        xref = img[0]
        b = doc.extract_image(xref)
        ext = b['ext']
        w = b['width']
        h = b['height']
        fn = f'test_output/pdf_images/page_{i+1}_img_{j+1}.{ext}'
        with open(fn, 'wb') as f:
            f.write(b['image'])
        print(f"Saved {fn} ({w}x{h})")
        count += 1

print(f"Total extracted: {count}")
