from math import log2, pow
import os
import gradio as gr
from whisper_driver import analyze_and_grade


def main_note(mic, upload, speech_type):
    if mic is not None:
        rate, data = mic
        mic = (rate, data)
    elif upload is not None:
        rate, data = upload
    else:
        return (
            gr.Textbox.update(visible=True, value="No recording found"),
            gr.Textbox.update(visible=True, value="No recording found"),
            gr.Textbox.update(visible=True, value="No recording found"),
        )
    grading, improvement, transcript = analyze_and_grade(
        data, rate=rate, speech_type=speech_type
    )
    return (
        gr.Textbox.update(visible=True, value=grading, label="Evaluation"),
        gr.Textbox.update(visible=True, value=transcript),
        gr.Textbox.update(visible=True, value=improvement),
    )


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            with gr.Box():
                with gr.Tab("Record"):
                    microphone_input = gr.Audio(source="microphone")
                with gr.Tab("Upload"):
                    file_input = gr.Audio()
        with gr.Column():
            with gr.Box():
                speech_type_input = gr.Radio(
                    ["Informative", "Persuasive"],
                    label="Speech Type",
                    value="Informative",
                )
    with gr.Row():
        submit_btn = gr.Button(value="Analyze").style(full_width=True)
    with gr.Row():
        evaluation_output = gr.Textbox(label="", visible=True)
    with gr.Row():
        with gr.Column():
            original_transcript_output = gr.Textbox(label="Transcript", visible=False)
        with gr.Column():
            improved_transcript_output = gr.Textbox(
                label="Suggested Outline", visible=False
            )
    submit_btn.click(
        main_note,
        inputs=[microphone_input, file_input, speech_type_input],
        outputs=[
            evaluation_output,
            original_transcript_output,
            improved_transcript_output,
        ],
    )

if __name__ == "__main__":
    demo.launch(show_api=False)
