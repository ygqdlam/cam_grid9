from flask import Flask, render_template, request, jsonify
import os, random, time
from utils import compute_mask_grid_cells
from datetime import datetime

app = Flask(__name__)

IMAGE_FOLDER = "static/images"
MASK_FOLDER = "static/masks"

# Build image list (up to 100 random)
all_images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg','.jpeg','.png'))]
image_list = random.sample(all_images, 100) if len(all_images) > 100 else all_images

# per-user state
image_index = {}          # user_id -> idx in image_list
correct_cells_map = {}    # user_id -> set of correct cells for current image
start_times = {}          # <<< 新增：记录当前图开始时间
total_images = len(image_list)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/next_image", methods=["GET"])
def next_image():
    user_id = request.args.get("user")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    idx = image_index.get(user_id, 0)
    if idx >= len(image_list):
        return jsonify({"done": True, "current": idx, "total": total_images})

    image_name = image_list[idx]
    base, _ = os.path.splitext(image_name)
    mask_name = f"{base}.png"
    mask_path = os.path.join(MASK_FOLDER, mask_name)

    # compute which 3x3 cells contain mask>0 (white)
    correct = compute_mask_grid_cells(mask_path, grid_size=(3,3), min_ratio=0.001)
    correct_cells_map[user_id] = correct

    image_index[user_id] = idx
    start_times[user_id] = time.time()     # <<< 新增：记下开始时间

    has_target = bool(correct)

    return jsonify({
        "image": f"/static/images/{image_name}",
        "mask": f"/static/masks/{mask_name}",
        "image_name": image_name,
        "current": idx + 1,
        "total": total_images,
        "has_target": has_target
    })


@app.route("/timeout", methods=["POST"])
def timeout():
    user_id = request.args.get("user")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    data = request.get_json(silent=True) or {}
    image_name = data.get("image_name", "")

    # <<< 新增：写入 CSV 日志（项目根目录 annotations.csv）
    log_path = os.path.join(os.path.dirname(__file__), "annotations.csv")
    new_file = not os.path.exists(log_path)
    system_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a", newline="", encoding="utf-8") as fp:
        import csv
        with open(log_path, "a", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            if new_file:
                writer.writerow(["image_name", "correct_cells", "user_id", "selected_cells", "elapsed_seconds", "all_correct", "timeout", "system_time"])
            writer.writerow([ image_name, None , user_id , None ,None  ,None , 'True', system_time ])

    # 让这个用户进入下一张图
    image_index[user_id] = image_index.get(user_id, 0) + 1
    return jsonify({"timeout": True})



@app.route("/validate", methods=["POST"])
def validate():
    user_id = request.args.get("user")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    data = request.get_json(silent=True) or {}
    selected = set(data.get("selected_cells", []))
    correct = correct_cells_map.get(user_id, set())

    # <<< 新增：打印调试信息（终端可见）
    #print(f"[DEBUG] 正确集合: {sorted(list(correct))}, 用户点击: {sorted(list(selected))}")

    missing = sorted(list(correct - selected))
    extra = sorted(list(selected - correct))
    all_correct = (selected == correct)

    # <<< 新增：计算本张用时
    start_t = start_times.get(user_id)
    elapsed = round(time.time() - start_t, 3) if start_t else 0.0

    # <<< 新增：将集合编码为字符串
    encode = lambda s: ",".join(str(i) for i in sorted(list(s)))
    correct_enc  = encode(correct)
    selected_enc = encode(selected)

    # <<< 新增：写入 CSV 日志（项目根目录 annotations.csv）
    log_path = os.path.join(os.path.dirname(__file__), "annotations.csv")
    new_file = not os.path.exists(log_path)
    system_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        import csv
        with open(log_path, "a", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            if new_file:
                writer.writerow(["image_name", "correct_cells", "user_id", "selected_cells", "elapsed_seconds", "all_correct", "timeout", "system_time"])
            writer.writerow([data.get("image_name", ""), correct_enc, user_id, selected_enc, elapsed, bool(all_correct), 'False', system_time])
    except Exception as e:
        print("[LOG ERROR]", e)
        
    if all_correct:
        image_index[user_id] = image_index.get(user_id, 0) + 1

    return jsonify({
        "all_correct": all_correct,
        "missing": missing,
        "extra": extra,
        "need": sorted(list(correct))
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)