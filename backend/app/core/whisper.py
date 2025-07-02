import torch
import torchaudio
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration

from app.core.config import logger

MODEL_NAME = "openai/whisper-tiny"

transcriber = None


def init_whisper_model():
    transcriber = WhisperTranscriber()


class WhisperTranscriber:
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.processor = WhisperProcessor.from_pretrained(MODEL_NAME)
        self.model = WhisperForConditionalGeneration.from_pretrained(
            MODEL_NAME).to(self.device)

    def transcribe(self, audio_path: str) -> str:
        logger.debug("Available backends:", torchaudio.list_audio_backends())

        # Load audio
        try:
            waveform, sample_rate = torchaudio.load(audio_path)
        except Exception as e:
            logger.error("failed to load audio", e)
            return ""

        # Resample to 16000 Hz if needed
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(
                orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        # Convert to mono
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        # Prepare inputs
        input_features = self.processor(
            waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt"
        ).input_features.to(self.device)

        # Generate
        predicted_ids = self.model.generate(input_features)
        transcription = self.processor.batch_decode(
            predicted_ids, skip_special_tokens=True)[0]

        return transcription


transcriber = WhisperTranscriber()
