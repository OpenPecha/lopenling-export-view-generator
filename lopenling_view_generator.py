from pathlib import Path

from openpecha.core.pecha import OpenPechaFS

def get_base_names(opf_path):
    base_names = []
    for base_path in list((opf_path / "base").iterdir()):
        base_names.append(base_path.stem)
    return base_names


def save_lopenling_plain_view(text_title, base_text, output_dir):
    lopenling_view = base_text.replace("\n", "")
    (output_dir / f"{text_title}.txt").write_text(lopenling_view, encoding='utf-8')

def get_page_annotation(ann):
    pg_ann = ''
    img_num = int(ann['imgnum'])
    folio_num = img_num//2
    if img_num%2 == 0:
        pg_ann = f"[{folio_num-1}བ]"
    else:
        pg_ann = f"[{folio_num}ན]"
    return pg_ann


def save_lopenling_layout_view(text_title, base_text, pagination_layer, output_dir):
    layout_view = ""
    char_walker = 0
    for _, ann in pagination_layer['annotations'].items():
        page_start = ann['span']['start']
        page_end = ann['span']['end']
        page_ann = get_page_annotation(ann)
        layout_view += f"{page_ann}{base_text[page_start:page_end+1]}\n"
    layout_view = layout_view.strip()
    (output_dir / f"{text_title}_layout.txt").write_text(layout_view, encoding='utf-8')


def serialize_lopenling_views(opf_path, output_dir):
    pecha_id = opf_path.stem
    pecha = OpenPechaFS(pecha_id, opf_path)
    base_names = get_base_names(opf_path)
    for base_name in base_names:
        text_title = pecha.meta.source_metadata['base'][base_name]['title']
        base_text = pecha.read_base_file(base_name)
        pagination_layer = pecha.read_layers_file(base_name, "Pagination")
        (output_dir / pecha_id).mkdir(parents=True, exist_ok=True)
        text_output_dir = (output_dir / pecha_id)
        save_lopenling_plain_view(text_title, base_text, text_output_dir)
        if "O" == pecha_id[0]:
            continue
        save_lopenling_layout_view(text_title, base_text, pagination_layer, text_output_dir)

if __name__ == "__main__":
    opf_paths = list(Path('./data/opfs/').iterdir())
    output_dir = Path('./data/lopenling_views/')
    for opf_path in opf_paths:
        opf_path = opf_path / f"{opf_path.stem}.opf"
        serialize_lopenling_views(opf_path, output_dir)