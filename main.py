import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, guess_lexer, PythonLexer
from pygments.formatters import ImageFormatter

def generate_card(
    file_list, theme, font_name, font_size, show_line_numbers, output_name, add_title, title_text
):
    style = "monokai" if theme == "dark" else "default"
    for file_path in file_list:
        if not os.path.isfile(file_path):
            messagebox.showerror("错误", f"文件不存在: {file_path}")
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        try:
            lexer = get_lexer_for_filename(file_path, code)
        except Exception:
            lexer = guess_lexer(code) if code.strip() else PythonLexer()
        if theme == "dark":
            line_number_bg = (40, 40, 40)
            line_number_fg = (200, 200, 200)
        else:
            line_number_bg = (255, 255, 255)
            line_number_fg = (80, 80, 80)
        formatter = ImageFormatter(
            font_name=font_name,
            font_size=font_size,
            line_numbers=show_line_numbers,
            image_format="BMP",
            style=style,
            line_number_bg=line_number_bg,
            line_number_fg=line_number_fg
        )
        img_data = highlight(code, lexer, formatter)
        base = os.path.splitext(os.path.basename(file_path))[0]
        out_file = output_name or f"{base}_card.bmp"
        out_file = out_file.replace("{basename}", base)
        with open(out_file, "wb") as f:
            f.write(img_data)
        if add_title and title_text:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.open(out_file)
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype(font_name, font_size + 8)
            except Exception:
                font = ImageFont.load_default()
            text_w, text_h = draw.textsize(title_text, font=font)
            new_img = Image.new("RGB", (img.width, img.height + text_h + 20), (255,255,255) if theme=="light" else (40,40,40))
            new_img.paste(img, (0, text_h + 20))
            draw = ImageDraw.Draw(new_img)
            draw.text(((img.width - text_w) // 2, 10), title_text, fill=(0,0,0) if theme=="light" else (255,255,255), font=font)
            new_img.save(out_file)
        messagebox.showinfo("完成", f"已生成：{out_file}")

def select_files(entry):
    files = filedialog.askopenfilenames(title="选择代码文件")
    if files:
        entry.delete(0, tk.END)
        entry.insert(0, ";".join(files))

def main():
    root = tk.Tk()
    root.title("代码卡片生成器")

    # 文件选择
    tk.Label(root, text="代码文件:").grid(row=0, column=0, sticky="e")
    file_entry = tk.Entry(root, width=50)
    file_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="选择文件", command=lambda: select_files(file_entry)).grid(row=0, column=2, padx=5)

    # 主题
    tk.Label(root, text="主题:").grid(row=1, column=0, sticky="e")
    theme_var = tk.StringVar(value="light")
    tk.OptionMenu(root, theme_var, "light", "dark").grid(row=1, column=1, sticky="w", padx=5, pady=5)

    # 字体
    tk.Label(root, text="字体:").grid(row=2, column=0, sticky="e")
    font_entry = tk.Entry(root)
    font_entry.insert(0, "Consolas")
    font_entry.grid(row=2, column=1, padx=5, pady=5)

    # 字号
    tk.Label(root, text="字号:").grid(row=3, column=0, sticky="e")
    size_entry = tk.Entry(root)
    size_entry.insert(0, "24")
    size_entry.grid(row=3, column=1, padx=5, pady=5)

    # 行号
    tk.Label(root, text="显示行号:").grid(row=4, column=0, sticky="e")
    lineno_var = tk.BooleanVar(value=True)
    tk.Checkbutton(root, variable=lineno_var).grid(row=4, column=1, sticky="w", padx=5, pady=5)

    # 输出文件名
    tk.Label(root, text="输出文件名:").grid(row=5, column=0, sticky="e")
    output_entry = tk.Entry(root)
    output_entry.grid(row=5, column=1, padx=5, pady=5)

    # 标题
    title_var = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text="添加标题", variable=title_var).grid(row=6, column=1, sticky="w", padx=5, pady=5)
    tk.Label(root, text="标题内容:").grid(row=7, column=0, sticky="e")
    title_entry = tk.Entry(root)
    title_entry.grid(row=7, column=1, padx=5, pady=5)

    def on_generate():
        files = file_entry.get().strip()
        if not files:
            messagebox.showerror("错误", "请选择代码文件")
            return
        file_list = [f.strip() for f in files.split(";") if f.strip()]
        try:
            font_size = int(size_entry.get())
        except Exception:
            font_size = 24
        generate_card(
            file_list=file_list,
            theme=theme_var.get(),
            font_name=font_entry.get() or "Consolas",
            font_size=font_size,
            show_line_numbers=lineno_var.get(),
            output_name=output_entry.get(),
            add_title=title_var.get(),
            title_text=title_entry.get() if title_var.get() else ""
        )

    tk.Button(root, text="生成卡片", command=on_generate, bg="#4CAF50", fg="white").grid(row=8, column=1, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()