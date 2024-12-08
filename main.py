import gradio as gr
from datasets import load_dataset

title = "elyza/ELYZA-tasks-100データセットの確認ツール"

# データセットのロード
ds = load_dataset("elyza/ELYZA-tasks-100")
data = ds["test"]
current_index = {"index": 0}


# データを表示する関数
def display_data(index, direction):
    i = int(index) if index.isdigit() else 0
    if direction == "next":
        if i + 1 < len(data):
            i += 1
    elif direction == "prev":
        if 0 < i:
            i -= 1
    else:
        i = min(max(i, 0), len(data) - 1)

    item = data[i]
    return i, item["input"], item["output"], item["eval_aspect"]


shortcut_js = """
<script>
function shortcuts(e) {

    if (e.key ==  'ArrowLeft') {
        document.getElementById("prev_button").click();
    }
    else if (e.key == 'ArrowRight') {
        document.getElementById("next_button").click();
    }
}
document.addEventListener('keyup', shortcuts, false);
</script>
"""

# Gradio インターフェースの構築
with gr.Blocks(title=title, head=shortcut_js) as demo:
    gr.Markdown(f"# {title}")
    with gr.Row():
        task_id = gr.Textbox(label=f"タスクID (0 - {len(data) - 1})")
        with gr.Row():
            prev_button = gr.Button("前へ", elem_id="prev_button")
            next_button = gr.Button("次へ", elem_id="next_button")
    input_display = gr.Textbox(label="Input", interactive=False)
    output_display = gr.Textbox(label="Output", interactive=False)
    eval_display = gr.Textbox(label="Eval Aspect", interactive=False)

    # ボタンの動作
    task_id.submit(
        display_data,
        inputs=[task_id, gr.Textbox(value=task_id, visible=False)],
        outputs=[task_id, input_display, output_display, eval_display],
    )
    prev_button.click(
        display_data,
        inputs=[task_id, gr.Textbox(value="prev", visible=False)],
        outputs=[task_id, input_display, output_display, eval_display],
    )
    next_button.click(
        display_data,
        inputs=[task_id, gr.Textbox(value="next", visible=False)],
        outputs=[task_id, input_display, output_display, eval_display],
    )

    # 起動時の表示
    demo.load(
        fn=display_data,
        inputs=[gr.Textbox(value="0", visible=False)],
        outputs=[task_id, input_display, output_display, eval_display],
    )

# アプリ起動
demo.launch()
