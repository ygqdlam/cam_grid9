from PIL import Image
import numpy as np

def compute_mask_grid_cells(mask_path, grid_size=(3,3), min_ratio=0.001):
    """
    Treat nonzero (white) pixels as target. Split mask into grid and
    return indices (0..rows*cols-1) of cells containing target.
    min_ratio: minimum fraction of target pixels in a cell to consider it positive.
    """
    # 使用PIL读取图像并转换为灰度图
    mask = Image.open(mask_path).convert("L")
    mask = np.array(mask)  # 转换为NumPy数组
    if mask is None:
        return set()

    h, w = mask.shape[:2]
    rows, cols = grid_size
    cell_h = h // rows
    cell_w = w // cols

    # 设定目标像素值（假设目标像素为非零值）
    target = (mask > 0)

    cells = set()
    for r in range(rows):
        for c in range(cols):
            y0 = r * cell_h
            x0 = c * cell_w
            y1 = h if r == rows - 1 else (r + 1) * cell_h
            x1 = w if c == cols - 1 else (c + 1) * cell_w
            cell = target[y0:y1, x0:x1]
            if cell.size == 0:
                continue
            ratio = float(np.count_nonzero(cell)) / float(cell.size)
            if ratio >= min_ratio:
                cells.add(r * cols + c)
    return cells
