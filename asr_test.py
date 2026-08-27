from time import perf_counter

from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess


AUDIO_PATH = (
    "test_man2.wav"
)

print("正在加载 SenseVoiceSmall 模型……")
load_start = perf_counter()

model = AutoModel(
    model="iic/SenseVoiceSmall",
    vad_model="fsmn-vad",
    device="cpu",
)

load_time = perf_counter() - load_start
print(f"模型加载完成，耗时：{load_time:.2f} 秒")

print("\n正在识别测试音频……")
asr_start = perf_counter()

result = model.generate(
    input=AUDIO_PATH,
    cache={},
    language="auto",
    use_itn=True,
    batch_size_s=60,
    merge_vad=True,
    merge_length_s=15,
)

asr_time = perf_counter() - asr_start

text = rich_transcription_postprocess(result[0]["text"])

print("\n识别结果：")
print(text)
print(f"\n识别耗时：{asr_time:.2f} 秒")